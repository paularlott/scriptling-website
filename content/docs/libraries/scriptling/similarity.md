---
title: scriptling.similarity
linkTitle: similarity
weight: 1
---

The `scriptling.similarity` library provides text similarity utilities for fuzzy matching, tokenization, and MinHash signatures.

## Available Functions

| Function | Description |
| --- | --- |
| `search(query, items, max_results, threshold, key)` | Find multiple fuzzy matches in a list |
| `best(query, items, entity_type, key, threshold)` | Find the best fuzzy match with error formatting |
| `score(s1, s2)` | Calculate fuzzy similarity between two strings |
| `tokenize(text)` | Split text into lowercase alphanumeric tokens |
| `minhash(text, num_hashes=64)` | Compute a MinHash signature for text |
| `minhash_similarity(a, b)` | Compare two MinHash signatures |

## Functions

### scriptling.similarity.search(query, items, max_results=5, threshold=0.5, key="name")

Searches for fuzzy matches in a list of strings or dicts.

**Parameters:**

- `query` (string): The search string to match against
- `items` (list): List of strings or dicts to search
- `max_results` (int, optional): Maximum number of results to return (default: 5)
- `threshold` (float, optional): Minimum similarity score (default: 0.5)
- `key` (string, optional): Dict key to use for matching when items are dicts (default: `"name"`)

**Returns:** `list` - List of matching items sorted by similarity

**Example:**

```python
import scriptling.similarity as sim

projects = [
    {"id": 1, "name": "Website Redesign"},
    {"id": 2, "name": "Mobile App Development"},
    {"id": 3, "name": "Server Migration"},
]

results = sim.search("web", projects, max_results=3)
```

### scriptling.similarity.best(query, items, entity_type="item", key="name", threshold=0.5)

Finds the best fuzzy match and returns either a match or a helpful error.

**Parameters:**

- `query` (string): The search string to match against
- `items` (list): List of strings or dicts to search
- `entity_type` (string, optional): Name used in error messages (default: `"item"`)
- `key` (string, optional): Dict key to use for matching when items are dicts (default: `"name"`)
- `threshold` (float, optional): Minimum similarity score (default: 0.5)

**Returns:** `dict` - Dict with `found` (bool), and either the matched item or an `error` message

**Example:**

```python
import scriptling.similarity as sim

match = sim.best("website redesign", projects, entity_type="project")
if match["found"]:
    print(match["id"])
else:
    print(match["error"])
```

### scriptling.similarity.score(s1, s2)

Returns a fuzzy similarity score between two strings.

**Parameters:**

- `s1` (string): First string
- `s2` (string): Second string

**Returns:** `float` - Similarity score between `0.0` and `1.0`

**Example:**

```python
import scriptling.similarity as sim

score = sim.score("hello", "hallo")
```

### scriptling.similarity.tokenize(text)

Splits text into lowercase alphanumeric tokens.

**Parameters:**

- `text` (string): Text to tokenize

**Returns:** `list` - List of lowercase alphanumeric tokens

**Example:**

```python
import scriptling.similarity as sim

tokens = sim.tokenize("Hello, world! 123")
# ["hello", "world", "123"]
```

### scriptling.similarity.minhash(text, num_hashes=64)

Computes a MinHash signature suitable for approximate similarity checks.

**Parameters:**

- `text` (string): Text to compute the signature for
- `num_hashes` (int, optional): Number of hash functions to use (default: 64)

**Returns:** `list` - List of integers representing the MinHash signature

**Example:**

```python
import scriptling.similarity as sim

sig = sim.minhash("The quick brown fox jumps over the lazy dog")
```

### scriptling.similarity.minhash_similarity(a, b)

Returns the fraction of matching positions between two MinHash signatures.

**Parameters:**

- `a` (list): First MinHash signature
- `b` (list): Second MinHash signature

**Returns:** `float` - Fraction of matching positions between `0.0` and `1.0`

**Example:**

```python
import scriptling.similarity as sim

a = sim.minhash("The quick brown fox")
b = sim.minhash("A quick brown fox")
score = sim.minhash_similarity(a, b)
```

## Notes

- `search`, `best`, and `score` are the home for the old fuzzy-matching API.
- `minhash` uses 64 hashes by default, which is a good balance for lightweight similarity estimation.
- `tokenize` and `minhash` are useful for memory stores, semantic recall, and approximate deduplication.
