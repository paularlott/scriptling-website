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
- [AI](https://scriptling.dev/okf/scriptling-libraries/scriptling/ai/ai.md): AI and LLM functions for OpenAI-compatible APIs
- [Agent](https://scriptling.dev/okf/scriptling-libraries/scriptling/ai/agent.md): Agentic AI loop with automatic tool execution
- [Agent Interaction](https://scriptling.dev/okf/scriptling-libraries/scriptling/ai/interact.md): Interactive terminal interface for AI agents
- [Memory](https://scriptling.dev/okf/scriptling-libraries/scriptling/ai/memory.md): Long-term memory store for AI agents

#### MCP
- [MCP Client](https://scriptling.dev/okf/scriptling-libraries/scriptling/mcp/client.md): MCP (Model Context Protocol) client for connecting to MCP servers
- [MCP Tools](https://scriptling.dev/okf/scriptling-libraries/scriptling/mcp/tool.md): Helper library for authoring MCP tools
- [Writing MCP Tools](https://scriptling.dev/okf/scriptling-libraries/scriptling/mcp/writing-mcp-tools.md): Guide for creating MCP tools

#### Messaging
- [Telegram](https://scriptling.dev/okf/scriptling-libraries/scriptling/messaging/telegram.md): Telegram Bot API client
- [Discord](https://scriptling.dev/okf/scriptling-libraries/scriptling/messaging/discord.md): Discord Bot API client
- [Slack](https://scriptling.dev/okf/scriptling-libraries/scriptling/messaging/slack.md): Slack Bot API client
- [Console](https://scriptling.dev/okf/scriptling-libraries/scriptling/messaging/console.md): Console-based messaging client

#### Networking
- [Gossip](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/gossip.md): Gossip protocol cluster membership and messaging
- [Multicast](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/multicast.md): UDP multicast group messaging
- [Unicast](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/unicast.md): UDP and TCP point-to-point messaging
- [Resolve](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/resolve.md): DNS resolution for IP, SRV, and srv+http URLs
- [Websocket](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/websocket.md): WebSocket client for connecting to WebSocket servers

#### Databases
- [SQLite](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/sqlite.md): Embedded relational database (pure Go)
- [SQL](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/sql.md): MySQL, MariaDB and PostgreSQL client
- [Valkey](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/valkey.md): Valkey and Redis key/value client
- [BadgerDB](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/badgerdb.md): Embedded key/value store mirroring the valkey API

#### Provisioning
- [Provisioning](https://scriptling.dev/okf/scriptling-libraries/scriptling/provisioning.md): File/directory provisioning and HTTP/HTTPS fetch provisioning

#### Runtime
- [Runtime](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/runtime.md): Background tasks and async execution
- [HTTP](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/http.md): HTTP route registration and response helpers
- [JSON-RPC](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/jsonrpc.md): JSON-RPC 2.0 server registration for stdio or HTTP
- [KV](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/kv.md): Thread-safe key-value store
- [Sync](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/sync.md): Named cross-environment concurrency primitives
- [Sandbox](https://scriptling.dev/okf/scriptling-libraries/scriptling/runtime/sandbox.md): Isolated script execution environments

#### Utilities
- [Console](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/console.md): Console input/output functions
- [Container](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/container.md): Container lifecycle management for Docker, Podman, and Apple Containers
- [Nomad](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/nomad.md): HashiCorp Nomad client covering CSI volumes and jobs
- [Grep](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/grep.md): Fast file content search with regex or literal patterns
- [Find](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/find.md): Find files and directories by name, type, mtime, and size
- [CSV](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/csv.md): CSV parsing and formatting (string-based, no filesystem access)
- [XML](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/xml.md): XML parsing and formatting (dict-based, string-only)
- [Sed](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/sed.md): In-place file content replacement with literal strings or regex patterns
- [Secrets](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/secret.md): Resolve secrets through host-configured provider aliases
- [Wait For](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/wait_for.md): Wait for resources to become available
- [Plugin](https://scriptling.dev/okf/scriptling-libraries/scriptling/plugin.md): Control library for executable plugins
- [Toon](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/toon.md): TOON (Token-Oriented Object Notation) encoding/decoding
- [Similarity](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/similarity.md): Text similarity utilities including fuzzy search and MinHash
- [Templates](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/template.md): Go-powered template rendering (HTML and text)
- [Markdown](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/markdown.md): Markdown to HTML conversion (GitHub Flavored Markdown)

## Usage

```python
import scriptling.ai as ai

response = ai.chat("gpt-4", "Hello!")
print(response)
```

## Registration

These libraries require explicit registration when embedding Scriptling in Go. See [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) for registration code.

## See Also

- [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) - How to register libraries in Go
- [Standard Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Built-in libraries (json, math, re, etc.)
- [Writing MCP Tools](https://scriptling.dev/okf/scriptling-libraries/scriptling/mcp/writing-mcp-tools.md) - Guide for creating MCP tools
