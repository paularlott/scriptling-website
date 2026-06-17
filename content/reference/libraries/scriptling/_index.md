---
title: Scriptling Libraries
description: Scriptling-specific libraries for AI, MCP, messaging, networking, and runtime functionality.
weight: 9
---

Scriptling-specific libraries that provide functionality not available in Python's standard library. They use the `scriptling.` namespace prefix.

#### AI
- [AI](ai/ai/) — AI and LLM functions for OpenAI-compatible APIs
- [Agent](ai/agent/) — Agentic AI loop with automatic tool execution
- [Agent Interaction](ai/interact/) — Interactive terminal interface for AI agents
- [Memory](ai/memory/) — Long-term memory store for AI agents

#### MCP
- [MCP Client](mcp/client/) — MCP (Model Context Protocol) client for connecting to MCP servers
- [MCP Tools](mcp/tool/) — Helper library for authoring MCP tools
- [Writing MCP Tools](mcp/writing-mcp-tools/) — Guide for creating MCP tools

#### Messaging
- [Telegram](messaging/telegram/) — Telegram Bot API client
- [Discord](messaging/discord/) — Discord Bot API client
- [Slack](messaging/slack/) — Slack Bot API client
- [Console](messaging/console/) — Console-based messaging client

#### Networking
- [Gossip](networking/gossip/) — Gossip protocol cluster membership and messaging
- [Multicast](networking/multicast/) — UDP multicast group messaging
- [Unicast](networking/unicast/) — UDP and TCP point-to-point messaging
- [Resolve](networking/resolve/) — DNS resolution for IP, SRV, and srv+http URLs
- [Websocket](networking/websocket/) — WebSocket client for connecting to WebSocket servers

#### Provisioning
- [Provisioning](provisioning/provision-file/) — File and directory provisioning

#### Runtime
- [Runtime](runtime/runtime/) — Background tasks and async execution
- [HTTP](runtime/http/) — HTTP route registration and response helpers
- [KV](runtime/kv/) — Thread-safe key-value store
- [Sync](runtime/sync/) — Named cross-environment concurrency primitives
- [Sandbox](runtime/sandbox/) — Isolated script execution environments

#### Utilities
- [Console](utilities/console/) — Console input/output functions
- [Container](utilities/container/) — Container lifecycle management for Docker, Podman, and Apple Containers
- [Grep](utilities/grep/) — Fast file content search with regex or literal patterns
- [Sed](utilities/sed/) — In-place file content replacement with literal strings or regex patterns
- [Secrets](utilities/secret/) — Resolve secrets through host-configured provider aliases
- [Wait For](utilities/wait_for/) — Wait for resources to become available
- [Plugin](utilities/plugin/) — Control library for executable plugins
- [Toon](utilities/toon/) — TOON (Token-Oriented Object Notation) encoding/decoding
- [Similarity](utilities/similarity/) — Text similarity utilities including fuzzy search and MinHash
- [Templates](utilities/template/) — Go-powered template rendering (HTML and text)
- [Markdown](utilities/markdown/) — Markdown to HTML conversion (GitHub Flavored Markdown)

## Usage

```python
import scriptling.ai as ai

response = ai.chat("gpt-4", "Hello!")
print(response)
```

## Registration

These libraries require explicit registration when embedding Scriptling in Go. See [Library Registration](/docs/go-integration/library-registration/) for registration code.

## See Also

- [Library Registration](/docs/go-integration/library-registration/) - How to register libraries in Go
- [Standard Libraries](../) - Built-in libraries (json, math, re, etc.)
- [Writing MCP Tools](mcp/writing-mcp-tools/) - Guide for creating MCP tools
