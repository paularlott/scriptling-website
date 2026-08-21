---
description: HTTP client for making GET, POST, PUT, DELETE, and PATCH requests.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/http-process/requests/
sources:
    - resource: https://scriptling.dev/reference/libraries/http-process/requests/
status: stable
tags:
    - libraries
    - http
title: requests
type: API Reference
---
# requests

The `requests` library provides functions for making HTTP requests, matching Python's `requests` library API. Reach for it any time a script needs to call an HTTP/HTTPS API.

## Available Functions

| Function | Description |
|----------|-------------|
| `get(url, **kwargs)` | Make a GET request. |
| `post(url, data=None, **kwargs)` | Make a POST request. |
| `put(url, data=None, **kwargs)` | Make a PUT request. |
| `delete(url, **kwargs)` | Make a DELETE request. |
| `patch(url, data=None, **kwargs)` | Make a PATCH request. |
| `parallel(requests, max_parallel=4)` | Execute multiple HTTP requests concurrently. |

## Functions

### `get(url, **kwargs)`

Send an HTTP GET request to the specified URL.

**Parameters:**
- `url` (`str`): URL to request.
- `**kwargs` (optional):
  - `timeout` (`int`): Request timeout in seconds. Default: `5`.
  - `headers` (`dict`): HTTP headers to send.
  - `params` (`dict`): Query parameters to append to the URL.
  - `auth` (`tuple`/`list`): Basic authentication as `(username, password)`.

