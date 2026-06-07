---
title: Libraries
description: Available libraries and APIs in Scriptling.
weight: 10
---

## [Quick Reference: Library Cheat Sheet](/reference/libraries/cheat-sheet/)

Scriptling provides 60+ libraries organized by capability.

## Libraries

- [Data Formats](data-formats/) — JSON, YAML, TOML
- [Text Processing](text-processing/) — Regex, strings, HTML, diffing
- [Math & Numbers](math-numbers/) — Math, random, statistics, hashing, UUID
- [Collections & Iteration](collections-iteration/) — Collections, itertools, functools
- [Time & System](time-system/) — Time, datetime, I/O, platform, URL handling
- [File System](filesystem/) — OS, paths, binary I/O, glob
- [HTTP & Process](http-process/) — HTTP requests, subprocesses, system, logging, secrets
- [Scriptling Libraries](scriptling/) — AI, MCP, messaging, networking, runtime, utilities

> File System, HTTP & Process, and Scriptling libraries require [registration](/docs/go-integration/library-registration/) when embedding in Go. In the CLI they are available by default.

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```
