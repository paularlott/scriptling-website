---
description: Specialized container datatypes, counters, double-ended queues, named tuples, and chained dicts.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/collections-iteration/collections/
sources:
    - resource: https://scriptling.dev/reference/libraries/collections-iteration/collections/
status: stable
tags:
    - libraries
    - collections
title: collections
type: API Reference
---
# collections

The `collections` library provides Python-compatible specialized container datatypes: counters, double-ended queues, named tuples, default-value dicts, and chained dicts.

## Available Functions

| Function | Description |
|----------|-------------|
| `Counter([iterable_or_mapping], **kwargs)` | Create a counter of element occurrences. |
| `most_common(counter[, n])` | Get the `n` most common elements from a `Counter`. |
| `OrderedDict([items], **kwargs)` | Create an order-preserving dict with `move_to_end()` and `popitem(last=False)`. |
| `deque([iterable[, maxlen]])` | Create a double-ended queue (with `appendleft()`, `popleft()`, `extendleft()`, `rotate()`, `maxlen`). |
| `namedtuple(typename, field_names)` | Create a class for named tuple instances. |
| `defaultdict(default_factory)` | Create a dict that builds a default value for missing keys. |
| `ChainMap(*maps)` | Group multiple dicts for a single lookup. |

## Functions

### `Counter([iterable_or_mapping], **kwargs)`

A dict of element -> count, as in Python. Count an iterable, copy a mapping or Counter, or pass counts as keyword arguments. A missing element counts `0`.

```python
import collections

c = collections.Counter([1, 1, 2, 3, 3, 3])
print(c)                  # Counter({3: 3, 1: 2, 2: 1})
print(c[3], c[4])         # 3 0
print(c.most_common(2))   # [(3, 3), (1, 2)]

c.update([1, 1])          # add counts
c.subtract({3: 1})        # subtract counts (may go negative)
print(c.total())          # 7

words = collections.Counter("hello")
print(words["l"], "h" in words, len(words))   # 2 True 4
print(collections.Counter(a=3) + collections.Counter(a=1, b=2))  # Counter({'a': 4, 'b': 2})
```

Counters support `c[key]`, assignment, `del`, `len`, `in`, iteration, `keys()`, `values()`, `items()`, `get()`, `pop()`, `copy()`, `clear()`, `update()`, `subtract()`, `total()`, `most_common([n])`, `elements()`, `==`, and the `+`, `-`, `|` and `&` operators (which keep only positive counts). Elements with equal counts are ordered by value rather than first insertion.

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

### `OrderedDict([items], **kwargs)`

Creates a dict that maintains insertion order. Scriptling's regular dicts already maintain insertion order, so an `OrderedDict` is an ordinary dict; what it adds for Python compatibility is the two methods LRU-cache code relies on, `move_to_end()` and `popitem(last=False)`.

**Parameters:**
- `items` (`dict` or `list`/`tuple` of 2-tuples, optional): Initial key-value pairs.
- `**kwargs`: Further entries, added after `items` in sorted key order (call order is not kept).

**Returns:** `dict`

| Method | Description |
|--------|-------------|
| `od.move_to_end(key, last=True)` | Move an existing key to the end, or to the front with `last=False`. Raises `KeyError` if the key is missing. |
| `od.popitem(last=True)` | Remove and return the newest `(key, value)` pair, or the oldest with `last=False`. Raises `KeyError` when empty. |

```python
import collections

od = collections.OrderedDict([("a", 1), ("b", 2), ("c", 3)])
od.move_to_end("a")
print(list(od))                  # ['b', 'c', 'a']
od.move_to_end("a", last=False)
print(list(od))                  # ['a', 'b', 'c']
print(od.popitem(last=False))    # ('a', 1)

# The LRU-cache idiom
cache = collections.OrderedDict()
def put(key, value, capacity=2):
    if key in cache:
        cache.move_to_end(key)
    cache[key] = value
    if len(cache) > capacity:
        cache.popitem(last=False)   # evict the least recently used
```

Unlike Python, `move_to_end()` and `popitem(last=...)` are accepted on every dict, not only on an `OrderedDict`, and an `OrderedDict` prints like a plain dict (`{'a': 1}`, not `OrderedDict({'a': 1})`).

### `deque([iterable[, maxlen]])`

Creates a double-ended queue object, like Python's `collections.deque`.

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`, optional): Initial elements.
- `maxlen` (`int` or `None`, optional): Maximum length. If the initial elements exceed it, only the last `maxlen` are kept. Available afterwards as `d.maxlen`.

**Returns:** `deque`. Supports `len()`, indexing, iteration, `list(d)`, and these methods:

- `d.append(x)` / `d.appendleft(x)`: add to the right / left end.
- `d.pop()` / `d.popleft()`: remove and return from the right / left end (`IndexError` if empty).
- `d.extend(iterable)` / `d.extendleft(iterable)`: add several elements; `extendleft` adds them one at a time, so they end up in reverse order.
- `d.rotate(n)`: rotate `n` steps to the right (negative `n` rotates left).
- `d.clear()`: remove all elements.

```python
import collections

