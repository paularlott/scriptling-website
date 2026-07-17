---
title: scriptling.runtime.http
linkTitle: runtime.http
description: Register HTTP routes, middleware, and response helpers for a Scriptling-backed server.
tags: [libraries, runtime, http]
weight: 1
---

## Overview

The `scriptling.runtime.http` library lets a setup script register routes, middleware, and static file serving, then build JSON/HTML/text/redirect responses from handlers. Reach for it when you want a Scriptling script to act as (or contribute routes to) an HTTP server.

## Available Functions

| Function | Description |
|----------|-------------|
| `get(path, handler)` | Register a GET route |
| `post(path, handler)` | Register a POST route |
| `put(path, handler)` | Register a PUT route |
| `delete(path, handler)` | Register a DELETE route |
| `route(path, handler, methods=["GET", "POST", "PUT", "DELETE"])` | Register a route for multiple methods |
| `middleware(handler)` | Register global middleware |
| `not_found(handler)` | Register a custom 404 handler |
| `static(path, directory)` | Register static file serving |
| `websocket(path, handler)` | Register a WebSocket route |
| `json(status_code, data)` | Create a JSON response |
| `html(status_code, content)` | Create an HTML response |
| `text(status_code, content)` | Create a plain text response |
| `redirect(location, status=302)` | Create a redirect response |
| `parse_query(query_string)` | Parse a URL query string |

## Functions

### `get(path, handler)`

Registers a GET route.

**Parameters:**
- `path` (`str`): URL path (e.g. `"/api/users"`).
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.get("/users", "handlers.list_users")
```

### `post(path, handler)`

Registers a POST route.

**Parameters:**
- `path` (`str`): URL path.
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.post("/users", "handlers.create_user")
```

### `put(path, handler)`

Registers a PUT route.

**Parameters:**
- `path` (`str`): URL path.
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.put("/users/:id", "handlers.update_user")
```

### `delete(path, handler)`

Registers a DELETE route.

**Parameters:**
- `path` (`str`): URL path.
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.delete("/users/:id", "handlers.delete_user")
```

### `route(path, handler, methods=["GET", "POST", "PUT", "DELETE"])`

Registers a route for multiple HTTP methods.

**Parameters:**
- `path` (`str`): URL path.
- `handler` (`str`): Handler function as `"library.function"`.
- `methods` (`list`, optional): HTTP methods to match. Default: `["GET", "POST", "PUT", "DELETE"]` (all of the standard methods).

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.route("/users/:id", "handlers.user_resource", methods=["GET", "PUT", "DELETE"])
```

### `middleware(handler)`

Registers global middleware that runs before every route handler. The middleware receives the request and should return `None` to continue to the handler, or a response dict to short-circuit the request.

**Parameters:**
- `handler` (`str`): Middleware function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

def auth(request):
    if "authorization" not in request.headers:
        return runtime.http.json(401, {"error": "Unauthorized"})
    return None  # Continue to handler

runtime.http.middleware("handlers.auth")
```

### `not_found(handler)`

Registers a custom 404 Not Found handler. The handler receives the request object and should return a response. It is called when no route matches the request path, or when the `--web-root` directory is configured but the requested file is not found.

**Parameters:**
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

def not_found(request):
    return runtime.http.html(404, f"<h1>404 - {request.path} not found</h1>")

runtime.http.not_found("handlers.not_found")
```

### `static(path, directory)`

Registers static file serving under a URL path prefix.

**Parameters:**
- `path` (`str`): URL path prefix (e.g. `"/assets"`).
- `directory` (`str`): Local directory to serve.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.static("/assets", "./public/assets")
```

### `websocket(path, handler)`

Registers a WebSocket route. The handler receives a `WebSocketClient` object and runs for the lifetime of the connection: it should loop while `client.connected()` and use `client.receive()` / `client.send()`.

**Parameters:**
- `path` (`str`): URL path for the WebSocket endpoint (e.g. `"/ws"`).
- `handler` (`str`): Handler function as a `"library.function"` string.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.websocket("/chat", "handlers.chat_handler")

# In handlers.py:
def chat_handler(client):
    client.send("Welcome!")
    while client.connected():
        msg = client.receive(timeout=60)
        if msg:
            client.send(f"Echo: {msg}")
