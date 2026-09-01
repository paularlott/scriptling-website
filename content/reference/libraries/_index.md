---
title: Libraries
description: Available libraries and APIs in Scriptling.
tags: [libraries]
weight: 11

aliases:
  - /reference/libraries/scriptling/
---

Scriptling provides 60+ libraries organized by capability. Availability depends on the binary, execution mode, and host registration; it is not safe to assume every library is present.

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

The `scriptling.*` libraries provide functionality beyond Python's standard library:

- [AI](ai/): LLM clients, agents, memory, tool schemas
- [Databases](databases/): SQLite, SQL, Valkey, BadgerDB, and the ORM
- [MCP](mcp/): MCP clients and tool authoring
- [Messaging](messaging/): Telegram, Discord, Slack, console
- [Networking](networking/): Gossip, multicast, unicast, DNS, WebSocket
- [Package](package/): Read files and metadata from loaded app/plugin bundles
- [Plugin](plugin/): Control library for executable plugins
- [Provisioning](provisioning/): File and fetch provisioning
- [Runtime](runtime/): Background tasks, HTTP, JSON-RPC, MCP, KV, sync, sandbox
- [Template](template/): Go-powered HTML and text templates
- [Utilities](utilities/): Console, containers, Nomad, grep, find, CSV, XML, secrets, and more

## Availability

A bare `scriptling.New()` environment has no libraries; embedders register every capability they intend to expose. The default CLI setup composes a broader set, subject to execution mode and disable flags.

| Library group | Default CLI and server setup | Bare embedding |
|---------------|------------------------------|----------------|
| Standard libraries | Registered together | `stdlib.RegisterAll(p)` |
| Core extended and `scriptling.*` libraries | Registered unless disabled; the exact set varies by mode | Register each required library explicitly |
| `scriptling.ai.tools` | The standalone namespace is not registered by normal setup; use `scriptling.ai.ToolRegistry` when `scriptling.ai` is present | Register the standalone tools library explicitly if needed |
| `scriptling.ai.agent.interact` | Added on the ordinary non-server CLI execution path; evaluator factories and server modes omit it | Register it explicitly together with its console dependency |
| Database libraries | Compiled into the default `scriptling` build, matching custom build tags, or discovered external database plugins | Register compiled plugins or load external plugins; see [Database availability](databases/#availability) |
| `scriptling.package` | Present only when a non-nil app/plugin bundle loader is available, including ordinary CLI or server execution | Register it with a non-nil package loader |
| `scriptling.runtime.mcp` | Included wherever CLI setup registers the runtime aggregate, in ordinary CLI and server modes, unless disabled | `RegisterRuntimeLibraryAll(...)` includes it; `RegisterRuntimeMCPLibrary(p)` registers only this sub-library |

There is no universal extended-library `RegisterAll`. `stdlib.RegisterAll` covers only the standard libraries; CLI composition and plugin discovery are separate from the embedding API. See [Library Registration](/docs/go-integration/library-registration/) for individual calls.

## Security and Capability Boundaries

Registration grants scripts the host process's authority for that surface. In particular:

- filesystem, subprocess, environment, secret, and provisioning libraries can read, write, execute, or disclose host data according to their configured restrictions;
- `requests` can use an embedding `netsecurity.Config` or the CLI network-policy file, but raw networking, messaging, Nomad, container, plugin, and some provisioning clients are separate surfaces and must not be assumed to inherit that HTTP policy;
- container and Nomad libraries can control available local runtimes or remote cluster workloads;
- runtime HTTP/JSON-RPC/MCP/plugin servers and messaging handlers create remotely reachable entry points; authentication and authorization remain the application's responsibility;
- plugin loading and package bundles add host-selected code and content, while provisioning can change files or fetch remote content.

Register only what a script needs, apply each library's own controls, and use OS/container egress and process isolation where a library has no matching in-process policy. See the [Security Guide](/docs/security/) and each library's security section for details.

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```