d = collections.deque([1, 2, 3])
d.appendleft(0)
d.append(4)
print(d)                  # deque([0, 1, 2, 3, 4])
print(d.popleft(), d.pop(), d)  # 0 4 deque([1, 2, 3])

d.extendleft([4, 5])
print(d)                  # deque([5, 4, 1, 2, 3])

d = collections.deque([1, 2, 3, 4])
d.rotate(1)
print(d)                  # deque([4, 1, 2, 3])
d.rotate(-1)
print(d)                  # deque([1, 2, 3, 4])

d = collections.deque([1, 2, 3, 4, 5], maxlen=3)
print(d, d.maxlen)        # deque([3, 4, 5], maxlen=3) 3
```

### `namedtuple(typename, field_names, defaults=None)`

Creates a class for named tuple instances. Instances behave like tuples (indexing, slicing, `len()`, iteration, unpacking, `*` splatting, `in`, equality with plain tuples, hashing and tuple ordering) and also expose attribute access (`p.x`) and dict-style access (`p["x"]`). They are immutable: assigning to a field raises `AttributeError`.

**Parameters:**
- `typename` (`str`): Name of the generated class.
- `field_names` (`list` or `tuple` of `str`, or a space-separated `str`): Field names. A string is split on spaces and/or commas.
- `defaults` (`list` or `tuple`, optional): Default values for the rightmost fields.

**Returns:** `type`: a class whose instances expose the given fields.

```python
import collections

Point = collections.namedtuple("Point", ["x", "y"])
p = Point(1, 2)
print(p.x, p.y)    # 1 2
print(p["x"])      # 1

Person = collections.namedtuple("Person", "name age")

# Tuple behaviour
x, y = p                           # unpacking
print(p[0], p[-1], p[::-1], len(p))  # 1 2 (2, 1) 2
print(p == (1, 2), max(p), 2 in p)   # True 2 True
print(sorted([Point(2, 1), Point(1, 5)]))  # [Point(x=1, y=5), Point(x=2, y=1)]

# Keyword construction, defaults and helpers
print(Point(y=2, x=1))             # Point(x=1, y=2)
Opt = collections.namedtuple("Opt", "a b c", defaults=(0, 9))
print(Opt(1))                      # Opt(a=1, b=0, c=9)
print(p._replace(x=9), p._asdict(), Point._fields)
```

### `defaultdict(default_factory)`

Creates a dict that builds a default value when a missing key is read. A `defaultdict` is an ordinary dict, so every dict operation works on it: iteration, `items()`, `get()`, `pop()`, `update()`, `copy()`, `==`, `json.dumps()` and insertion order.

**Parameters:**
- `default_factory` (callable or `None`): Called with no arguments to produce the default for a missing key. Use a type (`int`, `list`, `set`, `dict`, `float`, `str`), a function, or a lambda; `None` makes a plain dict that raises `KeyError`.
- `init` (`dict` or list of pairs, optional) and `**kwargs`: initial entries, as for `dict()`.

**Returns:** `defaultdict`: a dict that creates, stores and returns the default on a missing-key read.

Only a read of a missing key (`d[key]`) calls the factory. `d.get(key)`, `key in d`, `d.pop(key, default)` and `d.setdefault(key, v)` never do, as in Python.

```python
import collections

counts = collections.defaultdict(int)
for word in "a b a c b a".split():
    counts[word] += 1
print(sorted(counts.items(), key=lambda kv: -kv[1]))   # [('a', 3), ('b', 2), ('c', 1)]

groups = collections.defaultdict(list)
for key, value in [("x", 1), ("y", 2), ("x", 3)]:
    groups[key].append(value)
print(groups)                       # defaultdict(<class 'list'>, {'x': [1, 3], 'y': [2]})

# Nested counting needs a lambda (or function) factory
nested = collections.defaultdict(lambda: collections.defaultdict(int))
nested["a"]["b"] += 1
print(dict(nested["a"]))            # {'b': 1}

print(groups.default_factory)       # the factory object
print(dict(groups))                 # a plain dict copy: {'x': [1, 3], 'y': [2]}
```

`copy()`, `copy.copy()` and `copy.deepcopy()` keep the factory; `dict(d)` and `{**d}` give plain dicts. `isinstance(d, defaultdict)` and `isinstance(d, dict)` are both true. A class cannot inherit from `defaultdict` (or from `dict`, `list` or `OrderedDict`).

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

- [itertools](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/itertools.md): iteration and combinatorics utilities.
- [functools](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/functools.md): higher-order functions like `reduce()` and `partial()`.
