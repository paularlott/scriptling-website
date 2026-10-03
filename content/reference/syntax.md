---
title: Syntax Rules
description: Indentation, comments, strings, multiline syntax, imports and keywords in Scriptling.
tags: [reference, syntax]
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

## Escape Sequences

Strings, triple-quoted strings, f-strings and bytes literals process Python's escape sequences:

| Escape | Meaning |
|--------|---------|
| `\n`, `\t`, `\r` | Newline, tab, carriage return |
| `\\`, `\'`, `\"` | Backslash and quotes |
| `\a`, `\b`, `\f`, `\v` | Bell, backspace, form feed, vertical tab |
| `\xhh` | Character (in bytes, the byte) with hex value `hh` |
| `\ooo` | Character or byte with octal value `ooo` (`\0` is NUL) |
| `\uXXXX`, `\UXXXXXXXX` | Unicode code point (not in bytes literals) |
| `\` at the end of a line | Continues the string on the next line |

Any other backslash sequence, such as `\d` in a regular expression, is kept as written. `\N{name}` is not supported; use `\u` with the code point. Raw strings are still the clearest choice for regular expressions.

```python
"caf\u00e9"    # 'café'
b"\x00\xff"     # 2 bytes
"\x41\101"      # 'AA'
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

# Raw bytes: rb"..." or br"..."
raw_bytes = rb"\x41"  # 4 bytes: backslash, x, 4, 1
```

### Adjacent String Literals

String literals next to each other in the same expression are concatenated at parse time. This works with ordinary strings and f-strings, including across lines inside parentheses:

```python
message = "hello " "world"                 # "hello world"
name = "Alice"
greeting = ("Hello, "
            f"{name}!")                     # "Hello, Alice!"
parts = ["one" "two", "three"]             # ["onetwo", "three"]
```

Only literal tokens concatenate this way. Variables do not concatenate implicitly, and a statement boundary such as a semicolon or an ungrouped newline ends the expression.

### Raw F-Strings

Combine `r` and `f` prefixes (in either order) to create raw f-strings that preserve backslashes while supporting expression interpolation:

```python
# Raw f-string: backslashes are literal, {expr} still works
name = "world"
greeting = rf"hello {name}"  # "hello world"

# Useful for regex patterns with interpolation
digit_pattern = r"\d+"
pattern = rf"{digit_pattern}\.{digit_pattern}"  # \d+\.\d+

# Both prefix orders work: rf, fr, RF, FR, rF, fR, etc.
path = fr"C:\Users\{name}"  # Backslashes preserved
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

### Explicit Line Continuation

A backslash at the very end of a line joins it to the next line, exactly as in Python. Use it where there are no brackets to continue inside, such as a long condition or an assignment:

```python
simple = (not images) and \
    (not loom_urls) and \
    estimate_tokens(body) <= budget

if simple and \
        total < 100:
    print("single call")
```

The continuation line's indentation is not significant, and the whole statement belongs to the block it started in. The backslash must be the last character on the line; a backslash followed by anything else is a syntax error. An error inside a continued statement is reported against the line the statement starts on. Inside parentheses, brackets or braces no backslash is needed, and that remains the preferred style.

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

## Imports

Imports work as in Python. A library must be made available by the host (or the CLI's library paths) before a script can import it.

```python
import json                          # binds json
import urllib.parse                  # binds urllib, with urllib.parse inside
import urllib.parse as up            # binds up only
import math, json                    # several at once

from math import sqrt, floor         # binds the names directly
from math import sqrt as root        # with an alias
```

### Parenthesized Import Lists

Wrap the names in parentheses to split a long list across lines. A trailing comma is allowed:

```python
from scriptling.ai import (
    Client,
    ToolRegistry,
    estimate_tokens,
)
```

### Relative Imports

Inside a library module, leading dots import relative to that module's package, as in Python. `from . import x` imports a sibling, `from .. import x` goes up one level, and `from .helpers import x` imports from a sibling module. Relative imports are only valid inside a library; the main script has no package.

### Lazy Imports

Python 3.15's `lazy import` (PEP 810) is accepted so such code runs unchanged:

```python
lazy import json
lazy from math import sqrt
```

The `lazy` hint is ignored and the import happens immediately. Imports in Scriptling are already cheap, and importing eagerly means a missing library fails at the import line rather than at first use. `lazy` is only special directly before `import` or `from`, so it is still an ordinary name everywhere else.

### Not Supported

`from module import *` is not supported; import the names you need.

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
assert     break      class      continue   def
del        elif       else       except     finally
for        from       global     if         import
in         is         lambda     nonlocal   not
or         pass       raise      return     try
while      with
```

`match` and `case` are contextual keywords: they are only special inside a `match` statement and may be used as ordinary identifiers everywhere else (for example, `match = 5`).

`lazy` is also contextual: it is only special directly before `import` or `from` (see [Lazy Imports](#lazy-imports)).

`async`, `await`, and `yield` are not keywords in Scriptling (the features they denote in Python are not implemented). `super` is an ordinary builtin function, not a keyword.

## See Also

- [Data Types](../types/) - Available data types in Scriptling
- [Functions](../functions/) - Function definition and parameters
- [Python Differences](../python-differences/) - Differences from Python
