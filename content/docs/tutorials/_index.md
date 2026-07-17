---
title: Tutorials
description: Step-by-step guides for building with Scriptling.
tags: [tutorials]
weight: 8
---

Hands-on tutorials that walk through real-world scenarios from start to finish.

## CLI Tutorials

### [Fetching and Processing API Data](api-data-fetching/)

Write a CLI script that fetches data from a public API, processes it with JSON, and outputs formatted results. Covers GET/POST/PUT/DELETE requests, the `requests` library, error handling, and working with lists and dictionaries.

## Plugin Tutorials

### [Writing a Go Plugin](go-plugin/)

Build a Go executable plugin that exposes functions and classes under `plugin.*`.

### [Writing a Bash Plugin](bash-plugin/)

Implement the plugin JSON-RPC protocol directly from a shell script.

### [Writing a C Plugin](c-plugin/)

Build a multi-threaded C plugin with functions, classes, properties, callbacks, and logging using the single-header SDK.

### [Plugin Streaming Callbacks](plugin-callbacks/)

Pass a Scriptling function into a Go plugin and stream events back while the plugin function is running. Covers `plugin.Callback`, callback lifetime, and structured callback payloads.

## Go Integration Tutorials

### [Embedding a Rules Engine](embedding-rules-engine/)

Embed Scriptling in a Go application to evaluate business rules at runtime. Covers interpreter setup, variable exchange, custom function registration, and library loading.

## AI Integration Tutorials

### [Building an MCP Tool Server](mcp-tool-server/)

Create a Model Context Protocol server with custom tools that AI assistants can call. Covers tool definition, script implementation, and server startup.
