---
title: scriptling.markdown
linkTitle: markdown
description: Convert Markdown to HTML using the GitHub Flavored Markdown specification.
tags: [libraries, utilities, text]
weight: 5

aliases:
  - /reference/libraries/scriptling/utilities/markdown/
---

The `scriptling.markdown` library converts Markdown to HTML using the [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/) specification, backed by [goldmark](https://github.com/yuin/goldmark). Reach for it whenever a script needs to turn Markdown text: including LLM output: into safe, ready-to-render HTML.

## Available Functions

| Function | Description |
|----------|-------------|
| `to_html(markdown_string)` | Convert a Markdown string to an HTML string |

## Functions

### `to_html(markdown_string)`

Converts a Markdown string to HTML. Supports ATX and setext headings; bold (`**text**`), italic (`_text_`), and strikethrough (`~~text~~`); inline and fenced code blocks with optional language hints; ordered, unordered, and nested lists; task lists (`- [x] done` / `- [ ] todo`); blockquotes; GFM tables; and auto-linked bare URLs.

**Parameters:**
- `markdown_string` (`str`): The Markdown source to convert.

**Returns:** `str`: HTML representation of the Markdown input.

**Raises:** `Error`: only if conversion encounters an internal error; the function never fails on well-formed UTF-8 Markdown.

```python
import scriptling.markdown as markdown

html = markdown.to_html("# Hello\n\nThis is **bold** and _italic_.")
# <h1 id="hello">Hello</h1>
# <p>This is <strong>bold</strong> and <em>italic</em>.</p>
```

## Examples

### Basic formatting

```python
import scriptling.markdown as markdown

md = """
# Report

Status: **completed**

- Item one
- Item two
  - Nested item
"""

html = markdown.to_html(md)
```

### Table conversion

```python
import scriptling.markdown as markdown

md = """
| Name  | Score |
|-------|-------|
| Alice | 98    |
| Bob   | 75    |
"""

html = markdown.to_html(md)
```

### Fenced code block

```python
import scriptling.markdown as markdown

md = "```python\nprint('hello')\n```"
html = markdown.to_html(md)
```

### Task list

```python
import scriptling.markdown as markdown

md = "- [x] Deploy to staging\n- [ ] Run smoke tests\n- [ ] Deploy to production"
html = markdown.to_html(md)
```

### Convert before writing to an HTML field

```python
import scriptling.markdown as markdown

detail_md = "## Summary\n\nFix deployed to **production**. See [ticket](https://example.com/123)."
detail_html = markdown.to_html(detail_md)
# Pass detail_html to any API that expects HTML content
```

## Notes

`to_html` uses goldmark with GFM extensions enabled. Raw HTML in the Markdown source is **not** passed through: goldmark's safe default drops raw HTML blocks and inline HTML (replacing them with an HTML comment) so untrusted input, such as LLM output, cannot inject `<script>` tags, event handlers, or other dangerous markup. The output is safe for direct insertion into an HTML page. HTML-like syntax inside code spans and fenced code blocks is still rendered, with the angle brackets HTML-escaped.

## See Also

- [scriptling.template.html](../../template/html/) - Render the converted HTML into a larger page template
