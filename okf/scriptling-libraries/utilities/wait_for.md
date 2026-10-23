---
description: Wait for files, directories, ports, HTTP endpoints, or processes to become available.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/utilities/wait_for/
sources:
    - resource: https://scriptling.dev/reference/libraries/utilities/wait_for/
status: stable
tags:
    - libraries
    - utilities
title: scriptling.wait_for
type: API Reference
---
# scriptling.wait_for

The `scriptling.wait_for` library provides functions for waiting on resources to become available. It's useful for coordination between services: waiting for a file to be written, a port to start accepting connections, an HTTP health check to pass, or a process to start.

## Available Functions

| Function | Description |
|----------|-------------|
| `file(path, timeout=30, poll_rate=1)` | Wait for a file to exist |
| `dir(path, timeout=30, poll_rate=1)` | Wait for a directory to exist |
| `port(host, port, timeout=30, poll_rate=1)` | Wait for a TCP port to accept connections |
| `http(url, timeout=30, poll_rate=1, status_code=200)` | Wait for an HTTP endpoint to return the expected status |
| `file_content(path, content, timeout=30, poll_rate=1)` | Wait for a file to contain specific content |
| `process_name(name, timeout=30, poll_rate=1)` | Wait for a process to be running |

## Functions

### `file(path, timeout=30, poll_rate=1)`

Waits for a file to exist.

**Parameters:**
- `path` (`str`): Path to the file to wait for.
- `timeout` (`int`, optional): Maximum time to wait in seconds. Default: `30`.
- `poll_rate` (`float`, optional): Time between checks in seconds. Default: `1`.

**Returns:** `bool`: `True` if the file exists, `False` if the timeout was exceeded.

**Raises:** `PermissionError` if the path is outside `--allowed-paths` (checked on every poll), which the script cannot catch.

```python
import scriptling.wait_for as wait_for

# Wait for a file to be created (up to 2 minutes)
if wait_for.file("/mnt/nas/index_ready", timeout=120):
    print("File is ready!")
else:
    print("Timeout waiting for file")
```

### `dir(path, timeout=30, poll_rate=1)`

Waits for a directory to exist.

**Parameters:**
- `path` (`str`): Path to the directory to wait for.
- `timeout` (`int`, optional): Maximum time to wait in seconds. Default: `30`.
- `poll_rate` (`float`, optional): Time between checks in seconds. Default: `1`.

**Returns:** `bool`: `True` if the directory exists, `False` if the timeout was exceeded.

**Raises:** `PermissionError` if the path is outside `--allowed-paths` (checked on every poll), which the script cannot catch.

```python
import scriptling.wait_for as wait_for

# Wait for a backup directory to be created
if wait_for.dir("/mnt/nas/backups", timeout=60):
    print("Backup directory exists")
```

### `port(host, port, timeout=30, poll_rate=1)`

Waits for a TCP port to accept connections. Each connection attempt uses a 1-second timeout.

**Parameters:**
- `host` (`str`): Hostname or IP address.
- `port` (`int` or `str`): Port number.
- `timeout` (`int`, optional): Maximum time to wait in seconds. Default: `30`.
- `poll_rate` (`float`, optional): Time between checks in seconds. Default: `1`.

**Returns:** `bool`: `True` if the port is open, `False` if the timeout was exceeded.

**Raises:** an error if a configured network policy denies the address.

```python
import scriptling.wait_for as wait_for

# Wait for PostgreSQL to be ready
if wait_for.port("localhost", 5432, timeout=60):
    print("PostgreSQL is ready")
else:
    print("PostgreSQL did not start in time")
```

### `http(url, timeout=30, poll_rate=1, status_code=200)`

Waits for an HTTP endpoint to respond with the expected status code.

**Parameters:**
- `url` (`str`): URL to check.
- `timeout` (`int`, optional): Maximum time to wait in seconds. Default: `30`.
- `poll_rate` (`float`, optional): Time between checks in seconds. Default: `1`.
- `status_code` (`int`, optional): Expected HTTP status code. Default: `200`.

**Returns:** `bool`: `True` if the endpoint responds with the expected status, `False` if the timeout was exceeded.

