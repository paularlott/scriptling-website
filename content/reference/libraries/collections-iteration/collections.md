---
title: collections
description: Specialized container datatypes, counters, double-ended queues, named tuples, and chained dicts.
weight: 1

aliases:
  - /reference/libraries/stdlib/collections/
  - /reference/libraries/collections/
---

The `collections` library provides Python-compatible specialized container datatypes: counters, double-ended queues, named tuples, default-value dicts, and chained dicts.

## Available Functions

| Function | Description |
|----------|-------------|
| `Counter([iterable])` | Create a counter of element occurrences. |
| `most_common(counter[, n])` | Get the `n` most common elements from a `Counter`. |
| `OrderedDict([items])` | Create an order-preserving dict. |
| `deque([iterable[, maxlen]])` | Create a double-ended queue. |
| `deque_appendleft(deque, elem)` | Add an element to the left of a deque. |
| `deque_popleft(deque)` | Remove and return the leftmost element of a deque. |
| `deque_extendleft(deque, iterable)` | Extend the left side of a deque with an iterable. |
| `deque_rotate(deque, n)` | Rotate a deque `n` steps to the right (or left if negative). |
| `namedtuple(typename, field_names)` | Create a class for named tuple instances. |
| `defaultdict(default_factory)` | Create a dict with default values for missing keys. |
| `ChainMap(*maps)` | Group multiple dicts for a single lookup. |

## Functions

### `Counter([iterable])`

Creates a dict-like object that counts occurrences of elements. Counting a missing key returns `0` instead of raising an error.

**Parameters:**
- `iterable` (`list`, `tuple`, `str`, or `dict`, optional): Elements to count. A list/tuple/string counts each element/character; a dict is copied directly as counts.

**Returns:** `Counter`: an instance supporting `c[key]`, `c.most_common([n])`, and `c.elements()`.

```python
import collections

c = collections.Counter([1, 1, 2, 3, 3, 3])
print(c[1])  # 2
print(c[4])  # 0 (missing keys return 0, not KeyError)

c = collections.Counter("hello")
print(c["l"])  # 2
```

Counter instances support these methods:

- `c[key]`: get the count for `key` (returns `0` if absent).
- `c.most_common([n])`: return the `n` most common `(element, count)` tuples, sorted by count descending. Omit `n` to return all.
- `c.elements()`: return a list of elements, each repeated by its count.

### `most_common(counter[, n])`

Returns the `n` most common elements and their counts from a `Counter`, sorted by count descending. Function form of `counter.most_common(n)`.

**Parameters:**
- `counter` (`Counter`): The counter to read from.
- `n` (`int`, optional): Number of elements to return. Default: all elements.

**Returns:** `list`: a list of `(element, count)` tuples.

```python
import collections

c = collections.Counter([1, 1, 2, 3, 3, 3])
print(collections.most_common(c, 2))
# [(3, 3), (1, 2)]
```

### `OrderedDict([items])`

Creates a dict that maintains insertion order. Scriptling's regular dicts already maintain insertion order, so this is equivalent to `dict()` and exists for Python-compatibility.

**Parameters:**
- `items` (`list` of 2-tuples, or `dict`, optional): Initial key-value pairs.

**Returns:** `dict`

```python
import collections

od = collections.OrderedDict([("a", 1), ("b", 2), ("c", 3)])
print(od["a"])  # 1
```

### `deque([iterable[, maxlen]])`

