---
description: Higher-order functions that act on or return other functions.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/collections-iteration/functools/
sources:
    - resource: https://scriptling.dev/reference/libraries/collections-iteration/functools/
status: stable
tags:
    - libraries
    - collections
title: functools
type: API Reference
---
# functools

The `functools` library provides higher-order functions that act on or return other functions, compatible with Python's `functools` module. Reach for it when reducing a list to a single value or pre-filling some of a function's arguments.

## Available Functions

| Function | Description |
|----------|-------------|
| `reduce(function, iterable[, initializer])` | Apply `function(acc, item)` left to right to reduce a `list` to one value; raises on an empty list with no `initializer`. |
| `partial(func, *args, **kwargs)` | New callable with positional and/or keyword arguments pre-filled; call-time arguments are appended. |

## Example

```python
import functools

def add(x, y):
    return x + y

print(functools.reduce(add, [1, 2, 3, 4, 5]))   # 15  (((1+2)+3)+4)+5
print(functools.reduce(add, [1, 2, 3], 10))     # 16  (starts from the initializer)

def merge(acc, pair):
    acc[pair[0]] = pair[1]
    return acc

merged = functools.reduce(merge, [["a", 1], ["b", 2]], {})
print(merged["a"], merged["b"])                 # 1 2

add_five = functools.partial(add, 5)
print(add_five(3))                              # 8

def greet(name, greeting="Hello"):
    return greeting + ", " + name + "!"

say_hi = functools.partial(greet, greeting="Hi")
print(say_hi("Alice"))                          # Hi, Alice!
```

## Python Compatibility

This library implements a subset of Python's `functools` module. `reduce()` requires a `list`: wrap tuples, ranges and other iterables with `list(...)`.

| Function | Supported |
|----------|-----------|
| `reduce` | Yes |
| `partial` | Yes |
| `partialmethod` | No |
| `lru_cache` | No |
| `cache` | No |
| `cached_property` | No |
| `wraps` | No |
| `total_ordering` | No |
| `cmp_to_key` | No |

## See Also

- [itertools](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/itertools.md): iteration and combinatorics utilities, including `accumulate()` for running totals.
- [contextlib](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/contextlib.md): context manager utilities.
