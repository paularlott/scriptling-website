---
title: scriptling.template.text
linkTitle: template.text
weight: 2
---

Text template rendering using Go's `text/template`. No escaping is applied — use this for emails, config files, or any non-HTML output.

## Available Functions

| Function | Description              |
| -------- | ------------------------ |
| `Set()`  | Create a template set    |

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

**Returns:** Rendered string

## Examples

### Simple template

```python
import scriptling.template.text as text

tmpl = text.Set()
tmpl.add("Hello, {{.Name}}! You have {{.Count}} messages.")
print(tmpl.render({"Name": "Alice", "Count": 5}))
```

### Conditionals and loops

```python
tmpl = text.Set()
tmpl.add("""Order #{{.OrderID}}
Status: {{if .Shipped}}Shipped{{else}}Pending{{end}}
{{- if .TrackingCode}}
Tracking: {{.TrackingCode}}
{{- end}}""")
print(tmpl.render({"OrderID": 1001, "Shipped": True, "TrackingCode": "TRK-9876"}))
```

### Partials with {{define}}

```python
tmpl = text.Set()
tmpl.add('{{define "greeting"}}Hello, {{.Name}}!{{end}}')
tmpl.add('{{define "email"}}{{template "greeting" .}}\n\nYour {{.Product}} trial expires in {{.Days}} days.{{end}}')
print(tmpl.render("email", {"Name": "Alice", "Product": "Scriptling Pro", "Days": 14}))
```

### From file

```python
import os
import scriptling.template.text as text

tmpl = text.Set()
tmpl.add(os.read_file("templates/email.txt"))
print(tmpl.render({"Name": "Alice", "Product": "Scriptling Pro", "ExpiryDays": 14}))
```

## Notes

- No HTML escaping — do not use for browser output (use `scriptling.template.html` instead)
- Template sets are parsed once and can be rendered many times
- Load templates from files using `os.read_file()`, which honours path restrictions
