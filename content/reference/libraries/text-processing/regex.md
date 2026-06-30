---
title: regex
description: Regular expression matching and text processing, following Python's re module conventions.
weight: 1

aliases:
  - /reference/libraries/stdlib/regex/
  - /reference/libraries/regex/
---

Regular expression functions for pattern matching, searching, substitution, and splitting text. Import this library as `re`; function signatures and behavior follow Python's `re` module conventions, though the underlying engine is Go's RE2 (see [Differences from Python](#differences-from-python) below).

## Available Functions

| Function | Description |
|----------|-------------|
| `match(pattern, string, flags=0)` | Match pattern at the beginning of string |
| `search(pattern, string, flags=0)` | Search for pattern anywhere in string |
| `fullmatch(pattern, string, flags=0)` | Match pattern against the entire string |
| `findall(pattern, string, flags=0)` | Find all non-overlapping matches |
| `finditer(pattern, string, flags=0)` | Find all non-overlapping matches as Match objects |
| `sub(pattern, repl, string, count=0, flags=0)` | Replace pattern matches with repl |
| `split(pattern, string, maxsplit=0, flags=0)` | Split string by pattern |
| `compile(pattern, flags=0)` | Compile pattern into a reusable Regex object |
| `escape(string)` | Escape special regex characters in a string |

## Constants

| Constant | Description |
|----------|-------------|
| `re.IGNORECASE` (alias `re.I`) | Case-insensitive matching (`2`) |
| `re.MULTILINE` (alias `re.M`) | `^` and `$` match at line boundaries, not just string boundaries (`8`) |
| `re.DOTALL` (alias `re.S`) | `.` also matches newline characters (`16`) |

Flags can be combined with the bitwise OR operator (`|`):

```python
import re

m = re.match("hello", "HELLO\nWORLD", re.I | re.M)
if m:
    print(m.group(0))  # "HELLO"
```

## Matching

### `match(pattern, string, flags=0)`

Checks whether `pattern` matches at the beginning of `string`. Does not require the match to consume the entire string.

**Parameters:**
- `pattern` (`str`): Regular expression pattern.
- `string` (`str`): String to test.
- `flags` (`int`, optional): Bitwise combination of flag constants (e.g. `re.IGNORECASE`). Default: `0`.

**Returns:** `Match`: a match object if the pattern matches at the start of `string`, or `None` if it does not.

```python
import re

m = re.match("[0-9]+", "123abc")
if m:
    print("String starts with digits:", m.group(0))  # "123"

m = re.match("[0-9]+", "abc123")
if m is None:
    print("Pattern must match at start")

# Case-insensitive matching
m = re.match("hello", "HELLO world", re.I)
if m:
    print("Case-insensitive match:", m.group(0))  # "HELLO"
```

### `fullmatch(pattern, string, flags=0)`

Checks whether `pattern` matches the entirety of `string`, not just a prefix.

**Parameters:**
- `pattern` (`str`): Regular expression pattern.
- `string` (`str`): String to test.
- `flags` (`int`, optional): Bitwise combination of flag constants. Default: `0`.

**Returns:** `Match`: a match object if the pattern matches the entire string, or `None` if it does not.

```python
import re

if re.fullmatch("[0-9]+", "123"):
    print("Entire string is digits")  # This prints

if re.fullmatch("[0-9]+", "123abc") is None:
    print("Doesn't match the entire string")

# Case-insensitive fullmatch
if re.fullmatch("hello", "HELLO", re.I):
    print("Case-insensitive full match")  # This prints
```

## Searching

### `search(pattern, string, flags=0)`

Scans through `string` looking for the first location where `pattern` matches.

**Parameters:**
- `pattern` (`str`): Regular expression pattern.
- `string` (`str`): String to search.
- `flags` (`int`, optional): Bitwise combination of flag constants. Default: `0`.

**Returns:** `Match`: a match object for the first match found anywhere in `string`, or `None` if there is no match.

```python
import re

m = re.search(r'\w+@\w+\.\w+', "Contact: user@example.com")
if m:
    print(m.group(0))  # "user@example.com"

result = re.search("[0-9]+", "no numbers")
print(result)  # None

# Case-insensitive search
m = re.search("world", "HELLO WORLD", re.I)
if m:
    print(m.group(0))  # "WORLD"

# Using capturing groups
m = re.search(r'(\d+)-(\d+)', "Phone: 555-1234")
if m:
    print(m.group(0))  # "555-1234"
    print(m.group(1))  # "555"
    print(m.group(2))  # "1234"
    print(m.groups())  # ("555", "1234")
```

### `findall(pattern, string, flags=0)`

Finds all non-overlapping occurrences of `pattern` in `string`, scanning left to right.

**Parameters:**
- `pattern` (`str`): Regular expression pattern.
- `string` (`str`): String to search.
- `flags` (`int`, optional): Bitwise combination of flag constants. Default: `0`.

**Returns:** `list`: full-match strings if the pattern has no capturing groups; strings of the single group's text if there is exactly one capturing group; or `tuple` of group strings (one tuple per match) if there are multiple capturing groups.

```python
import re

phones = re.findall("[0-9]{3}-[0-9]{4}", "Call 555-1234 or 555-5678")
print(phones)  # ["555-1234", "555-5678"]

# Case-insensitive findall
words = re.findall("a+", "aAbBaAa", re.I)
print(words)  # ["aA", "aAa"]

# One capturing group -> list of strings for that group
years = re.findall(r'\((\d{4})\)', "Built (2019), updated (2023)")
print(years)  # ["2019", "2023"]

# Multiple capturing groups -> list of tuples
pairs = re.findall(r'(\w+)=(\w+)', "a=1 b=2")
print(pairs)  # [("a", "1"), ("b", "2")]
```

### `finditer(pattern, string, flags=0)`

Finds all non-overlapping occurrences of `pattern` in `string` and returns them as `Match` objects rather than plain strings, giving access to match positions and groups.

**Parameters:**
- `pattern` (`str`): Regular expression pattern.
- `string` (`str`): String to search.
- `flags` (`int`, optional): Bitwise combination of flag constants. Default: `0`.

**Returns:** `list` of `Match`: one match object per match found.

```python
import re

matches = re.finditer("[0-9]{3}-[0-9]{4}", "Call 555-1234 or 555-5678")
for match in matches:
    print(match.group(0))  # "555-1234", "555-5678"
    print(match.start())   # 5, 18
    print(match.end())     # 13, 26

# With capturing groups
matches = re.finditer(r'(\d+)-(\d+)', "555-1234, 888-9999")
for match in matches:
    print(match.group(0))  # "555-1234", "888-9999"
    print(match.group(1))  # "555", "888"
    print(match.group(2))  # "1234", "9999"
    print(match.groups())  # ("555", "1234"), ("888", "9999")
```

## Substitution and Splitting

### `sub(pattern, repl, string, count=0, flags=0)`

Replaces occurrences of `pattern` in `string` with `repl`. `repl` may be a literal replacement string, or a function that receives a `Match` object and returns the replacement text for that match.

**Parameters:**
- `pattern` (`str`): Regular expression pattern.
- `repl` (`str` or `function`): Replacement string, or a function taking a `Match` object and returning a `str`.
- `string` (`str`): String to perform replacements on.
- `count` (`int`, optional): Maximum number of replacements to make. `0` means replace all occurrences. Default: `0`.
- `flags` (`int`, optional): Bitwise combination of flag constants. Default: `0`.

**Returns:** `str`: the string with matches replaced.

```python
import re

# String replacement
text = re.sub("[0-9]+", "XXX", "Price: 100")
print(text)  # "Price: XXX"

# Replace multiple occurrences
result = re.sub("[0-9]+", "#", "a1b2c3")
print(result)  # "a#b#c#"

# Limit replacements with count
result = re.sub("[0-9]+", "X", "a1b2c3", 2)
print(result)  # "aXbXc3"

# Case-insensitive replacement
result = re.sub("hello", "hi", "Hello HELLO hello", 0, re.I)
print(result)  # "hi hi hi"

# Function replacement - uppercase all words
result = re.sub(r'(\w+)', lambda m: m.group(1).upper(), "hello world")
print(result)  # "HELLO WORLD"

# Function replacement - swap first and last name
result = re.sub(r'(\w+) (\w+)', lambda m: m.group(2) + " " + m.group(1), "John Doe")
print(result)  # "Doe John"
```

### `split(pattern, string, maxsplit=0, flags=0)`

Splits `string` at each occurrence of `pattern`.

**Parameters:**
- `pattern` (`str`): Regular expression pattern.
- `string` (`str`): String to split.
- `maxsplit` (`int`, optional): Maximum number of splits to perform. `0` means split on every occurrence. Default: `0`.
- `flags` (`int`, optional): Bitwise combination of flag constants. Default: `0`.

**Returns:** `list` of `str`: the substrings between matches of `pattern`.

```python
import re

parts = re.split("[,;]", "one,two;three")
print(parts)  # ["one", "two", "three"]

# Limit splits
parts = re.split("[,;]", "a,b;c;d", 2)
print(parts)  # ["a", "b;c;d"]
```

### `escape(string)`

Escapes all characters in `string` that have special meaning in a regular expression, so the result can be used as a literal pattern fragment.

**Parameters:**
- `string` (`str`): String to escape.

**Returns:** `str`: the escaped text.

```python
import re

escaped = re.escape("a.b+c")
print(escaped)  # "a\.b\+c"
```

## Compiled Patterns

### `compile(pattern, flags=0)`

Compiles `pattern` into a reusable `Regex` object. Compiling once and reusing the result avoids repeated parsing when the same pattern is matched against many strings (Scriptling also caches compiled patterns internally, so calling the module-level functions repeatedly with the same pattern is not expensive).

**Parameters:**
- `pattern` (`str`): Regular expression pattern.
- `flags` (`int`, optional): Bitwise combination of flag constants. Default: `0`.

**Returns:** `Regex`: the compiled pattern object.

**Raises:** `Error`: when `pattern` is not a valid regular expression.

```python
import re

pattern = re.compile("[0-9]+")
print(type(pattern))  # "Regex"

# Compile with flags
pattern = re.compile("hello", re.I | re.M)
print(type(pattern))  # "Regex"
```

The `Regex` object returned by `compile()` exposes the following methods, each taking only the string to operate on (the pattern and flags are already bound):

| Method | Description |
|--------|-------------|
| `pattern.match(string)` | Match at the start of `string`. Returns `Match` or `None`. |
| `pattern.search(string)` | Search anywhere in `string`. Returns `Match` or `None`. |
| `pattern.findall(string)` | Find all matches. Returns `list` of `str` or `tuple` (see `findall()` above). |
| `pattern.finditer(string)` | Find all matches as `Match` objects. Returns `list` of `Match`. |

```python
import re

pattern = re.compile(r'\d+')
m = pattern.match("123abc")
if m:
    print(m.group(0))  # "123"

matches = pattern.findall("a1b2c3")  # ["1", "2", "3"]

match_objects = pattern.finditer("a1b2c3")
for match in match_objects:
    print(match.group(0), match.start(), match.end())
    # "1" 1 2
    # "2" 3 4
    # "3" 5 6
```

## Match Objects

`match()`, `search()`, `fullmatch()`, and the `Regex` methods of the same names all return a `Match` object on success, or `None` if there is no match. `Match` objects expose the following methods:

| Method | Description |
|--------|-------------|
| `group(n=0)` | Returns the nth matched group (`0` = full match). |
| `groups()` | Returns a tuple of all capturing groups (excluding group `0`). |
| `start(n=0)` | Returns the start position of the match. |
| `end(n=0)` | Returns the end position of the match. |
| `span(n=0)` | Returns a `(start, end)` tuple for the match. |

> **Note:** `start()`, `end()`, and `span()` currently only support group `0` (the full match): passing a non-zero group number raises an error.

### `group(n=0)`

Returns the text of the nth matched group.

**Parameters:**
- `n` (`int`, optional): Group number, where `0` is the entire match and `1`, `2`, ... are capturing groups in order. Default: `0`.

**Returns:** `str`: the text matched by group `n`.

**Raises:** `Error`: when `n` does not correspond to an existing group.

```python
import re

m = re.search(r'(\w+)@(\w+)\.(\w+)', 'Email: user@example.com')
if m:
    print(m.group(0))   # 'user@example.com' (full match)
    print(m.group(1))   # 'user' (first group)
    print(m.group(2))   # 'example' (second group)
    print(m.group(3))   # 'com' (third group)
```

### `groups()`

Returns the text of all capturing groups, excluding group `0` (the full match).

**Parameters:** None

**Returns:** `tuple` of `str`: one entry per capturing group, in order.

```python
import re

m = re.search(r'(\w+)@(\w+)\.(\w+)', 'Email: user@example.com')
if m:
    print(m.groups())   # ('user', 'example', 'com')
```

### `start(n=0)`

Returns the index in the source string where the match (or group `n`) begins.

**Parameters:**
- `n` (`int`, optional): Group number. Only `0` is currently supported. Default: `0`.

**Returns:** `int`: the start index of the match.

**Raises:** `Error`: when `n` is not `0`.

```python
import re

m = re.search(r'(\w+)@(\w+)\.(\w+)', 'Email: user@example.com')
if m:
    print(m.start())    # 7 (position where match starts)
```

### `end(n=0)`

Returns the index in the source string just past where the match (or group `n`) ends.

**Parameters:**
- `n` (`int`, optional): Group number. Only `0` is currently supported. Default: `0`.

**Returns:** `int`: the end index of the match.

**Raises:** `Error`: when `n` is not `0`.

```python
import re

m = re.search(r'(\w+)@(\w+)\.(\w+)', 'Email: user@example.com')
if m:
    print(m.end())      # 23 (position where match ends)
```

### `span(n=0)`

Returns the `(start, end)` indices of the match (or group `n`) as a single tuple: equivalent to `(m.start(n), m.end(n))`.

**Parameters:**
- `n` (`int`, optional): Group number. Only `0` is currently supported. Default: `0`.

**Returns:** `tuple` of `int`: `(start, end)`.

**Raises:** `Error`: when `n` is not `0`.

```python
import re

m = re.search(r'(\w+)@(\w+)\.(\w+)', 'Email: user@example.com')
if m:
    print(m.span())     # (7, 23)
```

## Regular Expression Syntax

Scriptling uses Go's `regexp` syntax, which is similar to Perl/Python:

### Basic Patterns

- `.`: Any character (newlines only with the `DOTALL` flag)
- `\d`: Digit (`0`-`9`)
- `\D`: Non-digit
- `\w`: Word character (`a`-`z`, `A`-`Z`, `0`-`9`, `_`)
- `\W`: Non-word character
- `\s`: Whitespace
- `\S`: Non-whitespace

### Quantifiers

- `*`: Zero or more
- `+`: One or more
- `?`: Zero or one
- `{n}`: Exactly n times
- `{n,}`: n or more times
- `{n,m}`: Between n and m times

### Character Classes

- `[abc]`: Any of a, b, or c
- `[^abc]`: Not a, b, or c
- `[a-z]`: Any lowercase letter
- `[A-Z]`: Any uppercase letter
- `[0-9]`: Any digit

### Anchors

- `^`: Start of string (or line with the `MULTILINE` flag)
- `$`: End of string (or line with the `MULTILINE` flag)
- `\b`: Word boundary
- `\B`: Not a word boundary

### Inline Flags

Flag modifiers can also be embedded directly in the pattern instead of passed as the `flags` argument:

- `(?i)`: Case-insensitive
- `(?m)`: Multiline mode
- `(?s)`: Dotall mode (`.` matches newlines)

```python
import re

m = re.match("(?i)hello", "HELLO world")
if m:
    print("Inline flag match:", m.group(0))
```

## Python Compatibility

Scriptling uses Go's RE2 engine, which intentionally omits some features found in Python's `re` module (which uses a backtracking engine):

| Feature | Python `re` | Scriptling (RE2) | Workaround |
|---------|-------------|------------------|------------|
| Backreferences (`\1`, `\2`) | Yes | No | Restructure pattern to avoid them |
| Lookahead (`(?=...)`) | Yes | No | Restructure pattern or post-filter results |
| Lookbehind (`(?<=...)`) | Yes | No | Restructure pattern or post-filter results |
| Negative lookahead (`(?!...)`) | Yes | No | Restructure pattern or post-filter results |
| Negative lookbehind (`(?<!...)`) | Yes | No | Restructure pattern or post-filter results |
| Atomic groups (`(?>...)`) | Yes | No | Not needed with RE2 (no backtracking) |
| Possessive quantifiers (`*+`, `++`) | Yes | No | Not needed with RE2 (no backtracking) |
| Named backreferences (`(?P=name)`) | Yes | No | Restructure pattern to avoid them |

The most common issue is **backreferences**: patterns like `r'<(h\d)>.*?</\1>'` that use `\1` to match the same text as a capturing group will fail with a compile error. Rewrite them to repeat the pattern explicitly:

```python
import re

# Python - uses backreference \1 to match closing tag
# pattern = r'<(h\d)>(.*?)</\1>'  # Does NOT work in Scriptling

# Scriptling - repeat the pattern instead
matches = re.findall(r'<(h\d)>(.*?)</(?:h\d)>', html, re.IGNORECASE | re.DOTALL)
for tag, content in matches:
    print(tag, content)
```

Other differences worth noting:

- `match()` and `search()` return `Match` objects (not strings), matching Python.
- All matching is case-sensitive by default; use `re.IGNORECASE`/`re.I` or the inline `(?i)` flag for case-insensitive matching.
- `Match.start()`, `Match.end()`, and `Match.span()` only support group `0`: Python supports any group number for these.

## See Also

- [html](../html/): HTML escaping and unescaping utilities
- [html.parser](../html.parser/): HTML/XHTML parser for structured markup
- [string](../string/): String constants
- [difflib](../difflib/): Sequence comparison and diff generation
