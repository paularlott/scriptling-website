---
title: Libraries
description: Available libraries and APIs in Scriptling.
weight: 5
---

## [Quick Reference: Library Cheat Sheet](/docs/libraries/cheat-sheet/)

Scriptling provides 60+ libraries organized by capability.

## Core Functions

Always available without importing:

| Function | Description |
|----------|-------------|
| `print(value)` | Output to console |
| `str(value)` | Convert to string |
| `int(value)` | Convert to integer |
| `float(value)` | Convert to float |
| `bool(value)` | Convert to boolean |
| `list(value)` | Convert to list |
| `dict(value)` | Convert to dictionary |
| `type(object)` | Get type of object |
| `isinstance(object, type)` | Check if object is instance of type |
| `help([object])` | Display help information |

## Built-in Libraries

Available for import without registration:

- [Data Formats](data-formats/) — JSON, YAML, TOML
- [Text Processing](text-processing/) — Regex, strings, HTML, diffing
- [Math & Numbers](math-numbers/) — Math, random, statistics, hashing, UUID
- [Collections & Iteration](collections-iteration/) — Collections, itertools, functools
- [Time & System](time-system/) — Time, datetime, I/O, platform, URL handling

## Extended Libraries

Require [registration](../go-integration/library-registration/) when embedding in Go. In the CLI they are available by default.

- [File System](filesystem/) — OS, paths, binary I/O, glob
- [HTTP & Process](http-process/) — HTTP requests, subprocesses, system, logging, secrets

## Scriptling Libraries

Scripting-specific libraries that provide functionality not available in Python's standard library. They use the `scriptling.` namespace prefix.

### AI
- [AI](scriptling/ai/ai/) — AI and LLM functions for OpenAI-compatible APIs
- [Agent](scriptling/ai/agent/) — Agentic AI loop with automatic tool execution
- [Agent Interaction](scriptling/ai/interact/) — Interactive terminal interface for AI agents
- [Memory](scriptling/ai/memory/) — Long-term memory store for AI agents

### MCP
- [MCP Client](scriptling/mcp/client/) — MCP (Model Context Protocol) client for connecting to MCP servers
- [MCP Tools](scriptling/mcp/tool/) | Helper library for authoring MCP tools
- [Writing MCP Tools](scriptling/mcp/writing-mcp-tools/) | Guide for creating MCP tools

### Messaging
- [Telegram](scriptling/messaging/telegram/) — Telegram Bot API client
- [Discord](scriptling/messaging/discord/) — Discord Bot API client
- [Slack](scriptling/messaging/slack/) — Slack Bot API client
- [Console](scriptling/messaging/console/) — Console-based messaging client

### Networking
- [Gossip](scriptling/networking/gossip/) — Gossip protocol cluster membership and messaging
- [Multicast](scriptling/networking/multicast/) — UDP multicast group messaging
- [Unicast](scriptling/networking/unicast/) — UDP and TCP point-to-point messaging
- [Resolve](scriptling/networking/resolve/) — DNS resolution for IP, SRV, and srv+http URLs
- [Websocket](scriptling/networking/websocket/) — WebSocket client for connecting to WebSocket servers

### Provisioning
- [Provisioning](scriptling/provisioning/provision-file/) — File and directory provisioning

### Runtime
- [Runtime](scriptling/runtime/runtime/) — Background tasks and async execution
- [HTTP](scriptling/runtime/http/) — HTTP route registration and response helpers
- [KV](scriptling/runtime/kv/) — Thread-safe key-value store
- [Sync](scriptling/runtime/sync/) — Named cross-environment concurrency primitives
- [Sandbox](scriptling/runtime/sandbox/) — Isolated script execution environments

### Utilities
- [Console](scriptling/utilities/console/) — Console input/output functions
- [Container](scriptling/utilities/container/) — Container lifecycle management
- [Grep](scriptling/utilities/grep/) — Fast file content search
- [Sed](scriptling/utilities/sed/) — In-place file content replacement
- [Secrets](scriptling/utilities/secret/) — Resolve secrets through host-configured provider aliases
- [Wait For](scriptling/utilities/wait_for/) — Wait for resources to become available
- [Toon](scriptling/utilities/toon/) — TOON encoding/decoding
- [Similarity](scriptling/utilities/similarity/) — Text similarity utilities
- [Templates](scriptling/utilities/template/) — Go-powered template rendering

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```

