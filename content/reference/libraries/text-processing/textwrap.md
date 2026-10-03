---
title: textwrap
description: Text wrapping and filling utilities, compatible with Python's textwrap module.
tags: [libraries, text]
weight: 3

aliases:
  - /reference/libraries/stdlib/textwrap/
  - /reference/libraries/textwrap/
---

The `textwrap` library wraps and fills paragraphs of text, dedents indented blocks, adds line prefixes, and truncates text to a fixed width. Reach for it when formatting text for fixed-width output such as terminals or plain-text reports.

## Available Functions

| Function | Description |
|----------|-------------|
| `wrap(text, width=70, **options)` | Collapse whitespace and wrap into a list of lines no wider than `width`. Accepts Python's `TextWrapper` options, such as `initial_indent`, `subsequent_indent` and `break_long_words`. |
| `fill(text, width=70, **options)` | `wrap()`, joined with newlines into one string. |
| `dedent(text)` | Remove leading whitespace common to every non-blank line. |
| `indent(text, prefix)` | Add `prefix` to every line that is not empty or whitespace-only. |
| `shorten(text, width, placeholder="[...]")` | Collapse whitespace and truncate at a word boundary so the result, placeholder included, fits in `width`. |

## Example

```python
import textwrap

text = "This is a long line of text that needs to be wrapped"
print(textwrap.wrap(text, 20))   # ['This is a long line', 'of text that needs', 'to be wrapped']
print(textwrap.fill(text, 20))
# This is a long line
# of text that needs
# to be wrapped

template = """
    This text has
    common indentation
"""
print(textwrap.dedent(template).strip())   # lines now start at column 0

print(textwrap.indent("Hello\n\nWorld", "> "))
# > Hello
#
# > World

title = "A Very Long Title That Needs To Be Truncated For Display"
print(textwrap.shorten(title, 30))                   # A Very Long Title That [...]
print(textwrap.shorten(title, 30, placeholder="..."))  # A Very Long Title That...
```

## Differences from Python

- The `TextWrapper` class is not available; `wrap()`, `fill()` and `shorten()` take all of its options as keywords.

## See Also

- [string](../string/) - String constants for character classification
- [regex](../regex/) - Regular expressions for pattern matching
- [difflib](../difflib/) - Sequence comparison and diffing utilities
