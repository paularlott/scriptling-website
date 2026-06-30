---
title: html.parser
description: An HTML/XHTML parser compatible with Python's html.parser module.
weight: 1

aliases:
  - /reference/libraries/extlib/html.parser/
  - /reference/libraries/html.parser/
---

The `html.parser` library provides an HTML/XHTML parser compatible with Python's `html.parser` module. Subclass `HTMLParser` and override its handler methods to react to start tags, end tags, text, comments, and other markup as the parser feeds through a document.

## Import

```python
import html.parser

HTMLParser = html.parser.HTMLParser
```

## Available Functions

| Function | Description |
|----------|-------------|
| `HTMLParser(convert_charrefs=True)` | Construct a new parser instance |
| `feed(data)` | Feed HTML data to the parser |
| `reset()` | Reset the parser instance |
| `close()` | Force processing of buffered data |
| `get_starttag_text()` | Get the text of the most recently opened start tag |
| `getpos()` | Get the current `(line, offset)` position |
| `handle_starttag(tag, attrs)` | Handler called for a start tag (override) |
| `handle_endtag(tag)` | Handler called for an end tag (override) |
| `handle_startendtag(tag, attrs)` | Handler called for a self-closing tag (override) |
| `handle_data(data)` | Handler called for text content (override) |
| `handle_comment(data)` | Handler called for an HTML comment (override) |
| `handle_decl(decl)` | Handler called for a DOCTYPE declaration (override) |
| `handle_pi(data)` | Handler called for a processing instruction (override) |
| `handle_entityref(name)` | Handler called for a named character reference (override) |
| `handle_charref(name)` | Handler called for a numeric character reference (override) |
| `unknown_decl(data)` | Handler called for an unrecognized declaration (override) |

## Constructing a Parser

### `HTMLParser(convert_charrefs=True)`

Creates a new parser instance. Use a subclass and override the `handle_*` methods to process the elements you care about; `feed()` then drives those handlers as it parses.

**Parameters:**
- `convert_charrefs` (`bool`, keyword-only, optional): If `True`, character references (e.g. `&amp;`) are automatically decoded before being passed to `handle_data`, and `handle_entityref`/`handle_charref` are never called. Default: `True`.

**Returns:** `HTMLParser`: a new parser instance.

```python
import html.parser

class MyHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        self.data = []

    def handle_starttag(self, tag, attrs):
        print(f"Start tag: {tag}")
        print(f"Attrs: {attrs}")

    def handle_endtag(self, tag):
        print(f"End tag: {tag}")

    def handle_data(self, data):
        self.data.append(data)

parser = MyHTMLParser()
parser.feed("<html><body><p>Hello World!</p></body></html>")
```

> **Note:** `super().__init__()` is not required (or available): the parent class `__init__` is called automatically.

## Feeding and Controlling the Parser

### `feed(data)`

Feeds a chunk of HTML to the parser. The data is parsed immediately and the appropriate `handle_*` methods are invoked as elements are recognized.

**Parameters:**
- `data` (`str`): HTML markup to parse.

**Returns:** `None`

```python
import html.parser

parser = html.parser.HTMLParser()
parser.feed("<h1>Title</h1><p>Paragraph</p>")
```

### `reset()`

Resets the parser to its initial state, clearing internal buffers and position tracking. Automatically called when the instance is created.

**Parameters:** None

**Returns:** `None`

```python
import html.parser

parser = html.parser.HTMLParser()
parser.feed("<p>First document</p>")
parser.reset()
parser.feed("<p>Second document</p>")
```

### `close()`

Forces processing of any data still buffered. Call this once you've fed all available data.

**Parameters:** None

**Returns:** `None`

```python
import html.parser

parser = html.parser.HTMLParser()
parser.feed("<p>Some content</p>")
parser.close()
```

### `get_starttag_text()`

Returns the exact source text of the most recently opened start tag, including attributes as written (not normalized).

**Parameters:** None

**Returns:** `str` or `None`: the raw text of the last start tag, or `None` if no start tag has been seen yet.

```python
import html.parser

class MyParser(html.parser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        text = self.get_starttag_text()
        print(f"Raw tag: {text}")

parser = MyParser()
parser.feed('<div id="main" class="content">')
# Raw tag: <div id="main" class="content">
```

### `getpos()`

Returns the parser's current position in the source as a `(line, offset)` tuple. Line numbers start at `1`. Position tracking is not updated during parsing; `getpos()` currently always returns `(1, 0)` after construction.

**Parameters:** None

**Returns:** `tuple` of `int`: `(line, offset)`.

```python
import html.parser

parser = html.parser.HTMLParser()
parser.feed("<p>Hello</p>")
pos = parser.getpos()
print(f"Line: {pos[0]}, Offset: {pos[1]}")
```

## Handler Methods

Override these methods in a subclass to react to the elements you care about. The default implementation of each does nothing (except `handle_startendtag`, which by default calls `handle_starttag` followed by `handle_endtag`).

### `handle_starttag(tag, attrs)`

