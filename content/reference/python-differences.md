---
title: Python Differences
description: What's NOT supported and key differences between Scriptling and Python.
tags: [reference, python]
weight: 12
---

Scriptling is inspired by Python but has intentional limitations for embedded scripting. This page documents what's NOT supported and key differences.

## Python Features NOT Supported

### Language Features

| Feature | Notes |
|---------|-------|
| `async`/`await` | Asynchronous programming is not supported |
| Generators with `yield` | Generator functions are not supported |
| Positional-only separator (`/`) | Rejected with a parse error; bare `*` keyword-only parameters are supported |
| Multiple inheritance | Only single inheritance is supported |
| Metaclasses | Custom metaclasses are not supported |
| Descriptors | The descriptor protocol is not implemented: a `__get__` method is never invoked, attribute access returns the object itself |
| Regex backreferences (`\1`, `\2`) | RE2 engine used; no backreferences, lookaheads, or lookbehinds: see [regex docs](../../reference/libraries/text-processing/regex/) |

### Built-in Functions NOT Supported

| Function | Alternative |
|----------|-------------|
| `input()` | Only registered when a stdin reader is attached (CLI scripts); absent in embedded and server evaluators — see [sys](../libraries/http-process/sys/) |
| `open()` | Use `os.read_file()` and `os.write_file()` |
| `compile()`, `eval()`, `exec()` | Dynamic code execution not supported |
| `globals()`, `locals()` | Scope introspection not available |
| `vars()` | Variable introspection not supported |
| `__import__()` | Use `import` statement |
| `memoryview()`, `bytearray()` | Advanced byte manipulation not supported; `bytes()` and `b"..."` literals work |
| `complex()` | Complex numbers not implemented |
| `frozenset()` | Use regular `set()` |

### Standard Library NOT Included

| Module | Notes |
|--------|-------|
| `asyncio` | Async I/O framework |
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
| Exception hierarchy | Simplified error model |
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
| Dict iteration order | Unspecified and not reproducible run to run (unlike Python 3.7+): `for k in d`, `keys()`/`values()`/`items()`, and printing a dict may come out in any order. Lookups, equality, and `json.dumps` are unaffected (dumps sorts keys). Sort explicitly (`sorted(d)`) when order matters |
| Walrus in a comprehension | `y` in `[y for x in a if (y := f(x))]` binds inside the comprehension and does not leak to the enclosing scope, unlike Python (PEP 572); use the collected list instead |
| `type(x).__name__` | `type(x)` returns the type name directly as a string (`type(42)` is `"INTEGER"`, a custom class instance gives its class name), so there is no type object to hang `.__name__` on — use `type(x)` itself; a raised built-in exception reports the class it was raised as (`"ValueError"`) |
| Lazy iteration | `any`/`all`/`sorted`/`min`/`max`/`map`/`filter` materialize their iterable eagerly; `any([True, boom()])` raises where Python short-circuits |

## Supported Python 3 Features

Scriptling **does support**:

