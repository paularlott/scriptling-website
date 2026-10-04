---
title: Error Handling
description: try/except/else/finally, raise, assert, and exception types in Scriptling.
tags: [reference, error-handling]
weight: 6
---

Scriptling provides comprehensive error handling with Python 3-style exception handling.

## Try/Except/Finally

The basic structure for error handling:

```python
try:
    # Code that might raise an exception
    result = 10 / 0
except ZeroDivisionError:
    # Handle division by zero
    print("Cannot divide by zero")
finally:
    # Always executes (optional)
    print("Cleanup code here")
```

`except` catches both runtime errors raised by the interpreter (type errors, missing names, bad indexes, division by zero), whose exception type is [inferred from the error message](#automatic-exception-type-inference), and exceptions raised explicitly with `raise`. The one exception is `SystemExit`, which bypasses `except` handlers (see [SystemExit Exception](#systemexit-exception)).

### Try/Except/Else

The `else` clause runs only when the `try` block completes without raising an exception. This is distinct from placing code after the `try/except` block: the `else` body is skipped if an exception was caught:

```python
try:
    result = int(user_input)
except ValueError:
    print("Not a valid number")
else:
    # Only runs if no exception was raised
    print("Parsed successfully:", result)
finally:
    # Always runs regardless
    print("Done")
```

A common pattern is to keep the `try` block minimal and put the success-path logic in `else`:

```python
try:
    data = fetch_data(url)
except Exception as e:
    log_error(e)
    data = None
else:
    process(data)  # Only runs when fetch_data() succeeded
```

### Multiple Exception Types

Handle different error types with separate except blocks:

```python
try:
    value = int(user_input)
    result = 100 / value
except ValueError as e:
    print("Invalid number: " + str(e))
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print("Unexpected error: " + str(e))
```

### Catching with Variable

```python
try:
    raise Exception("something went wrong")
except Exception as e:
    print("Error: " + str(e))
```

### Bare Except

```python
try:
    risky_operation()
except:
    print("Error occurred")  # Catches any exception
```

## Exception Type Hierarchy

Scriptling supports Python 3-style exception type matching:

```
BaseException
└── Exception (base class)
    ├── ValueError        - Invalid values
    ├── TypeError         - Type mismatches
    ├── NameError         - Undefined names
    ├── ImportError       - Library or imported name cannot be imported
    ├── ArithmeticError
    │   ├── ZeroDivisionError - Division by zero
    │   └── OverflowError     - Result too large (e.g. an integer ratio beyond int64)
    ├── LookupError
    │   ├── IndexError    - Sequence index out of range
    │   └── KeyError      - Dictionary key not found
    ├── AttributeError    - Attribute not found on object
    ├── OSError           - OS-level errors
    └── RuntimeError      - General runtime errors
```

An `except` clause catches its type and the types below it, so `except LookupError:` catches both `KeyError` and `IndexError`. The type can also come from a variable, including a tuple of types:

```python
retryable = (KeyError, IndexError)
try:
    value = data[key]
except retryable:
    value = None
```

### Built-in Exception Types

| Exception Type | When Raised |
|----------------|-------------|
| `Exception` | Base class for all exceptions |
| `LookupError` | Base of `IndexError` and `KeyError` |
| `ArithmeticError` | Base of `ZeroDivisionError` and `OverflowError` |
| `ValueError` | Invalid value for operation |
| `TypeError` | Operation on wrong type |
| `NameError` | Variable/identifier not found |
| `ImportError` | Library or imported name cannot be imported |
| `ZeroDivisionError` | Division or modulo by zero |
| `IndexError` | Sequence index out of range |
| `KeyError` | Dictionary key not found |
| `AttributeError` | Attribute not found on object |
| `OSError` | OS-level errors (file not found, permission denied, etc.) |
| `RuntimeError` | General runtime errors |

### Automatic Exception Type Inference

Scriptling automatically infers exception types from error messages:

```python
try:
    x = "string" + 123  # Type mismatch
except TypeError as e:
    print("Caught type error")  # This works!

try:
    x = undefined_variable
except NameError as e:
    print("Caught name error")  # This works!

try:
    import optional_library
except ImportError:
    print("Optional library is not available")
```

## Raise Statement

### Basic Raise

```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return True
```

### Exception Constructors

Built-in exception types can be raised using constructors:

```python
raise Exception("generic error")
raise ValueError("invalid value")
raise TypeError("wrong type")
raise NameError("name not defined")
raise ImportError("module not found")
```

### Raise Requires an Exception

The operand of `raise` must be an `Exception` instance (or an instance of a subclass). Raising a plain string, number, or other value is rejected with `"exceptions must derive from BaseException"`:

```python
raise ValueError("invalid value")   # OK
raise "invalid value"                # Error: exceptions must derive from BaseException
```

### Re-raising Exceptions

Re-raise an exception after handling:

```python
try:
    risky_operation()
except Exception as e:
    log_error(e)
    raise  # Re-raise the same exception
```

Bare `raise` outside an except block raises an error:

```python
raise  # Error: No active exception to re-raise
```

### Raise with Different Type

Raise a different type, carrying the original message (`raise ... from ...` chaining is not supported):

```python
try:
    parse_config(data)
except ValueError as e:
    raise TypeError("Configuration error: " + str(e))
```

## Assert Statement

Test conditions and raise errors when they fail:

```python
# Basic assert - raises AssertionError if condition is False
assert x > 0

# Assert with optional error message
assert x > 0, "x must be positive"

# Common use cases
assert len(data) > 0, "Data cannot be empty"
assert user is not None, "User not found"
assert response.status_code == 200, "Request failed"

# Use in functions for validation
def divide(a, b):
    assert b != 0, "Cannot divide by zero"
    return a / b
```

## Exception Object Properties

When you catch an exception with `as e`, you can access its properties:

```python
try:
    result = 10 / 0
except Exception as e:
    print("Type: " + type(e))       # Type: ZeroDivisionError
    print("Message: " + str(e))     # Message: division by zero
```

## Common Patterns

### Safe Dictionary Access

```python
# Option 1: Using try/except
try:
    value = data["key"]
except KeyError:
    value = default_value

# Option 2: Using get() method (preferred)
value = data.get("key", default_value)
```

### Safe List Access

```python
try:
    item = items[index]
except IndexError:
    item = None
```

### Resource Cleanup with Finally (or `with`)

Use `with` when the resource implements `__enter__`/`__exit__`:

```python
with open_connection() as conn:
    process(conn)
# __exit__ called automatically: no finally needed
```

Fall back to `try/finally` when no context manager is available:

```python
file = None
try:
    file = open_file("data.txt")
    process_file(file)
except Exception as e:
    print("Error: " + str(e))
finally:
    if file:
        file.close()
```

### HTTP Error Handling

```python
import requests

try:
    options = {"timeout": 5}
    response = requests.get("https://api.example.com/data", options)

    if response.status_code != 200:
        raise RuntimeError("HTTP error: " + str(response.status_code))

    data = response.json()
    print("Success: " + str(len(data)))
except:
    print("Request failed")
    data = []
finally:
    print("Request complete")
```

## Custom Exceptions

Scriptling cannot define custom exception classes: `class MyError(Exception)` fails because classes cannot derive from the built-in exception types. Raise a built-in type with a descriptive message instead, and wrap lower-level errors by re-raising with added context:

```python
import json

def validate_user(user):
    if not user.get("name"):
        raise ValueError("User must have a name")
    if "@" not in user.get("email", ""):
        raise ValueError("Invalid email format")
    return True

def load_config(text):
    try:
        return json.loads(text)
    except Exception as e:
        raise ValueError("Invalid config format: " + str(e))
```

## SystemExit Exception

`sys.exit()` raises a special `SystemExit` exception that bypasses all script `except` handlers. `finally` blocks still run, then the exception returns to the Go host:

```python
import sys

try:
    sys.exit(42)
except Exception:
    print("not reached")
finally:
    print("cleanup runs")

# This line is not reached.
print("continuing")
```

`sys.exit("Fatal error occurred")` carries the message and uses exit code 1. A host can inspect the returned exception and decide whether to terminate the process, return an HTTP status, or continue using the interpreter.

## For Go Developers

Inspect the returned object even when `err` is nil: `SystemExit(0)` is treated as a clean exit and may return a nil Go error. Non-zero exits return the exception with an error.

```go
result, err := p.Eval(script)

if ex, ok := object.AsException(result); ok && ex.IsSystemExit() {
    exitCode := ex.GetExitCode()
    // Map the exit to host behavior; do not assume the Go process must exit.
    handleExit(exitCode)
    return
}
if err != nil {
    // Handle other evaluation failures.
    return
}
```

## See Also

- [Functions](../functions/) - Function definitions
- [Python Differences](../python-differences/) - Exception handling differences
