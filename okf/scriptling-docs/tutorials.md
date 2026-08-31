---
description: Step-by-step guides for building with Scriptling.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/tutorials/
sources:
    - resource: https://scriptling.dev/docs/tutorials/
status: stable
tags:
    - tutorials
title: Tutorials
type: Guide
---
# Tutorials

Hands-on tutorials that walk through real-world scenarios from start to finish. Choose the section for your role: CLI user, plugin author, Go embedder, or AI/server integrator.

These are project walkthroughs, not exhaustive reference pages. For language learning, library lookup, or database APIs, use the [Language Guide](https://scriptling.dev/okf/scriptling-reference/scriptling-reference.md), [Library Reference](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md), or [Database Libraries](https://scriptling.dev/okf/scriptling-libraries/databases.md).

## CLI Tutorials

### [Fetching and Processing API Data](https://scriptling.dev/okf/scriptling-docs/tutorials/api-data-fetching.md)

Write a CLI script that fetches data from a public API, processes it with JSON, and outputs formatted results. Covers GET/POST/PUT/DELETE requests, the `requests` library, error handling, and working with lists and dictionaries.

## Plugin Tutorials

### [Writing a Go Plugin](https://scriptling.dev/okf/scriptling-docs/tutorials/go-plugin.md)

Build a Go executable plugin that exposes functions and classes under `plugin.*`.

### [Writing a Fetcher Plugin](https://scriptling.dev/okf/scriptling-docs/tutorials/fetcher-plugin.md)

Serve libraries in any namespace, static assets, and script sources from a plugin-owned scheme such as `demo://`.

### [Writing a Bash Plugin](https://scriptling.dev/okf/scriptling-docs/tutorials/bash-plugin.md)

Implement the plugin JSON-RPC protocol directly from a shell script.

### [Writing a C Plugin](https://scriptling.dev/okf/scriptling-docs/tutorials/c-plugin.md)

Build a multi-threaded C plugin with functions, classes, properties, callbacks, and logging using the single-header SDK.

### [Plugin Streaming Callbacks](https://scriptling.dev/okf/scriptling-docs/tutorials/plugin-callbacks.md)

Pass a Scriptling function into a Go plugin and stream events back while the plugin function is running. Covers `plugin.Callback`, callback lifetime, and structured callback payloads.

## Go Integration Tutorials

### [Embedding a Rules Engine](https://scriptling.dev/okf/scriptling-docs/tutorials/embedding-rules-engine.md)

Embed Scriptling in a Go application to evaluate business rules at runtime. Covers interpreter setup, variable exchange, custom function registration, and library loading.

## AI Integration Tutorials

### [Building an MCP Tool Server](https://scriptling.dev/okf/scriptling-docs/tutorials/mcp-tool-server.md)

Create a Model Context Protocol server with custom tools that AI assistants can call. Covers tool definition, script implementation, and server startup.

### [Building an MCP Resources & Prompts Server](https://scriptling.dev/okf/scriptling-docs/tutorials/mcp-resources-prompts.md)

Expose MCP resources and prompts as files, alongside tools.
