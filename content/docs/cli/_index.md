---
title: CLI Reference
description: Command-line interface for Scriptling.
weight: 2
---

Scriptling includes a command-line interface for running scripts, interactive mode, and HTTP/MCP servers.

## Quick Start

```bash
# Run a script
scriptling script.py

# Interactive mode
scriptling -i

# Start HTTP server
scriptling --server :8000 setup.py

# Start MCP server with tools
scriptling --server :8000 --mcp-tools ./tools setup.py
```

## Documentation

### [Basic Usage](./basic-usage/)

Installation, running scripts, interactive mode, lint mode, command line options, environment configuration, and library loading.

### [HTTP Server Mode](./http-server/)

Running Scriptling as an HTTP server with custom routes, TLS, and authentication.

### [MCP Server Mode](./mcp-server/)

Running Scriptling as a Model Context Protocol server for AI integration, including the script execution tool.

### [Packages](./packages/)

Create, distribute, and load Scriptling packages from local files or URLs.

## Features

- **File execution**: Run Scriptling scripts from files
- **Stdin execution**: Pipe scripts to stdin
- **Interactive mode**: REPL-like interactive execution
- **Lint mode**: Check scripts for syntax errors without execution
- **HTTP Server**: Start HTTP server with custom routes via `--server`
- **MCP Server**: Serve tools via Model Context Protocol with `--mcp-tools`
- **MCP Script Execution**: Allow LLMs to execute Scriptling code via `--mcp-exec-script`
- **Packages**: Load libraries from local or remote ZIP packages with `--package`
- **Path restrictions**: Restrict filesystem access with `--allowed-paths`
- **Custom libraries**: Libraries are loaded automatically from the script's directory
- **Environment configuration**: Auto-load settings from `.env` file
- **Configurable logging**: Set log level with `--log-level`
- **Cross-platform**: Built for Linux, macOS, and Windows on AMD64 and ARM64
- **Minimal size**: Optimized with stripped binaries (~10MB)

## Common Commands

```bash
# Show help
scriptling --help

# Run with debug logging
scriptling --log-level debug script.py

# Restrict filesystem access
scriptling --allowed-paths "/tmp,./data" script.py

# Start HTTPS server with self-signed cert
scriptling --server :8443 --tls-generate setup.py

# Load a package and run
scriptling --package ./libs/utils.zip script.py

# Load package from URL
scriptling --package https://example.com/lib.zip script.py

# Create a package
scriptling pack ./mylib -o mylib.zip
```