```

#### WebSocketClient Object

The object passed to a `websocket()` handler:

| Member | Description |
|--------|-------------|
| `connected()` | Returns `True` while the connection is open. |
| `receive(timeout=30)` | Receives the next message, blocking up to `timeout` seconds. |
| `send(text)` | Sends a text message. |
| `send_binary(data)` | Sends a `list` of byte values (0-255) as a binary message. |
| `close()` | Closes the connection. |
| `remote_addr` | The client's remote address as a `str`. |

This is the server-side counterpart to the client documented on the [scriptling.net.websocket](/reference/libraries/scriptling/networking/websocket/) page: the two expose the same `connected()`/`receive()`/`send()`/`send_binary()`/`close()`/`remote_addr` surface. Use `scriptling.net.websocket.is_text()` / `is_binary()` to inspect a received message's type.

### `json(status_code, data)`

Creates a JSON response.

**Parameters:**
- `status_code` (`int`): HTTP status code.
- `data` (any): Data to serialize as JSON.

**Returns:** `dict`: response dict compatible with the server.

```python
import scriptling.runtime as runtime

def list_users(request):
    users = runtime.kv.default.get("users", default=[])
    return runtime.http.json(200, {"users": users})
```

### `html(status_code, content)`

Creates an HTML response.

**Parameters:**
- `status_code` (`int`): HTTP status code.
- `content` (`str`): HTML content.

**Returns:** `dict`: response dict compatible with the server.

```python
import scriptling.runtime as runtime

runtime.http.html(200, "<h1>Hello</h1>")
```

### `text(status_code, content)`

Creates a plain text response.

**Parameters:**
- `status_code` (`int`): HTTP status code.
- `content` (`str`): Text content.

**Returns:** `dict`: response dict compatible with the server.

```python
import scriptling.runtime as runtime

runtime.http.text(200, "pong")
```

### `redirect(location, status=302)`

Creates a redirect response.

**Parameters:**
- `location` (`str`): URL to redirect to.
- `status` (`int`, optional): HTTP status code. Default: `302`.

**Returns:** `dict`: response dict compatible with the server.

```python
import scriptling.runtime as runtime

runtime.http.redirect("/login")
```

### `parse_query(query_string)`

Parses a URL query string.

**Parameters:**
- `query_string` (`str`): Query string to parse.

**Returns:** `dict`: key-value pairs.

```python
import scriptling.runtime as runtime

params = runtime.http.parse_query("page=2&limit=10")
print(params["page"])  # "2"
```

## Request Object

Handlers receive a Request object with these fields:

- `method` (`str`): HTTP method.
- `path` (`str`): Request path.
- `body` (`str`): Request body.
- `headers` (`dict`): Request headers (lowercase keys).
- `query` (`dict`): Query parameters.

**Methods:**

- `json()`: parse the body as JSON.

## Examples

### Basic routes with a 404 handler

```python
# setup.py
import scriptling.runtime as runtime

runtime.http.get("/users", "handlers.list_users")
runtime.http.post("/users", "handlers.create_user")
runtime.http.middleware("handlers.auth")
runtime.http.not_found("handlers.not_found")
```

```python
# handlers.py
import scriptling.runtime as runtime

def list_users(request):
    users = runtime.kv.get("users", default=[])
    return runtime.http.json(200, {"users": users})

def create_user(request):
    data = request.json()
    users = runtime.kv.get("users", default=[])
    users.append(data)
    runtime.kv.set("users", users)
    return runtime.http.json(201, {"user": data})
```

Routes are registered during setup script execution. Use `--web-root <dir>` to serve static files from the CLI; unmatched requests fall through to the `not_found` handler.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.runtime.http` does not make outbound requests: it registers routes and handlers that turn the embedding process into (or adds to) an HTTP **server**, exposing a network listener. The risk shape is therefore about what gets exposed: every registered route, middleware, and static directory becomes reachable by anyone who can reach the listening address. Review handler logic for authorization, and be deliberate about what `static()` directories you expose. For a full risk breakdown across all libraries, see the [Security Guide](/docs/security/).

## See Also

- [scriptling.runtime](../runtime/): background tasks, `start_server()`, and the rest of the runtime namespace
- [scriptling.runtime.jsonrpc](../jsonrpc/): JSON-RPC 2.0 server sharing the same handler model
- [scriptling.runtime.kv](../kv/): share state across HTTP handlers
- [Security Guide](/docs/security/)
