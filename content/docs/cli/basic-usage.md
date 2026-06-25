---
title: Basic Usage
description: Running scripts, interactive mode, and command line options.
weight: 1
---

## Running Scripts

### Run a Script File

```bash
scriptling script.py
```

### Pipe Script via Stdin

```bash
echo 'print("Hello")' | scriptling
cat script.py | scriptling
```

### Interactive Mode (REPL)

```bash
scriptling --interactive
# or
scriptling -i
```

## Lint Mode

Lint scripts for syntax errors without executing them:

```bash
# Lint a file
scriptling --lint script.py

# Lint from stdin
echo 'x = 1 +' | scriptling --lint

# JSON output format
scriptling --lint --lint-format json script.py
```

**Text output format:**

```
script.py:3: expected token COLON (error)
```

**JSON output format:**

```json
{
  "files_checked": 1,
  "has_errors": true,
  "errors": [
    {
      "file": "script.py",
      "line": 3,
      "message": "expected token COLON",
      "severity": "error",
      "code": "parse-error"
    }
  ]
}
```

The linter exits with code 0 if no errors are found, and code 1 if any errors exist.

## Command Line Options

| Flag                  | Env Variable               | Config Path                  | Description                                          | Default          |
| --------------------- | -------------------------- | ---------------------------- | ---------------------------------------------------- | ---------------- |
| `-C`, `--config`      | `SCRIPTLING_CONFIG`        | -                            | Path to configuration file                           | see below        |
| `-i`, `--interactive` | -                          | -                            | Start interactive mode                               | -            |
| `-c`, `--code`        | -                          | -                            | Execute inline code string                           | -                |
| `-l`, `--lint`        | -                          | -                            | Lint script files without executing                  | -            |
| `--lint-format`       | `SCRIPTLING_LINT_FORMAT`   | `lint.format`                | Output format for lint (text/json)                   | text             |
| `-p`, `--package`     | -                          | `packages`                   | Package (.zip) path or URL to load (repeatable)      | (none)           |
| `-k`, `--insecure`    | -                          | `insecure`                   | Allow self-signed HTTPS certificates                 | false            |
| `--cache-dir`         | `SCRIPTLING_CACHE_DIR`     | `cache.dir`                  | Cache directory for remote packages                  | OS default       |
| `-L`, `--libpath`     | `SCRIPTLING_LIBPATH`       | `libpath`                    | Extra library search directory (repeatable)          | (none)           |
| `--plugin-dir`       | `SCRIPTLING_PLUGIN_DIR`    | `plugins.dirs`               | Plugin executable directory (repeatable)             | (none)           |
| `--log-level`         | `SCRIPTLING_LOG_LEVEL`     | `log.level`                  | Log level (trace/debug/info/warn/error)              | info             |
| `--log-format`        | `SCRIPTLING_LOG_FORMAT`    | `log.format`                 | Log format (console/json)                            | console          |
| `-S`, `--server`      | `SCRIPTLING_SERVER`        | `server.address`             | HTTP server address (host:port)                      | (disabled)       |
| `--json-rpc`          | `SCRIPTLING_JSONRPC`       | -                            | JSON-RPC server mode: stdio by default, HTTP `/json-rpc` with `--server` | false            |
| `--mcp-tools`         | `SCRIPTLING_MCP_TOOLS`     | `mcp.tools`                  | Directory containing MCP tools                       | (disabled)       |
| `--mcp-exec-script`   | `SCRIPTLING_MCP_EXEC_SCRIPT` | `mcp.exec_script`          | Enable MCP script execution tool                     | false            |
| `--bearer-token`      | `SCRIPTLING_BEARER_TOKEN`  | `server.bearer_token`        | Bearer token for authentication                      | none             |
| `--allowed-paths`     | `SCRIPTLING_ALLOWED_PATHS` | `security.allowed_paths`     | Comma-separated allowed filesystem paths             | (no restriction) |
| `--disable-lib`       | `SCRIPTLING_DISABLE_LIB`   | `security.disable_libs`      | Disable a built-in library by name (repeatable)      | (none)           |
| `--list-libs`         | -                          | -                            | List available built-in libraries and exit           | -            |
| `--kv-storage`        | `SCRIPTLING_KV_STORAGE`    | `kv.storage`                 | Directory for persistent KV store                    | (in-memory)      |
| `--docker-host`       | `DOCKER_HOST`              | `container.docker_host`      | Docker endpoint (socket path, tcp://, https://)      | `/var/run/docker.sock` |
| `--podman-host`       | `CONTAINER_HOST`           | `container.podman_host`      | Podman endpoint (socket path or unix:// URI)         | `/var/run/podman.sock` |
| `--secret-config`     | `SCRIPTLING_SECRET_CONFIG` | `secret.config`              | TOML file for secret provider aliases                | none             |
| `--tls-cert`          | `SCRIPTLING_TLS_CERT`      | `tls.cert`                   | TLS certificate file                                 | none             |
| `--tls-key`           | `SCRIPTLING_TLS_KEY`       | `tls.key`                    | TLS key file                                         | none             |
| `--tls-generate`      | -                          | `tls.generate`               | Generate self-signed certificate                     | -            |

## Configuration File

Scriptling looks for `scriptling.toml` in the following locations (in order):

1. Current directory (`.`)
2. `$HOME/`
3. `$HOME/.config/scriptling/`
4. `/etc/scriptling/`

Use `--config` (or `-C`) to specify a different path explicitly.

All flags that have a config path can be set in the file. The TOML structure mirrors the config paths shown in the flags table above:

```toml
# scriptling.toml

[log]
level = "debug"
format = "console"

libpath = ["/shared/libs", "/company/libs"]

packages = ["./mypackage.zip", "https://example.com/lib.zip"]
insecure = false

[server]
address = ":8000"
bearer_token = "secret"

[mcp]
tools = "./tools"
exec_script = false

[security]
allowed_paths = "/tmp/data,./uploads"
disable_libs = ["subprocess", "os"]

[kv]
storage = "/var/lib/scriptling/kv"

[container]
docker_host = "unix:///Users/paul/.lima/docker/sock/docker.sock"
podman_host = "unix:///run/user/1000/podman/podman.sock"

[secret]
config = "/etc/scriptling/secrets.toml"

[tls]
cert = "/etc/scriptling/tls.crt"
key = "/etc/scriptling/tls.key"
generate = false

[cache]
dir = "/var/cache/scriptling"

[lint]
format = "text"
```

Priority order (highest to lowest): **command-line flag** > **environment variable** > **config file** > **default**.

## Container Endpoints {#container-endpoints}

When using the `scriptling.container` library, Docker and Podman endpoints can be configured via flags or environment variables. Both accept any of the following forms:

| Form | Example |
|---|---|
| Unix socket path | `/var/run/docker.sock` |
| Unix socket URI | `unix:///var/run/docker.sock` |
| TCP (Docker only) | `tcp://192.168.1.10:2375` or `192.168.1.10:2375` |
| TLS TCP (Docker only) | `https://192.168.1.10:2376` |

Podman does not expose a plain TCP endpoint — use a Unix socket path or URI. For remote Podman, use `podman system service` with SSH tunnelling and point the socket at the local tunnel endpoint.

```bash
scriptling --docker-host unix:///Users/paul/.lima/docker/sock/docker.sock script.py
scriptling --docker-host tcp://192.168.1.10:2375 script.py
scriptling --podman-host unix:///run/user/1000/podman/podman.sock script.py
```

## Environment Variables and .env Files

The CLI automatically loads environment variables from a `.env` file in the current directory (if it exists). For persistent configuration, prefer `scriptling.toml` — the `.env` file is useful for secrets or environment-specific overrides that shouldn't be committed to version control.

**Example `.env` file:**

```bash
# Log configuration
SCRIPTLING_LOG_LEVEL=debug
SCRIPTLING_LOG_FORMAT=console

# Extra library search paths (space-separated)
SCRIPTLING_LIBPATH=/shared/libs

# Server configuration
SCRIPTLING_SERVER=:8000
SCRIPTLING_MCP_TOOLS=./tools
SCRIPTLING_BEARER_TOKEN=your-secret-token

# Filesystem restrictions
SCRIPTLING_ALLOWED_PATHS=/tmp/data,./uploads
```

## Library Loading

Scriptling automatically searches for libraries in the same directory as the running script — matching Python's behaviour. For interactive mode or stdin, the current working directory is used.

```bash
# Libraries in ./myproject/ are found automatically
scriptling ./myproject/script.py

# Interactive mode: libraries in cwd are found automatically
scriptling --interactive
```

Use `--libpath` (repeatable, alias `-L`) to add extra search directories. The script directory (or cwd) is always searched first:

```bash
# Search script dir first, then /shared/libs
scriptling --libpath /shared/libs script.py

# Multiple extra directories
scriptling --libpath /shared/libs --libpath /company/libs script.py

# Via environment variable
SCRIPTLING_LIBPATH=/shared/libs scriptling script.py
```

Libraries follow Python-style folder organisation:

```
myproject/
  script.py
  utils.py              # import utils
  knot/
    groups.py           # import knot.groups
    roles.py            # import knot.roles
```

```python
# In script.py — no --libpath needed, same directory is searched automatically
import utils           # Loads from myproject/utils.py
import knot.groups     # Loads from myproject/knot/groups.py
```

For nested imports like `knot.groups`, the loader checks:
1. `dir/knot/groups.py` (folder structure — preferred)
2. `dir/knot.groups.py` (flat file — legacy fallback)

## Disabling and Listing Libraries

### List Available Libraries

Use `--list-libs` to print all built-in library names and exit:

```bash
scriptling --list-libs
```

When combined with `--disable-lib`, disabled libraries are excluded from the output:

```bash
scriptling --disable-lib subprocess --list-libs
```

### Disable Specific Libraries

Use `--disable-lib` (repeatable) to prevent specific built-in libraries from loading:

```bash
# Disable a single library
scriptling --disable-lib subprocess script.py

# Disable multiple libraries
scriptling --disable-lib subprocess --disable-lib os script.py

# Via environment variable
SCRIPTLING_DISABLE_LIB=subprocess scriptling script.py
```

If a script attempts to import a disabled library, it raises `ImportError`, which can be caught with `try` / `except`.

## Script Execution Modes

Scriptling supports three levels of filesystem access control:

| Mode           | Flag                            | Filesystem Access       | Path Restrictions    |
| -------------- | ------------------------------- | ----------------------- | -------------------- |
| **Full**       | (default)                       | All libraries           | None                 |
| **Restricted** | `--allowed-paths /path1,/path2` | All libraries           | Only specified paths |
| **None**       | `--allowed-paths -`             | All libraries           | No paths allowed     |

### Full Mode (default)

All libraries available, no restrictions:

```bash
scriptling script.py
```

### Restricted Mode

All libraries available, but filesystem operations restricted to specified paths:

```bash
# Restrict to specific directories
scriptling --allowed-paths "/tmp/data,./uploads" script.py

# With relative paths
scriptling --allowed-paths "./data,../shared" script.py

# Via environment variable
SCRIPTLING_ALLOWED_PATHS="/var/www,./public" scriptling script.py
```

### No File Access Mode

Disable all filesystem access (useful for running untrusted scripts):

```bash
scriptling --allowed-paths - script.py
```

All file operations (`os.read_file`, `os.write_file`, `pathlib`, `glob`, `sandbox.exec_file`) will be denied.

When a script tries to access a path outside the allowed directories:

```python
import os
# This will raise an error if /etc/passwd is not in allowed paths
try:
    content = os.read_file("/etc/passwd")
except Exception as e:
    print(f"Access denied: {e}")
    # Output: Access denied: access denied: path '/etc/passwd' is outside allowed directories
```

**Available libraries:**

- Standard libraries: `json`, `math`, `random`, `re`, `time`, `base64`, `hashlib`, `hmac`, `urllib`
- `datetime` - Date and time operations
- `yaml`, `toml` - YAML and TOML parsing
- `html.parser` - HTML parsing
- `requests` - HTTP client
- `os` - Environment variables and file operations (path-restricted)
- `pathlib`, `glob` - File system access (path-restricted)
- `secrets` - Cryptographic random number generation
- `scriptling.runtime` - Runtime utilities including sandbox and background tasks
- `subprocess` - Process execution
- `scriptling.wait_for` - Process monitoring
- AI, agent, and MCP libraries

## Accessing Environment Variables

You can access environment variables from within Scriptling scripts using the `os` library:

```python
import os

# Get a specific environment variable
api_key = os.getenv("API_KEY", "default-key")
print(f"API Key: {api_key}")

# Get all environment variables
env = os.environ()
print(f"Home: {env['HOME']}")
print(f"Path: {env['PATH']}")
```

## See Also

- [HTTP Server Mode](../http-server/) - Running Scriptling as an HTTP server
- [MCP Server Mode](../mcp-server/) - Model Context Protocol integration
- [Writing MCP Tools](../../../reference/libraries/scriptling/mcp/writing-mcp-tools/) - Creating custom MCP tools
