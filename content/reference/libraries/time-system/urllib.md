---
title: urllib.parse
description: Parse, split, join, and percent-encode/decode URLs and query strings. No network access (use requests for actual HTTP calls).
weight: 1

aliases:
  - /reference/libraries/stdlib/urllib/
  - /reference/libraries/urllib/
---

The `urllib.parse` library provides URL parsing, splitting, joining, and percent-encoding/decoding, matching Python's `urllib.parse` module. It does not perform any network access: use it to take URLs and query strings apart and put them back together as plain strings.

## Available Functions

| Function | Description |
|----------|-------------|
| `quote(string, safe='')` | URL-encode a string using percent-encoding. |
| `quote_plus(string, safe='')` | URL-encode a string, encoding spaces as `+`. |
| `unquote(string)` | Decode a percent-encoded string. |
| `unquote_plus(string)` | Decode a percent-encoded string, decoding `+` as spaces. |
| `urlparse(urlstring)` | Parse a URL into a `ParseResult` object. |
| `urlunparse(components)` | Reconstruct a URL string from components. |
| `urlsplit(urlstring)` | Split a URL into a 5-element list (no params). |
| `urlunsplit(components)` | Reconstruct a URL string from a 5-element list. |
| `urljoin(base, url)` | Join a base URL with a relative or absolute URL. |
| `parse_qs(qs, keep_blank_values=False)` | Parse a query string into a dict of lists. |
| `parse_qsl(qs, keep_blank_values=False)` | Parse a query string into a list of key/value tuples. |
| `urlencode(query, doseq=False)` | Encode a dict or list of pairs into a query string. |

## Functions

### `quote(string, safe='')`

URL-encodes a string using percent-encoding. Letters, digits, and the characters `-_.~` are never encoded; spaces are encoded as `%20`. Characters listed in `safe` are also left unencoded.

**Parameters:**
- `string` (`str`): String to encode.
- `safe` (`str`, optional): Characters that should not be encoded. Default: `''`.

**Returns:** `str`: the percent-encoded string.

```python
import urllib.parse

encoded = urllib.parse.quote("hello world")
# "hello%20world"

encoded = urllib.parse.quote("hello/world", safe="/")
# "hello/world"

encoded = urllib.parse.quote("hello/world")
# "hello%2Fworld"
```

### `quote_plus(string, safe='')`

Like `quote()`, but also replaces spaces with plus signs (`+`) instead of `%20`. Commonly used for encoding query string values.

**Parameters:**
- `string` (`str`): String to encode.
- `safe` (`str`, optional): Characters that should not be encoded. Default: `''`.

**Returns:** `str`: the percent-encoded string with spaces as `+`.

```python
import urllib.parse

encoded = urllib.parse.quote_plus("hello world")
# "hello+world"
```

### `unquote(string)`

Decodes a percent-encoded string back to its original form.

**Parameters:**
- `string` (`str`): Percent-encoded string to decode.

**Returns:** `str`: the decoded string.

**Raises:** `Error`: if the string contains invalid percent-encoding.

```python
import urllib.parse

decoded = urllib.parse.unquote("hello%20world")
# "hello world"
```

### `unquote_plus(string)`

Like `unquote()`, but also decodes plus signs (`+`) as spaces before decoding percent-escapes.

**Parameters:**
- `string` (`str`): Percent-encoded string to decode.

**Returns:** `str`: the decoded string.

**Raises:** `Error`: if the string contains invalid percent-encoding.

```python
import urllib.parse

decoded = urllib.parse.unquote_plus("hello+world")
# "hello world"
```

### `urlparse(urlstring)`

Parses a URL into its components and returns a `ParseResult` object with `scheme`, `netloc`, `path`, `params`, `query`, and `fragment` attributes. `netloc` includes userinfo (`user:pass@host:port`), matching Python's behavior. Call `.geturl()` on the result to reconstruct the URL string.

**Parameters:**
- `urlstring` (`str`): URL string to parse.

