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

| Flag                  | Environment Variable       | Description                                          | Default          |
| --------------------- | -------------------------- | ---------------------------------------------------- | ---------------- |
| `-i`, `--interactive` | -                          | Start interactive mode                               | false            |
| `-l`, `--lint`        | -                          | Lint script files without executing                  | false            |
| `--lint-format`       | `SCRIPTLING_LINT_FORMAT`   | Output format for lint (text/json)                   | text             |
| `-L`, `--libpath`     | `SCRIPTLING_LIBPATH`       | Extra library search directory (repeatable)          | (none)           |
| `--log-level`         | `SCRIPTLING_LOG_LEVEL`     | Log level (trace/debug/info/warn/error)              | info             |
| `--log-format`        | `SCRIPTLING_LOG_FORMAT`    | Log format (console/json)                            | console          |
| `-S`, `--server`      | `SCRIPTLING_SERVER`        | HTTP server address (host:port)                      | (disabled)       |
| `--mcp-tools`         | `SCRIPTLING_MCP_TOOLS`     | Directory containing MCP tools                       | (disabled)       |
| `--mcp-exec-script`   | -                          | Enable MCP script execution tool                     | false            |
| `--bearer-token`      | `SCRIPTLING_BEARER_TOKEN`  | Bearer token for authentication                      | none             |
| `--allowed-paths`     | `SCRIPTLING_ALLOWED_PATHS` | Comma-separated allowed filesystem paths             | (no restriction) |
| `--tls-cert`          | `SCRIPTLING_TLS_CERT`      | TLS certificate file                                 | none             |
| `--tls-key`           | `SCRIPTLING_TLS_KEY`       | TLS key file                                         | none             |
| `--tls-generate`      | -                          | Generate self-signed certificate                     | false            |

## Environment Configuration

The CLI automatically loads environment variables from a `.env` file in the current directory (if it exists). This is useful for setting default values for flags without typing them on the command line.

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

- Standard libraries: `json`, `math`, `random`, `re`, `time`, `base64`, `hashlib`, `urllib`
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
- [Writing MCP Tools](../../../libraries/scriptling/writing-mcp-tools/) - Creating custom MCP tools
