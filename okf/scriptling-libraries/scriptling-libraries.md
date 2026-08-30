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

## [Quick Reference: Library Cheat Sheet](https://scriptling.dev/okf/scriptling-libraries/cheat-sheet.md)

Scriptling provides 60+ libraries organized by capability.

## Libraries

- [Data Formats](https://scriptling.dev/okf/scriptling-libraries/./data-formats.md): JSON, YAML, TOML
- [Text Processing](https://scriptling.dev/okf/scriptling-libraries/./text-processing.md): Regex, strings, HTML, diffing
- [Math & Numbers](https://scriptling.dev/okf/scriptling-libraries/./math-numbers.md): Math, random, statistics, hashing, UUID
- [Collections & Iteration](https://scriptling.dev/okf/scriptling-libraries/./collections-iteration.md): Collections, itertools, functools
- [Time & System](https://scriptling.dev/okf/scriptling-libraries/./time-system.md): Time, datetime, I/O, platform, URL handling
- [File System](https://scriptling.dev/okf/scriptling-libraries/./filesystem.md): OS, paths, binary I/O, glob
- [HTTP & Process](https://scriptling.dev/okf/scriptling-libraries/./http-process.md): HTTP requests, subprocesses, system, logging, secrets
- [Scriptling Libraries](https://scriptling.dev/okf/scriptling-libraries/./scriptling.md): AI, MCP, messaging, networking, runtime, utilities

## Registration

Every library is available by default in the CLI and MCP server, no setup needed there.

When embedding in Go, you register libraries explicitly. Each library page is marked **Standard library** or **Extended library**:

- **Standard libraries** (the 23 libraries also documented under [Data Formats](https://scriptling.dev/okf/scriptling-libraries/./data-formats.md), [Text Processing](https://scriptling.dev/okf/scriptling-libraries/./text-processing.md), [Math & Numbers](https://scriptling.dev/okf/scriptling-libraries/./math-numbers.md), [Collections & Iteration](https://scriptling.dev/okf/scriptling-libraries/./collections-iteration.md), and [Time & System](https://scriptling.dev/okf/scriptling-libraries/./time-system.md)) are all registered together with `stdlib.RegisterAll(p)`.
- **Extended libraries** (everything under [File System](https://scriptling.dev/okf/scriptling-libraries/./filesystem.md), [HTTP & Process](https://scriptling.dev/okf/scriptling-libraries/./http-process.md), and [Scriptling Libraries](https://scriptling.dev/okf/scriptling-libraries/./scriptling.md)) must be registered individually, and some take extra arguments such as `allowedPaths` to restrict filesystem access.

See [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) for the full list of registration calls, and the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) for which libraries carry filesystem, network, process, or secrets risk.

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```
