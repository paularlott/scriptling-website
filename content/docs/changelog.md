---
title: Changelog
description: Scriptling release history and changes.
layout: changelog
nav-skip: true
---

## February 2026

{{< version "v0.1.0" >}}

Initial pre-release of Scriptling.

**Features:**

- Python-like syntax with indentation-based blocks
- Core types: integers, floats, strings, booleans, lists, dictionaries, sets
- Control flow: if/elif/else, while, for loops, break, continue, match statements
- Object-oriented: Classes with single inheritance, methods, and constructors
- Functions, lambda, list comprehensions, error handling
- Background tasks with `scriptling.runtime` for concurrent execution
- 25+ built-in libraries including JSON, regex, math, HTTP requests, subprocess
- Go integration with direct type mapping
- AI/LLM integration with OpenAI-compatible API support
- MCP (Model Context Protocol) server and client
- HTTP server with route registration
- Sandboxed execution with configurable security
- CLI tool with interactive mode, HTTP/MCP server, and built-in linter
- Extensible: create custom functions, libraries, and classes in Go or Scriptling
- Cross-platform binaries for Linux, macOS, and Windows
