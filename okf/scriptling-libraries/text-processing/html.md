---
description: Escape and unescape HTML special characters and entities.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/text-processing/html/
sources:
    - resource: https://scriptling.dev/reference/libraries/text-processing/html/
status: stable
tags:
    - libraries
    - text
title: html
type: API Reference
---
# html

HTML escaping and unescaping library, matching Python's `html` module.

## Available Functions

| Function | Description |
|----------|-------------|
| `escape(s)` | Escape `&`, `<`, `>`, `"` and `'` so `s` can be embedded in HTML. |
| `unescape(s)` | Convert named and numeric entities (`&lt;`, `&#60;`, `&#x3c;`) back to characters. |

## Example

```python
import html

safe = html.escape("<script>alert('xss')</script>")
print(safe)          # &lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;
print(html.escape('Say "hi" & bye'))  # Say &quot;hi&quot; &amp; bye

print(html.unescape("Tom &amp; Jerry"))      # Tom & Jerry
print(html.unescape("&#60;b&#x3e; &quot;"))  # <b> "

original = '<div class="test">Content</div>'
print(html.unescape(html.escape(original)) == original)  # True
```

## Python Compatibility

- `unescape(s)` - ✅ Compatible
- `escape(s, quote=True)` - ✅ Compatible

## See Also

- [html.parser](https://scriptling.dev/okf/scriptling-libraries/text-processing/html.parser.md) - HTML parsing for extracting tags and data
- [string](https://scriptling.dev/okf/scriptling-libraries/text-processing/string.md) - String constants for character classification
- [regex](https://scriptling.dev/okf/scriptling-libraries/text-processing/regex.md) - Regular expressions for text processing
