---
title: Syntax Rules
description: Indentation, comments, case sensitivity, and multiline syntax in Scriptling.
weight: 1
---

Scriptling uses Python-inspired syntax with specific rules for code structure.

## Indentation

Scriptling uses **Python-style indentation** (4 spaces recommended) to define code blocks:

```python
if x > 5:
    print("yes")    # 4 spaces indent
    y = 10
```

Indentation determines which statements belong to which block. Consistent indentation is required throughout a file.

## Comments

```python
# Single-line comments only
x = 5  # Inline comments supported
```

Comments start with `#` and extend to the end of the line. Multi-line comments are not supported (use multiple single-line comments).

## Triple-Quoted Strings

Scriptling supports triple-quoted strings for multi-line text:

```python
multi_line = """
This is a
multi-line string
"""

single_line = '''Also works with single quotes'''
```

## Raw Strings

Raw string prefixes `r` or `R` prevent escape sequence processing:

```python
# Regular string - \n is a newline
regular = "line1\nline2"

# Raw string - \n is literal backslash-n
raw = r"\n\t"  # Contains backslash-n and backslash-t literally

# Useful for regular expressions and file paths
import re
pattern = r"\d+\.\d+"  # Matches decimal numbers
```

## Case Sensitivity

- **Keywords**: lowercase (`if`, `while`, `def`, `return`, `for`, `in`, `not`, `and`, `or`)
- **Booleans**: `True`, `False` (capitalized)
- **None**: `None` (capitalized)
- **Variables**: case-sensitive (`myVar` ≠ `myvar`)

```python
# Keywords are lowercase
if x > 0:
    while x < 10:
        x += 1

# Booleans are capitalized
is_valid = True
is_empty = False
result = None

# Variables are case-sensitive
name = "Alice"
Name = "Bob"  # Different variable
NAME = "Charlie"  # Yet another variable
```

## Multiline Syntax

Scriptling supports multiline definitions for lists, dictionaries, function calls, and function definitions. Indentation is ignored inside parentheses, brackets, and braces.

### Multiline Lists

```python
numbers = [
    1,
    2,
    3,
]

nested = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
```

### Multiline Dictionaries

```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "NYC",
}

config = {
    "database": {
        "host": "localhost",
        "port": 5432,
    },
    "cache": {
        "enabled": True,
        "ttl": 3600,
    },
}
```

### Multiline Function Calls

```python
result = my_function(
    arg1,
    arg2,
    key="value",
    timeout=30,
)

response = requests.get(
    "https://api.example.com/data",
    {
        "timeout": 10,
        "headers": {"Authorization": "Bearer token"},
    }
)
```

### Multiline Function Definitions

```python
def process_data(
    input_data,
    output_path,
    format="json",
    validate=True,
    max_retries=3,
):
    # Function body
    pass
```

## Trailing Commas

Trailing commas are allowed in lists, dictionaries, function calls, and function definitions. This makes it easier to add or remove items in multiline structures.

```python
# Lists with trailing comma
items = [
    "first",
    "second",
    "third",  # Trailing comma OK
]

# Dictionaries with trailing comma
config = {
    "host": "localhost",
    "port": 8080,  # Trailing comma OK
}

# Function calls with trailing comma
result = process(
    data,
    options,
    callback,  # Trailing comma OK
)
```

## Identifiers

Variable and function names must follow these rules:

- Start with a letter or underscore
- Contain letters, digits, and underscores
- Cannot be a reserved keyword

```python
# Valid identifiers
name = "valid"
_name = "valid"
name123 = "valid"
my_function = "valid"
MyClass = "valid"

# Invalid identifiers
123name = "invalid"  # Starts with digit
my-var = "invalid"  # Contains hyphen
my var = "invalid"  # Contains space
```

## Reserved Keywords

These words cannot be used as identifiers:

```
False      None       True       and        as
assert     async      await      break      class
continue   def        del        elif       else
except     finally    for        from       global
if         import     in         is         lambda
nonlocal   not        or         pass       raise
return     try        while      with       yield
match      case       super
```

## See Also

- [Data Types](./types/) - Available data types in Scriptling
- [Functions](./functions/) - Function definition and parameters
- [Python Differences](./python-differences/) - Differences from Python
