---
title: Libraries
description: Available libraries and APIs in Scriptling.
tags: [libraries]
weight: 11

aliases:
  - /reference/libraries/scriptling/
---

## [Quick Reference: Library Cheat Sheet](/reference/libraries/cheat-sheet/)

Scriptling provides 60+ libraries organized by capability.

## Standard Libraries

- [Data Formats](data-formats/): JSON, YAML, TOML
- [Text Processing](text-processing/): Regex, strings, HTML, diffing
- [Math & Numbers](math-numbers/): Math, random, statistics, hashing, UUID
- [Collections & Iteration](collections-iteration/): Collections, itertools, functools
- [Time & System](time-system/): Time, datetime, I/O, platform, URL handling

## Extended Libraries

- [File System](filesystem/): OS, paths, binary I/O, glob
- [HTTP & Process](http-process/): HTTP requests, subprocesses, system, logging, secrets

## Scriptling Libraries

The `scriptling.*` libraries provide functionality beyond Python's standard library, under the `scriptling.` namespace prefix:

- [AI](ai/): LLM clients, agents, memory, tool schemas
- [Databases](databases/): SQLite, SQL, Valkey, BadgerDB, and the ORM
- [MCP](mcp/): MCP clients and tool authoring
- [Messaging](messaging/): Telegram, Discord, Slack, console
- [Networking](networking/): Gossip, multicast, unicast, DNS, WebSocket
- [Plugin](plugin/): Control library for executable plugins
- [Provisioning](provisioning/): File and fetch provisioning
- [Runtime](runtime/): Background tasks, HTTP, JSON-RPC, KV, sync, sandbox
- [Template](template/): Go-powered HTML and text templates
- [Utilities](utilities/): Console, containers, grep, find, CSV, XML, secrets, and more

## Registration

Every library is available by default in the CLI and MCP server, no setup needed there.

When embedding in Go, you register libraries explicitly. Each library page is marked **Standard library** or **Extended library**:

- **Standard libraries** (the 23 libraries also documented under [Data Formats](data-formats/), [Text Processing](text-processing/), [Math & Numbers](math-numbers/), [Collections & Iteration](collections-iteration/), and [Time & System](time-system/)) are all registered together with `stdlib.RegisterAll(p)`.
- **Extended libraries** (everything under [File System](filesystem/) and [HTTP & Process](http-process/), plus every `scriptling.*` library listed under [Scriptling Libraries](#scriptling-libraries)) must be registered individually, and some take extra arguments such as `allowedPaths` to restrict filesystem access.

See [Library Registration](/docs/go-integration/library-registration/) for the full list of registration calls, and the [Security Guide](/docs/security/) for which libraries carry filesystem, network, process, or secrets risk.

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```
