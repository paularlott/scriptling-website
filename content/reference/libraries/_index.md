---
title: Libraries
description: Available libraries and APIs in Scriptling.
tags: [libraries]
weight: 11

aliases:
  - /reference/libraries/scriptling/
---

Scriptling provides 90+ libraries organized by capability. Availability depends on the binary, execution mode, and host registration; it is not safe to assume every library is present.

Know the import name? Jump to the [A–Z list of every library](#all-libraries-az).

## Python-Style Libraries

Modules that mirror Python's standard library, grouped by subject:

- [Data Formats](data-formats/): json, yaml, toml, msgpack, bytes
- [Text Processing](text-processing/): re, string, html, html.parser, difflib, shlex, textwrap, io
- [Math & Numbers](math-numbers/): math, random, statistics, base64, hashlib, hmac, uuid, secrets
- [Collections & Iteration](collections-iteration/): collections, itertools, functools, contextlib
- [Time & System](time-system/): time, datetime, platform, sys, logging
- [File System](filesystem/): os, os.path, pathlib, glob, fs, shutil, tempfile, tarfile, zipfile
- [HTTP & Process](http-process/): requests, urllib.parse, subprocess

The *standard* set (json, re, time, datetime, math, random, statistics, base64, hashlib, hmac, uuid, string, html, textwrap, difflib, io, platform, urllib.parse, collections, itertools, functools, contextlib, msgpack) has no access to the host and is registered together by `stdlib.RegisterAll`. The rest are *extended* libraries, registered one by one because they reach the file system, network, processes or host: see [Availability](#availability).

## Scriptling Libraries

The `scriptling.*` libraries provide functionality beyond Python's standard library:

- [AI](ai/): LLM clients, agents, memory, tool schemas
- [Databases](databases/): SQLite, SQL, Valkey, BadgerDB, and the ORM
- [MCP](mcp/): MCP clients and tool authoring
- [Messaging](messaging/): Telegram, Discord, Slack, console
- [Networking](networking/): Gossip, multicast, unicast, DNS, WebSocket
- [Packages](package/): Read files and metadata from loaded app/plugin bundles
- [Plugins](plugin/): Control library for executable plugins
- [Provisioning](provisioning/): File and fetch provisioning
- [Runtime](runtime/): Background tasks, HTTP, JSON-RPC, MCP, KV, sync, sandbox
- [Templates](template/): Go-powered HTML and text templates
- [Utilities](utilities/): Console, containers, Nomad, grep, find, CSV, XML, secrets, and more

## All Libraries A–Z {#all-libraries-az}

Every library by the name you import it as. Use the [cheat sheet](cheat-sheet/) for quick examples of the common ones.

{{< library-index >}}

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
