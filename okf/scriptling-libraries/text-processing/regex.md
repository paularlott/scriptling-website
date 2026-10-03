---
description: Regular expression matching and text processing, following Python's re module conventions.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/text-processing/regex/
sources:
    - resource: https://scriptling.dev/reference/libraries/text-processing/regex/
status: stable
tags:
    - libraries
    - text
    - regex
    - regular-expressions
title: re
type: API Reference
---
# re

Regular expression functions for pattern matching, searching, substitution, and splitting text. Import this library as `re`; function signatures and behavior follow Python's `re` module conventions, though the underlying engine is Go's RE2 (see [Python Compatibility](#python-compatibility) below).

## Available Functions

| Function | Description |
|----------|-------------|
| `match(pattern, string, flags=0)` | Match at the start of `string`. Returns a `Match` or `None`. |
| `search(pattern, string, flags=0)` | First match anywhere in `string`. Returns a `Match` or `None`. |
| `fullmatch(pattern, string, flags=0)` | Match the whole of `string`. Returns a `Match` or `None`. |
| `findall(pattern, string, flags=0)` | All non-overlapping matches: strings, one group's text, or tuples when there are several groups. |
| `finditer(pattern, string, flags=0)` | All matches as a `list` of `Match` objects. |
| `sub(pattern, repl, string, count=0, flags=0)` | Replace matches with a string (`\1`, `\g<name>` allowed) or the result of a function taking a `Match`. |
| `subn(pattern, repl, string, count=0, flags=0)` | Like `sub()`, returning `(new_string, number_of_substitutions)`. |
| `split(pattern, string, maxsplit=0, flags=0)` | Split `string` at each match; `maxsplit` limits the number of splits. |
| `compile(pattern, flags=0)` | Compile into a reusable `Regex` object (see [Compiled Patterns](#compiled-patterns)). |
| `escape(string)` | Escape regex metacharacters so `string` matches literally. |

## Constants

| Constant | Description |
|----------|-------------|
| `re.IGNORECASE` (alias `re.I`) | Case-insensitive matching (`2`) |
| `re.MULTILINE` (alias `re.M`) | `^` and `$` match at line boundaries, not just string boundaries (`8`) |
| `re.DOTALL` (alias `re.S`) | `.` also matches newline characters (`16`) |

Combine flags with `|` (for example `re.I | re.M`). Pass them **positionally**, or inline in the pattern as `(?i)`, `(?m)`, `(?s)`: the `flags=` keyword form is currently ignored (see [Python Compatibility](#python-compatibility)).

## Example

```python
import re

# match / fullmatch / search return a Match or None
print(re.match(r"\d+", "123abc").group())       # 123
print(re.match(r"\d+", "abc123"))               # None
print(re.fullmatch(r"\d+", "123abc"))           # None
m = re.search(r"(\d+)-(\d+)", "Phone: 555-1234")
print(m.group(0), m.group(1), m.groups())       # 555-1234 555 ('555', '1234')
print(m.start(), m.end(), m.span())             # 7 15 (7, 15)

# findall: whole matches, one group's text, or tuples for several groups
print(re.findall(r"\d{3}-\d{4}", "Call 555-1234 or 555-5678"))  # ['555-1234', '555-5678']
print(re.findall(r"\((\d{4})\)", "Built (2019), updated (2023)"))  # ['2019', '2023']
print(re.findall(r"(\w+)=(\w+)", "a=1 b=2"))     # [('a', '1'), ('b', '2')]
for m in re.finditer(r"\d+", "a1b22"):
    print(m.group(), m.start())                 # 1 1, then 22 3

# sub / subn: string or function replacement, optional count
print(re.sub(r"\d+", "#", "a1b2c3"))            # a#b#c#
print(re.sub(r"\d+", "X", "a1b2c3", count=2))   # aXbXc3
print(re.sub(r"(\w+) (\w+)", r"\2 \1", "John Doe"))  # Doe John
print(re.sub(r"\w+", lambda m: m.group().upper(), "hello world"))  # HELLO WORLD
print(re.subn("a", "b", "banana"))              # ('bbnbnb', 3)

# split, with an optional maxsplit
print(re.split("[,;]", "one,two;three"))        # ['one', 'two', 'three']
print(re.split("[,;]", "a,b;c;d", maxsplit=2))  # ['a', 'b', 'c;d']

print(re.escape("a.b+c"))                       # a\.b\+c

# Flags: pass positionally, or inline as (?i), (?m), (?s)
print(re.sub("hello", "hi", "Hello HELLO hello", 0, re.I))  # hi hi hi
print(re.search("(?i)world", "HELLO WORLD").group())        # WORLD

# Named groups
m = re.search(r"(?P<user>\w+)@(?P<host>[\w.]+)", "Email: user@example.com")
print(m.group("user"), m.groupdict()["host"])   # user example.com
```

## Compiled Patterns

`compile()` returns a `Regex` object whose methods take only the string (the pattern and flags are already bound). Scriptling also caches compiled patterns internally, so calling the module-level functions repeatedly with the same pattern is not expensive. An invalid pattern raises an error at compile time.

| Method | Description |
|--------|-------------|
| `pattern.match(string)` | Match at the start of `string`. Returns `Match` or `None`. |
| `pattern.search(string)` | Search anywhere in `string`. Returns `Match` or `None`. |
| `pattern.findall(string)` | All matches, as for `findall()`. |
| `pattern.finditer(string)` | All matches as a `list` of `Match` objects. |

`Regex` objects have no `sub`, `split`, or `fullmatch` methods; call the module-level functions instead.

```python
import re

digits = re.compile(r"\d+")
print(digits.findall("a1b2c3"))       # ['1', '2', '3']
print(digits.match("123abc").group())  # 123

word = re.compile("hello", re.I)
print(word.search("Say HELLO").group())  # HELLO
```

## Match Objects

| Method | Description |
|--------|-------------|
| `group(n=0)` | Text of group `n` (`0` is the whole match), or of a named group `group("name")`. |
| `groups()` | Tuple of all capturing groups, excluding group `0`. |
| `groupdict()` | Dict of named groups (`(?P<name>...)`) to their text. |
| `start(n=0)` | Start index of the match. |
| `end(n=0)` | End index of the match. |
| `span(n=0)` | `(start, end)` tuple for the match. |

`start()`, `end()`, and `span()` support only group `0`; passing another group number raises an error.

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
html = "<h1>Title</h1><h2>Intro</h2>"
matches = re.findall(r'<(h\d)>(.*?)</(?:h\d)>', html, re.IGNORECASE | re.DOTALL)
for tag, content in matches:
    print(tag, content)  # h1 Title, then h2 Intro
```

Other differences worth noting:

- The `flags=` keyword argument is ignored by `match`, `search`, `fullmatch`, `findall`, `finditer`, `sub`, `subn`, `split`, and `compile`: `re.search("world", "HELLO WORLD", flags=re.I)` returns `None`. Pass flags positionally (`re.search("world", "HELLO WORLD", re.I)`) or use inline flags. The `count=` and `maxsplit=` keywords work.
- Only `IGNORECASE`, `MULTILINE`, and `DOTALL` exist; there is no `re.VERBOSE`, `re.ASCII`, or `re.purge()`.
- `finditer()` returns a list, not an iterator.
- A group that did not participate in the match is `""`, not `None` (for example `re.search(r"(a)|(b)", "b").groups()` is `('', 'b')`).
- `split()` with capturing groups in the pattern does not include the captured separators in the result.
- `Match` objects are not subscriptable (`m[1]`) and `group()` takes a single argument; use `m.group(1)` or `m.groups()`.
- `Match.start()`, `Match.end()`, and `Match.span()` only support group `0`.

## See Also

- [html](https://scriptling.dev/okf/scriptling-libraries/text-processing/html.md): HTML escaping and unescaping utilities
- [html.parser](https://scriptling.dev/okf/scriptling-libraries/text-processing/html.parser.md): HTML/XHTML parser for structured markup
- [string](https://scriptling.dev/okf/scriptling-libraries/text-processing/string.md): String constants
- [difflib](https://scriptling.dev/okf/scriptling-libraries/text-processing/difflib.md): Sequence comparison and diff generation
