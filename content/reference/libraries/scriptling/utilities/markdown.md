---
title: scriptling.markdown
linkTitle: markdown
weight: 5
---

The `scriptling.markdown` library converts Markdown to HTML using the
[GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/) specification,
backed by [goldmark](https://github.com/yuin/goldmark).

## Available Functions

| Function | Description |
| --- | --- |
| `to_html(markdown_string)` | Convert a Markdown string to an HTML string |

## Functions

### scriptling.markdown.to_html(markdown_string)

Converts a Markdown string to HTML.

**Parameters:**

- `markdown_string` (string): The Markdown source to convert.

**Returns:** `string` — HTML representation of the Markdown input.

**Supported syntax:**

- ATX and setext headings
- Bold (`**text**`), italic (`_text_`), strikethrough (`~~text~~`)
- Inline and fenced code blocks (with optional language hint)
- Ordered and unordered lists, nested lists
- Task lists (`- [x] done` / `- [ ] todo`)
- Blockquotes
- GFM tables
- Auto-linked bare URLs

**Example:**

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

- `to_html` uses goldmark with GFM extensions enabled. Raw HTML in the Markdown
  source is **not** passed through: goldmark's safe default drops raw HTML
  blocks and inline HTML (replacing them with an HTML comment) so untrusted
  input, such as LLM output, cannot inject `<script>` tags, event handlers,
  or other dangerous markup. The output is safe for direct insertion into an
  HTML page. HTML-like syntax inside code spans and fenced code blocks is still
  rendered, with the angle brackets HTML-escaped.
- The function never fails on well-formed UTF-8 Markdown; it raises an
  exception only if conversion encounters an internal error.