Creates a double-ended queue from an iterable. The returned value is a regular list; use the `deque_*` functions for deque-specific operations (`append()`/`pop()` work directly via the list's own methods for the right side).

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`, optional): Initial elements.
- `maxlen` (`int`, optional): If given and the deque is longer, elements are trimmed from the left so only the last `maxlen` elements remain.

**Returns:** `list`: usable as a deque with the `deque_*` functions.

```python
import collections

d = collections.deque([1, 2, 3])
```

### `deque_appendleft(deque, elem)`

Adds an element to the left side of a deque, in place.

**Parameters:**
- `deque` (`list`): The deque to modify.
- `elem` (`any`): Element to add.

**Returns:** `None`

```python
import collections

d = collections.deque([1, 2, 3])
collections.deque_appendleft(d, 0)
print(d)  # [0, 1, 2, 3]
```

### `deque_popleft(deque)`

Removes and returns the leftmost element of a deque, in place.

**Parameters:**
- `deque` (`list`): The deque to modify.

**Returns:** `any`: the removed element.

**Raises:** `Error`: if the deque is empty.

```python
import collections

d = collections.deque([1, 2, 3])
x = collections.deque_popleft(d)
print(x, d)  # 1 [2, 3]
```

### `deque_extendleft(deque, iterable)`

Extends the left side of a deque with elements from `iterable`, in place. Elements are added in reverse order, so the first element of `iterable` ends up closest to the front.

**Parameters:**
- `deque` (`list`): The deque to modify.
- `iterable` (`list` or `tuple`): Elements to add.

**Returns:** `None`

```python
import collections

d = collections.deque([1, 2, 3])
collections.deque_extendleft(d, [4, 5])
print(d)  # [5, 4, 1, 2, 3]
```

### `deque_rotate(deque, n)`

Rotates a deque `n` steps to the right, in place. Negative `n` rotates left.

**Parameters:**
- `deque` (`list`): The deque to modify.
- `n` (`int`): Number of steps to rotate.

**Returns:** `None`

```python
import collections

d = collections.deque([1, 2, 3, 4])
collections.deque_rotate(d, 1)
print(d)  # [4, 1, 2, 3]

d = collections.deque([1, 2, 3, 4])
collections.deque_rotate(d, -1)
print(d)  # [2, 3, 4, 1]
```

### `namedtuple(typename, field_names)`

Creates a class for named tuple instances, supporting both attribute access (`p.x`) and dict-style access (`p["x"]`).

**Parameters:**
- `typename` (`str`): Name of the generated class.
- `field_names` (`list` or `tuple` of `str`, or a space-separated `str`): Field names. A string is split on spaces and/or commas.

**Returns:** `type`: a class whose instances expose the given fields.

```python
import collections

Point = collections.namedtuple("Point", ["x", "y"])
p = Point(1, 2)
print(p.x, p.y)    # 1 2
print(p["x"])      # 1

Person = collections.namedtuple("Person", "name age")
```

### `defaultdict(default_factory)`

Creates a dict that automatically creates a default value (using `default_factory`) when a missing key is accessed.

**Parameters:**
- `default_factory` (callable or `type`): Called with no arguments to produce the default value for a missing key (e.g. `list`, `int`, `dict`, or a custom function).

**Returns:** `defaultdict`: a dict-like instance with automatic default value creation.

```python
import collections

d = collections.defaultdict(list)
d["items"].append(1)  # creates [] then appends -> [1]

counts = collections.defaultdict(int)
counts["x"] = counts["x"] + 1  # creates 0 then increments -> 1
```

### `ChainMap(*maps)`

Merges multiple dicts into a single dict. Earlier dicts take priority over later ones for duplicate keys. Unlike Python's `ChainMap`, the result is a snapshot: later writes to the original dicts are not reflected in it.

**Parameters:**
- `*maps` (`dict`): Dicts to merge, highest priority first.

**Returns:** `dict`: a new dict with keys from all inputs, first dict wins on conflicts.

```python
import collections

d1 = {"a": 1, "b": 2}
d2 = {"b": 20, "c": 3}
cm = collections.ChainMap(d1, d2)

print(cm["a"])  # 1 (from d1)
print(cm["b"])  # 2 (d1 has priority over d2)
print(cm["c"])  # 3 (from d2)
```

## See Also

- [itertools](../itertools/): iteration and combinatorics utilities.
- [functools](../functools/): higher-order functions like `reduce()` and `partial()`.
