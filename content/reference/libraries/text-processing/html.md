---
title: html
description: Escape and unescape HTML special characters and entities.
tags: [libraries, text]
weight: 1

aliases:
  - /reference/libraries/stdlib/html/
  - /reference/libraries/html/
---

HTML escaping and unescaping library, matching Python's `html` module.

## Available Functions

| Function | Description |
|----------|-------------|
| `escape(s)` | Escape HTML special characters in a string. |
| `unescape(s)` | Unescape HTML entities in a string. |

## Functions

### `escape(s)`

Escapes HTML special characters in a string so it can be safely embedded in HTML. Converts `&` to `&amp;`, `<` to `&lt;`, `>` to `&gt;`, `"` to `&#34;`, and `'` to `&#39;`.

**Parameters:**

- `s` (`str`): String to escape.

**Returns:** `str`: the escaped string.

```python
import html

safe = html.escape("<script>alert('xss')</script>")
print(safe)  # "&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;"
```

### `unescape(s)`

Unescapes HTML entities in a string, converting them back to their corresponding characters. Handles named entities (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&#39;`) and numeric entities (`&#60;`, `&#x3c;`).

**Parameters:**

- `s` (`str`): String with HTML entities to unescape.

**Returns:** `str`: the unescaped string.

```python
import html

text = html.unescape("&lt;script&gt;")
print(text)  # "<script>"
```

## Examples

### Sanitize User Input

```python
import html

user_input = "<script>alert('xss')</script>"
safe_output = html.escape(user_input)
print(safe_output)
# Output: &lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;
```

### Build Safe HTML

```python
import html

def create_element(tag, content):
    safe_content = html.escape(content)
    return "<" + tag + ">" + safe_content + "</" + tag + ">"

print(create_element("p", "Hello <world>"))
# Output: <p>Hello &lt;world&gt;</p>
```

### Process HTML Entities

```python
import html

# From API response
encoded = "Tom &amp; Jerry"
decoded = html.unescape(encoded)
print(decoded)  # "Tom & Jerry"
```

### Roundtrip Conversion

```python
import html

original = '<div class="test">Content</div>'
escaped = html.escape(original)
restored = html.unescape(escaped)

print(original == restored)  # True
```

## Python Compatibility

- `unescape(s)` - ✅ Compatible
- `escape(s)` - ⚠️ Mostly compatible. The implementation uses Go's `html.EscapeString`, which emits numeric character references for quotes (`"` → `&#34;`, `'` → `&#39;`) rather than Python's named/hex forms (`"` → `&quot;`, `'` → `&#x27;`). The escaped output is semantically equivalent but not byte-identical.

Note: Python's `html.escape()` has an optional `quote` parameter (default `True`) which is not implemented. This implementation always escapes quotes.

## See Also

- [html.parser](../html.parser/) - HTML parsing for extracting tags and data
- [string](../string/) - String constants for character classification
- [regex](../regex/) - Regular expressions for text processing
