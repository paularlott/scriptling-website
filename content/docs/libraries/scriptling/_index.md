---
title: Scriptling Libraries
description: Scriptling-specific libraries for AI, MCP, messaging, and runtime functionality.
weight: 2
---

Scriptling-specific libraries that provide functionality not available in Python's standard library. They use the `scriptling.` namespace prefix.

## AI & LLM

| Library | Description |
|---------|-------------|
| [scriptling.ai](ai/ai/) | AI and LLM functions for OpenAI-compatible APIs |
| [scriptling.ai.agent](ai/agent/) | Agentic AI loop with automatic tool execution |
| [scriptling.ai.agent.interact](ai/interact/) | Interactive terminal interface for AI agents |
| [scriptling.ai.memory](ai/memory/) | Long-term memory store for AI agents |

## MCP Protocol

| Library | Description |
|---------|-------------|
| [scriptling.mcp](mcp/client/) | MCP (Model Context Protocol) client for connecting to MCP servers |
| [scriptling.mcp.tool](mcp/tool/) | Helper library for authoring MCP tools |
| [Writing MCP Tools](mcp/writing-mcp-tools/) | Guide for creating MCP tools |

## Messaging

| Library | Description |
|---------|-------------|
| [scriptling.messaging.telegram](messaging/telegram/) | Telegram Bot API client |
| [scriptling.messaging.discord](messaging/discord/) | Discord Bot API client |
| [scriptling.messaging.slack](messaging/slack/) | Slack Bot API client |
| [scriptling.messaging.console](messaging/console/) | Console-based messaging client |

## Runtime

| Library | Description |
|---------|-------------|
| [scriptling.runtime](runtime/runtime/) | Background tasks and async execution |
| [scriptling.runtime.http](runtime/http/) | HTTP route registration and response helpers |
| [scriptling.runtime.kv](runtime/kv/) | Thread-safe key-value store |
| [scriptling.runtime.sync](runtime/sync/) | Named cross-environment concurrency primitives |
| [scriptling.runtime.sandbox](runtime/sandbox/) | Isolated script execution environments |

## Utilities

| Library | Description |
|---------|-------------|
| [scriptling.console](console/) | Console input/output functions |
| [scriptling.wait_for](wait_for/) | Wait for resources to become available |
| [scriptling.websocket](websocket/) | WebSocket client for connecting to WebSocket servers |
| [scriptling.toon](toon/) | TOON (Token-Oriented Object Notation) encoding/decoding |
| [scriptling.fuzzy](fuzzy/) | Fuzzy string matching utilities |

## Usage

```python
import scriptling.ai as ai

response = ai.chat("gpt-4", "Hello!")
print(response)
```
