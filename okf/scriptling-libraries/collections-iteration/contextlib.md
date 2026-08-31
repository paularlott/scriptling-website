---
description: Utilities for common tasks involving the with statement.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/collections-iteration/contextlib/
sources:
    - resource: https://scriptling.dev/reference/libraries/collections-iteration/contextlib/
status: stable
tags:
    - libraries
    - collections
title: contextlib
type: API Reference
---
# contextlib

The `contextlib` library provides utilities for common tasks involving the `with` statement. Currently it provides `suppress`, a context manager that silently ignores specified exception types.

## Available Functions

| Function | Description |
|----------|-------------|
| `suppress(*exc_types)` | Context manager that suppresses the given exception types. |

## Functions

### `suppress(*exc_types)`

Returns a context manager that silently swallows any exception whose type matches one of the given types. If no types are given, all exceptions are suppressed. Non-matching exception types still propagate normally.

**Parameters:**
- `*exc_types` (`type` or `str`): Exception types to suppress (e.g. `ValueError`, or the equivalent type-name string). Omit to suppress all exceptions.

**Returns:** `ContextManager`: supports the `with` statement.

```python
import contextlib

with contextlib.suppress(ValueError):
    int("not a number")  # silently ignored

print("continues here")
```

Non-matching exceptions still propagate:

```python
import contextlib

try:
    with contextlib.suppress(ValueError):
        raise TypeError("this is not suppressed")
except TypeError as e:
    print("caught:", e)
```

Suppress everything by omitting the types:

```python
import contextlib

with contextlib.suppress():
    raise Exception("also ignored")
```

`from ... import` works as expected:

```python
from contextlib import suppress

with suppress(ValueError):
    raise ValueError("ignored")
```

When no exception occurs, the body runs normally:

```python
import contextlib

result = 0
with contextlib.suppress(ValueError):
    result = 42

print(result)  # 42
```

## See Also

- [functools](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/functools.md): higher-order functions like `reduce()` and `partial()`.
- [itertools](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/itertools.md): iteration and combinatorics utilities.
