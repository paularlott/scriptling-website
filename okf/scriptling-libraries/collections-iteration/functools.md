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
| `reduce(function, iterable[, initializer])` | Reduce an iterable to a single value. |
| `partial(func, *args, **kwargs)` | Create a function with some arguments pre-filled. |

## Functions

### `reduce(function, iterable[, initializer])`

Applies `function` of two arguments cumulatively to the items of `iterable`, from left to right, reducing it to a single value. Equivalent to `function(function(function(item0, item1), item2), item3)...`.

**Parameters:**
- `function` (`callable`): A function taking two arguments: `(accumulator, current_item)`.
- `iterable` (`list`): Items to reduce.
- `initializer` (`any`, optional): Starting value for the accumulator. If omitted, the first element of `iterable` is used as the initial accumulator and reduction starts from the second element.

**Returns:** `any`: the final accumulated value.

**Raises:** `Error`: if `iterable` is empty and no `initializer` is given.

```python
import functools

def add(x, y):
    return x + y

result = functools.reduce(add, [1, 2, 3, 4, 5])  # 15
result = functools.reduce(add, [1, 2, 3], 10)    # 16
```

`reduce()` applies the function cumulatively: `reduce(add, [1, 2, 3, 4, 5])` is equivalent to:

```
add(add(add(add(1, 2), 3), 4), 5)
= add(add(add(3, 3), 4), 5)
= add(add(6, 4), 5)
= add(10, 5)
= 15
```

It's commonly used for summing, building data structures, or chaining a pipeline of functions:

```python
import functools

def merge_dicts(acc, item):
    acc[item[0]] = item[1]
    return acc

pairs = [["a", 1], ["b", 2], ["c", 3]]
result = functools.reduce(merge_dicts, pairs, {})
# {"a": 1, "b": 2, "c": 3}
```

```python
import functools

def apply_fn(value, fn):
    return fn(value)

def double(x):
    return x * 2

def add_one(x):
    return x + 1

functions = [double, add_one, double]
result = functools.reduce(apply_fn, functions, 5)
# double(5) = 10, add_one(10) = 11, double(11) = 22
```

### `partial(func, *args, **kwargs)`

Creates a new callable with some positional and/or keyword arguments pre-filled. Calling the result with additional arguments appends them after the pre-filled positional arguments and merges keyword arguments.

**Parameters:**
- `func` (`callable`): The function to partially apply.
- `*args` (`any`): Positional arguments to pre-fill.
- `**kwargs` (`any`): Keyword arguments to pre-fill.

**Returns:** `callable`: a new function with the given arguments pre-filled.

```python
import functools

def add(x, y):
    return x + y

add_five = functools.partial(add, 5)
print(add_five(3))   # 8
print(add_five(10))  # 15
```

```python
def greet(name, greeting="Hello"):
    return greeting + ", " + name + "!"

say_hi = functools.partial(greet, greeting="Hi")
print(say_hi("Alice"))  # Hi, Alice!
```

## Python Compatibility

This library implements a subset of Python's `functools` module:

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
