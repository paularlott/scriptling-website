---
description: String constants for character classification, matching Python's string module.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/text-processing/string/
sources:
    - resource: https://scriptling.dev/reference/libraries/text-processing/string/
status: stable
tags:
    - libraries
    - text
title: string
type: API Reference
---
# string

The `string` library provides string constants for character classification, such as ASCII letters, digits, and punctuation. It is commonly used for validating input or building character sets, matching Python's `string` module.

## Constants

| Constant          | Description                                                            |
| ------------------ | ------------------------------------------------------------------------ |
| `ascii_letters`   | Concatenation of `ascii_lowercase` and `ascii_uppercase` (`"abc...xyzABC...XYZ"`) |
| `ascii_lowercase` | Lowercase ASCII letters (`"abcdefghijklmnopqrstuvwxyz"`)                |
| `ascii_uppercase` | Uppercase ASCII letters (`"ABCDEFGHIJKLMNOPQRSTUVWXYZ"`)                |
| `digits`          | Decimal digits (`"0123456789"`)                                         |
| `hexdigits`       | Hexadecimal digits (`"0123456789abcdefABCDEF"`)                         |
| `octdigits`       | Octal digits (`"01234567"`)                                             |
| `punctuation`     | ASCII punctuation characters (`` "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" ``) |
| `whitespace`      | Whitespace characters (`" \t\n\r\v\f"`)                                 |
| `printable`       | Concatenation of `digits`, `ascii_letters`, `punctuation`, and `whitespace` |

## Examples

### Character Validation

```python
import string

def is_valid_identifier(s):
    if len(s) == 0:
        return False
    # First char must be letter or underscore
    if s[0] not in string.ascii_letters + "_":
        return False
    # Rest can include digits
    valid = string.ascii_letters + string.digits + "_"
    for c in s:
        if c not in valid:
            return False
    return True

print(is_valid_identifier("my_var"))   # True
print(is_valid_identifier("123abc"))   # False
```

### Generate Random String

```python
import string
import random

def random_string(length):
    chars = string.ascii_letters + string.digits
    result = ""
    for i in range(length):
        result = result + random.choice(chars)
    return result

print(random_string(10))  # e.g., "aB3xY7mK2p"
```

### Check for Hex String

```python
import string

def is_hex(s):
    for c in s:
        if c not in string.hexdigits:
            return False
    return True

print(is_hex("deadbeef"))  # True
print(is_hex("xyz123"))    # False
```

## Python Compatibility

This module provides the same constants as Python's `string` module. The `capwords()` function and the `Template` and `Formatter` classes are not available; use `str.title()`, f-strings or `str.format()` instead.

## See Also

- [textwrap](https://scriptling.dev/okf/scriptling-libraries/text-processing/textwrap.md) - Text wrapping and filling utilities
- [regex](https://scriptling.dev/okf/scriptling-libraries/text-processing/regex.md) - Regular expressions for pattern matching
- [difflib](https://scriptling.dev/okf/scriptling-libraries/text-processing/difflib.md) - Sequence comparison and diffing utilities
- [html](https://scriptling.dev/okf/scriptling-libraries/text-processing/html.md) - HTML escaping and unescaping