**Returns:** `Response`: see [Response Object](#response-object).

```python
import requests

response = requests.get("https://api.example.com/users/1", timeout=10, headers={"Authorization": "Bearer token123"})
if response.status_code == 200:
    print("User data:", response.text)
```

### `post(url, data=None, **kwargs)`

Send an HTTP POST request to the specified URL with the given data.

**Parameters:**
- `url` (`str`): URL to request.
- `data` (`str` or [`bytes`](../data-formats/bytes.md), optional): Request body. Use `bytes` for binary payloads (msgpack, etc.). Default: `None`.
- `**kwargs` (optional):
  - `timeout` (`int`): Request timeout in seconds. Default: `5`.
  - `headers` (`dict`): HTTP headers to send.
  - `params` (`dict`): Query parameters to append to the URL.
  - `json` (`dict`/`list`): Data to JSON-encode as the request body (sets `Content-Type`). Use either `data` or `json`, not both.
  - `auth` (`tuple`/`list`): Basic authentication as `(username, password)`.

**Returns:** `Response`: see [Response Object](#response-object).

```python
import json
import requests

new_user = {"name": "Alice", "email": "alice@example.com"}
response = requests.post("https://api.example.com/users", json=new_user)

if response.status_code == 201:
    created = response.json()
    print("Created user:", created["id"])
```

### `put(url, data=None, **kwargs)`

Send an HTTP PUT request to the specified URL with the given data.

**Parameters:**
- `url` (`str`): URL to request.
- `data` (`str` or [`bytes`](../data-formats/bytes.md), optional): Request body. Use `bytes` for binary payloads (msgpack, etc.). Default: `None`.
- `**kwargs` (optional):
  - `timeout` (`int`): Request timeout in seconds. Default: `5`.
  - `headers` (`dict`): HTTP headers to send.
  - `params` (`dict`): Query parameters to append to the URL.
  - `json` (`dict`/`list`): Data to JSON-encode as the request body (sets `Content-Type`). Use either `data` or `json`, not both.
  - `auth` (`tuple`/`list`): Basic authentication as `(username, password)`.

**Returns:** `Response`: see [Response Object](#response-object).

```python
import requests

response = requests.put("https://api.example.com/users/1", json={"name": "Alice Updated"})
```

### `delete(url, **kwargs)`

Send an HTTP DELETE request to the specified URL.

**Parameters:**
- `url` (`str`): URL to request.
- `**kwargs` (optional):
  - `timeout` (`int`): Request timeout in seconds. Default: `5`.
  - `headers` (`dict`): HTTP headers to send.
  - `params` (`dict`): Query parameters to append to the URL.
  - `auth` (`tuple`/`list`): Basic authentication as `(username, password)`.

**Returns:** `Response`: see [Response Object](#response-object).

```python
import requests

response = requests.delete("https://api.example.com/users/1")
```

### `patch(url, data=None, **kwargs)`

Send an HTTP PATCH request to the specified URL with the given data.

**Parameters:**
- `url` (`str`): URL to request.
- `data` (`str` or [`bytes`](../data-formats/bytes.md), optional): Request body. Use `bytes` for binary payloads (msgpack, etc.). Default: `None`.
- `**kwargs` (optional):
  - `timeout` (`int`): Request timeout in seconds. Default: `5`.
  - `headers` (`dict`): HTTP headers to send.
  - `params` (`dict`): Query parameters to append to the URL.
  - `json` (`dict`/`list`): Data to JSON-encode as the request body (sets `Content-Type`). Use either `data` or `json`, not both.
  - `auth` (`tuple`/`list`): Basic authentication as `(username, password)`.

**Returns:** `Response`: see [Response Object](#response-object).

```python
import requests

response = requests.patch("https://api.example.com/users/1", json={"name": "Alice P."})
```

### `parallel(requests, max_parallel=4)`

Execute multiple HTTP requests concurrently with a configurable concurrency limit. Results are returned in the same order as the input requests, regardless of completion order.

**Parameters:**
- `requests` (`list`): List of request specification dicts, each containing:
  - `method` (`str`): HTTP method: `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`, or `"PATCH"`. Default: `"GET"`.
  - `url` (`str`): The URL to request. Required.
  - `data` (`str` or `bytes`, optional): Request body (string or binary).
  - `json` (`dict`/`list`, optional): Data to JSON-encode as the request body (sets `Content-Type`).
  - `headers` (`dict`, optional): HTTP headers.
  - `params` (`dict`, optional): Query parameters to append to the URL.
  - `auth` (`list`/`tuple`, optional): Basic authentication as `[username, password]`.
  - `timeout` (`int`, optional): Request timeout in seconds. Default: `30`.
- `max_parallel` (`int`, optional): Maximum number of concurrent requests. Default: `4`.

**Returns:** `list`: `Response` objects in the same order as the input list. A malformed request spec (missing `url` or un-encodable `json`) yields a `Response` with `status_code=0` and the error message in `body`; a transport-level failure (timeout, DNS, connection refused) surfaces as an `Error` object in the corresponding position.

```python
import requests

results = requests.parallel([
    {"method": "GET", "url": "https://api.example.com/items/1"},
    {"method": "GET", "url": "https://api.example.com/items/2"},
    {"method": "POST", "url": "https://api.example.com/items", "json": {"name": "new"}},
], max_parallel=4)

for resp in results:
    if resp.status_code == 200:
        data = resp.json()
        print(data)
```

## Response Object

All HTTP functions return a `Response` object with the following attributes, accessible either as properties or by indexing:

- `status_code` / `["status_code"]` (`int`): HTTP status code.
- `text` / `["text"]` (`str`): Response body decoded as a string.
- `content` / `["content"]` ([`bytes`](../data-formats/bytes.md)): Raw response body. Use this instead of `.text` for binary content (images, msgpack, etc.).
- `body` / `["body"]` (`str`): Deprecated alias for `text`.
- `headers` / `["headers"]` (`dict`): Response headers.
- `url` / `["url"]` (`str`): The URL of the response.

### `Response.json()`

Parse the response body as JSON.

**Returns:** `dict`/`list`: the parsed JSON body.

```python
data = response.json()
```

### `Response.raise_for_status()`

Raise an exception if the status code indicates an error (`>= 400`).

**Returns:** `None`

**Raises:** `HTTPError`: if the status code is `>= 400`.

```python
import requests

try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
except requests.HTTPError as e:
    print("HTTP error:", e)
except requests.RequestException as e:
    print("Request failed:", e)
```

## Exceptions

The `requests` library exposes the following exception types for error handling:

- `RequestException`: base exception for all request errors.
- `HTTPError`: raised by `raise_for_status()` for HTTP error responses (4xx, 5xx).

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](../../scriptling-docs/go-integration/library-registration.md#extended-libraries).

`requests` can make arbitrary HTTP/HTTPS requests to any URL reachable from the host. There is no built-in URL allowlisting: if you need to restrict which hosts a script can reach, filter URLs at the application layer before passing them to script execution. See the [Security Guide](../../scriptling-docs/security.md#network-security).

## Notes

- HTTP/2 support with automatic fallback to HTTP/1.1.
- Connection pooling (100 connections per host).
- Self-signed certificates are rejected by default; the embedder can opt in via `InsecureSkipVerify` on the HTTP client.
- Default timeout: 5 seconds (30 seconds for `parallel()`).

## See Also

- [subprocess](subprocess.md): Run external commands
- [secrets](secrets.md): Generate tokens for API authentication
