---
title: LLM Script Generation Guide
description: One-page guidance for generating accurate, Python-like Scriptling code.
weight: 7
---

Use this page as a compact reference for generating high-quality Scriptling scripts.

## Overview

Scriptling is **Python-like**, and the best default is to generate normal, readable Python 3 style code unless you know a Scriptling-specific limitation applies. Use `.py` files, 4-space indentation, `True`/`False`, `None`, `def`, `class`, `try`/`except`, comprehensions, and normal Python control flow.

## Write Scriptling Like This

- Prefer clear Pythonic code over custom conventions.
- Use `import json`, `import math`, `import re`, `import time`, and similar module imports.
- Use normal methods such as `d.items()`, `d.keys()`, `d.values()`, `s.split()`, `"x".join(parts)`, and `response.json()`.
- Use keyword arguments naturally: `requests.get(url, timeout=10, headers={...})`.
- Use `f"..."`, `.format()`, list/dict/set comprehensions, and generator expressions.
- Use `for key, value in data.items():` for dictionary iteration.
- Use `super().__init__(...)` or `super(ClassName, self).__init__(...)` in subclasses.
- Use `match` / `case` when it makes the code simpler.

## Supported Language Features

Scriptling supports the Python features LLMs most often need:

- Functions with defaults, `*args`, `**kwargs`, and argument unpacking with `*` / `**`.
- Lambdas, closures, recursion, `assert`, and conditional expressions.
- Lists, dicts, tuples, sets, slicing, `del`, chained comparisons, and augmented assignment.
- Classes, single inheritance, `super()`, and common dunder methods.
- `try` / `except` / `else` / `finally`.
- `with` statements and context managers.
- `match` / `case`, including guards and structural matching for dicts and sequences.
- `__name__ == "__main__"` patterns.
- Builtins such as `len`, `str`, `int`, `float`, `bool`, `list`, `tuple`, `set`, `dict`, `range`, `enumerate`, `zip`, `map`, `filter`, `sorted`, `sum`, `min`, `max`, `isinstance`, and `issubclass`.

## Important Differences from Python

Avoid these Python features because they are not supported or differ in Scriptling:

- No `async` / `await`.
- No `yield`-based generator functions.
- No type annotations.
- No walrus operator (`:=`).
- No multiple inheritance.
- No nested classes.
- No built-in `open()`, `eval()`, `exec()`, `globals()`, or `locals()`.
- Regex uses RE2 semantics, so backreferences and lookaround are not supported.

Do not generate those features unless the host application explicitly provides an alternative.

Two differences matter a lot when generating code:

1. **Scriptling is sandboxed by design.**
   Filesystem, subprocess, network, and similar capabilities only exist if the host registers the relevant library.
2. **Fatal errors and catchable exceptions are different.**
   Use `try` / `except` for normal exceptions, but do not assume every runtime failure is catchable.

## Libraries

### Standard Libraries

These are the main Python-style modules to reach for first:

| Import         | Typical use                   |
| -------------- | ----------------------------- |
| `json`         | JSON encode/decode            |
| `re`           | Regular expressions           |
| `math`         | Numeric functions             |
| `time`         | Timestamps, sleep, formatting |
| `datetime`     | Dates, datetimes, timedeltas  |
| `random`       | Random values                 |
| `statistics`   | Aggregations                  |
| `itertools`    | Iteration helpers             |
| `functools`    | `partial`, `reduce`           |
| `collections`  | Containers and counters       |
| `textwrap`     | Text formatting               |
| `hashlib`      | Hashing                       |
| `base64`       | Base64 encode/decode          |
| `uuid`         | UUID generation               |
| `urllib.parse` | URL parsing and encoding      |
| `html`         | HTML escaping                 |
| `io`           | String I/O utilities          |
| `difflib`      | Diffs and similarity          |
| `string`       | String constants and helpers  |
| `platform`     | Platform metadata             |
| `contextlib`   | Context manager helpers       |

### Extended / Host-Provided Libraries

These are powerful, but they may not exist unless the embedding app enables them:

| Import                                 | Typical use             |
| -------------------------------------- | ----------------------- |
| `requests`                             | HTTP client             |
| `os`, `os.path`, `pathlib`, `glob`     | Filesystem access       |
| `subprocess`                           | Process execution       |
| `logging`                              | Structured logs         |
| `yaml`, `toml`                         | Config parsing          |
| `html.parser`                          | HTML parsing            |
| `sys`                                  | Runtime info            |
| `scriptling.mcp`                       | MCP tools and responses |
| `scriptling.ai`, `scriptling.ai.agent` | AI integration          |
| `scriptling.net.websocket`             | WebSockets              |
| `scriptling.similarity`                | Similarity search       |

