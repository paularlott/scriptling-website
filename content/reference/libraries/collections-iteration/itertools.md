---
title: itertools
description: Iteration utilities for efficient looping, filtering, and combinatorics.
weight: 1

aliases:
  - /reference/libraries/stdlib/itertools/
  - /reference/libraries/itertools/
---

The `itertools` library provides Python-compatible iteration utilities for chaining, filtering, batching, and generating combinations/permutations. Reach for it whenever you need to combine multiple lists, slice by index, or enumerate combinatorial possibilities without writing the loop yourself.

## Available Functions

| Function | Description |
|----------|-------------|
| `chain(*iterables)` | Chain multiple iterables together. |
| `cycle(iterable, n)` | Cycle through an iterable `n` times. |
| `repeat(elem[, n])` | Repeat an element `n` times (default `1`). |
| `zip_longest(*iterables, fillvalue=None)` | Zip iterables, filling shorter ones with `fillvalue`. |
| `count(start, stop[, step])` | Generate a sequence of numbers. |
| `islice(iterable, ...)` | Slice an iterable by indices. |
| `takewhile(predicate, iterable)` | Take elements while `predicate` is true. |
| `dropwhile(predicate, iterable)` | Drop elements while `predicate` is true, then return the rest. |
| `filterfalse(predicate, iterable)` | Return elements where `predicate` is false. |
| `compress(data, selectors)` | Filter `data` by truthy `selectors`. |
| `permutations(iterable[, r])` | Generate all `r`-length permutations. |
| `combinations(iterable, r)` | Generate all `r`-length combinations (no repetition). |
| `combinations_with_replacement(iterable, r)` | Generate `r`-length combinations (with repetition). |
| `product(*iterables)` | Cartesian product of iterables. |
| `groupby(iterable[, key])` | Group consecutive elements by key. |
| `accumulate(iterable[, func])` | Running totals/accumulation. |
| `pairwise(iterable)` | Successive overlapping pairs. |
| `batched(iterable, n)` | Group elements into batches of size `n`. |
| `starmap(func, iterable)` | Apply a function to argument tuples. |

## Functions

### Chaining and Combining

#### `chain(*iterables)`

Chains multiple iterables together into a single list.

**Parameters:**
- `*iterables` (`list`, `tuple`, or `str`): Iterables to chain together, in order.

**Returns:** `list`: all elements concatenated.

```python
import itertools

itertools.chain([1, 2], [3, 4])  # [1, 2, 3, 4]
itertools.chain("ab", "cd")      # ["a", "b", "c", "d"]
```

#### `cycle(iterable, n)`

Cycles through an iterable, repeating it `n` times.

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`): Elements to cycle through.
- `n` (`int`): Number of times to repeat the full iterable.

**Returns:** `list`: `iterable`'s elements repeated `n` times.

```python
import itertools

itertools.cycle([1, 2], 3)  # [1, 2, 1, 2, 1, 2]
```

> **Note:** Unlike Python's infinite `cycle()`, this requires specifying a count.

#### `repeat(elem[, n])`

Repeats a single element `n` times.

**Parameters:**
- `elem` (`any`): Element to repeat.
- `n` (`int`, optional): Number of repetitions. Default: `1`.

**Returns:** `list`: `elem` repeated `n` times.

```python
import itertools

itertools.repeat("x", 3)  # ["x", "x", "x"]
itertools.repeat(0, 5)    # [0, 0, 0, 0, 0]
```

#### `zip_longest(*iterables, fillvalue=None)`

Zips iterables together into tuples, filling shorter iterables with `fillvalue` once they run out of elements.

**Parameters:**
- `*iterables` (`list`, `tuple`, or `str`): Iterables to zip.
- `fillvalue` (`any`, keyword-only, optional): Value used in place of missing elements. Default: `None`.

**Returns:** `list` of `tuple`: one tuple per index up to the longest iterable's length.

```python
import itertools

itertools.zip_longest([1, 2, 3], ["a", "b"])
# [(1, "a"), (2, "b"), (3, None)]

