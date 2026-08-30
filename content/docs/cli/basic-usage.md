---
title: Basic Usage
description: Running scripts, interactive mode, and lint mode.
tags: [cli]
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

## Environment Variables and .env Files

The CLI automatically loads environment variables from a `.env` file in the current directory (if it exists). For persistent configuration, prefer `scriptling.toml`: the `.env` file is useful for secrets or environment-specific overrides that shouldn't be committed to version control.

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

- [Command Line Options](../command-line-options/) - Every flag, environment variable, and config file setting
- [Network Policy](../network-policy/) - Restricting script outbound network access
- [Libraries](../libraries/) - Loading, disabling, and access modes
- [HTTP Server Mode](../http-server/) - Running Scriptling as an HTTP server
- [MCP Server Mode](../mcp-server/) - Model Context Protocol integration
- [Writing MCP Tools](../../../reference/libraries/mcp/writing-mcp-tools/) - Creating custom MCP tools
