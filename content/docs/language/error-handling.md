---
title: Error Handling
description: try/except/finally, raise, assert, and exception types in Scriptling.
weight: 6
---

Scriptling provides comprehensive error handling with Python 3-style exception handling.

## Error vs Exception

Scriptling has two distinct types of runtime error conditions:

| Aspect | **Error** | **Exception** |
|--------|-----------|---------------|
| **Purpose** | Fatal runtime errors | Recoverable conditions |
| **Can be caught?** | No (try/except won't catch them) | Yes (with try/except) |
| **Examples** | Parse errors, syntax errors, VM errors | SystemExit, ValueError, user-defined |
| **Propagation** | Immediately converted to Go error | Propagated for try/except |

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
    raise "something went wrong"
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
Exception (base class)
├── ValueError      - Invalid values
├── TypeError       - Type mismatches
├── NameError       - Undefined names
├── ZeroDivisionError - Division by zero
├── IndexError      - Sequence index out of range
├── KeyError        - Dictionary key not found
├── AttributeError  - Attribute not found on object
└── ... (more specific types)
```

### Built-in Exception Types

| Exception Type | When Raised |
|----------------|-------------|
| `Exception` | Base class for all exceptions |
| `ValueError` | Invalid value for operation |
| `TypeError` | Operation on wrong type |
| `NameError` | Variable/identifier not found |
| `ZeroDivisionError` | Division or modulo by zero |
| `IndexError` | Sequence index out of range |
| `KeyError` | Dictionary key not found |
| `AttributeError` | Attribute not found on object |

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
```

### Simple String Raise

```python
if x < 0:
    raise "Value must be positive"
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

Change the exception type while preserving context:

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
    print("Type: " + type(e))       # "EXCEPTION"
    print("Message: " + str(e))     # "division by zero"
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
# __exit__ called automatically — no finally needed
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
import json
import requests

try:
    options = {"timeout": 5}
    response = requests.get("https://api.example.com/data", options)

    if response.status_code != 200:
        raise "HTTP error: " + str(response.status_code)

    data = json.loads(response.body)
    print("Success: " + str(len(data)))
except:
    print("Request failed")
    data = []
finally:
    print("Request complete")
```

## Custom Exception Patterns

### Creating Custom Error Messages

```python
def validate_user(user):
    if not user.get("name"):
        raise ValueError("User must have a name")
    if not user.get("email"):
        raise ValueError("User must have an email")
    if "@" not in user["email"]:
        raise ValueError("Invalid email format")
    return True
```

### Exception Chaining

```python
def load_config(path):
    try:
        data = read_file(path)
        return parse_json(data)
    except FileNotFoundError:
        raise ValueError("Config file not found: " + path)
    except JSONParseError as e:
        raise ValueError("Invalid config format: " + str(e))
```

## SystemExit Exception

The `sys.exit()` function raises a SystemExit exception that can be caught:

```python
import sys

try:
    sys.exit(42)
except Exception as e:
    print("Caught: " + str(e))  # "Caught: SystemExit: 42"

# Exit with custom message
sys.exit("Fatal error occurred")
```

## Exception Handling in Libraries

When writing libraries, follow these guidelines:

1. **Document exceptions** your functions can raise
2. **Use specific exception types** for different error conditions
3. **Preserve original exceptions** when wrapping errors
4. **Consider recovery scenarios** - can the caller reasonably recover?

```python
# Good library design
def parse_date(date_string):
    """
    Parse a date string into components.

    Args:
        date_string: Date in YYYY-MM-DD format

    Returns:
        Dict with year, month, day

    Raises:
        ValueError: If date_string is not valid format
        TypeError: If date_string is not a string
    """
    if not isinstance(date_string, str):
        raise TypeError("date_string must be a string")
    # ... parsing logic
```

## Common Pitfalls

### Catching Too Broadly

```python
# Bad - catches everything including system exits
try:
    some_operation()
except Exception:
    pass  # Silently ignores all errors

# Good - catch specific exceptions
try:
    some_operation()
except (ValueError, TypeError) as e:
    log_error(e)
    # Handle specific expected errors
```

### Silent Failures

```python
# Bad - silently ignores errors
try:
    risky_operation()
except:
    pass  # What went wrong?

# Good - at least log the error
try:
    risky_operation()
except Exception as e:
    print("Operation failed: " + str(e))
```

### Overly Broad Try Blocks

```python
# Bad - too much code in try block
try:
    config = load_config()
    connect_database()
    process_data()
    save_results()
except Exception:
    handle_error()  # Which part failed?

# Good - narrow try blocks
config = load_config()
connect_database()
try:
    process_data()  # Just the risky part
except DataError as e:
    handle_data_error(e)
save_results()
```

## Performance Considerations

### Try/Except vs Conditional Checks

```python
# Slower for frequent expected failures
try:
    value = dict["key"]
except KeyError:
    value = default

# Faster for expected lookups
value = dict.get("key", default)
```

**Rule of thumb**: Use exceptions for exceptional cases, not for control flow.

## For Go Developers

When calling Scriptling from Go:

```go
// Check for Error objects
if obj.IsError(result) {
    // Handle fatal error
}

// Check for Exception objects
if ex, ok := result.(*object.Exception); ok {
    // Check for SystemExit specifically
    if ex.IsSystemExit() {
        exitCode := ex.GetExitCode()
        // Handle exit
    }
}
```

## Summary

- Use `try/except/finally` for structured error handling
- Catch specific exception types when possible
- Use exceptions for exceptional cases, not control flow
- Always preserve original exceptions when wrapping errors
- Document which exceptions your functions can raise
- Add context to exceptions to aid debugging
- Avoid silent failures and overly broad exception handlers

## See Also

- [Functions](./functions/) - Function definitions
- [HTTP & JSON](./http/) - HTTP error handling patterns
- [Python Differences](./python-differences/) - Exception handling differences
