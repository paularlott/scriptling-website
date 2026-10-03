---
description: Iteration utilities for efficient looping, filtering, and combinatorics.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/collections-iteration/itertools/
sources:
    - resource: https://scriptling.dev/reference/libraries/collections-iteration/itertools/
status: stable
tags:
    - libraries
    - collections
title: itertools
type: API Reference
---
# itertools

The `itertools` library provides iteration utilities, named after Python's, for chaining, filtering, batching, and generating combinations/permutations. Reach for it whenever you need to combine multiple lists, slice by index, or enumerate combinatorial possibilities without writing the loop yourself.

## Available Functions

Unlike Python, these functions return a **list** (of tuples, where Python yields tuples), not a lazy iterator. Inputs can be lists, tuples, strings, ranges or other iterables.

| Function | Description |
|----------|-------------|
| `chain(*iterables)` | Concatenate iterables into one list. |
| `cycle(iterable[, n])` | With `n`: the elements repeated `n` times, as a list. Without `n`: an endless iterator (see below). |
| `repeat(elem[, n])` | An iterator giving `elem` `n` times, or endlessly when `n` is omitted. |
| `zip_longest(*iterables, fillvalue=None)` | Zip, padding shorter inputs with `fillvalue`. |
| `count(start=0, step=1)` | Endless count from `start` by `step`; take items with `islice()`, `zip()` or `next()`. |
| `islice(iterable, stop)` / `islice(iterable, start, stop[, step])` | Elements selected by index, like slice notation. |
| `takewhile(predicate, iterable)` | Leading elements while `predicate` is true. |
| `dropwhile(predicate, iterable)` | Elements from the first one where `predicate` is false. |
| `filterfalse(predicate, iterable)` | Elements where `predicate` is false. |
| `compress(data, selectors)` | Elements of `data` whose matching selector is truthy. |
| `product(*iterables, repeat=1)` | Cartesian product. |
| `permutations(iterable[, r])` | All `r`-length orderings (default: full length). |
| `combinations(iterable, r)` | All `r`-length combinations, no repetition. |
| `combinations_with_replacement(iterable, r)` | All `r`-length combinations, elements may repeat. |
| `groupby(iterable[, key])` | `(key, [elements])` pairs for runs of consecutive equal keys; sort first to group globally. |
| `accumulate(iterable[, func])` | Running totals, or running `func(acc, item)`. |
| `pairwise(iterable)` | Successive overlapping pairs. |
| `batched(iterable, n)` | Tuples of `n` elements; the last may be shorter. |
| `starmap(func, iterable)` | `func(*args)` for each argument tuple. |

## Example

```python
import itertools

# Chaining, repeating, zipping
print(itertools.chain([1, 2], [3, 4], "ab"))        # [1, 2, 3, 4, 'a', 'b']
print(itertools.cycle([1, 2], 3))                   # [1, 2, 1, 2, 1, 2]
print(list(itertools.repeat("x", 3)))               # ['x', 'x', 'x']
print(itertools.zip_longest([1, 2, 3], ["a"], fillvalue="-"))  # [(1, 'a'), (2, '-'), (3, '-')]

# Slicing and filtering
print(list(itertools.islice(itertools.count(0, 2), 5)))   # [0, 2, 4, 6, 8]
print(itertools.islice([0, 1, 2, 3, 4], 1, 4))      # [1, 2, 3]
print(itertools.takewhile(lambda x: x < 5, [1, 3, 5, 2]))   # [1, 3]
print(itertools.dropwhile(lambda x: x < 5, [1, 3, 5, 2]))   # [5, 2]
print(itertools.filterfalse(lambda x: x % 2, [1, 2, 3, 4]))  # [2, 4]
print(itertools.compress("abcd", [1, 0, 1, 0]))     # ['a', 'c']

# Combinatorics
print(itertools.product([1, 2], "ab"))              # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
print(itertools.product([0, 1], repeat=2))          # [(0, 0), (0, 1), (1, 0), (1, 1)]
print(itertools.permutations("abc", 2))             # [('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]
print(itertools.combinations([1, 2, 3], 2))         # [(1, 2), (1, 3), (2, 3)]
print(itertools.combinations_with_replacement([1, 2], 2))  # [(1, 1), (1, 2), (2, 2)]

# Grouping, accumulating, pairing
print(itertools.groupby(["aa", "ab", "ba"], lambda s: s[0]))  # [('a', ['aa', 'ab']), ('b', ['ba'])]
print(itertools.accumulate([100, 200, 150]))        # [100, 300, 450]
print(itertools.accumulate([1, 2, 3, 4], lambda a, b: a * b))  # [1, 2, 6, 24]
print(itertools.pairwise([1, 2, 3]))                # [(1, 2), (2, 3)]
print(itertools.batched([1, 2, 3, 4, 5], 2))        # [(1, 2), (3, 4), (5,)]
print(itertools.starmap(pow, [(2, 3), (3, 2)]))     # [8, 9]
```

## Differences from Python

- Results are lists, so they can be indexed and printed directly but are built eagerly. Avoid huge combinatorial inputs. `count()`, `repeat()` and `cycle()` without a count are iterators, as in Python.
- Passing an endless iterator (`count()`, `cycle()`, `repeat()` without a count) to a function that builds a list, such as `dropwhile()` or `list()`, raises an error instead of running out of memory. Bound it with `islice()` first.
- `groupby()` returns a list of `(key, list)` pairs rather than lazy groupers.
- `tee()` and `chain.from_iterable()` are not available; use `itertools.chain(*nested)` to flatten.

## See Also

- [functools](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/functools.md): `reduce()` for collapsing an iterable to a single value.
- [collections](https://scriptling.dev/okf/scriptling-libraries/collections-iteration/collections.md): `deque` and other specialized containers.
