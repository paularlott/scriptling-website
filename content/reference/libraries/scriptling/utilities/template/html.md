---
title: scriptling.template.html
linkTitle: html
description: HTML template rendering using Go's html/template, with automatic escaping.
weight: 1
---

The `scriptling.template.html` library renders HTML templates using Go's `html/template`. All values are automatically HTML-escaped, making this the safe choice for generating web pages: including pages that embed untrusted or LLM-generated content.

## Available Functions

| Function | Description |
|----------|-------------|
| `Set()` | Create a template set |

`Set()` returns a `Set` object with two methods:

| Method | Description |
|--------|-------------|
| `add(source)` | Add a template source to the set |
| `render(data)` / `render(name, data)` | Render a template from the set |

## Functions

### `Set()`

Creates a new, empty HTML template set.

**Returns:** `Set`: a template set with `add(source)` and `render([name,] data)` methods.

```python
import scriptling.template.html as html

tmpl = html.Set()
tmpl.add("<h1>Hello, {{.Name}}!</h1>")
print(tmpl.render({"Name": "Alice"}))
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

- [scriptling.template.text](../text/) - Unescaped template rendering for non-HTML output
- [scriptling.markdown](../../markdown/) - Convert Markdown to HTML before rendering it into a template
