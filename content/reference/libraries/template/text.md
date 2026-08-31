---
title: scriptling.template.text
linkTitle: template.text
description: Text template rendering using Go's text/template, with no escaping.
tags: [libraries, utilities, template]
weight: 2

aliases:
  - /reference/libraries/scriptling/utilities/template/text/
---

The `scriptling.template.text` library renders text templates using Go's `text/template`. No escaping is applied: use this for emails, config files, or any other non-HTML output. For browser-rendered output, use [scriptling.template.html](../html/) instead.

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

Creates a new, empty text template set.

**Parameters:**
- `left` (`str`, optional): Left action delimiter. Defaults to `{{`. Pass an empty string to keep the default.
- `right` (`str`, optional): Right action delimiter. Defaults to `}}`. Pass an empty string to keep the default.

**Returns:** `Set`: a template set with `add(source)` and `render([name,] data)` methods.

```python
import scriptling.template.text as text

tmpl = text.Set()
tmpl.add("Hello, {{.Name}}! You have {{.Count}} messages.")
print(tmpl.render({"Name": "Alice", "Count": 5}))

# Custom delimiters, e.g. to keep {{ }} literally in the output
cfg = text.Set(left="{%", right="%}")
cfg.add("server {{ name }}: {%.Host%}:{%.Port%}")
print(cfg.render({"Host": "127.0.0.1", "Port": 8080}))
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

### Custom delimiters

Use `left` and `right` when template content should contain literal `{{ }}` (e.g. a config file that already uses `{{ }}` for its own placeholders):

```python
tmpl = text.Set(left="{%", right="%}")
tmpl.add("Hello, {%.Name%}! Config from upstream: {{ service.tag }}")
print(tmpl.render({"Name": "Alice"}))
# Output: Hello, Alice! Config from upstream: {{ service.tag }}
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
