---
description: TOON (Token-Oriented Object Notation) encoding and decoding, a compact, human-readable alternative to JSON.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/utilities/toon/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/utilities/toon/
status: stable
tags:
    - libraries
    - utilities
    - data-formats
title: scriptling.toon
type: API Reference
---
# scriptling.toon

The `scriptling.toon` library encodes and decodes TOON (Token-Oriented Object Notation), a human-readable data format that's more compact than JSON, with support for inline objects, flexible syntax, comments, and tabular data. Reach for it when writing config files by hand, exchanging data with humans in the loop, or minimizing token usage when passing structured data to an LLM.

## Available Functions

| Function | Description |
|----------|-------------|
| `encode(data)` | Encode data to TOON format |
| `decode(text)` | Decode a TOON string to objects |
| `encode_options(data, indent, delimiter)` | Encode with custom indentation and delimiter |
| `decode_options(text, strict, indent_size)` | Decode with custom parsing options |

## Functions

### `encode(data)`

Encodes a Scriptling value to TOON format.

**Parameters:**
- `data`: Any Scriptling value to encode (`str`, `int`, `float`, `bool`, `list`, `dict`).

**Returns:** `str`: TOON-formatted string.

```python
import scriptling.toon as toon

# Encode a dictionary
data = {"name": "Alice", "age": 30, "active": true}
text = toon.encode(data)
print(text)
# name: Alice
# age: 30
# active: true

# Encode a list
items = [1, 2, 3, 4, 5]
text = toon.encode(items)
print(text)
# - 1
# - 2
# - 3
# - 4
# - 5
```

### `decode(text)`

Decodes a TOON-formatted string to Scriptling objects.

**Parameters:**
- `text` (`str`): TOON-formatted string.

**Returns:** Decoded Scriptling value (`dict`, `list`, `str`, `int`, `float`, `bool`, or `None`).

**Raises:** `Error`: on invalid TOON syntax under strict parsing.

```python
import scriptling.toon as toon

text = """
name: Alice
age: 30
active: true
tags:
  - python
  - golang
"""

data = toon.decode(text)
print(data.name)    # "Alice"
print(data.age)     # 30
print(data.active)  # True
print(data.tags[0]) # "python"
```

### `encode_options(data, indent, delimiter)`

Encodes data to TOON format with a custom indentation width and array delimiter.

**Parameters:**
- `data`: Any Scriptling value to encode.
- `indent` (`int`): Number of spaces per indentation level.
- `delimiter` (`str`): Delimiter for arrays and tabular data.

**Returns:** `str`: TOON-formatted string.

```python
import scriptling.toon as toon

data = [1, 2, 3, 4, 5]

# Custom delimiter
text = toon.encode_options(data, 2, "|")
# [1|2|3|4|5]
```

### `decode_options(text, strict, indent_size)`

Decodes a TOON-formatted string with custom parsing options.

**Parameters:**
- `text` (`str`): TOON-formatted string.
- `strict` (`bool`): Enable strict validation; when `False`, parsing attempts to continue past errors.
- `indent_size` (`int`): Expected indentation size; `0` auto-detects it from the input.

**Returns:** Decoded Scriptling value.

**Raises:** `Error`: on invalid TOON syntax when `strict=True`.

```python
import scriptling.toon as toon

text = """
name: Alice
age: thirty  # Invalid number
"""

# Strict mode (default): raises on errors
try:
    data = toon.decode(text)
except Exception as e:
    print("Parse error:", e)

# Lenient mode: attempts to continue
data = toon.decode_options(text, False, 0)
```

## TOON Format Reference

### Basic types

```toon
name: Alice
description: Hello, World!
empty: ""
count: 42
price: 19.99
negative: -10
scientific: 1.5e-10
active: true
deleted: false
value: null
```

### Lists

Inline lists:

```toon
numbers: [1, 2, 3]
names: [Alice, Bob, Charlie]
mixed: [1, two, 3.0, true]
```

Multiline lists:

```toon
fruits:
  - apple
  - banana
  - orange
```

### Dictionaries

Inline dictionaries:

```toon
person: {name: Alice, age: 30}
```

Multiline dictionaries, including nesting:

```toon
company:
  name: TechCorp
  employees:
    - name: Alice
      role: Developer
    - name: Bob
      role: Designer
  address:
    street: 123 Main St
    city: San Francisco
```

### Tabular data

TOON detects uniform lists of records automatically and can render them as a table:

```toon
users:
  name    | age   | city
  Alice   | 30    | Paris
  Bob     | 25    | London
  Charlie | 35    | New York
```

This decodes to:

```python
{
  "users": [
    {"name": "Alice", "age": 30, "city": "Paris"},
    {"name": "Bob", "age": 25, "city": "London"},
    {"name": "Charlie", "age": 35, "city": "New York"}
  ]
}
```

### Comments

TOON supports `#` comments, both standalone and inline:

```toon
# This is a comment
name: Alice  # Inline comment
age: 30
```

## Comparing TOON to JSON

**JSON:**

```json
{"name":"Alice","age":30,"active":true,"tags":["python","golang"]}
```

**TOON:**

```toon
name: Alice
age: 30
active: true
tags: [python, golang]
```

Use TOON for hand-written config, human-in-the-loop data, comments, and tabular data. Use JSON when interoperating with other systems or machine parsing is the priority.

## See Also

- [scriptling.similarity](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/similarity.md) - Fuzzy matching and tokenization, often used alongside decoded TOON records
