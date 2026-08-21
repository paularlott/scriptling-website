---
description: Scriptling-specific libraries for AI, MCP, messaging, networking, and runtime functionality.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/
status: stable
tags:
    - libraries
title: Scriptling Libraries
type: API Reference
---
# Scriptling Libraries

Scriptling-specific libraries that provide functionality not available in Python's standard library. They use the `scriptling.` namespace prefix.

#### AI
- [AI](scriptling/ai/ai.md): AI and LLM functions for OpenAI-compatible APIs
- [Agent](scriptling/ai/agent.md): Agentic AI loop with automatic tool execution
- [Agent Interaction](scriptling/ai/interact.md): Interactive terminal interface for AI agents
- [Memory](scriptling/ai/memory.md): Long-term memory store for AI agents

#### MCP
- [MCP Client](scriptling/mcp/client.md): MCP (Model Context Protocol) client for connecting to MCP servers
- [MCP Tools](scriptling/mcp/tool.md): Helper library for authoring MCP tools
- [Writing MCP Tools](scriptling/mcp/writing-mcp-tools.md): Guide for creating MCP tools

#### Messaging
- [Telegram](scriptling/messaging/telegram.md): Telegram Bot API client
- [Discord](scriptling/messaging/discord.md): Discord Bot API client
- [Slack](scriptling/messaging/slack.md): Slack Bot API client
- [Console](scriptling/messaging/console.md): Console-based messaging client

#### Networking
- [Gossip](scriptling/networking/gossip.md): Gossip protocol cluster membership and messaging
- [Multicast](scriptling/networking/multicast.md): UDP multicast group messaging
- [Unicast](scriptling/networking/unicast.md): UDP and TCP point-to-point messaging
- [Resolve](scriptling/networking/resolve.md): DNS resolution for IP, SRV, and srv+http URLs
- [Websocket](scriptling/networking/websocket.md): WebSocket client for connecting to WebSocket servers

#### Provisioning
- [Provisioning](scriptling/provisioning.md): File/directory provisioning and HTTP/HTTPS fetch provisioning

#### Runtime
- [Runtime](scriptling/runtime/runtime.md): Background tasks and async execution
- [HTTP](scriptling/runtime/http.md): HTTP route registration and response helpers
- [JSON-RPC](scriptling/runtime/jsonrpc.md): JSON-RPC 2.0 server registration for stdio or HTTP
- [KV](scriptling/runtime/kv.md): Thread-safe key-value store
- [Sync](scriptling/runtime/sync.md): Named cross-environment concurrency primitives
- [Sandbox](scriptling/runtime/sandbox.md): Isolated script execution environments

#### Utilities
- [Console](scriptling/utilities/console.md): Console input/output functions
- [Container](scriptling/utilities/container.md): Container lifecycle management for Docker, Podman, and Apple Containers
- [Nomad](scriptling/utilities/nomad.md): HashiCorp Nomad client covering CSI volumes and jobs
- [Grep](scriptling/utilities/grep.md): Fast file content search with regex or literal patterns
- [Find](scriptling/utilities/find.md): Find files and directories by name, type, mtime, and size
- [CSV](scriptling/utilities/csv.md): CSV parsing and formatting (string-based, no filesystem access)
- [XML](scriptling/utilities/xml.md): XML parsing and formatting (dict-based, string-only)
- [Sed](scriptling/utilities/sed.md): In-place file content replacement with literal strings or regex patterns
- [Secrets](scriptling/utilities/secret.md): Resolve secrets through host-configured provider aliases
- [Wait For](scriptling/utilities/wait_for.md): Wait for resources to become available
- [Plugin](scriptling/plugin.md): Control library for executable plugins
- [Toon](scriptling/utilities/toon.md): TOON (Token-Oriented Object Notation) encoding/decoding
- [Similarity](scriptling/utilities/similarity.md): Text similarity utilities including fuzzy search and MinHash
- [Templates](scriptling/utilities/template.md): Go-powered template rendering (HTML and text)
- [Markdown](scriptling/utilities/markdown.md): Markdown to HTML conversion (GitHub Flavored Markdown)

## Usage

```python
import scriptling.ai as ai

response = ai.chat("gpt-4", "Hello!")
print(response)
```

## Registration

These libraries require explicit registration when embedding Scriptling in Go. See [Library Registration](../scriptling-docs/go-integration/library-registration.md) for registration code.

## See Also

- [Library Registration](../scriptling-docs/go-integration/library-registration.md) - How to register libraries in Go
- [Standard Libraries](scriptling-libraries.md) - Built-in libraries (json, math, re, etc.)
- [Writing MCP Tools](scriptling/mcp/writing-mcp-tools.md) - Guide for creating MCP tools
