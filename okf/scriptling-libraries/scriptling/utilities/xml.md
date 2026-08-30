---
description: XML parsing and formatting (dict-based, string-only).
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/utilities/xml/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/utilities/xml/
status: stable
tags:
    - libraries
    - utilities
    - data-formats
title: scriptling.xml
type: API Reference
---
# scriptling.xml

The `scriptling.xml` library provides simple XML parsing and formatting using a dict-based representation (similar to Python's `xmltodict`). Unlike Python's `xml.dom` or `xml.etree.ElementTree` (which use tree objects), this operates on plain dicts and strings — `loads`/`dumps`, consistent with `json`, `yaml`, `toml`, and `csv`.

Available in all environments (including MCP — no filesystem access required).

## Conventions

- Element tags → dict keys
- Text content → string value (or `"#text"` key when the element also has attributes/children)
- Attributes → `"@"`-prefixed keys (e.g. `"@id"`)
- Repeated child elements → list values
- Empty elements → empty string `""`

## Available Functions

| Function | Description |
|----------|-------------|
| `loads(content)` | Parse an XML string into a nested dict. |
| `dumps(data, indent="")` | Format a dict into an XML string. |

## Functions

### `loads(content)`

Parse an XML string into a nested dict using the dict-based representation.

**Parameters:** `content` (`str`): XML text to parse.

**Returns:** `dict`: nested dict representing the XML document.

```python
import scriptling.xml as xml

# Simple elements
data = xml.loads("<root><name>Alice</name><age>30</age></root>")
# {"root": {"name": "Alice", "age": "30"}}

# Attributes
data = xml.loads('<user id="123"><name>Alice</name></user>')
# {"user": {"@id": "123", "name": "Alice"}}

# Text + attributes
data = xml.loads('<msg type="greeting">Hello</msg>')
# {"msg": {"@type": "greeting", "#text": "Hello"}}

# Repeated elements → list
data = xml.loads("<items><item>a</item><item>b</item></items>")
# {"items": {"item": ["a", "b"]}}
```

### `dumps(data, indent="")`

Format a dict back into an XML string. The dict should have a single root key whose value is the root element's content.

**Parameters:**
- `data` (`dict`): Dict with a single root element key.
- `indent` (`str`, keyword-only): Indentation string. Default: `""` (compact).

**Returns:** `str`: XML-formatted text.

```python
import scriptling.xml as xml

# Basic
text = xml.dumps({"root": {"name": "Alice", "age": "30"}})
# <root><name>Alice</name><age>30</age></root>

# With attributes
text = xml.dumps({"user": {"@id": "123", "name": "Alice"}})
# <user id="123"><name>Alice</name></user>

# Repeated elements
text = xml.dumps({"items": {"item": ["a", "b"]}})
# <items><item>a</item><item>b</item></items>

# Indented
text = xml.dumps({"root": {"child": "value"}}, indent="  ")
# <root>
#   <child>value</child>
# </root>
```

## Reading and Writing Files

Pair with `os` for file I/O:

```python
import scriptling.xml as xml
import os

data = xml.loads(os.read_file("config.xml"))
data["config"]["server"]["port"] = "9090"
os.write_file("config.xml", xml.dumps(data, indent="  "))
```

## See Also

- [json](https://scriptling.dev/okf/scriptling-libraries/data-formats/json.md): JSON parsing and formatting
- [yaml](https://scriptling.dev/okf/scriptling-libraries/data-formats/yaml.md): YAML parsing
- [toml](https://scriptling.dev/okf/scriptling-libraries/data-formats/toml.md): TOML parsing
- [scriptling.csv](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/csv.md): CSV parsing and formatting
