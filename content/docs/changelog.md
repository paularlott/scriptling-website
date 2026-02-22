---
title: Changelog
description: Scriptling release history and changes.
layout: changelog
nav-skip: true
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
