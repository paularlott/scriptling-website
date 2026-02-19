---
title: Scriptling Libraries
description: Scriptling-specific libraries for AI, MCP, and runtime functionality.
weight: 2
---

Scriptling-specific libraries that provide functionality not available in Python's standard library. They use the `scriptling.` namespace prefix.

## AI & LLM

| Library | Description |
|---------|-------------|
| [scriptling.ai](ai/) | AI and LLM functions for OpenAI-compatible APIs |
| [scriptling.ai.agent](agent/) | Agentic AI loop with automatic tool execution |
| [scriptling.ai.agent.interact](interact/) | Interactive terminal interface for AI agents |

## MCP Protocol

| Library | Description |
|---------|-------------|
| [scriptling.mcp](mcp/) | MCP (Model Context Protocol) tool interaction |

## Runtime

| Library | Description |
|---------|-------------|
| [scriptling.runtime](runtime/) | Background tasks and async execution |
| [scriptling.runtime.http](runtime-http/) | HTTP route registration and response helpers |
| [scriptling.runtime.kv](runtime-kv/) | Thread-safe key-value store |
| [scriptling.runtime.sync](runtime-sync/) | Named cross-environment concurrency primitives |
| [scriptling.runtime.sandbox](sandbox/) | Isolated script execution environments |

## Utilities

| Library | Description |
|---------|-------------|
| [scriptling.console](console/) | Console input/output functions |
| [scriptling.toon](toon/) | TOON (Token-Oriented Object Notation) encoding/decoding |
| [scriptling.fuzzy](fuzzy/) | Fuzzy string matching utilities |

## Usage

```python
import scriptling.ai as ai

response = ai.chat("gpt-4", "Hello!")
print(response)
```
