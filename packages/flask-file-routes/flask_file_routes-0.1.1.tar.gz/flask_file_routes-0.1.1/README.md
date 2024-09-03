# Flask-File-Routes

File-based routing with a new mix-code file format that combines python code and a jinja template.  
Inspired by [Astro pages](https://docs.astro.build/en/basics/astro-pages/#astro-pages).

This uses [Jinjapy](https://github.com/hyperflask/jinjapy) for the page format.

## Installation

    pip install flask-file-routes

## Usage

Activate the extension:

```python
from flask import Flask
from flask_file_routes import FileRoutes

app = Flask(__name__)
FileRoutes(app)
```

Create a *pages/index.jpy* file:

```
---
page.message = "hello world"
def post():
    page.message = f"hello {request.form['name']}"
---
{{ message }}
<hr>
<form method="post">
    <input type="text" name="name" placeholder="your name">
    <button type="submit">say hello</button>
</form>
```

Go to <http://localhost:5000>.

## Page file format

Pages can use the following format:

- **html**: a standard jinja template with no additional code execution
- **md**: a standard jinja template that will be rendered using markdown
- **jpy**: jinjapy hybrid format that let you execute code before rendering the template

A jinjapy file contains 2 sections:

- A frontmatter with some Python code (enclosed by lines containg 3 dashes "---")
- A body containing some Jinja template code

Both are optional:

- If the frontmatter is missing, the file only contains a Jinja template
- If the frontmatter is left unclosed (the file starts with "---" on a single line followed by some python code), the file has no template

The python code has a few global variables injected when executed: `page`, `request`, `abort`, `redirect`, `url_for`, `current_app`, `render_template`.

## How routing works

The URL rule is constructed using the following rules:

- `index.ext` file are roots
- folder hierarchy are transformed to url paths:
    - `posts/release-annoucement.ext` converts to `/posts/release-annoucement`
    - `posts/index.ext` converts to `/posts`
    - `folder/subfolder/page.ext` converts to `/folder/subfolder/page`
- placeholders are allowed in filenames as they would in url rules
    - `posts/<slug>.ext` converts to `/posts/<slug>`

Allowed HTTP methods are determined by, in order:

1. A comment at the start of the python code listing allowed http methods in the following format: `# methods=GET,POST`
2. functions with HTTP method names in lower case

## The page object

The page object is accessible under `flask_file_routes.page` or `g.page` in **all** endpoints of your app.

Any properties set onto the object will be available as a variable in the template.

You can send a response immediatly and stop any further processing using `page.respond(response)`.

View args are available as read-only properties of the page object.

```python
from flask_file_routes import page

@app.route("/")
def index():
    page.message = "hello world"
    return render_template_string("{{message}}")
```

Helpers can be registered on the page object:

```python
file_routes = FileRoutes(app)

@file_routes.page_helper
def method(page):
    return request.method
```

*pages/index.jpy*

```
---
#methods=GET,POST
if page.method == "POST": # call the helper
    page.message = "hello from post"
else:
    page.message = "hello from get"
---
{{message}}
```