---
description: What's NOT supported and key differences between Scriptling and Python.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/python-differences/
sources:
    - resource: https://scriptling.dev/reference/python-differences/
status: stable
tags:
    - reference
    - python
title: Python Differences
type: Reference
---
# Python Differences

Scriptling is inspired by Python but has intentional limitations for embedded scripting. This page documents what's NOT supported and key differences.

## Python Features NOT Supported

### Language Features

| Feature | Notes |
|---------|-------|
| `async`/`await` | Not supported; use [`runtime.background()`](https://scriptling.dev/okf/scriptling-libraries/runtime/runtime.md) for concurrency |
| Generators with `yield` | Generator functions are not supported |
| Multiple inheritance | Only single inheritance is supported |
| Metaclasses | Custom metaclasses are not supported |
| Descriptors | The descriptor protocol is not implemented: a `__get__` method is never invoked, attribute access returns the object itself |
| Regex backreferences (`\1`, `\2`) | RE2 engine used; no backreferences, lookaheads, or lookbehinds: see [regex docs](https://scriptling.dev/okf/scriptling-libraries/text-processing/regex.md) |

### Built-in Functions NOT Supported

| Function | Alternative |
|----------|-------------|
| `input()` | Only registered when a stdin reader is attached (CLI scripts); absent in embedded and server evaluators — see [sys](https://scriptling.dev/okf/scriptling-libraries/time-system/sys.md) |
| `open()` | Use `os.read_file()` and `os.write_file()` |
| `compile()`, `eval()`, `exec()` | Dynamic code execution not supported |
| `globals()`, `locals()` | Scope introspection not available |
| `vars()` | Variable introspection not supported |
| `__import__()` | Use `import` statement |
| `memoryview()`, `bytearray()` | Advanced byte manipulation not supported; `bytes()` and `b"..."` literals work |
| `complex()` | Complex numbers not implemented |

### Standard Library NOT Included

| Module | Notes |
|--------|-------|
| `asyncio` | Use [`runtime.background()`](https://scriptling.dev/okf/scriptling-libraries/runtime/runtime.md) for concurrency |
| `threading`, `multiprocessing` | Use `runtime.background`: `shared=True` for shared-env threads, default for isolated parallel workers |
| `socket` | Low-level networking; use `requests` for HTTP |
| `pickle`, `marshal` | Use `json` for serialization |
| `struct` | Binary data structures |
| `array` | Typed arrays |
| `ctypes`, `cffi` | Foreign function interfaces |
| `sqlite3` | Database access |
| `xml` | Use `html.parser` for HTML |
| `email`, `smtplib` | Email handling |
| `argparse`, `optparse` | Command-line parsing |
| `unittest`, `doctest` | Use `assert` statements |
| `pdb` | Debugger |
| `profile`, `cProfile` | Profiling tools |

### Exception Handling Differences

| Feature | Notes |
|---------|-------|
| Exception hierarchy | Built-in types only: `BaseException`, `Exception`, `LookupError` and `ArithmeticError` group the common errors, but there is no `OSError` subtree such as `FileNotFoundError` |
| Exception groups (Python 3.11+) | Not supported |
| `except*` syntax | Not supported |
| `raise X from Y` | Exception chaining not supported; use `raise ExcType(msg)` directly |
| Custom exception classes | Cannot inherit from built-in exception types |

### Other Differences

| Feature | Notes |
|---------|-------|
| Module `__all__` | Export lists are not used |
| `__future__` imports | Not applicable |
| `__next__` returning a `StopIteration()` *value* | Ends iteration without yielding it — only *raising* `StopIteration` signals end-of-iteration |
| Default argument evaluation | Defaults are evaluated on each call (Python evaluates once, at `def` time) |
| Type annotations | Parsed and ignored, including `def f(a: int) -> str`, `x: int = 5`, and `self.n: int = 0`; there is no `__annotations__` and no runtime checking, and comma subscripts parse as tuple indexes (`dict[str, int]`) |
| Dict iteration order | Unspecified and not reproducible run to run (unlike Python 3.7+): `for k in d`, `keys()`/`values()`/`items()`, and printing a dict may come out in any order. Lookups, equality, and `json.dumps` are unaffected (dumps sorts keys). Sort explicitly (`sorted(d)`) when order matters. Because two walks of one dict can differ, `zip()` and `map()` refuse two dicts or dict views at once (`zip(d.keys(), d.values())` is a `TypeError`); use `d.items()` |
| Walrus in a comprehension | `y` in `[y for x in a if (y := f(x))]` binds inside the comprehension and does not leak to the enclosing scope, unlike Python (PEP 572); use the collected list instead |
| `type(x).__name__` | `type(x)` returns the type name directly as a string (`type(42)` is `"INTEGER"`, a custom class instance gives its class name), so there is no type object to hang `.__name__` on — use `type(x)` itself; a raised built-in exception reports the class it was raised as (`"ValueError"`) |
| Generator expressions | `(x for x in a)` syntax works but is evaluated eagerly into a list, not a lazy generator object; over an endless iterator such as `itertools.count()` it raises an error instead of hanging (`any(map(f, itertools.count()))` does terminate: `map`/`filter` and `any`/`all` pull lazily over them) |
| `\N{name}` string escapes | Not supported; use `\u` with the code point |
| Number methods | `bit_length()`, `bit_count()`, `is_integer()`, `hex()`, `fromhex()` and `as_integer_ratio()` work ([see Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md#number-methods)); other number attributes (`x.real`, `x.imag`, `(5).to_bytes()`) do not exist |
| `dir()` with no argument | Lists the builtin names, not the local scope |
| `json.dumps()` output | Compact with sorted keys: `json.dumps({"b": 1, "a": [1, 2]})` gives `{"a":[1,2],"b":1}` (Python gives `{"b": 1, "a": [1, 2]}`) |

Everything not listed on this page behaves as in Python 3; see the [Language Guide](https://scriptling.dev/okf/scriptling-reference/scriptling-reference.md).

## Key Behavioral Differences

### Library Import

Imports work as in Python, but a library is only importable if the host has made it available. The CLI provides the standard and extended libraries; an embedding Go program registers the ones it wants.

`from module import *` is not supported. Python 3.15's `lazy import` is accepted but imports immediately. See [Imports](https://scriptling.dev/okf/scriptling-reference/syntax.md#imports).

### Default Timeout

`requests` calls time out after 5 seconds by default (Python's `requests` waits indefinitely). Pass `timeout=` for slower endpoints:

```python
response = requests.get("https://slow-api.com", timeout=30)
```

### File System Access

There is no built-in `open()`; files are read and written through libraries such as `os` (`os.read_file()`, `os.write_file()`) and `pathlib`. Whether those libraries exist, and what they can reach, depends on the host: a bare embedded interpreter has no filesystem libraries unless the Go host registers them with allowed paths, while the `scriptling` CLI registers them with full filesystem access unless `--allowed-paths` restricts it. See the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md#file-system-security).

```python
import os
content = os.read_file("data.txt")   # instead of open("data.txt").read()
```

### Errors and Exceptions Are Catchable, Except SystemExit

`try`/`except` catches interpreter errors (with the exception type inferred from the message, so `except NameError:` works) and explicitly raised exceptions. `SystemExit` (from `sys.exit()`) is different from Python: no `except` clause can catch it; `finally` blocks run and the exit returns to the Go host. See [Error Handling](https://scriptling.dev/okf/scriptling-reference/error-handling.md#systemexit-exception).

## See Also

- [Syntax Rules](https://scriptling.dev/okf/scriptling-reference/syntax.md) - Scriptling syntax
- [Functions](https://scriptling.dev/okf/scriptling-reference/functions.md) - Function parameters
- [Error Handling](https://scriptling.dev/okf/scriptling-reference/error-handling.md) - try/except, raise, and SystemExit
- [Classes](https://scriptling.dev/okf/scriptling-reference/classes.md) - Class limitations
