---
title: difflib
weight: 3
---

Helpers for computing deltas between sequences. Provides unified diff generation, similarity ratios, and close-match finding — matching Python 3's `difflib` module behaviour.

## Available Functions

| Function | Description |
| -------- | ----------- |
| `unified_diff(a, b, fromfile="", tofile="", n=3)` | Return a unified format diff string |
| `ratio(a, b)` | Return a similarity ratio between 0.0 and 1.0 |
| `opcodes(a, b)` | Return list of edit operations turning `a` into `b` |
| `get_close_matches(word, possibilities, n=3, cutoff=0.6)` | Return best matches from a list |

## unified_diff

Returns a unified diff string comparing two multi-line strings. The output format matches `diff -u` and is suitable for display or passing to LLMs.

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

Returns an empty string if the inputs are identical.

The `n` parameter controls lines of context (default 3).

## ratio

Returns a float between 0.0 (completely different) and 1.0 (identical) indicating how similar two strings are. Operates character-by-character, matching Python's `SequenceMatcher` behaviour.

```python
import difflib

print(difflib.ratio("hello", "hello"))   # 1.0
print(difflib.ratio("hello", "world"))   # 0.4
print(difflib.ratio("", ""))             # 1.0
```

## opcodes

Returns a list of `(tag, i1, i2, j1, j2)` tuples describing the edit operations needed to turn `a` into `b`, operating on lines. Tags are `"equal"`, `"insert"`, `"delete"`, or `"replace"`.

```python
import difflib

ops = difflib.opcodes("line1\nline2\nline3\n", "line1\nLINE2\nline3\n")
for tag, i1, i2, j1, j2 in ops:
    print(tag, i1, i2, j1, j2)
# equal 0 1 0 1
# replace 1 2 1 2
# equal 2 3 2 3
```

## get_close_matches

Returns a list of the best matches for `word` from `possibilities`, sorted by similarity. Returns at most `n` matches with a similarity ratio of at least `cutoff`.

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

## Usage Examples

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
