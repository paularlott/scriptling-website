---
description: CSV parsing and formatting (string-based, no filesystem access).
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/utilities/csv/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/utilities/csv/
status: stable
tags:
    - libraries
    - utilities
    - data-formats
title: scriptling.csv
type: API Reference
---
# scriptling.csv

The `scriptling.csv` library provides CSV parsing and formatting using Go's `encoding/csv` (RFC 4180 compliant). Unlike Python's `csv` module (which works with file objects), this library operates on strings — parse a CSV string into rows, or format rows into a CSV string. Use `os.read_file()` / `os.write_file()` for file I/O.

Available in all environments (including MCP — no filesystem access required).

## Available Functions

| Function | Description |
|----------|-------------|
| `loads(content, delimiter=",")` | Parse CSV text into a list of rows (lists). |
| `loads_dict(content, delimiter=",")` | Parse CSV text into a list of dicts (first row = headers). |
| `dumps(rows, delimiter=",")` | Format a list of lists into CSV text. |
| `dumps_dict(rows, delimiter=",", columns=None)` | Format a list of dicts into CSV text. |

## Functions

### `loads(content, delimiter=",")`

Parse a CSV string into a list of rows. Handles quoting, embedded commas, and embedded newlines per RFC 4180.

**Parameters:**
- `content` (`str`): CSV text to parse.
- `delimiter` (`str`, keyword-only): Field delimiter character. Default: `","`.

**Returns:** `list[list[str]]`: rows of string values.

```python
import scriptling.csv as csv

text = "name,age\nAlice,30\nBob,25\n"
rows = csv.parse(text)
# [["name", "age"], ["Alice", "30"], ["Bob", "25"]]

# Quoted fields with embedded commas
rows = csv.parse('a,b\n"hello, world",x\n')
# [["a", "b"], ["hello, world", "x"]]
```

### `loads_dict(content, delimiter=",")`

Parse CSV text where the first row contains column headers. Each subsequent row becomes a dict mapping header names to cell values.

**Returns:** `list[dict]`: list of dicts keyed by header names.

```python
import scriptling.csv as csv

people = csv.parse_dict("name,age\nAlice,30\nBob,25\n")
# [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
print(people[0]["name"])  # "Alice"
```

### `dumps(rows, delimiter=",")`

Format a list of lists into CSV text. Values containing commas, quotes, or newlines are automatically quoted.

**Parameters:**
- `rows` (`list[list[str]]`): Rows to format.
- `delimiter` (`str`, keyword-only): Field delimiter. Default: `","`.

**Returns:** `str`: CSV-formatted text.

```python
import scriptling.csv as csv

text = csv.format([["a", "b"], ["1,000", "2"]])
# 'a,b\n"1,000",2\n'
```

### `dumps_dict(rows, delimiter=",", columns=None)`

Format a list of dicts into CSV text with a header row. Column headers are taken from the `columns` kwarg if provided, otherwise from the sorted keys of the first dict.

**Parameters:**
- `rows` (`list[dict]`): Dicts to format.
- `delimiter` (`str`, keyword-only): Field delimiter. Default: `","`.
- `columns` (`list[str]`, keyword-only): Explicit column order. Default: sorted keys.

**Returns:** `str`: CSV-formatted text with header row.

```python
import scriptling.csv as csv

text = csv.format_dict([
    {"name": "Alice", "age": "30"},
    {"name": "Bob", "age": "25"},
], columns=["name", "age"])
# "name,age\nAlice,30\nBob,25\n"
```

## Reading and Writing Files

Pair with `os` for file I/O:

```python
import scriptling.csv as csv
import os

# Read
rows = csv.parse_dict(os.read_file("data.csv"))

# Write
os.write_file("output.csv", csv.format_dict(rows, columns=["name", "age"]))
```

## See Also

- [json](https://scriptling.dev/okf/scriptling-libraries/data-formats/json.md): JSON parsing and formatting
- [yaml](https://scriptling.dev/okf/scriptling-libraries/data-formats/yaml.md): YAML parsing
- [toml](https://scriptling.dev/okf/scriptling-libraries/data-formats/toml.md): TOML parsing
