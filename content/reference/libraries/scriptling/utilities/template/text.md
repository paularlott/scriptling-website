---
title: scriptling.template.text
linkTitle: text
description: Text template rendering using Go's text/template, with no escaping.
weight: 2
---

The `scriptling.template.text` library renders text templates using Go's `text/template`. No escaping is applied: use this for emails, config files, or any other non-HTML output. For browser-rendered output, use [scriptling.template.html](../html/) instead.

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

Creates a new, empty text template set.

**Returns:** `Set`: a template set with `add(source)` and `render([name,] data)` methods.

```python
import scriptling.template.text as text

tmpl = text.Set()
tmpl.add("Hello, {{.Name}}! You have {{.Count}} messages.")
print(tmpl.render({"Name": "Alice", "Count": 5}))
```

### `Set.add(source)`

Adds a template source to the set. The source may be a plain template or contain one or more `{{define "name"}}...{{end}}` blocks.

**Parameters:**
- `source` (`str`): Template source string.

**Returns:** `None`

**Raises:** `Error`: if the template source fails to parse.

```python
tmpl = text.Set()
tmpl.add('{{define "greeting"}}Hello, {{.Name}}!{{end}}')
tmpl.add('{{define "email"}}{{template "greeting" .}}\n\nYour {{.Product}} trial expires in {{.Days}} days.{{end}}')
```

### `Set.render(data)` / `Set.render(name, data)`

Renders a template from the set.

**Parameters:**
- `name` (`str`, optional): Name of the template to render, from a matching `{{define "name"}}` block. Omit to render an anonymous/single template.
- `data` (`dict`): Template data passed as the dot (`.`) value.

**Returns:** `str`: the rendered output. No escaping is applied.

**Raises:** `Error`: if execution fails (e.g. unknown template name).

```python
# Anonymous / single template
tmpl = text.Set()
tmpl.add("Hello, {{.Name}}!")
print(tmpl.render({"Name": "Alice"}))

# Named template
print(tmpl.render("email", {"Name": "Alice", "Product": "Scriptling Pro", "Days": 14}))
```

## Examples

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

- No HTML escaping: do not use for browser output (use `scriptling.template.html` instead).
- Template sets are parsed once and can be rendered many times.
- Load templates from files using `os.read_file()`, which honours path restrictions.

## See Also

- [scriptling.template.html](../html/) - Auto-escaped template rendering for browser output
