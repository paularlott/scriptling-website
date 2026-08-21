---
description: Compute deltas between sequences, including unified diffs, similarity ratios, and close-match finding.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/text-processing/difflib/
sources:
    - resource: https://scriptling.dev/reference/libraries/text-processing/difflib/
status: stable
tags:
    - libraries
    - text
title: difflib
type: API Reference
---
# difflib

Helpers for computing deltas between sequences. Provides unified diff generation, similarity ratios, and close-match finding: matching Python 3's `difflib` module behavior.

## Available Functions

| Function | Description |
|----------|-------------|
| `unified_diff(a, b, fromfile="", tofile="", n=3)` | Return a unified format diff string. |
| `ratio(a, b)` | Return a similarity ratio between 0.0 and 1.0. |
| `opcodes(a, b)` | Return a list of edit operations turning `a` into `b`. |
| `get_close_matches(word, possibilities, n=3, cutoff=0.6)` | Return the best matches for `word` from a list of possibilities. |

## Functions

### `unified_diff(a, b, fromfile="", tofile="", n=3)`

Returns a unified diff string comparing two multi-line strings, line by line. The output format matches `diff -u` and is suitable for display or passing to LLMs. Returns an empty string if the inputs are identical.

**Parameters:**

- `a` (`str`): The original text.
- `b` (`str`): The modified text.
- `fromfile` (`str`, keyword-only, optional): Label used for the `---` header line. Default: `""`.
- `tofile` (`str`, keyword-only, optional): Label used for the `+++` header line. Default: `""`.
- `n` (`int`, keyword-only, optional): Number of lines of context shown around each change. Default: `3`.

**Returns:** `str`: a unified diff, or an empty string if `a` and `b` are identical.

```python
import difflib

a = "line1\nline2\nline3\n"
b = "line1\nLINE2\nline3\n"

diff = difflib.unified_diff(a, b, fromfile="before.txt", tofile="after.txt")
print(diff)
# --- before.txt
# +++ after.txt
# @@ -1,3 +1,3 @@
#  line1
# -line2
# +LINE2
#  line3
```

### `ratio(a, b)`

Returns a float between `0.0` (completely different) and `1.0` (identical) indicating how similar two strings are. Operates character-by-character, matching Python's `SequenceMatcher` behavior. The result is rounded to two decimal places.

**Parameters:**

- `a` (`str`): The first string.
- `b` (`str`): The second string.

**Returns:** `float`: similarity ratio between `0.0` and `1.0`.

```python
import difflib

print(difflib.ratio("hello", "hello"))   # 1.0
print(difflib.ratio("hello", "world"))   # 0.4
print(difflib.ratio("", ""))             # 1.0
```

### `opcodes(a, b)`

Returns a list of `(tag, i1, i2, j1, j2)` tuples describing the edit operations needed to turn `a` into `b`, operating on lines. Tags are `"equal"`, `"insert"`, `"delete"`, or `"replace"`.

**Parameters:**

- `a` (`str`): The original text.
- `b` (`str`): The modified text.

**Returns:** `list`: a list of `(tag, i1, i2, j1, j2)` tuples.

```python
import difflib

ops = difflib.opcodes("line1\nline2\nline3\n", "line1\nLINE2\nline3\n")
for tag, i1, i2, j1, j2 in ops:
    print(tag, i1, i2, j1, j2)
# equal 0 1 0 1
# replace 1 2 1 2
# equal 2 3 2 3
```

### `get_close_matches(word, possibilities, n=3, cutoff=0.6)`

Returns a list of the best matches for `word` from `possibilities`, sorted by similarity (best match first). Returns at most `n` matches, each with a similarity ratio of at least `cutoff`.

**Parameters:**

- `word` (`str`): The string to match against.
- `possibilities` (`list`): List of candidate strings.
- `n` (`int`, optional): Maximum number of matches to return. Default: `3`.
- `cutoff` (`float`, optional): Minimum similarity ratio (0.0 to 1.0) for a candidate to be included. Default: `0.6`.

**Returns:** `list`: matching strings from `possibilities`, ordered by similarity.

```python
import difflib

matches = difflib.get_close_matches("appel", ["ape", "apple", "peach", "puppy"])
print(matches)  # ["apple", "ape"]

# Stricter cutoff
matches = difflib.get_close_matches("appel", ["ape", "apple", "peach"], cutoff=0.8)
print(matches)  # ["apple"]

# Limit results
matches = difflib.get_close_matches("appel", ["ape", "apple", "peach"], n=1)
print(matches)  # ["apple"]
```

## Examples

### Comparing API responses

```python
import difflib
import requests

before = requests.get("https://api.example.com/config/v1").text
after  = requests.get("https://api.example.com/config/v2").text

diff = difflib.unified_diff(before, after, fromfile="v1", tofile="v2")
if diff:
    print("Changes detected:")
    print(diff)
else:
    print("No changes")
```

### Fuzzy command matching

```python
import difflib

commands = ["start", "stop", "restart", "status", "reload"]
user_input = "statsu"

suggestions = difflib.get_close_matches(user_input, commands)
if suggestions:
    print(f"Did you mean: {suggestions[0]}?")
```

### Similarity check before update

```python
import difflib

def has_significant_change(old, new, threshold=0.9):
    return difflib.ratio(old, new) < threshold

if has_significant_change(old_content, new_content):
    print("Warning: large change detected")
```

## See Also

- [string](string.md) - String constants for character classification
- [textwrap](textwrap.md) - Text wrapping and filling utilities
- [regex](regex.md) - Regular expressions for pattern matching
