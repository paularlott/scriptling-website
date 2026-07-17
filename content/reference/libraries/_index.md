---
title: Libraries
description: Available libraries and APIs in Scriptling.
tags: [libraries]
weight: 10
---

## [Quick Reference: Library Cheat Sheet](/reference/libraries/cheat-sheet/)

Scriptling provides 60+ libraries organized by capability.

## Libraries

- [Data Formats](data-formats/): JSON, YAML, TOML
- [Text Processing](text-processing/): Regex, strings, HTML, diffing
- [Math & Numbers](math-numbers/): Math, random, statistics, hashing, UUID
- [Collections & Iteration](collections-iteration/): Collections, itertools, functools
- [Time & System](time-system/): Time, datetime, I/O, platform, URL handling
- [File System](filesystem/): OS, paths, binary I/O, glob
- [HTTP & Process](http-process/): HTTP requests, subprocesses, system, logging, secrets
- [Scriptling Libraries](scriptling/): AI, MCP, messaging, networking, runtime, utilities

## Registration

Every library is available by default in the CLI and MCP server, no setup needed there.

When embedding in Go, you register libraries explicitly. Each library page is marked **Standard library** or **Extended library**:

- **Standard libraries** (the 23 libraries also documented under [Data Formats](data-formats/), [Text Processing](text-processing/), [Math & Numbers](math-numbers/), [Collections & Iteration](collections-iteration/), and [Time & System](time-system/)) are all registered together with `stdlib.RegisterAll(p)`.
- **Extended libraries** (everything under [File System](filesystem/), [HTTP & Process](http-process/), and [Scriptling Libraries](scriptling/)) must be registered individually, and some take extra arguments such as `allowedPaths` to restrict filesystem access.

See [Library Registration](/docs/go-integration/library-registration/) for the full list of registration calls, and the [Security Guide](/docs/security/) for which libraries carry filesystem, network, process, or secrets risk.

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```
