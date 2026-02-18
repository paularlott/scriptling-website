---
title: Python Differences
description: Key differences between Scriptling and Python 3.
weight: 6
---

Scriptling is inspired by Python but has some key differences. This page outlines what you need to know when transitioning from Python.

## Language Features

### Single Inheritance Only

Scriptling supports only single inheritance, not multiple inheritance:

```python
# Works in Scriptling
class Dog(Animal):
    def speak(self):
        return "Woof!"

# NOT supported - multiple inheritance
class Dog(Animal, Pet):  # Error!
    pass
```

### No Nested Classes

Classes must be defined at the module level:

```python
# NOT supported - nested class
class Outer:
    class Inner:  # Error!
        pass
```

## Standard Library Differences

### HTTP Response Object

HTTP responses return a Response object with fields (not a dictionary):

```python
import requests

response = requests.get("https://api.example.com")
# Response object with fields:
#   status_code - HTTP status code (int)
#   body        - Response body (string)
#   text        - Response body (string, same as body)
#   headers     - Response headers (dict)
#   url         - Request URL (string)

print(response.status_code)  # Access status code
print(response.body)         # Access response body
print(response.text)         # Same as body
print(response.headers)      # Headers dictionary
```

This is similar to Python's `requests` library, but Scriptling uses `response.body` instead of `response.text` as the primary field name.

### Default HTTP Timeout

HTTP requests have a default 5-second timeout:

```python
# Default timeout is 5 seconds
response = requests.get("https://api.example.com")

# Override timeout
response = requests.get("https://api.example.com", {"timeout": 30})
```

## Security Model

### Sandboxed by Default

Scriptling runs in a sandbox with restricted access:

```python
# NOT available unless explicitly enabled
import os
os.system("rm -rf /")  # Blocked!

import subprocess
subprocess.run(["cmd"])  # Blocked unless enabled

# File operations blocked unless enabled
f = open("/etc/passwd")  # Blocked!
```

### Configurable Security

Security can be configured when embedding in Go:

- Filesystem access: read/write paths can be restricted
- Network access: can be disabled or limited
- Subprocess execution: disabled by default
- Execution timeout: prevents infinite loops

## Missing Features

The following Python features are not implemented in Scriptling:

| Feature                   | Notes                                   |
| ------------------------- | --------------------------------------- |
| Multiple inheritance      | Single inheritance only                 |
| Nested classes            | Classes at module level only            |
| Decorators                | Not supported (use wrapper functions)   |
| Generators/yield          | Not supported                           |
| Async/await               | Not supported                           |
| Type hints                | Not supported                           |
| Walrus operator (`:=`)    | Not supported                           |
| Context managers (`with`) | Not supported                           |
| Metaclasses               | Not supported                           |
| Descriptors               | Not supported                           |

## String Formatting

Scriptling supports multiple string formatting options including f-strings:

```python
name = "Alice"
age = 30

# f-strings (recommended)
message = f"{name} is {age} years old"

# % formatting
message = "%s is %d years old" % (name, age)

# format() method
message = "{} is {} years old".format(name, age)
```

## Error Handling

Basic try/except is supported but without exception types:

```python
# Supported
try:
    risky_operation()
except:
    print("An error occurred")
finally:
    cleanup()

# NOT supported - exception types
# try:
#     risky_operation()
# except ValueError as e:
#     print(e)
```

## Import System

Scriptling supports various import styles:

```python
# Import entire module
import json
import requests

# Import specific names from a module
from json import loads, dumps

# Import with alias
import json as j
from json import loads as parse_json
```

## Summary

Scriptling provides a Python-like experience while being simpler and more secure by default. Most common Python patterns work, but if you're embedding Scriptling in a Go application or building LLM tools, you'll appreciate the sandboxed execution and consistent behavior.