**Raises:** an error if a configured network policy denies the URL.

```python
import scriptling.wait_for as wait_for

# Wait for a health check endpoint
if wait_for.http("http://localhost:8080/health", timeout=60):
    print("Service is healthy")

# Wait for a specific status code
if wait_for.http("http://api.example.com/ready", timeout=30, status_code=200):
    print("API is ready")
```

### `file_content(path, content, timeout=30, poll_rate=1)`

Waits for a file to exist and contain specific content.

**Parameters:**
- `path` (`str`): Path to the file to check.
- `content` (`str`): Content to search for in the file.
- `timeout` (`int`, optional): Maximum time to wait in seconds. Default: `30`.
- `poll_rate` (`float`, optional): Time between checks in seconds. Default: `1`.

**Returns:** `bool`: `True` if the file contains the content, `False` if the timeout was exceeded.

**Raises:** `PermissionError` if the path is outside `--allowed-paths` (checked on every poll), which the script cannot catch.

```python
import scriptling.wait_for as wait_for

# Wait for a readiness file to contain "ready=true"
if wait_for.file_content("/tmp/service.status", "ready=true", timeout=120):
    print("Service is ready")

# Wait for a specific pattern in a log file
if wait_for.file_content("/var/log/app.log", "Server started", timeout=30):
    print("Application has started")
```

### `process_name(name, timeout=30, poll_rate=1)`

Waits for a process with the specified name to be running. Process name matching is platform-dependent (uses `/proc` on Linux, `ps` on macOS/BSD) and matches on substring, case-insensitively.

**Parameters:**
- `name` (`str`): Process name to search for.
- `timeout` (`int`, optional): Maximum time to wait in seconds. Default: `30`.
- `poll_rate` (`float`, optional): Time between checks in seconds. Default: `1`.

**Returns:** `bool`: `True` if the process is running, `False` if the timeout was exceeded.

```python
import scriptling.wait_for as wait_for

# Wait for nginx to start
if wait_for.process_name("nginx", timeout=30):
    print("nginx is running")

# Wait for a custom application
if wait_for.process_name("my-app", timeout=60):
    print("Application is running")
```

## Examples

### Database migration coordination

```python
import scriptling.wait_for as wait_for
import subprocess

# Wait for PostgreSQL to be ready
if not wait_for.port("localhost", 5432, timeout=60):
    print("ERROR: PostgreSQL did not start")
    exit(1)

subprocess.run(["python", "manage.py", "migrate"])

# Wait for the migration lock file to be removed
while wait_for.file("/tmp/migration.lock", timeout=1):
    print("Waiting for migrations to complete...")

print("Migrations complete, starting application")
```

### Multi-service HTTP health checks

```python
import scriptling.wait_for as wait_for

services = [
    ("http://localhost:8080/health", "API Gateway"),
    ("http://localhost:8081/health", "Auth Service"),
    ("http://localhost:8082/health", "Data Service"),
]

print("Waiting for services to be healthy...")
for url, name in services:
    if wait_for.http(url, timeout=60):
        print(f"  OK {name}")
    else:
        print(f"  FAIL {name} failed health check")
        exit(1)

print("All services are healthy!")
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`file()`, `dir()` and `file_content()` honor `--allowed-paths` (or the embedder's allowed paths) like the `os` library: a path that resolves outside them, including through a symlink or `..`, raises a `PermissionError` before anything is read, so they cannot be used to probe for files or test their contents outside the jail.

`scriptling.wait_for` can be used to probe network reachability and timing: `port()` and `http()` make outbound TCP/HTTP connections to any host or URL the script provides. Both honor a configured [network policy](https://scriptling.dev/okf/scriptling-docs/cli/network-policy.md): a denied host or URL raises a `network policy: …` error immediately rather than polling until the timeout. Without a policy there is no restriction on which hosts or ports a script can probe, so register one where scripts are untrusted. For a full risk breakdown across all libraries, see the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md).

## See Also

- [scriptling.runtime](https://scriptling.dev/okf/scriptling-libraries/runtime.md) - Background tasks and coordination primitives that often pair with wait_for
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security guidance for host-provided libraries
