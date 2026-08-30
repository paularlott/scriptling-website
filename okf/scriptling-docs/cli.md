---
description: Command-line interface for Scriptling.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/cli/
sources:
    - resource: https://scriptling.dev/docs/cli/
status: stable
tags:
    - cli
title: CLI Guide
type: Guide
---
# CLI Guide

Scriptling includes a command-line interface for running scripts, interactive mode, and HTTP/MCP/JSON-RPC servers.

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

# Start stdio JSON-RPC server
scriptling --json-rpc setup.py

# Start HTTP JSON-RPC server
scriptling --server :8000 --json-rpc setup.py
```

## Documentation

### [Basic Usage](https://scriptling.dev/okf/scriptling-docs/cli/basic-usage.md)

Running scripts, interactive mode, lint mode, and environment configuration.

### [Command Line Options](https://scriptling.dev/okf/scriptling-docs/cli/command-line-options.md)

Every CLI flag, environment variable, and configuration file setting, plus container endpoints.

### [Network Policy](https://scriptling.dev/okf/scriptling-docs/cli/network-policy.md)

Restricting script outbound network access with a policy file.

### [Libraries](https://scriptling.dev/okf/scriptling-docs/cli/libraries.md)

Loading, disabling, and controlling library and filesystem access.

### [HTTP Server Mode](https://scriptling.dev/okf/scriptling-docs/cli/http-server.md)

Running Scriptling as an HTTP server with custom routes, TLS, and authentication.

### [JSON-RPC Server Mode](https://scriptling.dev/okf/scriptling-docs/cli/jsonrpc-server.md)

Running Scriptling as a concurrent JSON-RPC 2.0 server over stdio or HTTP.

### [Plugin Server Mode](https://scriptling.dev/okf/scriptling-docs/cli/plugin-server.md)

Running a Scriptling script as a first-class plugin peer with full handshake support (agent variant only).

### [MCP Server Mode](https://scriptling.dev/okf/scriptling-docs/cli/mcp-server.md)

Running Scriptling as a Model Context Protocol server for AI integration, including the script execution tool.

### [Packages](https://scriptling.dev/okf/scriptling-docs/cli/packages.md)

Create, distribute, and load Scriptling packages from local files or URLs.

## Features

- **File execution**: Run Scriptling scripts from files
- **Stdin execution**: Pipe scripts to stdin
- **Interactive mode**: REPL-like interactive execution
- **Lint mode**: Check scripts for syntax errors without execution
- **HTTP Server**: Start HTTP server with custom routes via `--server`
- **JSON-RPC Server**: Serve concurrent JSON-RPC 2.0 over stdio, or over HTTP `/json-rpc` with `--server --json-rpc`
- **Plugin Server**: Expose a script as a first-class plugin peer (agent variant only) with `runtime.plugin.serve()` + `runtime.plugin.register_function()`
- **MCP Server**: Serve tools via Model Context Protocol with `--mcp-tools`
- **MCP Script Execution**: Allow LLMs to execute Scriptling code via `--mcp-exec-script`
- **Packages**: Load libraries from local or remote ZIP packages with `--package`
- **Path restrictions**: Restrict filesystem access with `--allowed-paths`
- **Secret aliases**: Load host-owned secret providers with `--secret-config`
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

# Load host-owned secret providers for scriptling.secret
scriptling --secret-config ./secrets.toml script.py

# Load package from URL
scriptling --package https://example.com/lib.zip script.py

# Create a package
scriptling pack ./mylib -o mylib.zip
```
