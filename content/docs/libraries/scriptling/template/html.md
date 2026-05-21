---
title: scriptling.template.html
linkTitle: template.html
weight: 1
---

HTML template rendering using Go's `html/template`. All values are automatically HTML-escaped, making this safe for generating web pages.

## Available Functions

| Function | Description              |
| -------- | ------------------------ |
| `Set()`  | Create a template set    |

## Setup

```go
import "github.com/paularlott/scriptling/extlibs"

extlibs.RegisterTemplateHTMLLibrary(p)
```

## Set Object

`Set()` returns a `Set` object with two methods:

### Set.add(source)

Add a template source to the set. The source may be a plain template or contain one or more `{{define "name"}}...{{end}}` blocks.

**Parameters:**

- `source` (string): Template source string

### Set.render(data) / Set.render(name, data)

Render a template from the set.

**Parameters:**

- `name` (string, optional): Name of the template to render (from `{{define "name"}}`)
- `data` (dict): Template data passed as the dot (`.`) value

**Returns:** Rendered HTML string (values are auto-escaped)

## Examples

### Simple template

```python
import scriptling.template.html as html

tmpl = html.Set()
tmpl.add("<h1>Hello, {{.Name}}!</h1>")
print(tmpl.render({"Name": "Alice"}))
```

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

- Use this library for any output rendered in a browser — values are automatically escaped
- Template sets are parsed once and can be rendered many times — prefer module-level variables in HTTP handlers
- Load templates from files using `os.read_file()`, which honours path restrictions