itertools.zip_longest([1, 2], ["a"], fillvalue="-")
# [(1, "a"), (2, "-")]
```

### Slicing and Filtering

#### `count(start, stop[, step])`

Generates a sequence of numbers, similar to the builtin `range()`.

**Parameters:**
- `start` (`int`): First value.
- `stop` (`int`): End of the range (exclusive).
- `step` (`int`, optional): Increment between values. Default: `1`. Cannot be `0`.

**Returns:** `list` of `int`

```python
import itertools

itertools.count(0, 5)       # [0, 1, 2, 3, 4]
itertools.count(0, 10, 2)   # [0, 2, 4, 6, 8]
itertools.count(5, 0, -1)   # [5, 4, 3, 2, 1]
```

#### `islice(iterable, stop)` / `islice(iterable, start, stop[, step])`

Slices an iterable by indices, like Python's slice notation.

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`): Iterable to slice.
- `start` (`int`, optional): Start index. Omit to slice from the beginning (single-argument form).
- `stop` (`int`): End index (exclusive).
- `step` (`int`, optional): Step between elements. Default: `1`. Must be positive.

**Returns:** `list`: the sliced elements.

```python
import itertools

itertools.islice([0, 1, 2, 3, 4], 3)        # [0, 1, 2]
itertools.islice([0, 1, 2, 3, 4], 1, 4)     # [1, 2, 3]
itertools.islice([0, 1, 2, 3, 4], 0, 5, 2)  # [0, 2, 4]
```

#### `takewhile(predicate, iterable)`

Takes elements from the start of `iterable` as long as `predicate` returns true, stopping at the first false result.

**Parameters:**
- `predicate` (`callable`): Function returning a truthy/falsy value for each element.
- `iterable` (`list` or `tuple`): Elements to filter.

**Returns:** `list`: the leading elements for which `predicate` was true.

```python
import itertools

itertools.takewhile(lambda x: x < 5, [1, 3, 5, 2, 4])
# [1, 3]
```

#### `dropwhile(predicate, iterable)`

Drops elements from the start of `iterable` while `predicate` is true, then returns all remaining elements (even if `predicate` becomes true again later).

**Parameters:**
- `predicate` (`callable`): Function returning a truthy/falsy value for each element.
- `iterable` (`list` or `tuple`): Elements to filter.

**Returns:** `list`: the elements starting from the first one where `predicate` is false.

```python
import itertools

itertools.dropwhile(lambda x: x < 5, [1, 3, 5, 2, 4])
# [5, 2, 4]
```

#### `filterfalse(predicate, iterable)`

Returns elements for which `predicate` is false (the inverse of the builtin `filter()`).

**Parameters:**
- `predicate` (`callable`): Function returning a truthy/falsy value for each element.
- `iterable` (`list` or `tuple`): Elements to filter.

**Returns:** `list`: elements for which `predicate` returned false.

```python
import itertools

itertools.filterfalse(lambda x: x % 2, [1, 2, 3, 4])
# [2, 4]  (even numbers)
```

#### `compress(data, selectors)`

Filters `data`, keeping only elements whose corresponding `selectors` value is truthy.

**Parameters:**
- `data` (`list` or `tuple`): Elements to filter.
- `selectors` (`list` or `tuple`): Truthy/falsy values, matched by index against `data`.

**Returns:** `list`: elements of `data` where the matching selector is truthy. Extra elements past the shorter of the two inputs are ignored.

```python
import itertools

itertools.compress([1, 2, 3, 4], [True, False, True, False])
# [1, 3]
```

### Combinatorics

#### `product(*iterables)`

Computes the Cartesian product of the input iterables.

**Parameters:**
- `*iterables` (`list`, `tuple`, or `str`): Iterables to combine. If any is empty, the result is empty.

**Returns:** `list` of `tuple`: every combination of one element from each iterable.

```python
import itertools

itertools.product([1, 2], ["a", "b"])
# [(1, "a"), (1, "b"), (2, "a"), (2, "b")]
```

#### `permutations(iterable[, r])`

Generates all `r`-length permutations of elements from `iterable`, without repeating elements within a single permutation.

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`): Elements to permute.
- `r` (`int`, optional): Length of each permutation. Default: the length of `iterable` (full permutations).

**Returns:** `list` of `tuple`

```python
import itertools

itertools.permutations([1, 2, 3], 2)
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

