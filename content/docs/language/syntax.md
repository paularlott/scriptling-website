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

## F-Strings

F-strings (formatted string literals) embed expressions directly in strings using `{expr}` syntax:

```python
name = "Alice"
age = 30
pi = 3.14159

# Basic expression embedding
greeting = f"Hello, {name}! You are {age} years old."

# Arithmetic in expressions
result = f"Sum: {2 + 2}, Product: {3 * 4}"

# Method calls
upper = f"Name: {name.upper()}"
```

### Format Specifiers

F-strings support Python's full format spec mini-language: `f"{value:[[fill]align][sign][0][width][,][.precision][type]}"`

#### Alignment

| Spec | Meaning | Example | Result |
|------|---------|---------|--------|
| `<width` | Left-align | `f"{'hi':<10}"` | `"hi        "` |
| `>width` | Right-align | `f"{'hi':>10}"` | `"        hi"` |
| `^width` | Center | `f"{'hi':^10}"` | `"    hi    "` |
| `fill<width` | Left-align with fill | `f"{'hi':*<10}"` | `"hi********"` |
| `fill>width` | Right-align with fill | `f"{'hi':*>10}"` | `"********hi"` |
| `fill^width` | Center with fill | `f"{'hi':*^10}"` | `"****hi****"` |

#### Sign

| Spec | Meaning | Example | Result |
|------|---------|---------|--------|
| `+` | Always show sign | `f"{42:+d}"` | `"+42"` |
| `-` | Only show for negative (default) | `f"{42:-d}"` | `"42"` |
| ` ` | Space for positive | `f"{42: d}"` | `" 42"` |

#### Integer Types

| Spec | Meaning | Example | Result |
|------|---------|---------|--------|
| `d` | Decimal | `f"{255:d}"` | `"255"` |
| `x` | Hex lowercase | `f"{255:x}"` | `"ff"` |
| `X` | Hex uppercase | `f"{255:X}"` | `"FF"` |
| `o` | Octal | `f"{8:o}"` | `"10"` |
| `b` | Binary | `f"{10:b}"` | `"1010"` |
| `08x` | Zero-padded hex | `f"{255:08x}"` | `"000000ff"` |
| `010d` | Zero-padded decimal | `f"{42:010d}"` | `"0000000042"` |
| `,` | Thousands separator | `f"{1234567:,}"` | `"1,234,567"` |

#### Float Types

| Spec | Meaning | Example | Result |
|------|---------|---------|--------|
| `.2f` | Fixed 2 decimal places | `f"{3.14159:.2f}"` | `"3.14"` |
| `10.2f` | Width + precision | `f"{3.14:10.2f}"` | `"      3.14"` |
| `,.2f` | Thousands + precision | `f"{1234.5:,.2f}"` | `"1,234.50"` |
| `.2e` | Scientific notation | `f"{12345:.2e}"` | `"1.23e+04"` |
| `.2E` | Scientific uppercase | `f"{12345:.2E}"` | `"1.23E+04"` |
| `.3g` | General (shorter of f/e) | `f"{0.00012:.3g}"` | `"0.00012"` |
| `.1%` | Percentage | `f"{0.75:.1%}"` | `"75.0%"` |
| `+.2f` | Always show sign | `f"{3.14:+.2f}"` | `"+3.14"` |

#### String Types

| Spec | Meaning | Example | Result |
|------|---------|---------|--------|
| `.5` | Truncate to 5 chars | `f"{'hello world':.5}"` | `"hello"` |
| `.5s` | Truncate (explicit) | `f"{'hello world':.5s}"` | `"hello"` |
| `<20` | Left-align in 20 chars | `f"{'hi':<20}"` | `"hi                  "` |
| `>20` | Right-align in 20 chars | `f"{'hi':>20}"` | `"                  hi"` |

#### Combining Specifiers

```python
# Date formatting
year, month, day = 2024, 3, 5
date = f"{year:04d}-{month:02d}-{day:02d}"  # "2024-03-05"

# Table formatting
for name, score in [("Alice", 95.5), ("Bob", 87.3)]:
    print(f"{name:<10} {score:6.1f}")
# Alice       95.5
# Bob         87.3

# Financial formatting
amount = 1234567.89
print(f"Total: ${amount:,.2f}")  # "Total: $1,234,567.89"

# Hex dump
for byte in [0, 127, 255]:
    print(f"0x{byte:02x}")  # "0x00", "0x7f", "0xff"
```

### Escaped Braces

Use `{{` and `}}` to include literal braces:

```python
name = "world"
result = f"{{hello}} {name}"  # "{hello} world"
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