**Returns:** `ParseResult`: object with `scheme`, `netloc`, `path`, `params`, `query`, `fragment` attributes (`params` is always `''`: Scriptling's parser does not split path parameters out separately) and a `geturl()` method.

**Raises:** `Error`: if the URL cannot be parsed.

```python
import urllib.parse

parsed = urllib.parse.urlparse("https://user:pw@example.com:8080/path?query=value#section")
print(parsed.scheme)    # "https"
print(parsed.netloc)    # "user:pw@example.com:8080"
print(parsed.path)      # "/path"
print(parsed.query)     # "query=value"
print(parsed.fragment)  # "section"

print(parsed.geturl())
# "https://user:pw@example.com:8080/path?query=value#section"
```

### `urlunparse(components)`

Reconstructs a URL string from a 6-element `dict`, `list`, `tuple` (in order `scheme, netloc, path, params, query, fragment`), or a `ParseResult` object such as one returned by `urlparse()`.

**Parameters:**
- `components` (`dict`, `list`, `tuple`, or `ParseResult`): URL components. For `dict`, use keys `scheme`, `netloc`, `path`, `query`, `fragment` (the `params` key is accepted but ignored). For `list`/`tuple`, supply exactly 6 elements in order: `[scheme, netloc, path, params, query, fragment]`.

**Returns:** `str`: the reconstructed URL.

**Raises:** `Error`: if a `list`/`tuple` is given without exactly 6 elements, or if `components` is not one of the supported types.

```python
import urllib.parse

url = urllib.parse.urlunparse({
    "scheme": "https",
    "netloc": "example.com",
    "path": "/path",
    "query": "key=value",
})
# "https://example.com/path?key=value"

# Or as a 6-element list: [scheme, netloc, path, params, query, fragment]
url = urllib.parse.urlunparse(["https", "example.com", "/path", "", "key=value", ""])
# "https://example.com/path?key=value"
```

### `urlsplit(urlstring)`

Parses a URL into 5 components, omitting `params` (use `urlparse()` if you need that field, though it is always empty in Scriptling). `netloc` includes userinfo, matching `urlparse()`.

**Parameters:**
- `urlstring` (`str`): URL string to parse.

**Returns:** `list`: 5 elements in order `[scheme, netloc, path, query, fragment]`.

**Raises:** `Error`: if the URL cannot be parsed.

```python
import urllib.parse

parsed = urllib.parse.urlsplit("https://example.com/path?query=value#section")
# ["https", "example.com", "/path", "query=value", "section"]

scheme, netloc, path, query, fragment = parsed
```

### `urlunsplit(components)`

Reconstructs a URL string from a 5-element list, the counterpart to `urlsplit()`.

**Parameters:**
- `components` (`list`): Exactly 5 elements in order `[scheme, netloc, path, query, fragment]`.

**Returns:** `str`: the reconstructed URL.

**Raises:** `Error`: if `components` does not have exactly 5 elements.

```python
import urllib.parse

url = urllib.parse.urlunsplit(["https", "example.com", "/path", "key=value", "section"])
# "https://example.com/path?key=value#section"
```

### `urljoin(base, url)`

Joins a base URL with another URL, resolving relative references the way a browser would. If `url` is absolute, it is returned (resolved against `base`'s scheme/host as needed); if `url` is relative, it's resolved against `base`.

**Parameters:**
- `base` (`str`): Base URL.
- `url` (`str`): URL to join: relative or absolute.

**Returns:** `str`: the resolved URL.

**Raises:** `Error`: if `base` or `url` cannot be parsed.

```python
import urllib.parse

full_url = urllib.parse.urljoin("https://example.com/path/", "page.html")
# "https://example.com/path/page.html"

full_url = urllib.parse.urljoin("https://example.com/path/", "/other")
# "https://example.com/other"
```

### `parse_qs(qs, keep_blank_values=False)`

Parses a URL query string into a dict where each value is a list of strings (since a key may appear multiple times).

**Parameters:**
- `qs` (`str`): Query string to parse.
- `keep_blank_values` (`bool`, optional): Accepted for Python compatibility but has no effect; blank values are always retained. Default: `False`.

**Returns:** `dict`: keys mapped to `list` of `str` values.

**Raises:** `Error`: if the query string is invalid.

```python
import urllib.parse

params = urllib.parse.parse_qs("name=John&tags=python&tags=go")
# {"name": ["John"], "tags": ["python", "go"]}
```

### `parse_qsl(qs, keep_blank_values=False)`

Parses a URL query string into a list of `(key, value)` tuples, including repeated keys. Note: the order of keys in the result is not guaranteed to match the input order.

**Parameters:**
- `qs` (`str`): Query string to parse.
- `keep_blank_values` (`bool`, optional): Accepted for Python compatibility but has no effect; blank values are always retained. Default: `False`.

**Returns:** `list`: `(key, value)` tuples, each a `tuple` of two `str` values.

**Raises:** `Error`: if the query string is invalid.

```python
import urllib.parse

params = urllib.parse.parse_qsl("name=John&age=30")
# [("name", "John"), ("age", "30")]
```

### `urlencode(query, doseq=False)`

Encodes a `dict` or a list of `(key, value)` pairs into a URL query string, percent-encoding keys and values as needed.

**Parameters:**
- `query` (`dict` or `list`): Mapping of keys to values, or a list of `(key, value)` tuples. Dict values may be a `str` or a `list` of `str` to repeat the key.
- `doseq` (`bool`, optional): Accepted for Python compatibility but has no effect; sequence-valued dict entries are always expanded into repeated `key=value` pairs. Default: `False`.

**Returns:** `str`: the encoded query string.

**Raises:** `Error`: if `query` is not a `dict` or `list`.

```python
import urllib.parse

query = urllib.parse.urlencode({"name": "John", "age": "30"})
# "age=30&name=John"

# With a sequence value
query = urllib.parse.urlencode({"tags": ["python", "go"]}, True)
# "tags=python&tags=go"
```

## See Also

- [requests](../../http-process/requests/) - Make actual HTTP requests (GET/POST/etc.); use it together with `urllib.parse` for building and parsing URLs.
- [datetime](../datetime/) - Date and time types.
- [io](../io/) - In-memory I/O streams.