itertools.permutations("ab")
# [("a", "b"), ("b", "a")]
```

#### `combinations(iterable, r)`

Generates all `r`-length combinations of elements from `iterable`, without repetition and without regard to order.

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`): Elements to combine.
- `r` (`int`): Length of each combination.

**Returns:** `list` of `tuple`

```python
import itertools

itertools.combinations([1, 2, 3], 2)
# [(1, 2), (1, 3), (2, 3)]
```

#### `combinations_with_replacement(iterable, r)`

Generates all `r`-length combinations of elements from `iterable`, allowing the same element to be chosen more than once.

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`): Elements to combine.
- `r` (`int`): Length of each combination.

**Returns:** `list` of `tuple`

```python
import itertools

itertools.combinations_with_replacement([1, 2], 2)
# [(1, 1), (1, 2), (2, 2)]
```

### Grouping and Accumulation

#### `groupby(iterable[, key])`

Groups consecutive elements of `iterable` that share the same key. Note that, like Python's `groupby`, only *consecutive* matches are grouped: sort the input first if you want all matching elements grouped together regardless of position.

**Parameters:**
- `iterable` (`list` or `tuple`): Elements to group.
- `key` (`callable`, optional): Function computing the grouping key for each element. Default: the element itself.

**Returns:** `list` of `tuple`: `(key, group)` pairs where `group` is a `list` of the elements in that run.

```python
import itertools

itertools.groupby([1, 1, 2, 2, 3])
# [(1, [1, 1]), (2, [2, 2]), (3, [3])]

itertools.groupby(["aa", "ab", "ba"], lambda x: x[0])
# [("a", ["aa", "ab"]), ("b", ["ba"])]
```

#### `accumulate(iterable[, func])`

Returns a running accumulation of `iterable`, applying `func` cumulatively (left to right). Defaults to a running sum.

**Parameters:**
- `iterable` (`list` or `tuple`): Elements to accumulate.
- `func` (`callable`, optional): Function taking `(accumulator, next_item)`. Default: addition.

**Returns:** `list`: same length as `iterable`, each entry the accumulated value up to that point.

```python
import itertools

itertools.accumulate([1, 2, 3, 4])
# [1, 3, 6, 10]  (running sum)
```

### Pairing and Batching

#### `pairwise(iterable)`

Returns successive overlapping pairs from `iterable`.

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`): Elements to pair up.

**Returns:** `list` of `tuple`: `len(iterable) - 1` pairs, or an empty list if `iterable` has fewer than 2 elements.

```python
import itertools

itertools.pairwise([1, 2, 3, 4])
# [(1, 2), (2, 3), (3, 4)]
```

#### `batched(iterable, n)`

Groups elements of `iterable` into batches of size `n`. The final batch may be shorter if the length isn't an exact multiple of `n`.

**Parameters:**
- `iterable` (`list`, `tuple`, or `str`): Elements to batch.
- `n` (`int`): Batch size. Must be positive.

**Returns:** `list` of `tuple`

```python
import itertools

itertools.batched([1, 2, 3, 4, 5], 2)
# [(1, 2), (3, 4), (5,)]
```

### Function Application

#### `starmap(func, iterable)`

Applies `func` to each tuple/list in `iterable`, unpacking its elements as positional arguments.

**Parameters:**
- `func` (`callable`): Function to apply.
- `iterable` (`list` or `tuple`): Sequence of argument tuples/lists.

**Returns:** `list`: one result per call to `func`.

```python
import itertools

itertools.starmap(pow, [(2, 3), (3, 2)])
# [8, 9]
```

## Examples

### Generate all 2-letter combinations

```python
import itertools

letters = "abc"
combos = itertools.combinations(letters, 2)
# [("a", "b"), ("a", "c"), ("b", "c")]
```

### Flatten nested lists

```python
import itertools

nested = [[1, 2], [3, 4], [5, 6]]
flat = itertools.chain(nested[0], nested[1], nested[2])
# [1, 2, 3, 4, 5, 6]
```

### Running total

```python
import itertools

sales = [100, 200, 150, 300]
running_total = itertools.accumulate(sales)
# [100, 300, 450, 750]
```

## See Also

- [functools](../functools/): `reduce()` for collapsing an iterable to a single value.
- [collections](../collections/): `deque` and other specialized containers.