Called when a start tag is encountered, such as `<div id="main">`.

**Parameters:**
- `tag` (`str`): Tag name, lowercased (e.g. `"div"`, `"p"`).
- `attrs` (`list`): List of `(name, value)` tuples for the tag's attributes.

**Returns:** `None`

```python
def handle_starttag(self, tag, attrs):
    print(f"<{tag}>")
    for name, value in attrs:
        print(f"  {name}={value}")
```

### `handle_endtag(tag)`

Called when an end tag is encountered, such as `</div>`.

**Parameters:**
- `tag` (`str`): Tag name, lowercased.

**Returns:** `None`

```python
def handle_endtag(self, tag):
    print(f"</{tag}>")
```

### `handle_startendtag(tag, attrs)`

Called for XHTML-style self-closing tags, such as `<br/>` or `<img ... />`. The default implementation calls `handle_starttag` followed by `handle_endtag` with the same arguments, so most subclasses don't need to override this directly.

**Parameters:**
- `tag` (`str`): Tag name, lowercased.
- `attrs` (`list`): List of `(name, value)` tuples for the tag's attributes.

**Returns:** `None`

```python
def handle_startendtag(self, tag, attrs):
    print(f"<{tag}/>")
```

### `handle_data(data)`

Called with the text content found between tags.

**Parameters:**
- `data` (`str`): Text content.

**Returns:** `None`

```python
def handle_data(self, data):
    if data.strip():
        print(f"Text: {data}")
```

### `handle_comment(data)`

Called when an HTML comment is encountered.

**Parameters:**
- `data` (`str`): Comment content, without the surrounding `<!--` and `-->`.

**Returns:** `None`

```python
def handle_comment(self, data):
    print(f"Comment: {data}")
```

### `handle_decl(decl)`

Called for DOCTYPE and other markup declarations.

**Parameters:**
- `decl` (`str`): Declaration content, without the surrounding `<!` and `>`.

**Returns:** `None`

```python
def handle_decl(self, decl):
    print(f"Declaration: {decl}")
```

### `handle_pi(data)`

Called for processing instructions, such as `<?xml ...?>`.

**Parameters:**
- `data` (`str`): Processing instruction content.

**Returns:** `None`

```python
def handle_pi(self, data):
    print(f"PI: {data}")
```

### `handle_entityref(name)`

Called for named character references, such as `&gt;`. Only invoked when `convert_charrefs` is `False`; otherwise these are decoded automatically and delivered through `handle_data`.

**Parameters:**
- `name` (`str`): Entity name, without the surrounding `&` and `;`.

**Returns:** `None`

```python
def handle_entityref(self, name):
    print(f"Entity: &{name};")
```

### `handle_charref(name)`

Called for numeric character references, such as `&#62;`. Only invoked when `convert_charrefs` is `False`.

**Parameters:**
- `name` (`str`): Character code, without the surrounding `&#` and `;`.

**Returns:** `None`

```python
def handle_charref(self, name):
    print(f"Char ref: &#{name};")
```

### `unknown_decl(data)`

Called for unrecognized declaration types that are not handled by `handle_decl`, `handle_comment`, or as CDATA. The default implementation is a no-op.

**Parameters:**
- `data` (`str`): Declaration content.

**Returns:** `None`

## Instance Attributes

### `convert_charrefs`

Controls whether character references are automatically decoded.

**Type:** `bool`. Default: `True`.

When `True`, entities like `&amp;` are converted to `&` before being passed to `handle_data`, and `handle_entityref`/`handle_charref` are not called. Set it to `False` before feeding data if you need to handle references yourself.

```python
parser = html.parser.HTMLParser()
parser.convert_charrefs = False
```

## Complete Example

```python
import html.parser

class LinkExtractor(html.parser.HTMLParser):
    def __init__(self):
        self.links = []
        self.current_text = ""
        self.in_link = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.in_link = True
            for name, value in attrs:
                if name == "href":
                    self.links.append({"href": value, "text": ""})

    def handle_endtag(self, tag):
        if tag == "a":
            if self.links and self.in_link:
                self.links[-1]["text"] = self.current_text.strip()
            self.current_text = ""
            self.in_link = False

    def handle_data(self, data):
        if self.in_link:
            self.current_text = self.current_text + data

# Extract links from HTML
parser = LinkExtractor()
parser.feed("""
<html>
<body>
    <a href="https://example.com">Example</a>
    <a href="https://google.com">Google</a>
</body>
</html>
""")

for link in parser.links:
    print(f"{link['text']}: {link['href']}")
# Output:
# Example: https://example.com
# Google: https://google.com
```

## Python Compatibility

- `super().__init__()` is not required (or available): the parent class `__init__` is called automatically.
- The `from X import Y` syntax is not supported: use `import html.parser` then `html.parser.HTMLParser`.

## See Also

- [html](../html/): HTML escaping and unescaping utilities
- [re](../regex/): Regular expressions for text processing
- [difflib](../difflib/): Sequence comparison and diff generation
