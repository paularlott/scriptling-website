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
| `yield from` and `generator.send()` | Generator functions with `yield` work, but delegation (`yield from iterable`) and `send(value)` are not supported; loop or iterate manually |
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
| `vars()` | `vars(obj)` works like `obj.__dict__`; `vars()` with no argument returns the module-level bindings |
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
| Exception hierarchy | Built-in types group as in Python: `BaseException`, `LookupError` and `ArithmeticError` are catchable parents, and the `OSError` family (`FileNotFoundError`, `FileExistsError`, ...) derives from `OSError` |
| Exception groups (Python 3.11+) | Not supported |
| `except*` syntax | Not supported |
| `raise X from Y` | Accepted and re-raises `X` as in Python, but the chain is not introspectable: there is no `__cause__`/`__context__` attribute and no chained traceback |
| Custom exception classes | Can inherit from a built-in exception type (`class MyError(Exception)`) and from other user exception classes; multiple inheritance does not apply |

### Other Differences

| Feature | Notes |
|---------|-------|
| Module `__all__` | Export lists are not used |
| `__future__` imports | Not applicable |
| `__next__` returning a `StopIteration()` *value* | Ends iteration without yielding it — only *raising* `StopIteration` signals end-of-iteration |
| Type annotations | Parsed and ignored, including `def f(a: int) -> str`, `x: int = 5`, and `self.n: int = 0`; there is no `__annotations__` and no runtime checking, and comma subscripts parse as tuple indexes (`dict[str, int]`) |
| `**kwargs` order | The `**kwargs` dict holds the names in alphabetical order, not call order (deterministic, but not Python's order) |
| Subclassing built-in containers | `class C(dict)`, `class C(list)`, `class C(OrderedDict)` and `class C(defaultdict)` are not supported (`Counter` can be subclassed) |
| `OrderedDict` | An ordinary insertion-ordered dict: `move_to_end()` and `popitem(last=False)` work, but they are also accepted on plain dicts, and it prints like a plain dict |
| `obj.__dict__` | A fresh dict view per access that writes through to the object; `obj.__dict__ = {...}` is an `AttributeError`, names are not mangled (`__x` stays `__x`), and `SomeClass.__dict__` is not available |
| Dicts from other formats | Dicts built from YAML, TOML, MessagePack and plugin results have their keys in sorted order (those formats give no key order); `json.loads()`, `requests` `.json()` and literals keep document/insertion order |
| Walrus in a comprehension | `y` in `[y for x in a if (y := f(x))]` binds inside the comprehension and does not leak to the enclosing scope, unlike Python (PEP 572); use the collected list instead |
| `type(x).__name__` | `type(x)` returns the type name directly as a string (`type(42)` is `"INTEGER"`, a custom class instance gives its class name), so there is no type object to hang `.__name__` on — use `type(x)` itself; a raised built-in exception reports the class it was raised as (`"ValueError"`) |
| Generator expressions | `(x for x in a)` syntax works but is evaluated eagerly into a list, not a lazy generator object; over an endless iterator such as `itertools.count()` it raises an error instead of hanging (`any(map(f, itertools.count()))` does terminate: `map`/`filter` and `any`/`all` pull lazily over them) |
| `\N{name}` string escapes | Not supported; use `\u` with the code point |
| Number methods | `bit_length()`, `bit_count()`, `is_integer()`, `hex()`, `fromhex()` and `as_integer_ratio()` work ([see Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md#number-methods)); other number attributes (`x.real`, `x.imag`, `(5).to_bytes()`) do not exist |
| `dir()` with no argument | Lists the builtin names, not the local scope |

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
