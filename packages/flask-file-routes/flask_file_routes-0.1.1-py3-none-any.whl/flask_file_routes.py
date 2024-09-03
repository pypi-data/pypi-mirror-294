from flask import render_template, request, current_app, url_for, redirect, abort, g, render_template_string
from flask.views import http_method_funcs
from werkzeug.local import LocalProxy
from blinker import Namespace
import jinjapy
import runpy
import os
import re
import markdown
import yaml


page = LocalProxy(lambda: g.page)

_signals = Namespace()
before_page_module_execute = _signals.signal("before-page-module-execute")
before_page_module_render = _signals.signal("before-page-module-render")
after_page_module_render = _signals.signal("after-page-module-render")


DEFAULT_HELPERS = {}


class FileRoutes:
    def __init__(self, app=None, **kwargs):
        self.page_helpers = {}
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, pages_folder="pages", url_prefix="/", partials_folder="partials"):
        self.app = app

        @app.before_request
        def push_page_context():
            g.page = PageContext(self)

        @app.context_processor
        def template_context():
            return dict(page=g.page, **g.page.template_ctx)
        
        @app.errorhandler(PageResponseException)
        def handle_page_response(e):
            return e.response

        if pages_folder and os.path.exists(os.path.join(app.root_path, pages_folder)):
            self.loader, modules = register_page_package(app, pages_folder, url_prefix=url_prefix)

        if partials_folder and os.path.exists(os.path.join(app.root_path, partials_folder)):
            self.partials_loader = register_partials_package(app, partials_folder)

    def page_helper(self, func=None, name=None):
        def decorator(func):
            self.page_helpers[name or func.__name__] = func
            return func
        if func:
            return decorator(func)
        return decorator


class PageContext:
    def __init__(self, ext):
        object.__setattr__(self, "ext", ext)
        object.__setattr__(self, "template_ctx", {})
        object.__setattr__(self, "helpers", {})

    def __getattr__(self, key):
        if key in self.template_ctx:
            return self.template_ctx[key]
        if key in request.view_args:
            return request.view_args[key]
        if key in self.helpers:
            return self.helpers[key]
        if key in self.ext.page_helpers:
            self.helpers[key] = self.ext.page_helpers[key](self)
            return self.helpers[key]
        if key in DEFAULT_HELPERS:
            self.helpers[key] = DEFAULT_HELPERS[key](self)
            return self.helpers[key]
        raise AttributeError()

    def __setattr__(self, key, value):
        self.template_ctx[key] = value

    def get(self, key, default=None):
        return self.template_ctx.get(key, default)
    
    def respond(self, response):
        raise PageResponseException(response)
    
    def redirect(self, url):
        self.respond(redirect(url))

    def abort(self, code):
        abort(code)
    

class PageResponseException(Exception):
    def __init__(self, response):
        super().__init__()
        self.response = response


def decorator_as_page_helper(decorator):
    def page_helper(page):
        def func():
            r = decorator(lambda **kw: None)()  #noqa
            if r:
                page.respond(r)
        return func
    return page_helper


def register_page_package(app_or_blueprint, path="pages", package_name=None, template_prefix=None, url_prefix="", skip_missing_frontmatter=False, jinja_env=None):
    modules = []
    loader = _create_jinjapy_package(app_or_blueprint, path, package_name, template_prefix, jinja_env)
    for module_name, template in loader.list_files(module_with_package=False, with_template_prefix=False):
        if template:
            page_url_segments = template.rsplit(".", 1)[0].split(os.sep)
        else:
            page_url_segments = module_name.split(".")
        if page_url_segments[-1] == "index":
            del page_url_segments[-1]
        url = url_prefix + "/".join(page_url_segments)
        module_name = f"{loader.package_name}.{module_name}" if module_name else None
        page_module = ModuleView.create_from_module_template(loader, module_name, loader.prefix + template if template else None, url, skip_missing_frontmatter)
        if page_module:
            page_module.register(app_or_blueprint)
            modules.append(page_module)
    return loader, modules


