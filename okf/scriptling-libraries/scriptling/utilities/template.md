---
description: Go-powered text and HTML template rendering with automatic escaping.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/utilities/template/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/utilities/template/
status: stable
tags:
    - libraries
    - utilities
    - template
title: scriptling.template
type: API Reference
---
# scriptling.template

Go-powered template rendering. Two sub-libraries are available: import only what you need:

| Library | Import | Description |
|---------|--------|-------------|
| [`scriptling.template.html`](template/html.md) | `import scriptling.template.html as html` | `html/template`: automatic HTML escaping |
| [`scriptling.template.text`](template/text.md) | `import scriptling.template.text as text` | `text/template`: no escaping, plain text output |

Both expose a single `Set()` constructor that returns a `Set` object with `add(source)` and `render([name,] data)` methods.

## Quick Example

```python
import scriptling.template.html as html

tmpl = html.Set()
tmpl.add("<h1>Hello, {{.Name}}!</h1>")
print(tmpl.render({"Name": "Alice"}))
```

## Go Template Syntax

Templates use standard [Go template syntax](https://pkg.go.dev/text/template):

| Syntax | Description |
|--------|-------------|
| `{{.Field}}` | Access a field from the data dict |
| `{{.}}` | The entire data value |
| `{{if .Cond}} ... {{end}}` | Conditional |
| `{{range .Items}} {{.}} {{end}}` | Loop over a list |
| `{{define "name"}} ... {{end}}` | Define a named partial |
| `{{template "name" .}}` | Include a partial |
| `{{- ... -}}` | Trim surrounding whitespace |

## Partials

Named templates are defined inline using `{{define}}` and included with `{{template}}`:

```python
tmpl = html.Set()
tmpl.add('{{define "header"}}<header><h1>{{.Title}}</h1></header>{{end}}')
tmpl.add('{{define "page"}}{{template "header" .}}<main>{{.Body}}</main>{{end}}')
print(tmpl.render("page", {"Title": "Home", "Body": "Welcome"}))
```

## Custom Delimiters

By default both libraries use Go's standard `{{` `}}` action delimiters. Pass `left` and `right` to `Set()` to change them — useful when your template content contains literal `{{` `}}` (e.g. a client-side framework like Vue or Handlebars, JSON, or CSS):

```python
import scriptling.template.text as text

tmpl = text.Set(left="{%", right="%}")
tmpl.add("Hello, {%.Name%}! Your balance is {%.Balance%}.")
print(tmpl.render({"Name": "Alice", "Balance": 42}))
```

Both arguments are optional and default to the standard delimiters (`{{` and `}}`). Pass an empty string to fall back to a default for that side.

## Loading Templates from Files

The template libraries are intentionally filesystem-free. Load template source with `os.read_file()`, which respects path restrictions:

```python
import os
import scriptling.template.html as html

tmpl = html.Set()
tmpl.add(os.read_file("templates/partials.html"))
tmpl.add(os.read_file("templates/page.html"))
print(tmpl.render("page", {"Title": "Home"}))
```

## See Also

- [Utilities](../utilities.md) - Parent utilities namespace
- [scriptling.markdown](markdown.md) - Markdown to HTML conversion
- [Libraries](../../scriptling-libraries.md) - Full library reference index
