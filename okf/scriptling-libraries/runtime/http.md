---
description: Register HTTP routes, middleware, and response helpers for a Scriptling-backed server.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/runtime/http/
sources:
    - resource: https://scriptling.dev/reference/libraries/runtime/http/
status: stable
tags:
    - libraries
    - runtime
    - http
title: scriptling.runtime.http
type: API Reference
---
# scriptling.runtime.http

## Overview

The `scriptling.runtime.http` library lets a setup script register routes, middleware, and static file serving, then build JSON/HTML/text/redirect responses from handlers. Reach for it when you want a Scriptling script to act as (or contribute routes to) an HTTP server.

## Available Functions

| Function | Description |
|----------|-------------|
| `get(path, handler)` | Register a GET route |
| `post(path, handler)` | Register a POST route |
| `put(path, handler)` | Register a PUT route |
| `patch(path, handler)` | Register a PATCH route |
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

Route paths support wildcards: `{name}` matches one path segment and `{name...}` matches the rest of the path. Values are read in the handler with `request.path_param(name)` — see [Request Object](#request-object) below. Handler references may use dotted module paths: a handler in `routes/me.py` is referenced as `"routes.me.get_user"` — the module part is everything before the last dot.

## Functions

### `get(path, handler)`

Registers a GET route.

**Parameters:**
- `path` (`str`): URL path (e.g. `"/api/users"`). Supports `{name}` and `{name...}` wildcards.
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.get("/users", "handlers.list_users")
runtime.http.get("/users/{id}", "handlers.get_user")
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

runtime.http.put("/users/{id}", "handlers.update_user")
```

### `patch(path, handler)`

Registers a PATCH route.

**Parameters:**
- `path` (`str`): URL path.
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.patch("/users/{id}", "handlers.patch_user")
```

### `delete(path, handler)`

Registers a DELETE route.

**Parameters:**
- `path` (`str`): URL path.
- `handler` (`str`): Handler function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

runtime.http.delete("/users/{id}", "handlers.delete_user")
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

runtime.http.route("/users/{id}", "handlers.user_resource", methods=["GET", "PUT", "DELETE"])
```

### `middleware(handler)`

Registers global middleware that runs before every route handler — and, when the protocol endpoints are enabled, before the `/mcp`, `/json-rpc` and WebSocket handlers too. The middleware receives the request and should return `None` to continue to the handler, or a response dict to short-circuit the request.

The middleware can pass data to the handler by writing to `request.context`, a dict that starts empty on every request. HTTP route handlers read it straight off their request object; MCP tools and JSON-RPC methods read it with `request_context()` / `get_request()` (see the [MCP tool](https://scriptling.dev/okf/scriptling-libraries/mcp/tool.md) and [JSON-RPC](https://scriptling.dev/okf/scriptling-libraries/runtime/jsonrpc.md) pages). Keep plain data in it: `request_context()` copies dicts and lists deeply so concurrent handlers cannot race through them, but instances pass by reference (they may hold resources), so a shared instance is still shared. It can also register MCP entries for the life of the request — per-user tools, resources and prompts — with the [request-scoped registration](https://scriptling.dev/okf/scriptling-libraries/runtime/mcp.md#request-scoped-registration) functions.

**Parameters:**
- `handler` (`str`): Middleware function as `"library.function"`.

**Returns:** `None`

```python
import scriptling.runtime as runtime

def auth(request):
    if "authorization" not in request.headers:
        return runtime.http.json(401, {"error": "Unauthorized"})
    request.context["user"] = "alice"  # Readable by the handler
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

This is the server-side counterpart to the client documented on the [scriptling.net.websocket](https://scriptling.dev/okf/scriptling-libraries/networking/websocket.md) page: the two expose the same `connected()`/`receive()`/`send()`/`send_binary()`/`close()`/`remote_addr` surface. Use `scriptling.net.websocket.is_text()` / `is_binary()` to inspect a received message's type.

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
- `path_params` (`dict`): Path parameters captured from route wildcards.
- `remote_addr` (`str`): Remote address of the client.
- `context` (`dict`): Starts empty on every request; middleware can write to it (e.g. `request.context["user"] = name` after authenticating) and the handler reads it back. Per-request only — not related to the persistent KV store.

**Methods:**

- `path_param(name, default=None)`: get a path parameter captured from a route wildcard (`"/api/users/{id}"` captures `id`), percent-decoded.
- `query_param(name, default=None)`: get the first value of a query parameter.
- `header(name, default=None)`: get a request header; names are case-insensitive.
- `json()`: parse the body as JSON.

```python
def get_user(request):
    user_id = request.path_param("id")            # from "/api/users/{id}"
    page = request.query_param("page", "1")
    token = request.header("Authorization")
    data = request.json()
    return runtime.http.json(200, {"user_id": user_id})
```

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

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.runtime.http` does not make outbound requests: it registers routes and handlers that turn the embedding process into (or adds to) an HTTP **server**, exposing a network listener. The risk shape is therefore about what gets exposed: every registered route, middleware, and static directory becomes reachable by anyone who can reach the listening address. Review handler logic for authorization, and be deliberate about what `static()` directories you expose. For a full risk breakdown across all libraries, see the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md).

## See Also

- [scriptling.runtime](https://scriptling.dev/okf/scriptling-libraries/runtime.md): background tasks, `start_server()`, and the rest of the runtime namespace
- [scriptling.runtime.jsonrpc](https://scriptling.dev/okf/scriptling-libraries/runtime/jsonrpc.md): JSON-RPC 2.0 server sharing the same handler model
- [scriptling.runtime.kv](https://scriptling.dev/okf/scriptling-libraries/runtime/kv.md): share state across HTTP handlers
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md)
