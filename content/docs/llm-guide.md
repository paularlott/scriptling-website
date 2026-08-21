---
title: LLM Script Generation Guide
description: Guidance for generating accurate Scriptling code with LLMs — copy it into your agent's instructions or fetch the hosted docs.
tags: [docs, llm, ai]
weight: 9
aliases:
  - /docs/llm-guide/
---

This page is the source of truth for generating Scriptling code with LLMs. There are two ways to put it in front of your agent:

1. **Fetch the docs directly.** The full documentation is published as OKF 0.2 knowledge bundles that any markdown-reading agent can pull over HTTP — see [Fetching the Docs](#fetching-the-docs) below.
2. **Copy the guidance into your agent's instructions.** The block below is self-contained: paste it into your `AGENTS.md`, `CLAUDE.md`, or system prompt as-is.

## AGENTS.md Block

Copy everything inside the fence into your agent instructions:

````markdown
# Scriptling Script Generation

Scriptling is a sandboxed, Python-like scripting language for Go applications. Generate normal, readable Python 3 style code unless a Scriptling-specific limitation applies. Use `.py` files, 4-space indentation, `True`/`False`, `None`, `def`, `class`, `try`/`except`, comprehensions, and normal Python control flow.

## Write Scriptling Like This

- Prefer clear Pythonic code over custom conventions.
- Use `import json`, `import math`, `import re`, `import time`, and similar module imports.
- Use normal methods such as `d.items()`, `d.keys()`, `d.values()`, `s.split()`, `"x".join(parts)`, and `response.json()`.
- Use keyword arguments naturally: `requests.get(url, timeout=10, headers={...})`.
- Use `f"..."`, `.format()`, list/dict/set comprehensions, and generator expressions.
- Use `for key, value in data.items():` for dictionary iteration.
- Use `super().__init__(...)` in subclasses.
- Use `match` / `case` when it makes the code simpler.

## Supported Language Features

- Functions with defaults, `*args`, `**kwargs`, and argument unpacking with `*` / `**`.
- Lambdas, closures, recursion, `assert`, and conditional expressions.
- Lists, dicts, tuples, sets, slicing, `del`, chained comparisons, and augmented assignment.
- Classes, single inheritance, `super()`, and common dunder methods.
- `try` / `except` / `else` / `finally`; `with` statements and context managers.
- `match` / `case`, including guards and structural matching for dicts and sequences.
- `__name__ == "__main__"` patterns.
- Builtins such as `len`, `str`, `int`, `float`, `bool`, `list`, `tuple`, `set`, `dict`, `range`, `enumerate`, `zip`, `map`, `filter`, `sorted`, `sum`, `min`, `max`, `isinstance`, and `issubclass`.

## Important Differences from Python

- No `async` / `await`.
- No `yield`-based generator functions.
- No type annotations.
- No walrus operator (`:=`).
- No multiple inheritance; no nested classes.
- No built-in `open()`, `eval()`, `exec()`, `globals()`, or `locals()`.
- Regex uses RE2 semantics: no backreferences, no lookaround.
- Booleans display as `True` / `False` (matching Python); machine formats such as `json.dumps` and query parameters stay lowercase.

Two differences matter a lot:

1. **Scriptling is sandboxed by design.** Filesystem, subprocess, network, and similar capabilities only exist if the host registers the relevant library.
2. **Fatal errors and catchable exceptions are different.** Use `try` / `except` for normal exceptions, but do not assume every runtime failure is catchable.

## Libraries

Standard libraries are always available. Extended libraries are available in the CLI by default but require registration when embedding in Go. Prefer standard libraries for general scripting; use `scriptling.*` libraries only when the task depends on host runtime features such as MCP, AI agents, HTTP routes, or networking. When unsure what a host provides, use `help("modules")` or `help("library_name")` from inside a script.

For the full `scriptling` and standard library API, see the markdown bundle: https://scriptling.dev/okf/scriptling-libraries/index.md

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

- `requests` supports keyword arguments such as `timeout`, `headers`, `params`, `auth`, and `json`.
- The default HTTP timeout is 5 seconds if none is provided.
- Response objects expose `status_code`, `text`, `body`, `headers`, and `url`; `body` and `text` are aliases.
- `response.json()` and `response.raise_for_status()` are supported.
- Send warnings and errors to stderr so stdout stays clean for the report: `import sys` then `sys.stderr.write("warning\n")` or `print("error", file=sys.stderr)`.

## Common Exceptions

- `IndexError` for out-of-range sequence access.
- `KeyError` for missing dictionary keys.
- `AttributeError` for missing attributes.
- `ValueError` for bad values.
- `TypeError` for invalid argument or operand types.
- `ImportError` for optional libraries or imported names that are not available.

Use normal `try` / `except` patterns.

## Deletion

Scriptling supports Python-style `del` in the common cases: `del items[2]`, `del items[1:5:2]`, `del data["name"]`, `del user.email`. Prefer `del` over manual reassignment when the goal is to remove an item, slice, key, or attribute.

## Generation Rules

1. Generate standard Python-like code first, then remove unsupported features.
2. Prefer builtins and standard libraries before Scriptling-specific modules.
3. Use dictionary methods like `.items()` and keyword arguments naturally.
4. Use `del` for list indexes, list slices, dict keys, and object attributes when removing data.
5. For HTTP, always set an explicit timeout and check or raise on status.
6. For JSON APIs, prefer `response.json()` or `json.loads(response.body)`.
7. For string accumulation in loops, prefer `"".join(parts)` over repeated concatenation.
8. Keep code synchronous, explicit, and small rather than clever.

## Safe Default Template

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

## Validation and Reference

- Validate generated scripts with the linter when available: `scriptling --lint script.py`.
- Inspect available libraries from inside a script with `help("modules")`, `help("builtins")`, or `help("library.function")`.
- Full documentation is published as fetchable markdown bundles. Each bundle's `index.md` lists its concepts; follow the relative links from there:
  - For every library's API, see the markdown bundle: https://scriptling.dev/okf/scriptling-libraries/index.md
  - For the language reference (syntax, types, operators, control flow), see the markdown bundle: https://scriptling.dev/okf/scriptling-reference/index.md
  - For guides (CLI, Go integration, security, tutorials), see the markdown bundle: https://scriptling.dev/okf/scriptling-docs/index.md
````

## Fetching the Docs

The complete documentation is published as [OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 0.2 bundles — plain markdown with YAML frontmatter and relative links — at stable URLs an agent can fetch directly:

| Bundle | Contents | URL |
|--------|----------|-----|
| `scriptling-libraries` | API reference for every library | `https://scriptling.dev/okf/scriptling-libraries/index.md` |
| `scriptling-reference` | Language reference: syntax, types, operators, control flow | `https://scriptling.dev/okf/scriptling-reference/index.md` |
| `scriptling-docs` | Guides: CLI, Go integration, security, tutorials | `https://scriptling.dev/okf/scriptling-docs/index.md` |

Each bundle's `index.md` lists its concepts; follow the relative links from there. To give an agent search as well as reads, serve the bundles through an MCP server instead — see the [Documentation MCP Server](/docs/quick-start/documentation-mcp/) guide.
