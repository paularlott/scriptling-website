---
title: HTTP Server Mode
description: Running Scriptling as an HTTP server with custom routes.
weight: 2
---

Scriptling can run as an HTTP server, allowing you to build REST APIs and web services.

## Starting the Server

Use the `--server` flag to start an HTTP server:

```bash
# Start HTTP server on port 8000
scriptling --server :8000 setup.py
```

The setup script is executed when the server starts and typically registers route handlers.

## Server Options

| Flag                | Environment Variable      | Description                      | Default    |
| ------------------- | ------------------------- | -------------------------------- | ---------- |
| `--server`          | `SCRIPTLING_SERVER`       | HTTP server address (host:port)  | (disabled) |
| `--bearer-token`    | `SCRIPTLING_BEARER_TOKEN` | Bearer token for authentication  | none       |
| `--allowed-paths`   | `SCRIPTLING_ALLOWED_PATHS`| Allowed filesystem paths         | (none)     |
| `--tls-cert`        | `SCRIPTLING_TLS_CERT`     | TLS certificate file             | none       |
| `--tls-key`         | `SCRIPTLING_TLS_KEY`      | TLS key file                     | none       |
| `--tls-generate`    | -                         | Generate self-signed certificate | false      |

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

    # Request body
    body = request.body()

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

- [Basic Usage](../basic-usage/) - Installation and command line options
- [MCP Server Mode](../mcp-server/) - Model Context Protocol integration
- [Runtime HTTP Library](../../../libraries/scriptling/runtime-http/) - HTTP server API reference
