---
title: contextlib
weight: 2
---

Utilities for common tasks involving the `with` statement. Currently provides `suppress` — a context manager that silently ignores specified exception types.

## Available Functions

| Function | Description |
| -------- | ----------- |
| `suppress(*exc_types)` | Context manager that suppresses the given exception types |

## suppress

`contextlib.suppress(*exc_types)` returns a context manager that silently swallows any exception whose type matches one of the given types. If no types are given, all exceptions are suppressed.

Supports the `with` statement. The body runs normally when no exception occurs.

### Usage Examples

#### Suppress a specific exception type

```python
import contextlib

with contextlib.suppress(ValueError):
    int("not a number")  # silently ignored

print("continues here")
```

#### Suppress all exceptions

```python
import contextlib

with contextlib.suppress(Exception):
    raise RuntimeError("ignored")
```

#### Suppress with no types (suppress everything)

```python
import contextlib

with contextlib.suppress():
    raise Exception("also ignored")
```

#### Non-matching types still propagate

```python
import contextlib

try:
    with contextlib.suppress(ValueError):
        raise TypeError("this is not suppressed")
except TypeError as e:
    print("caught:", e)
```

#### Using from import

```python
from contextlib import suppress

with suppress(ValueError):
    raise ValueError("ignored")
```

#### No exception — body runs normally

```python
import contextlib

result = 0
with contextlib.suppress(ValueError):
    result = 42

print(result)  # 42
```
