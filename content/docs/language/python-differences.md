---
title: Python Differences
description: What's NOT supported and key differences between Scriptling and Python.
weight: 11
---

Scriptling is inspired by Python but has intentional limitations for embedded scripting. This page documents what's NOT supported and key differences.

## Python Features NOT Supported

### Language Features

| Feature | Notes |
|---------|-------|
| `async`/`await` | Asynchronous programming is not supported |
| Generators with `yield` | Generator functions are not supported |
| Dictionary comprehensions | Only list comprehensions are supported |
| Type annotations | Type hints like `def func(x: int) -> str:` are not parsed |
| Walrus operator (`:=`) | Assignment expressions are not supported |
| Parameter separators (`/` and `*`) | Positional-only and keyword-only parameter syntax |
| Decorators | `@decorator` syntax is not supported |
| Context managers (`with`) | The `with` statement is not implemented |
| Multiple inheritance | Only single inheritance is supported |
| Nested classes | Classes cannot be defined inside other classes/functions |
| Metaclasses | Custom metaclasses are not supported |
| Descriptors | The descriptor protocol is not implemented |
| Property decorators | `@property`, `@staticmethod`, `@classmethod` |
| Operator overloading | Magic methods like `__add__`, `__eq__` (except `__init__`) |

### Built-in Functions NOT Supported

| Function | Alternative |
|----------|-------------|
| `input()` | Not available in embedded environments |
| `open()` | Use `os.read_file()` and `os.write_file()` |
| `compile()`, `eval()`, `exec()` | Dynamic code execution not supported |
| `globals()`, `locals()` | Scope introspection not available |
| `vars()` | Variable introspection not supported |
| `dir()` | Limited to `type()` |
| `__import__()` | Use `import` statement |
| `memoryview()`, `bytearray()`, `bytes()` | Advanced byte manipulation not supported |
| `complex()` | Complex numbers not implemented |
| `frozenset()` | Use regular `set()` |

### Standard Library NOT Included

| Module | Notes |
|--------|-------|
| `asyncio` | Async I/O framework |
| `threading`, `multiprocessing` | Scriptling is single-threaded by design |
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
| Custom exception classes | Can raise string messages only |

### Other Differences

| Feature | Notes |
|---------|-------|
| `__name__ == "__main__"` | Not supported; scripts execute top-to-bottom |
| Module `__all__` | Export lists are not used |
| `__future__` imports | Not applicable |

## Supported Python 3 Features

Scriptling **does support**:

- ✅ Classes with single inheritance and `super()`
- ✅ Lambda functions and closures
- ✅ List comprehensions
- ✅ Iterators (`range`, `map`, `filter`, `enumerate`, `zip`)
- ✅ Dictionary views (`keys()`, `values()`, `items()`)
- ✅ F-strings and `.format()`
- ✅ True division (`/` always returns float)
- ✅ Set literals `{1, 2, 3}` and set operations
- ✅ Try/except/finally error handling
- ✅ Multiple assignment and tuple unpacking
- ✅ Extended unpacking with `*`
- ✅ Variadic arguments (`*args`)
- ✅ Keyword arguments (`**kwargs`)
- ✅ Default parameter values
- ✅ Conditional expressions (ternary operator)
- ✅ Augmented assignment (`+=`, `-=`, etc.)
- ✅ Slice notation with step (`[start:stop:step]`)
- ✅ `is` and `is not` operators
- ✅ `in` and `not in` operators
- ✅ Bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`)
- ✅ Boolean operators with short-circuit evaluation
- ✅ Assert statements (`assert condition, "message"`)
- ✅ String methods (most Python string methods)
- ✅ List, dict, set methods (most Python methods)

## Key Behavioral Differences

### HTTP Response Object

Python `requests` returns attributes, Scriptling returns an object:

```python
# Python
response.json()  # Method call
response.text    # Attribute

# Scriptling
json.loads(response.body)  # Parse manually
response.status_code       # Attribute
response.body              # Attribute (not response.text)
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

### Error vs Exception

Scriptling distinguishes between fatal Errors and catchable Exceptions:

```python
# Errors cannot be caught
try:
    x = undefined_variable  # NameError (fatal)
except:
    print("Won't get here")  # Never runs

# Exceptions can be caught
try:
    raise "Custom error"  # Exception
except:
    print("Caught!")  # This runs
```

## Migration Tips

### From Python to Scriptling

1. **Replace `open()` with `os` library**:
   ```python
   # Python
   with open("file.txt") as f:
       content = f.read()

   # Scriptling
   import os
   content = os.read_file("file.txt")
   ```

2. **Use explicit JSON handling**:
   ```python
   # Python
   data = response.json()

   # Scriptling
   import json
   data = json.loads(response.body)
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

- [Syntax Rules](./syntax/) - Scriptling syntax
- [Functions](./functions/) - Function parameters
- [Error Handling](./error-handling/) - Error vs Exception
- [Classes](./classes/) - Class limitations
