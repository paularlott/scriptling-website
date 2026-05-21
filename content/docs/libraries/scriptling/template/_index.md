---
title: scriptling.template
linkTitle: template
weight: 10
---

Go-powered template rendering. Two sub-libraries are available — import only what you need:

| Library | Import | Description |
|---------|--------|-------------|
| [`scriptling.template.html`](./html/) | `import scriptling.template.html as html` | `html/template` — automatic HTML escaping |
| [`scriptling.template.text`](./text/) | `import scriptling.template.text as text` | `text/template` — no escaping, plain text output |

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