If a script depends on one of these modules, import it explicitly and assume it may be unavailable in some hosts. This matters most for `requests`, `os`, `os.path`, `pathlib`, `subprocess`, `yaml`, `toml`, and the `scriptling.*` libraries.

### Scriptling-Specific Libraries

Use these when the task is specific to a Scriptling host environment rather than general Python-like scripting:

Prefer standard libraries for general scripting; use `scriptling.*` only when the task depends on host runtime features such as MCP, AI agents, HTTP routes, KV storage, sync primitives, or WebSockets.

| Import | Typical use |
|--------|-------------|
| `scriptling.mcp` | Build MCP tools and return structured MCP results |
| `scriptling.ai` | Call AI models and work with AI responses |
| `scriptling.ai.agent` | Run agent-style workflows with tools and memory |
| `scriptling.ai.agent.interact` | Interactive agent loops |
| `scriptling.runtime.http` | Register HTTP routes and handlers in hosted runtimes |
| `scriptling.runtime.kv` | Key-value storage |
| `scriptling.runtime.sync` | Atomics, queues, wait groups, and shared state |
| `scriptling.runtime.sandbox` | Runtime sandbox helpers |
| `scriptling.net.websocket` | WebSocket connections |
| `scriptling.similarity` | Fuzzy matching, ranking, and similarity search |
| `scriptling.toon` | Toon encoding and decoding |

Do not assume every `scriptling.*` library is available in every host.

## HTTP and JSON

When generating API code, prefer this pattern:

```python
import json
import requests

response = requests.get(
    "https://api.example.com/items",
    timeout=10,
    headers={"Authorization": "Bearer " + token},
)

response.raise_for_status()
data = response.json()

for item in data:
    print(item["name"])
```

Key points:

- `requests` supports keyword arguments such as `timeout`, `headers`, `params`, `auth`, and `json`.
- The default HTTP timeout is **5 seconds** if none is provided.
- Response objects expose `status_code`, `text`, `body`, `headers`, and `url`.
- `response.json()` and `response.raise_for_status()` are supported.
- `body` and `text` are aliases; either is acceptable.

## Common Exceptions

These are the most useful exception types to generate in normal scripts:

- `IndexError` for out-of-range sequence access.
- `KeyError` for missing dictionary keys.
- `AttributeError` for missing attributes.
- `ValueError` for bad values.
- `TypeError` for invalid argument or operand types.

Use normal `try` / `except` patterns:

```python
try:
    value = data["name"]
except KeyError:
    value = "unknown"
```

## Deletion

Scriptling supports Python-style `del` in the common cases:

```python
del items[2]
del items[1:5:2]
del data["name"]
del user.email
```

Prefer `del` over manual reassignment when the goal is to remove an item, slice, key, or attribute.

## Generation Rules for LLMs

When unsure, these defaults produce the best Scriptling:

1. Generate standard Python-like code first, then remove unsupported features.
2. Prefer builtins and standard libraries before Scriptling-specific modules.
3. Use dictionary methods like `.items()` and keyword arguments naturally.
4. Use `del` for list indexes, list slices, dict keys, and object attributes when removing data.
5. For HTTP, always set an explicit timeout and check or raise on status.
6. For JSON APIs, prefer `response.json()` or `json.loads(response.body)`.
7. For string accumulation in loops, prefer `"".join(parts)` over repeated concatenation.
8. Keep code synchronous, explicit, and small rather than clever.

## Safe Default Template

Use this shape when generating a general-purpose Scriptling script:

```python
import json
import requests

def main():
    response = requests.get(
        "https://api.example.com/items",
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    for item in data:
        print(item["name"])

if __name__ == "__main__":
    main()
```

If the script uses host-provided libraries, keep imports explicit and write the code so missing libraries fail clearly.

## Validation

Validate generated scripts with the Scriptling linter when possible:

```bash
scriptling --lint script.py
```

Use linting as a fast syntax and feature check before running generated code.

## Built-In Help

Scriptling provides an internal help system that can inspect builtins, libraries, and functions from inside a script:

```python
import scriptling.mcp

help(scriptling.mcp)
help("builtins")
help("scriptling.mcp")
```

Use `help()` when the host may expose additional libraries or functions beyond the common cases listed on this page.
