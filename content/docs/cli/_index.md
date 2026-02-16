---
title: CLI Reference
description: Command-line interface for Scriptling.
weight: 5
---

Scriptling includes a command-line interface for running scripts, interactive mode, and HTTP/MCP server.

## Installation

### Homebrew (macOS & Linux)

```bash
brew install paularlott/tap/scriptling
```

### GitHub Releases

Download pre-built binaries from [GitHub Releases](https://github.com/paularlott/scriptling/releases):

| Platform | Architectures |
|----------|---------------|
| Linux | AMD64, ARM64 |
| macOS | AMD64, ARM64 |
| Windows | AMD64, ARM64 |

### Build from Source

```bash
# Clone the repository
git clone https://github.com/paularlott/scriptling.git
cd scriptling

# Install Task (build tool)
brew install go-task/tap/go-task

# Build for current platform
task build

# Build for all platforms
task build-all
```

## Basic Usage

### Run a Script

```bash
scriptling script.py
```

### Pipe Script

```bash
echo 'print("Hello")' | scriptling
cat script.py | scriptling
```

### Interactive Mode

```bash
scriptling --interactive
```

## Command Line Options

```bash
Usage: scriptling [options] [script.py]

Options:
  -i, --interactive    Start interactive mode
  -s, --server ADDR    Start HTTP server on address
  --mcp-tools DIR      Enable MCP tools from directory
  --tls-generate       Generate self-signed TLS certificate
  --bearer-token TOKEN Bearer token for authentication
  --safe               Run in safe mode (restricted access)
  --lib-dir DIR        Custom library directory
  --env-file FILE      Load environment from file
  -h, --help           Show help
```

## HTTP Server

### Basic Server

```bash
scriptling --server :8000 script.py
```

### With TLS

```bash
scriptling --server :8443 --tls-generate script.py
```

### With Authentication

```bash
scriptling --server :8000 --bearer-token secret123 script.py
```

### With MCP Tools

```bash
scriptling --server :8000 --mcp-tools ./tools script.py
```

## MCP Server

Scriptling can run as an MCP (Model Context Protocol) server for LLM integration:

```bash
scriptling --server :8000 --mcp-tools ./tools script.py
```

MCP tools are Scriptling scripts that define tool metadata and handlers.

## Safe Mode

Run scripts in a restricted sandbox:

```bash
scriptling --safe script.py
```

Safe mode disables:
- File system access
- Network access
- Subprocess execution

## Environment Variables

Load environment from a `.env` file:

```bash
scriptling --env-file .env script.py
```

Access in scripts:

```python
import os
api_key = os.getenv("API_KEY")
```

## Custom Libraries

Load libraries from a custom directory:

```bash
scriptling --lib-dir ./mylibs script.py
```

## Examples

### REST API Client

```bash
scriptling api_client.py
```

```python
# api_client.py
import json
import requests

response = requests.get("https://api.example.com/users")
if response.status_code == 200:
    users = response.json()
    for user in users:
        print(user["name"])
```

### HTTP Server with Routes

```bash
scriptling --server :8000 server.py
```

```python
# server.py
import scriptling.runtime.http as http

@http.route("/api/hello", methods=["GET"])
def hello(request):
    return http.json({"message": "Hello, World!"})

@http.route("/api/echo", methods=["POST"])
def echo(request):
    return http.json(request["body"])
```

### MCP Tool

```bash
scriptling --server :8000 --mcp-tools ./tools server.py
```

```python
# ./tools/calculator.py
def add(a, b):
    """Add two numbers together."""
    return a + b

# Tool metadata
__mcp_tool__ = {
    "name": "calculator_add",
    "description": "Add two numbers",
    "parameters": {
        "a": {"type": "number", "description": "First number"},
        "b": {"type": "number", "description": "Second number"}
    }
}
```
