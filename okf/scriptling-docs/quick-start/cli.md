---
description: Install and start using the Scriptling CLI.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/quick-start/cli/
sources:
    - resource: https://scriptling.dev/docs/quick-start/cli/
status: stable
tags:
    - quick-start
    - cli
    - installation
title: CLI Getting Started
type: Guide
---
# CLI Getting Started

Get up and running with the Scriptling command-line interface.

## Installation

### Homebrew (macOS & Linux)

```bash
brew install paularlott/tap/scriptling
```

### GitHub Releases

Download pre-built binaries from [GitHub Releases](https://github.com/paularlott/scriptling/releases):

- Linux (AMD64, ARM64)
- macOS (AMD64, ARM64)
- Windows (AMD64, ARM64)

### Build from Source

```bash
git clone https://github.com/paularlott/scriptling.git
cd scriptling

# Build CLI for current platform
make build

# Run scripts
./bin/scriptling script.py
```

## Your First Script

Create a file called `hello.py`:

```python
name = "World"
print(f"Hello, {name}!")

# Use standard libraries
import json
import math

data = json.dumps({"numbers": [1, 2, 3]})
print(data)
print(f"sqrt(16) = {math.sqrt(16)}")
```

Run it:

```bash
scriptling hello.py
```

## Interactive Mode

Launch the REPL to experiment:

```bash
scriptling --interactive
```

## Pipe a Script

```bash
echo 'print("Hello")' | scriptling
```

## HTTP Server

Run Scriptling as an HTTP server:

```bash
scriptling --server :8000 setup.py
```

## MCP Server

Run Scriptling as a Model Context Protocol server for AI integration:

```bash
scriptling --server :8000 --mcp-tools ./tools setup.py
```

## Next Steps

- [Language Guide](../../scriptling-reference/scriptling-reference.md) - Learn the complete language syntax
- [Libraries](../../scriptling-libraries/scriptling-libraries.md) - Explore available libraries and APIs
- [CLI Reference](../cli.md) - Full command-line interface documentation
- [Security Guide](../security.md) - Security best practices
