---
description: Available libraries and APIs in Scriptling.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/
sources:
    - resource: https://scriptling.dev/reference/libraries/
status: stable
tags:
    - libraries
title: Libraries
type: API Reference
---
# Libraries

Scriptling provides 60+ libraries organized by capability. Availability depends on the binary, execution mode, and host registration; it is not safe to assume every library is present.

## Standard Libraries

- [Data Formats](https://scriptling.dev/okf/scriptling-libraries/data-formats.md): JSON, YAML, TOML
- [Text Processing](https://scriptling.dev/okf/scriptling-libraries/text-processing.md): Regex, strings, HTML, diffing
- [Math & Numbers](https://scriptling.dev/okf/scriptling-libraries/math-numbers.md): Math, random, statistics, hashing, UUID
- [Collections & Iteration](https://scriptling.dev/okf/scriptling-libraries/collections-iteration.md): Collections, itertools, functools
- [Time & System](https://scriptling.dev/okf/scriptling-libraries/time-system.md): Time, datetime, I/O, platform, URL handling

## Extended Libraries

- [File System](https://scriptling.dev/okf/scriptling-libraries/filesystem.md): OS, paths, binary I/O, glob
- [HTTP & Process](https://scriptling.dev/okf/scriptling-libraries/http-process.md): HTTP requests, subprocesses, system, logging, secrets

## Scriptling Libraries

The `scriptling.*` libraries provide functionality beyond Python's standard library:

- [AI](https://scriptling.dev/okf/scriptling-libraries/ai.md): LLM clients, agents, memory, tool schemas
- [Databases](https://scriptling.dev/okf/scriptling-libraries/databases.md): SQLite, SQL, Valkey, BadgerDB, and the ORM
- [MCP](https://scriptling.dev/okf/scriptling-libraries/mcp.md): MCP clients and tool authoring
- [Messaging](https://scriptling.dev/okf/scriptling-libraries/messaging.md): Telegram, Discord, Slack, console
- [Networking](https://scriptling.dev/okf/scriptling-libraries/networking.md): Gossip, multicast, unicast, DNS, WebSocket
- [Package](https://scriptling.dev/okf/scriptling-libraries/package.md): Read files and metadata from loaded app/plugin bundles
- [Plugin](https://scriptling.dev/okf/scriptling-libraries/plugin.md): Control library for executable plugins
- [Provisioning](https://scriptling.dev/okf/scriptling-libraries/provisioning.md): File and fetch provisioning
- [Runtime](https://scriptling.dev/okf/scriptling-libraries/runtime.md): Background tasks, HTTP, JSON-RPC, MCP, KV, sync, sandbox
- [Template](https://scriptling.dev/okf/scriptling-libraries/template.md): Go-powered HTML and text templates
- [Utilities](https://scriptling.dev/okf/scriptling-libraries/utilities.md): Console, containers, Nomad, grep, find, CSV, XML, secrets, and more

## Availability

A bare `scriptling.New()` environment has no libraries; embedders register every capability they intend to expose. The default CLI setup composes a broader set, subject to execution mode and disable flags.

| Library group | Default CLI and server setup | Bare embedding |
|---------------|------------------------------|----------------|
| Standard libraries | Registered together | `stdlib.RegisterAll(p)` |
| Core extended and `scriptling.*` libraries | Registered unless disabled; the exact set varies by mode | Register each required library explicitly |
| `scriptling.ai.tools` | The standalone namespace is not registered by normal setup; use `scriptling.ai.ToolRegistry` when `scriptling.ai` is present | Register the standalone tools library explicitly if needed |
| `scriptling.ai.agent.interact` | Added on the ordinary non-server CLI execution path; evaluator factories and server modes omit it | Register it explicitly together with its console dependency |
| Database libraries | Supplied by `scriptling-full`, matching custom build tags, or discovered external database plugins | Register compiled plugins or load external plugins; see [Database availability](https://scriptling.dev/okf/scriptling-libraries/databases.md#availability) |
| `scriptling.package` | Present only when a non-nil app/plugin bundle loader is available, including ordinary CLI or server execution | Register it with a non-nil package loader |
| `scriptling.runtime.mcp` | Included wherever CLI setup registers the runtime aggregate, in ordinary CLI and server modes, unless disabled | `RegisterRuntimeLibraryAll(...)` includes it; `RegisterRuntimeMCPLibrary(p)` registers only this sub-library |

There is no universal extended-library `RegisterAll`. `stdlib.RegisterAll` covers only the standard libraries; CLI composition and plugin discovery are separate from the embedding API. See [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) for individual calls.

## Security and Capability Boundaries

Registration grants scripts the host process's authority for that surface. In particular:

- filesystem, subprocess, environment, secret, and provisioning libraries can read, write, execute, or disclose host data according to their configured restrictions;
- `requests` can use an embedding `netsecurity.Config` or the CLI network-policy file, but raw networking, messaging, Nomad, container, plugin, and some provisioning clients are separate surfaces and must not be assumed to inherit that HTTP policy;
- container and Nomad libraries can control available local runtimes or remote cluster workloads;
- runtime HTTP/JSON-RPC/MCP/plugin servers and messaging handlers create remotely reachable entry points; authentication and authorization remain the application's responsibility;
- plugin loading and package bundles add host-selected code and content, while provisioning can change files or fetch remote content.

Register only what a script needs, apply each library's own controls, and use OS/container egress and process isolation where a library has no matching in-process policy. See the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) and each library's security section for details.

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```
