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

## [Quick Reference: Library Cheat Sheet](cheat-sheet.md)

Scriptling provides 60+ libraries organized by capability.

## Libraries

- [Data Formats](data-formats.md): JSON, YAML, TOML
- [Text Processing](text-processing.md): Regex, strings, HTML, diffing
- [Math & Numbers](math-numbers.md): Math, random, statistics, hashing, UUID
- [Collections & Iteration](collections-iteration.md): Collections, itertools, functools
- [Time & System](time-system.md): Time, datetime, I/O, platform, URL handling
- [File System](filesystem.md): OS, paths, binary I/O, glob
- [HTTP & Process](http-process.md): HTTP requests, subprocesses, system, logging, secrets
- [Scriptling Libraries](scriptling.md): AI, MCP, messaging, networking, runtime, utilities

## Registration

Every library is available by default in the CLI and MCP server, no setup needed there.

When embedding in Go, you register libraries explicitly. Each library page is marked **Standard library** or **Extended library**:

- **Standard libraries** (the 23 libraries also documented under [Data Formats](data-formats.md), [Text Processing](text-processing.md), [Math & Numbers](math-numbers.md), [Collections & Iteration](collections-iteration.md), and [Time & System](time-system.md)) are all registered together with `stdlib.RegisterAll(p)`.
- **Extended libraries** (everything under [File System](filesystem.md), [HTTP & Process](http-process.md), and [Scriptling Libraries](scriptling.md)) must be registered individually, and some take extra arguments such as `allowedPaths` to restrict filesystem access.

See [Library Registration](../scriptling-docs/go-integration/library-registration.md) for the full list of registration calls, and the [Security Guide](../scriptling-docs/security.md) for which libraries carry filesystem, network, process, or secrets risk.

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```