def register_partials_package(app_or_blueprint, path="partials", package_name=None, template_prefix=None, jinja_env=None):
    return _create_jinjapy_package(app_or_blueprint, path, package_name, template_prefix, jinja_env)


def _create_jinjapy_package(app_or_blueprint, path, package_name=None, template_prefix=None,  jinja_env=None):
    if not package_name:
        package_name = os.path.basename(path)
    if template_prefix is None:
        template_prefix = package_name.replace(".", "/")
    if app_or_blueprint.import_name != "__main__":
        package_name = f"{app_or_blueprint.import_name}.{package_name}"
    jinja_env = jinja_env or app_or_blueprint.jinja_env
    return jinjapy.register_package(package_name, os.path.join(app_or_blueprint.root_path, path), template_prefix, env=jinja_env)


class ModuleView:
    module_globals = dict(page=page, g=g, request=request, render_template=render_template,
                    url_for=url_for, redirect=redirect, abort=abort, app=current_app, current_app=current_app)
    
    @classmethod
    def create_from_module_template(cls, loader, module_name, template, url=None, skip_missing_frontmatter=False):
        if template:
            template_code, python_code = loader.split_source(template)
            if not template_code:
                template = None
        else:
            python_code = loader.split_source(loader.get_file_from_module(module_name))[1]

        if skip_missing_frontmatter and python_code is None:
            return None
        
        if module_name:
            m = re.match("#\s+methods\s*=\s*([a-z,\s]+)$", python_code, re.I)
            if m:
                methods = [me.strip().upper() for me in m.group(1).split(",")]
            else:
                methods = [m.upper() for m in http_method_funcs if re.search(f"^(def {m}\()|{m}\s*=", python_code, re.MULTILINE)]
            if not methods:
                methods = ["GET"]
        else:
            methods = ["GET"]
            module_name = None

        return cls(module_name, template, url, methods, frontmatter=python_code)

    def __init__(self, module_name, template, url=None, methods=None, decorators=None, frontmatter=None):
        if not methods:
            methods = ["GET"]
        self.module_name = module_name
        self.template = template
        self.url = url
        self.methods = methods
        self.decorators = decorators or []
        self.frontmatter = frontmatter

    def execute(self, view_args=None, method=None):
        if view_args is None:
            view_args = request.view_args
        if method is None:
            method = request.method.lower()
        page.template = self.template
        before_page_module_execute.send(self)
        out = None
        if self.module_name:
            m = runpy.run_module(self.module_name, self.module_globals)
            if method in m and callable(m[method]):
                resp = m[method](**view_args)
                if resp:
                    out = resp

        before_page_module_render.send(self)
        if out is None and page.template:
            if page.template.endswith(".md") and self.frontmatter:
                page.template_ctx.update(yaml.safe_load(self.frontmatter))
                page.is_markdown = True
            out = render_template(page.template)
            if page.get('is_markdown'):
                markdown_options = dict(current_app.config.get("PAGES_MARKDOWN_OPTIONS", {}), **page.get("markdown_options", {}))
                out = markdown.markdown(out, **markdown_options)
                if page.get("layout"):
                    layout = page.layout
                    block = "content"
                    if ":" in layout:
                        layout, block = layout.rsplit(":", 1)
                    out = render_template_string(
                        '{%% extends "%s" %%}{%% block %s %%}%s{%% endblock %%}' % (layout, block, out))
        after_page_module_render.send(self)
        return out or ""

    def as_view(self):
        def view_func(**args):
            return self.execute(args)
        for decorator in self.decorators:
            view_func = decorator(view_func)
        return view_func
    
    def register(self, app_or_blueprint, url=None, **add_url_rule_kwargs):
        add_url_rule_kwargs.setdefault("methods", self.methods)
        if self.module_name:
            add_url_rule_kwargs.setdefault("endpoint", self.module_name.rsplit(".")[-1])
        else:
            add_url_rule_kwargs.setdefault("endpoint", os.path.basename(self.template).split(".")[0])
        app_or_blueprint.add_url_rule(self.url if url is None else url, view_func=self.as_view(), **add_url_rule_kwargs)