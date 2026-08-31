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

Database support is optional. The plugin binaries live in their own formula:

```bash
brew install paularlott/tap/scriptling-plugins
export SCRIPTLING_PLUGIN_DIR="$(brew --prefix)/opt/scriptling-plugins/libexec/plugins"
```

Or use `scriptling-full` — the same CLI with all database plugins compiled
in (mutually exclusive with `scriptling`): `brew install paularlott/tap/scriptling-full`.

See [Plugins](https://scriptling.dev/okf/scriptling-docs/plugins.md) for how plugins load and the [database reference](https://scriptling.dev/okf/scriptling-libraries/databases.md) for the APIs.

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

Server modes evaluate a startup script before accepting requests. Create `setup.py` for any one-time initialization:

```python
print("Server initialized")
```

Then run Scriptling as an HTTP server:

```bash
scriptling --server :8000 setup.py
```

## MCP Server

The same startup script can initialize a Model Context Protocol server; tools are loaded from the directory passed to `--mcp-tools`:

```bash
scriptling --server :8000 --mcp-tools ./tools setup.py
```

## Next Steps

- [Language Guide](https://scriptling.dev/okf/scriptling-reference/scriptling-reference.md) - Learn the complete language syntax
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Explore available libraries and APIs
- [CLI Guide](https://scriptling.dev/okf/scriptling-docs/cli.md) - Full command-line interface documentation
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security best practices
