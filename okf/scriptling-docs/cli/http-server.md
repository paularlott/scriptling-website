---
description: Running Scriptling as an HTTP server with custom routes.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/cli/http-server/
sources:
    - resource: https://scriptling.dev/docs/cli/http-server/
status: stable
tags:
    - cli
    - http
title: HTTP Server Mode
type: Guide
---
# HTTP Server Mode

Scriptling can run as an HTTP server, allowing you to build REST APIs and web services.

## Starting the Server

Use the `--server` flag to start an HTTP server:

```bash
# Start HTTP server on port 8000
scriptling --server :8000 setup.py
```

The setup script is executed when the server starts and typically registers route handlers.

> **Keeping the setup script alive:** By default the setup script exits after registering handlers and the server runs until shutdown. To keep the script running alongside the server: e.g. to maintain gossip state, run a polling loop, or share objects with handlers via `runtime.sync`: call [`runtime.start_server()`](https://scriptling.dev/okf/scriptling-libraries/./runtime.md) instead of exiting. See the [runtime reference](https://scriptling.dev/okf/scriptling-libraries/./runtime.md) for details.

## Server Options

| Flag                | Environment Variable      | Description                      | Default    |
| ------------------- | ------------------------- | -------------------------------- | ---------- |
| `--server`          | `SCRIPTLING_SERVER`       | HTTP server address (host:port)  | (disabled) |
| `--json-rpc`        | `SCRIPTLING_JSONRPC`      | Mount JSON-RPC at `/json-rpc`    | false      |
| `--web-root`        | `SCRIPTLING_WEB_ROOT`     | Directory or zip to serve static files from | none       |
| `--bearer-token`    | `SCRIPTLING_BEARER_TOKEN` | Bearer token for authentication  | none       |
| `--allowed-paths`   | `SCRIPTLING_ALLOWED_PATHS`| Allowed filesystem paths         | (none)     |
| `--tls-cert`        | `SCRIPTLING_TLS_CERT`     | TLS certificate file             | none       |
| `--tls-key`         | `SCRIPTLING_TLS_KEY`      | TLS key file                     | none       |
| `--tls-generate`    | -                         | Generate self-signed certificate | false      |

## Static Assets

Use `--web-root` to serve static files (HTML, CSS, JS, images) from a directory or a zip archive. When a request doesn't match any registered route, the server looks for a matching file in the web root. If no file is found either, the `not_found` handler is called (if registered).

```bash
# Serve from a directory
scriptling --server :8000 --web-root ./public setup.py

# Serve from a zip archive
scriptling --server :8000 --web-root ./public.zip setup.py
```

Requests for `/` automatically serve `index.html` from the web root if present.

In your setup script, register a custom 404 handler for unmatched requests:

```python
# setup.py
import scriptling.runtime as runtime

runtime.http.get("/api/hello", "handlers.hello")
runtime.http.not_found("handlers.not_found")
```

```python
# handlers.py
import scriptling.runtime as runtime

def not_found(request):
    return runtime.http.html(404, f"<h1>404 - {request.path} not found</h1>")
```

Priority order for incoming requests:
1. Registered script routes (literal or `{param}` wildcard match)
2. Registered static routes (`runtime.http.static()`)
3. Web root directory (`--web-root`)
4. `not_found` handler (if registered)
5. Plain `404 Not Found`

## JSON-RPC Endpoint

Add `--json-rpc` to mount `scriptling.runtime.jsonrpc` handlers at
`POST /json-rpc` on the same HTTP server:

```bash
scriptling --server :8000 --json-rpc setup.py
```

This can run alongside normal HTTP routes, static files, MCP tools, and the MCP
script execution tool. See [JSON-RPC Server Mode](https://scriptling.dev/okf/scriptling-docs/cli/jsonrpc-server.md) for
single request, batch, and notification examples.

## TLS/HTTPS

### Self-Signed Certificate

Quick setup for development:

```bash
scriptling --server :8443 --tls-generate setup.py
```

This generates a self-signed certificate automatically.

### Custom Certificate

Provide your own certificate and key:

```bash
scriptling --server :8443 --tls-cert /path/to/cert.pem --tls-key /path/to/key.pem setup.py
```

## Authentication

Use bearer token authentication to protect your API:

```bash
# Set token via flag
scriptling --server :8000 --bearer-token my-secret-token setup.py

# Or via environment variable
SCRIPTLING_BEARER_TOKEN=my-secret-token scriptling --server :8000 setup.py
```

Clients must include the token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer my-secret-token" http://localhost:8000/api/hello
```

### Per-User Keys

For more than one key, skip the static token and register a script middleware
that checks the `Authorization` header itself — a dict lookup, the KV store,
or an API call all work. The middleware guards every HTTP route and, when
enabled, the `/mcp` and `/json-rpc` endpoints too, so one handler
authenticates API clients, MCP clients, and JSON-RPC callers alike:

```python
# auth.py
KEYS = {
    "Bearer alice-key": "alice",
    "Bearer bob-key": "bob",
}

def check(request):
    auth = request.header("authorization", "")
    if auth in KEYS:
        return None
    return {"status": 401, "body": "unauthorized"}
```

```python
# setup.py
import auth
import scriptling.runtime as runtime

runtime.http.middleware("auth.check")
```

When a middleware is registered it replaces static `--bearer-token` checking
on the protocol endpoints; without one, the static token guards everything
as before.

## Filesystem Restrictions

Restrict which paths scripts can access:

```bash
# Restrict to specific directories
scriptling --server :8000 --allowed-paths "/var/www,./uploads" setup.py
```

## Defining Routes

Register route handlers in your setup script:

```python
# setup.py
import scriptling.runtime as runtime

# Register routes (handler functions referenced as "module.function")
runtime.http.get("/api/hello", "handlers.hello")
runtime.http.post("/api/echo", "handlers.echo")
runtime.http.get("/api/users/{id}", "handlers.get_user")
```

Handler modules can live in subdirectories: `routes/me.py` is imported as
`import routes.me` and its functions are referenced as `"routes.me.get_user"`.
The module part of a handler reference may be any dotted module path.

```python
# handlers.py
import scriptling.runtime as runtime

def hello(request):
    return runtime.http.json(200, {"message": "Hello, World!"})

def echo(request):
    return runtime.http.json(200, request.json())

def get_user(request):
    user_id = request.path_param("id")
    return runtime.http.json(200, {"user_id": user_id})
```

### HTTP Methods

```python
runtime.http.get("/path", "handlers.get")
runtime.http.post("/path", "handlers.post")
runtime.http.put("/path", "handlers.put")
runtime.http.patch("/path", "handlers.patch")
runtime.http.delete("/path", "handlers.delete")
```

### Path Parameters

Route patterns capture path segments with `{name}` for a single segment and `{name...}` for the rest of the path. Values are read in the handler with `request.path_param(name)` and arrive percent-decoded:

```python
# setup.py
import scriptling.runtime as runtime

runtime.http.get("/api/users/{id}", "handlers.get_user")
runtime.http.get("/files/{path...}", "handlers.get_file")
```

```python
# handlers.py
import scriptling.runtime as runtime

def get_user(request):
    user_id = request.path_param("id")          # "/api/users/42"  -> "42"
    return runtime.http.json(200, {"user_id": user_id})

def get_file(request):
    path = request.path_param("path")           # "/files/a/b.txt" -> "a/b.txt"
    return runtime.http.json(200, {"path": path})
```

Matching follows Go's `ServeMux` rules: a literal route wins over a wildcard at the same position, so `/api/users/me` hits its own handler while `/api/users/42` matches `/api/users/{id}`. HEAD requests are dispatched to GET handlers, and values keep encoded slashes within one segment (`/api/users/a%2Fb` captures `a/b`).

### Decorator Syntax

Instead of registering routes separately in a setup script, attach them
directly to handler functions with decorators. Import the HTTP sub-library
and use `@http.get`, `@http.post`, `@http.put`, `@http.patch`, `@http.delete`,
`@http.route`, `@http.websocket`, `@http.middleware`, or `@http.not_found`:

```python
# handlers.py
import scriptling.runtime.http as http

@http.get("/health")
def health_check(request):
    return http.json(200, {"status": "ok"})

@http.post("/api/users")
def create_user(request):
    data = request.json()
    return http.json(201, {"name": data["name"]})

@http.route("/api/items", methods=["GET", "POST"])
def items(request):
    return http.json(200, [])

@http.websocket("/ws")
def ws_handler(client):
    client.send("Welcome!")

@http.middleware
def auth(request):
    if request.header("Authorization") == "":
        return http.json(401, {"error": "unauthorized"})
    return None  # continue to handler

@http.not_found
def handle_404(request):
    return http.html(404, "<h1>Not Found</h1>")
```

The setup script still triggers registration — it imports the handler library,
which fires the decorators:

```python
# setup.py
import handlers  # decorators fire, routes are registered
```

When the file is imported, the decorators register each route with the correct
`"module.function"` reference. The module name is derived from `__name__`
(or `__file__` when `__name__` is `"__main__"`), so decorators also work
directly in the setup/main script itself.

At request time, the server re-imports the library on a fresh evaluator and
calls the handler function. Re-import is idempotent — duplicate route
registrations are detected and skipped silently.

Route decorators must sit on module-level functions. A decorated method
inside a class registers a reference the server cannot dispatch (the function
is not at the top level of the module) — the route fails with a logged
"function not found" error on first request. Decorate a module-level function
that delegates to the class instead.

The imperative API (`runtime.http.get("/path", "lib.func")`) continues to
work unchanged. Both forms can coexist in the same project.

### Request Object

The request object passed to handlers provides:

```python
def handler(request):
    # HTTP method
    method = request.method

    # Path parameters (from URL patterns like /users/{id})
    user_id = request.path_param("id")

    # Query parameters
    page = request.query_param("page", "1")

    # Headers
    content_type = request.header("Content-Type")

    # Request body (a string field)
    body = request.body

    # JSON body (parsed)
    data = request.json()

    # Remote address
    remote_addr = request.remote_addr
```

### Response Helpers

```python
import scriptling.runtime as runtime

def handler(request):
    # JSON response
    return runtime.http.json(200, {"status": "ok"})

    # Text response
    return runtime.http.text(200, "Hello, World!")

    # HTML response
    return runtime.http.html(200, "<h1>Hello</h1>")

    # Custom status
    return runtime.http.json(404, {"error": "Not found"})

    # Redirect
    return runtime.http.redirect("/new-location")
```

## Complete Example

### REST API Server

```bash
scriptling --server :8000 --bearer-token secret123 app.py
```

```python
# app.py
import scriptling.runtime as runtime

# Register routes
runtime.http.get("/", "handlers.index")
runtime.http.get("/api/users", "handlers.list_users")
runtime.http.post("/api/users", "handlers.create_user")
runtime.http.get("/api/users/{id}", "handlers.get_user")
```

```python
# handlers.py
import scriptling.runtime as runtime

users = {
    "1": {"id": "1", "name": "Alice"},
    "2": {"id": "2", "name": "Bob"},
}

def index(request):
    return runtime.http.json(200, {"service": "User API", "version": "1.0"})

def list_users(request):
    return runtime.http.json(200, list(users.values()))

def get_user(request):
    user_id = request.path_param("id")
    if user_id in users:
        return runtime.http.json(200, users[user_id])
    return runtime.http.json(404, {"error": "User not found"})

def create_user(request):
    data = request.json()
    user_id = str(len(users) + 1)
    users[user_id] = {"id": user_id, "name": data.get("name")}
    return runtime.http.json(201, users[user_id])
```

### Testing the API

```bash
# List users
curl http://localhost:8000/api/users

# Get specific user
curl http://localhost:8000/api/users/1

# Create user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie"}'
```

## See Also

- [Basic Usage](https://scriptling.dev/okf/scriptling-docs/cli/basic-usage.md) - Running scripts, interactive mode, and lint mode
- [Command Line Options](https://scriptling.dev/okf/scriptling-docs/cli/command-line-options.md) - Every flag and configuration file setting
- [MCP Server Mode](https://scriptling.dev/okf/scriptling-docs/cli/mcp-server.md) - Model Context Protocol integration
- [Runtime HTTP Library](https://scriptling.dev/okf/scriptling-libraries/runtime/http.md) - HTTP server API reference
