---
title: scriptling.similarity
linkTitle: similarity
description: Text similarity utilities for fuzzy matching, tokenization, and MinHash signatures.
weight: 1
---

The `scriptling.similarity` library provides text similarity utilities for fuzzy matching, tokenization, and MinHash signatures. Reach for `search`/`best`/`score` when matching free-text input against a known list of items, and `tokenize`/`minhash`/`minhash_similarity` for lightweight approximate similarity over larger bodies of text.

## Available Functions

| Function | Description |
|----------|-------------|
| `search(query, items, max_results=5, threshold=0.5, key="name")` | Find multiple fuzzy matches in a list |
| `best(query, items, entity_type="item", key="name", threshold=0.5)` | Find the best fuzzy match with error formatting |
| `score(s1, s2)` | Calculate fuzzy similarity between two strings |
| `tokenize(text)` | Split text into lowercase alphanumeric tokens |
| `minhash(text, num_hashes=64)` | Compute a MinHash signature for text |
| `minhash_similarity(a, b)` | Compare two MinHash signatures |

## Functions

### `search(query, items, max_results=5, threshold=0.5, key="name")`

Searches for fuzzy matches in a list of strings or dicts, using a multi-tier algorithm (exact, then substring, then word boundary, then Levenshtein distance).

**Parameters:**
- `query` (`str`): The search string to match against.
- `items` (`list`): List of strings or dicts to search.
- `max_results` (`int`, optional): Maximum number of results to return. Default: `5`.
- `threshold` (`float`, optional): Minimum similarity score. Default: `0.5`.
- `key` (`str`, optional): Dict key to use for matching when items are dicts. Default: `"name"`.

**Returns:** `list`: matching items sorted by similarity, each a `dict` with `id`, `name`, and `score`.

```python
import scriptling.similarity as sim

projects = [
    {"id": 1, "name": "Website Redesign"},
    {"id": 2, "name": "Mobile App Development"},
    {"id": 3, "name": "Server Migration"},
]

results = sim.search("web", projects, max_results=3)
```

### `best(query, items, entity_type="item", key="name", threshold=0.5)`

Finds the best fuzzy match and returns either a match or a helpful error.

**Parameters:**
- `query` (`str`): The search string to match against.
- `items` (`list`): List of strings or dicts to search.
- `entity_type` (`str`, optional): Name used in error messages. Default: `"item"`.
- `key` (`str`, optional): Dict key to use for matching when items are dicts. Default: `"name"`.
- `threshold` (`float`, optional): Minimum similarity score. Default: `0.5`.

**Returns:** `dict`: `{"found": bool, "id", "name", "score", "error"}`. When `found` is `True`, `id`/`name`/`score` hold the match and `error` is `None`; when `False`, `error` holds a message and the others are `None`.

```python
import scriptling.similarity as sim

match = sim.best("website redesign", projects, entity_type="project")
if match["found"]:
    print(match["id"])
else:
    print(match["error"])
```

### `score(s1, s2)`

Returns a fuzzy similarity score between two strings, using edit-distance based matching.

**Parameters:**
- `s1` (`str`): First string.
- `s2` (`str`): Second string.

**Returns:** `float`: similarity score between `0.0` and `1.0`.

```python
import scriptling.similarity as sim

score = sim.score("hello", "hallo")
```

### `tokenize(text)`

Splits text into lowercase alphanumeric tokens. Only letters a-z and digits 0-9 are retained; everything else becomes a word boundary.

**Parameters:**
- `text` (`str`): Text to tokenize.

**Returns:** `list` of `str`: lowercase alphanumeric tokens.

```python
import scriptling.similarity as sim

tokens = sim.tokenize("Hello, world! 123")
# ["hello", "world", "123"]
```

### `minhash(text, num_hashes=64)`

Computes a MinHash signature suitable for approximate similarity checks.

**Parameters:**
- `text` (`str`): Text to compute the signature for.
- `num_hashes` (`int`, optional): Number of hash functions to use. Default: `64`.

**Returns:** `list` of `int`: the MinHash signature.

```python
import scriptling.similarity as sim

sig = sim.minhash("The quick brown fox jumps over the lazy dog")
```

### `minhash_similarity(a, b)`

Returns the fraction of matching positions between two MinHash signatures: an estimate of Jaccard similarity.

**Parameters:**
- `a` (`list`): First MinHash signature.
- `b` (`list`): Second MinHash signature.

**Returns:** `float`: fraction of matching positions between `0.0` and `1.0`.

```python
import scriptling.similarity as sim

a = sim.minhash("The quick brown fox")
b = sim.minhash("A quick brown fox")
score = sim.minhash_similarity(a, b)
```

## Notes

- `search`, `best`, and `score` are the home for the fuzzy-matching API.
- `minhash` uses 64 hashes by default, which is a good balance for lightweight similarity estimation.
- `tokenize` and `minhash` are useful for memory stores, semantic recall, and approximate deduplication.

## See Also

- [scriptling.toon](../toon/) - Compact data encoding, often paired with similarity search over decoded records
