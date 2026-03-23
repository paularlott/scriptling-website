---
title: Changelog
description: Scriptling release history and changes.
layout: changelog
nav-skip: true
---

## March 2026

{{< version "v0.4.0" >}}

{{< changelog-item "added" >}}
**Package System:**

- Packed library files — distribute Scriptling libraries as `.zip` packages with automatic download and caching
- `scriptling pack` command — create packages from directories with `# sha256=<hash>` integrity verification
- Package cache with ETag/Last-Modified validation and automatic pruning (7-day TTL)
- Documentation support in packages for `help` command integration

**Language:**

- Relative imports — `from .module import name` and `from ..package import name` for hierarchical module organization
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**CLI:**

- `help` command now works in TUI mode with topic lookup support
{{< /changelog-item >}}

---

{{< version "v0.3.2" >}}

{{< changelog-item "added" >}}
**Language:**

- Multiple `for` clauses in list, dict, set comprehensions and generator expressions (`[x for x in a for y in b]`)
- `__getitem__` and `__setitem__` dunder methods for custom bracket access (`obj[key]`) — dot access (`obj.attr`) no longer triggers `__getitem__`
- `__hash__` dunder method — instances that define `__hash__` can be used as dict keys and set elements; `hash()` builtin calls it
- Arithmetic dunder methods: `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__mod__`
- Set and dict entry points raise `TypeError` for unhashable types (lists, dicts, instances without `__hash__`), matching Python semantics
- Tuple `in`/`not in` operator
- Tuple slicing (`t[1:3]`, `t[::-1]`) returns a tuple
- Tuple `count()` and `index()` methods
{{< /changelog-item >}}

---

{{< version "v0.3.0" >}}

{{< changelog-item "added" >}}
**New messaging libraries:**

Platform-agnostic bot framework for building chat bots with a unified API:

- `scriptling.messaging.telegram` — Telegram Bot API client
- `scriptling.messaging.discord` — Discord Bot API client
- `scriptling.messaging.slack` — Slack Bot API client
- `scriptling.messaging.console` — Console-based messaging client for testing

All platforms share a common interface with:
- Command handlers (`/command` syntax)
- Button callbacks with keyboard support
- Message send/edit/delete operations
- File upload/download
- Typing indicators
- Rich message support (title, body, color, images)
- Authentication handlers for access control
{{< /changelog-item >}}

---

{{< version "v0.2.23" >}}

{{< changelog-item "added" >}}
**New standard libraries:**

- `scriptling.ai.memory` — Long-term memory store for AI agents with MinHash-based semantic search, memory types (fact, preference, event, note), importance scoring, decay, and optional LLM-powered compaction
- `scriptling.runtime.kv` — Persistent key-value store with TTL support, thread-safe operations, and both in-memory and file-backed storage

**Language:**

- Set comprehensions (`{x for x in iterable}`)
- `__file__` variable provides the current script's path

**AI API:**

- `Agent.interact()` gains `max_iterations` parameter to limit conversation turns
  {{< /changelog-item >}}

---

## February 2026

{{< version "v0.2.0" >}}

{{< changelog-item "added" >}}
**Language:**

- `with` statement and context managers
- Decorators (`@decorator`), `@property`, `@staticmethod`, and `@classmethod`
- Dunder methods: `__str__`, `__repr__`, `__len__`, `__bool__`, `__eq__`, `__lt__`, `__contains__`, `__iter__`
- Dict comprehensions (`{k: v for k, v in ...}`)
- Set literals (`{1, 2, 3}`)
- `for`/`while` `else` clauses
- `match` or-patterns
- `int()` now accepts a base argument for base conversion

**New built-in functions:**

- `next()`, `iter()`, `dir()`, `issubclass()`, `copy()`

**New standard libraries:**

- `io` — `StringIO` for in-memory I/O
- `contextlib` — `suppress` context manager
- `difflib` — LCS-based sequence comparison, unified diff, `get_close_matches`

**Go API:**

- `GetVarAsSet(name)` — typed getter for set variables
- `GetVarAsTuple(name)` — typed getter for tuple variables
- `EvalFile(path)` — read and evaluate a script file directly
- `ListVars()` — returns a sorted list of variable names in the current environment
- `UnsetVar(name)` — remove a variable from the environment
- `Clone()` — create an isolated interpreter that inherits library registrations but starts with a fresh environment
- `ClassBuilder` gains `Property`, `PropertyWithSetter`, and `StaticMethod` for registering Go-backed class members

**CLI / TUI:**

- Scripts that use `console.run()` now launch a full TUI automatically; no separate flag needed
- `console.set_labels()` lets scripts customise the user/assistant labels shown in the TUI
  {{< /changelog-item >}}

---

{{< version "v0.1.0" >}}

Initial pre-release of Scriptling.

**Features:**

- Python-like syntax with indentation-based blocks
- Core types: integers, floats, strings, booleans, lists, dictionaries, sets
- Control flow: if/elif/else, while, for loops, break, continue, match statements
- Object-oriented: Classes with single inheritance, methods, and constructors
- Functions, lambda, list comprehensions, error handling
- Background tasks with `scriptling.runtime` for concurrent execution
- 25+ built-in libraries including JSON, regex, math, HTTP requests, subprocess
- Go integration with direct type mapping
- AI/LLM integration with OpenAI-compatible API support
- MCP (Model Context Protocol) server and client
- HTTP server with route registration
- Sandboxed execution with configurable security
- CLI tool with interactive mode, HTTP/MCP server, and built-in linter
- Extensible: create custom functions, libraries, and classes in Go or Scriptling
- Cross-platform binaries for Linux, macOS, and Windows
