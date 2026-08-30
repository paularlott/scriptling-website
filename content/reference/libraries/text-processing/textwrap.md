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

| Function                                          | Description                              |
| -------------------------------------------------- | ----------------------------------------- |
| `wrap(text, width=70)`                            | Wrap text into a list of lines           |
| `fill(text, width=70)`                            | Wrap text and join lines with newlines   |
| `dedent(text)`                                    | Remove common leading whitespace         |
| `indent(text, prefix)`                            | Add a prefix to each non-empty line      |
| `shorten(text, width, placeholder="[...]")`       | Collapse whitespace and truncate to width |

## Functions

### `textwrap.wrap(text, width=70)`

Wraps a single paragraph of text and returns the result as a list of lines. Whitespace is collapsed to single spaces and lines are broken at word boundaries so no line exceeds `width` characters (except a single word longer than `width`, which is kept whole on its own line).

**Parameters:**
- `text` (`str`): The text to wrap.
- `width` (`int`, optional): Maximum line width. Default: `70`.

**Returns:** `list`: the wrapped lines.

```python
import textwrap

text = "This is a long line of text that needs to be wrapped"
lines = textwrap.wrap(text, 20)
print(lines)  # ["This is a long line", "of text that needs", "to be wrapped"]
```

### `textwrap.fill(text, width=70)`

Wraps a single paragraph of text the same way as `wrap()`, then joins the resulting lines with newlines into a single string.

**Parameters:**
- `text` (`str`): The text to wrap.
- `width` (`int`, optional): Maximum line width. Default: `70`.

**Returns:** `str`: the wrapped text with lines joined by `\n`.

```python
import textwrap

text = "This is a long line of text that needs to be wrapped"
result = textwrap.fill(text, 20)
print(result)
# This is a long line
# of text that needs
# to be wrapped
```

### `textwrap.dedent(text)`

Removes the common leading whitespace shared by every non-blank line in `text`. Lines that are blank or contain only whitespace are ignored when computing the common indentation and are left unchanged.

**Parameters:**
- `text` (`str`): The text to dedent.

**Returns:** `str`: the dedented text.

```python
import textwrap

text = "    Hello\n    World\n    Test"
result = textwrap.dedent(text)
print(result)  # "Hello\nWorld\nTest"
```

### `textwrap.indent(text, prefix)`

Adds `prefix` to the start of every non-empty line in `text`. Lines that are empty or contain only whitespace are left unchanged.

**Parameters:**
- `text` (`str`): The text to indent.
- `prefix` (`str`): The string to prepend to each non-empty line.

**Returns:** `str`: the indented text.

```python
import textwrap

text = "Hello\nWorld"
result = textwrap.indent(text, "  ")
print(result)  # "  Hello\n  World"

# Quote style
result = textwrap.indent(text, "> ")
print(result)  # "> Hello\n> World"
```

### `textwrap.shorten(text, width, placeholder="[...]")`

Collapses all whitespace in `text` to single spaces, then truncates the result to fit within `width` characters, appending `placeholder` and breaking at a word boundary where possible.

**Parameters:**
- `text` (`str`): The text to shorten.
- `width` (`int`): Maximum width of the result, including the placeholder.
- `placeholder` (`str`, optional): String appended to indicate truncation. Default: `"[...]"`.

**Returns:** `str`: the shortened text.

```python
import textwrap

text = "Hello World, this is a very long line of text"
result = textwrap.shorten(text, 20)
print(result)  # "Hello World,[...]"

# Custom placeholder
result = textwrap.shorten(text, 20, placeholder="...")
print(result)  # "Hello World,..."
```

## Examples

### Formatting Long Text

```python
import textwrap

article = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

# Wrap to 40 characters
wrapped = textwrap.fill(article, 40)
print(wrapped)
```

### Creating Indented Blocks

```python
import textwrap

code = "x = 1\ny = 2\nresult = x + y"
indented = textwrap.indent(code, "    ")
print(indented)  # "    x = 1\n    y = 2\n    result = x + y"
```

### Processing Multi-line Strings

```python
import textwrap

# Remove common indentation
template = """
    This text has
    common indentation
    that we want to remove
"""
clean = textwrap.dedent(template)
```

### Truncating for Display

```python
import textwrap

titles = [
    "A Short Title",
    "A Very Long Title That Needs To Be Truncated For Display"
]

for title in titles:
    display = textwrap.shorten(title, 30)
    print(display)
```

## Notes

- `wrap()` and `fill()` collapse whitespace and break at word boundaries.
- `dedent()` only removes common leading whitespace (spaces/tabs that appear at the start of every non-blank line).
- `indent()` does not add the prefix to empty or whitespace-only lines.
- `shorten()` attempts to break at a word boundary when truncating.

## Python Compatibility

This library implements a subset of Python's `textwrap` module:

| Function          | Supported |
| ----------------- | --------- |
| wrap              | ✅        |
| fill              | ✅        |
| dedent            | ✅        |
| indent            | ✅        |
| shorten           | ✅        |
| TextWrapper class | ❌        |

## See Also

- [string](../string/) - String constants for character classification
- [regex](../regex/) - Regular expressions for pattern matching
- [difflib](../difflib/) - Sequence comparison and diffing utilities
