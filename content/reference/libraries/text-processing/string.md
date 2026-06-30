---
title: string
description: String constants for character classification, matching Python's string module.
weight: 1

aliases:
  - /reference/libraries/stdlib/string/
  - /reference/libraries/string/
---

The `string` library provides string constants for character classification, such as ASCII letters, digits, and punctuation. It is commonly used for validating input or building character sets, matching Python's `string` module.

## Available Functions

This library has no functions, only constants.

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

### `string.ascii_letters`

Concatenation of `ascii_lowercase` and `ascii_uppercase`.

**Value:** `str` (`"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"`)

```python
import string
print(string.ascii_letters)  # "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
```

### `string.ascii_lowercase`

Lowercase ASCII letters.

**Value:** `str` (`"abcdefghijklmnopqrstuvwxyz"`)

```python
import string
print(string.ascii_lowercase)  # "abcdefghijklmnopqrstuvwxyz"
```

### `string.ascii_uppercase`

Uppercase ASCII letters.

**Value:** `str` (`"ABCDEFGHIJKLMNOPQRSTUVWXYZ"`)

```python
import string
print(string.ascii_uppercase)  # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```

### `string.digits`

Decimal digits.

**Value:** `str` (`"0123456789"`)

```python
import string
print(string.digits)  # "0123456789"
```

### `string.hexdigits`

Hexadecimal digits, including both lowercase and uppercase letter forms.

**Value:** `str` (`"0123456789abcdefABCDEF"`)

```python
import string
print(string.hexdigits)  # "0123456789abcdefABCDEF"
```

### `string.octdigits`

Octal digits.

**Value:** `str` (`"01234567"`)

```python
import string
print(string.octdigits)  # "01234567"
```

### `string.punctuation`

ASCII punctuation characters.

**Value:** `str` (`` "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" ``)

```python
import string
print(string.punctuation)  # "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
```

### `string.whitespace`

Whitespace characters: space, tab, newline, carriage return, vertical tab, and form feed.

**Value:** `str` (`" \t\n\r\v\f"`)

```python
import string
print(repr(string.whitespace))  # ' \t\n\r\x0b\x0c'
```

### `string.printable`

Concatenation of `digits`, `ascii_letters`, `punctuation`, and `whitespace`.

**Value:** `str`

```python
import string
print(string.printable)
```

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

This module provides the same constants as Python's `string` module.

## See Also

- [textwrap](./textwrap.md) - Text wrapping and filling utilities
- [regex](./regex.md) - Regular expressions for pattern matching
- [difflib](./difflib.md) - Sequence comparison and diffing utilities
- [html](./html.md) - HTML escaping and unescaping