- ✅ Classes with single inheritance and `super()`
- ✅ Nested classes (a class defined inside a function or another class)
- ✅ Dunder methods: `__str__`, `__repr__`, `__len__`, `__bool__`, `__eq__`, `__lt__`, `__gt__`, `__le__`, `__ge__`, `__ne__`, `__contains__`, `__iter__`, `__next__`, `__enter__`, `__exit__`
- ✅ Dunders honored everywhere: container membership/lookup use `__eq__`/`__hash__`, and comparisons reflect (`b.__gt__(a)` when `a` defines no `__lt__`)
- ✅ Lambda functions and closures
- ✅ List comprehensions, dict comprehensions, and set comprehensions
- ✅ Generator-expression syntax, evaluated eagerly and materialized rather than returned as a lazy generator object
- ✅ Multiple `for` clauses in comprehensions (`[x for x in a for y in b]`)
- ✅ Iterators (`range`, `map`, `filter`, `enumerate`, `zip`)
- ✅ Dictionary views (`keys()`, `values()`, `items()`)
- ✅ F-strings and `.format()`
- ✅ True division (`/` always returns float)
- ✅ Python number semantics: `//` floors toward negative infinity, `%` takes the divisor's sign (ints and floats), `round()` ties go to the even digit, `divmod()` agrees, and `sorted()` / `.sort()` are stable
- ✅ Set literals `{1, 2, 3}` and set operations
- ✅ Set hashability: `TypeError` raised for unhashable types (lists, dicts, sets, instances without `__hash__`) matching Python semantics
- ✅ Bool arithmetic: `True + True == 2`, `True == 1`, `False == 0`
- ✅ String comparison operators (`<`, `>`, `<=`, `>=`)
- ✅ Implicit tuple packing (`x = 1, 2`, `return a, b`, `t = 42,`)
- ✅ Chained assignment (`a = b = 5`)
- ✅ Try/except/else/finally error handling
- ✅ Multiple assignment and tuple unpacking
- ✅ Extended unpacking with `*`
- ✅ Variadic arguments (`*args`)
- ✅ Keyword-only parameters with bare `*`
- ✅ Keyword arguments (`**kwargs`)
- ✅ Default parameter values
- ✅ Conditional expressions (ternary operator)
- ✅ Walrus assignment expressions (`while (chunk := read()):`)
- ✅ Type annotations (`def f(a: int) -> str`, `count: int = 5`) parsed and ignored
- ✅ The `...` (Ellipsis) placeholder, including `def f(): ...` stub bodies
- ✅ Dict merge operators: `d1 | d2` builds a new dict (right wins), `d |= other` merges in place
- ✅ Augmented assignment (`+=`, `-=`, `**=`, etc.)
- ✅ Slice notation with step (`[start:stop:step]`)
- ✅ Slice assignment (`l[1:4] = [...]`, stepped and reversed forms)
- ✅ Python float repr: `str(2.0)` is `"2.0"`, `str(123456789.123)` is positional, scientific outside `1e-4`–`1e16`, in `json.dumps` too
- ✅ `str.rsplit` with `maxsplit`
- ✅ Callable instances (`__call__`), sequence ordering (`[1] < [2]`, tuples element-wise), `str.encode()` returning bytes, and `math.isclose`
- ✅ Python-shaped errors for the common cases: `unsupported operand type(s) for +: 'int' and 'str'`, `name 'x' is not defined`, quoted `KeyError` messages
- ✅ Python-style `repr` for strings (single quotes, escapes) across `repr()`, `%r`, `!r` and `f"{x=}"`
- ✅ `%`-formatting string width/precision/flags, the `f"{x=}"` debug specifier, numeric underscores (`1_000`), `del a, b`, `len(range(n))`, and `splitlines(keepends=True)`
- ✅ `startswith`/`endswith` with tuples and `start`/`end` offsets, `replace` with a count, and `b"..."` bytes literals
- ✅ `del` for variables, list indexes, list slices, dict keys, and attributes
- ✅ `is` and `is not` operators
- ✅ `in` and `not in` operators
- ✅ Bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`)
- ✅ Boolean operators with short-circuit evaluation
- ✅ Assert statements (`assert condition, "message"`)
- ✅ Context managers (`with` / `as`, `__enter__` / `__exit__`)
- ✅ String methods (most Python string methods)
- ✅ List, dict, set methods (most Python methods)
- ✅ `@property`, `@staticmethod`, `@classmethod` decorators
- ✅ `for/else` and `while/else`
- ✅ `match`/`case` with OR patterns (`case 1 | 2 | 3:`)
- ✅ `__name__` variable with `"__main__"` for main scripts and module name for imports

## Key Behavioral Differences

### HTTP Response Object

Python `requests` returns attributes, Scriptling returns an object:

```python
# Python
response.json()  # Method call
response.text    # Attribute

# Scriptling
response.json()            # Method call
response.text              # Attribute
response.body              # Legacy alias for response.text; prefer text
response.status_code       # Attribute
```

### Library Import

Scriptling uses dynamic imports that load libraries on first use:

```python
# Both work the same
import json
import requests

# Library is loaded when first accessed
data = json.loads('{"key": "value"}')
```

### Default Timeout

HTTP requests have a default 5-second timeout:

```python
# Python - no default timeout (hangs forever)
response = requests.get("https://slow-api.com")

# Scriptling - 5 second default
response = requests.get("https://slow-api.com")  # Times out after 5s

# Explicit timeout
response = requests.get("https://slow-api.com", {"timeout": 30})
```

### No Implicit Type Coercion

```python
# Python - implicit conversion
"Count: " + 5  # Error in Python 3, worked in Python 2

# Scriptling - explicit conversion required
"Count: " + str(5)  # "Count: 5"
```

### File System Access

File access is sandboxed by default:

```python
# Python - full file system access
f = open("/etc/passwd", "r")

# Scriptling - requires os library with allowed paths
import os
# Only works if /etc is in allowed paths
content = os.read_file("/etc/passwd")
```

### Errors and Exceptions Are Catchable, Except SystemExit

`try`/`except` catches runtime Errors (type errors, name errors, and so on) and ordinary explicitly raised Exceptions. When an Error is caught, Scriptling infers the exception type from the error message. `SystemExit` is the exception: it bypasses script `except` handlers, runs `finally` blocks, and returns to the Go host.

```python
# A runtime Error is caught, with its type inferred
try:
    x = undefined_variable  # produces a NameError-flavoured Error
except NameError:
    print("Caught!")  # This runs

# An explicitly raised Exception is caught too
try:
    raise ValueError("Custom error")
except Exception:
    print("Caught!")  # This runs
```

## Migration Tips

### From Python to Scriptling

1. **Replace `open()` with `os` library** (`with` works for custom context managers, but there is no built-in `open()`):
   ```python
   # Python
   with open("file.txt") as f:
       content = f.read()

   # Scriptling
   import os
   content = os.read_file("file.txt")
   ```

2. **Use the response JSON helper**:
   ```python
   # Python and Scriptling
   data = response.json()
   ```

3. **Avoid async/await**:
   ```python
   # Python
   async def fetch():
       response = await client.get(url)

   # Scriptling - synchronous only
   def fetch():
       return requests.get(url)
   ```

4. **Use match/case instead of complex if/elif**:
   ```python
   # Both work
   if status == 200:
       handle_success()
   elif status == 404:
       handle_not_found()

   match status:
       case 200:
           handle_success()
       case 404:
           handle_not_found()
   ```

## See Also

- [Syntax Rules](../syntax/) - Scriptling syntax
- [Functions](../functions/) - Function parameters
- [Error Handling](../error-handling/) - Error vs Exception
- [Classes](../classes/) - Class limitations
