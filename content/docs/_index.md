---
title: Documentation
description: Complete documentation for Scriptling - a minimal, sandboxed Python-like scripting language for Go applications.
weight: 1
---

Welcome to the Scriptling documentation. Scriptling is a minimal, sandboxed interpreter for Python-like scripting designed for embedding in Go applications.

## Getting Started

- [Getting Started](quick-start/)

## CLI Reference

- [CLI Reference](cli/)

## Go Integration

- [Go Integration](go-integration/)

## Language Guide

- [Language Guide](language/)

## Libraries

- [Libraries](libraries/)

## Security Guide

- [Security Guide](security/)

## Tutorials

- [Fetching API Data](tutorials/api-data-fetching/) - CLI script for HTTP + JSON processing
- [Embedding a Rules Engine](tutorials/embedding-rules-engine/) - Go integration with custom functions
- [Building an MCP Tool Server](tutorials/mcp-tool-server/) - Custom tools for AI assistants

## Core Concepts

### What is Scriptling?

Scriptling is a dynamically-typed, interpreted language with Python-inspired syntax. It supports:

- Variables, functions, and control flow
- Classes with single inheritance
- Lists, dictionaries, and sets
- String manipulation and JSON processing
- HTTP/REST API calls
- Go interoperability

### Key Features

- **Python-like syntax** with indentation-based blocks
- **Sandboxed execution** with configurable security
- **Go integration** with direct type mapping
- **Rich library ecosystem** with 60+ built-in libraries
- **AI/LLM ready** with MCP protocol support

### Differences from Python

While Scriptling is inspired by Python, it has some key differences:

- **Single Inheritance Only** - Classes support single inheritance but not multiple inheritance
- **No Nested Classes** - Classes cannot be defined within other classes
- **Simplified Scope** - `nonlocal` and `global` keywords work slightly differently
- **Go Integration** - Designed primarily for embedding in Go
- **Sandboxed** - No direct access to filesystem or network unless explicitly enabled

## Use Cases

- **AI & LLM Integration** - Let AI agents execute code safely
- **Go Embedding** - Add scripting capabilities to Go applications
- **REST API Automation** - Built-in HTTP client with JSON handling
- **Sandboxed Execution** - Run untrusted code with security controls
- **MCP Servers** - Build Model Context Protocol servers for LLM tools

