---
description: HTML template rendering using Go's html/template, with automatic escaping.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/utilities/template/html/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/utilities/template/html/
status: stable
tags:
    - libraries
    - utilities
    - template
title: scriptling.template.html
type: API Reference
---
# scriptling.template.html

The `scriptling.template.html` library renders HTML templates using Go's `html/template`. All values are automatically HTML-escaped, making this the safe choice for generating web pages: including pages that embed untrusted or LLM-generated content.

## Available Functions

| Function | Description |
|----------|-------------|
| `Set(left="{{", right="}}")` | Create a template set with optional custom delimiters |

`Set()` returns a `Set` object with two methods:

| Method | Description |
|--------|-------------|
| `add(source)` | Add a template source to the set |
| `render(data)` / `render(name, data)` | Render a template from the set |

## Functions

### `Set(left="{{", right="}}")`

Creates a new, empty HTML template set.

**Parameters:**
- `left` (`str`, optional): Left action delimiter. Defaults to `{{`. Pass an empty string to keep the default.
- `right` (`str`, optional): Right action delimiter. Defaults to `}}`. Pass an empty string to keep the default.

**Returns:** `Set`: a template set with `add(source)` and `render([name,] data)` methods.

```python
import scriptling.template.html as html

tmpl = html.Set()
tmpl.add("<h1>Hello, {{.Name}}!</h1>")
print(tmpl.render({"Name": "Alice"}))

# Custom delimiters, e.g. to embed Vue/Handlebars/{{ }} content literally
vue = html.Set(left="[[", right="]]")
vue.add("<p>[[.Message]] {{ user.name }}</p>")
print(vue.render({"Message": "Hello"}))
```

### `Set.add(source)`

Adds a template source to the set. The source may be a plain template or contain one or more `{{define "name"}}...{{end}}` blocks.

**Parameters:**
- `source` (`str`): Template source string.

**Returns:** `None`

**Raises:** `Error`: if the template source fails to parse.

```python
tmpl = html.Set()
tmpl.add('{{define "header"}}<header><h1>{{.Title}}</h1></header>{{end}}')
tmpl.add('{{define "footer"}}<footer>© {{.Year}}</footer>{{end}}')
tmpl.add('{{define "page"}}<!DOCTYPE html><html><body>{{template "header" .}}<main>{{.Body}}</main>{{template "footer" .}}</body></html>{{end}}')
```

### `Set.render(data)` / `Set.render(name, data)`

Renders a template from the set.

**Parameters:**
- `name` (`str`, optional): Name of the template to render, from a matching `{{define "name"}}` block. Omit to render an anonymous/single template.
- `data` (`dict`): Template data passed as the dot (`.`) value.

**Returns:** `str`: the rendered HTML, with all values auto-escaped.

**Raises:** `Error`: if execution fails (e.g. unknown template name).

```python
# Anonymous / single template
tmpl = html.Set()
tmpl.add("<h1>Hello, {{.Name}}!</h1>")
print(tmpl.render({"Name": "Alice"}))

# Named template
print(tmpl.render("page", {"Title": "Home", "Body": "Welcome!", "Year": 2026}))
```

## Examples

### Variables, conditionals, and loops

```python
tmpl = html.Set()
tmpl.add("""<!DOCTYPE html>
<html>
<head><title>{{.Title}}</title></head>
<body>
  <h1>{{.Title}}</h1>
  {{if .Items}}
  <ul>{{range .Items}}<li>{{.}}</li>{{end}}</ul>
  {{else}}<p>No items.</p>{{end}}
</body>
</html>""")
print(tmpl.render({"Title": "My List", "Items": ["Apple", "Banana"]}))
```

### Partials with {{define}}

```python
tmpl = html.Set()
tmpl.add('{{define "header"}}<header><h1>{{.Title}}</h1></header>{{end}}')
tmpl.add('{{define "footer"}}<footer>© {{.Year}}</footer>{{end}}')
tmpl.add('{{define "page"}}<!DOCTYPE html><html><body>{{template "header" .}}<main>{{.Body}}</main>{{template "footer" .}}</body></html>{{end}}')
print(tmpl.render("page", {"Title": "Home", "Body": "Welcome!", "Year": 2026}))
```

### XSS protection

```python
tmpl = html.Set()
tmpl.add("<p>{{.Content}}</p>")
print(tmpl.render({"Content": "<script>alert('xss')</script>"}))
# Output: <p>&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;</p>
```

### Custom delimiters

Use `left` and `right` when template content should contain literal `{{ }}` (e.g. a client-side framework, CSS, or JSON):

```python
# Embed Vue-style {{ }} in the output without Scriptling interpreting them
tmpl = html.Set(left="[[", right="]]")
tmpl.add('<div>Hello [[.Name]]! Your settings: {{ user.prefs }}</div>')
print(tmpl.render({"Name": "Alice"}))
# Output: <div>Hello Alice! Your settings: {{ user.prefs }}</div>
```

### From file

```python
import os
import scriptling.template.html as html

tmpl = html.Set()
tmpl.add(os.read_file("templates/partials.html"))
tmpl.add(os.read_file("templates/page.html"))
print(tmpl.render("page", {"Title": "Home"}))
```

### HTTP server handler

```python
import scriptling.template.html as html
import scriptling.runtime as runtime

_tmpl = html.Set()
_tmpl.add('{{define "header"}}<header><h1>{{.Title}}</h1></header>{{end}}')
_tmpl.add('{{define "page"}}<!DOCTYPE html><html><body>{{template "header" .}}<main>{{.Body}}</main></body></html>{{end}}')

def index(request):
    return runtime.http.html(200, _tmpl.render("page", {"Title": "Home", "Body": "Welcome!"}))
```

## Notes

- Use this library for any output rendered in a browser: values are automatically escaped.
- Template sets are parsed once and can be rendered many times: prefer module-level variables in HTTP handlers.
- Load templates from files using `os.read_file()`, which honours path restrictions.

## See Also

- [scriptling.template.text](text.md) - Unescaped template rendering for non-HTML output
- [scriptling.markdown](../markdown.md) - Convert Markdown to HTML before rendering it into a template
