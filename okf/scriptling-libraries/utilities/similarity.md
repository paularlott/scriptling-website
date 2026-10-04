---
description: Text similarity utilities for fuzzy matching, tokenization, MinHash signatures, and extractive text shortening.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/utilities/similarity/
sources:
    - resource: https://scriptling.dev/reference/libraries/utilities/similarity/
status: stable
tags:
    - libraries
    - utilities
    - text
title: scriptling.similarity
type: API Reference
---
# scriptling.similarity

The `scriptling.similarity` library provides text similarity utilities for fuzzy matching, tokenization, MinHash signatures, and extractive text shortening. Reach for `search`/`best`/`score` when matching free-text input against a known list of items, `tokenize`/`minhash`/`minhash_similarity` for lightweight approximate similarity over larger bodies of text, and `sentences`/`extract` to shorten a long text to its most informative sentences before handing it to a model.

## Available Functions

| Function | Description |
|----------|-------------|
| `search(query, items, max_results=5, threshold=0.5, key="name")` | Find multiple fuzzy matches in a list |
| `best(query, items, entity_type="item", key="name", threshold=0.5)` | Find the best fuzzy match with error formatting |
| `score(s1, s2)` | Calculate fuzzy similarity between two strings |
| `tokenize(text)` | Split text into lowercase alphanumeric tokens |
| `minhash(text, num_hashes=64)` | Compute a MinHash signature for text |
| `minhash_similarity(a, b)` | Compare two MinHash signatures |
| `cosine_similarity(a, b)` | Compare two numeric vectors (-1.0 to 1.0) |
| `most_similar(query, vectors, top_k=5)` | Rank vectors by similarity to a query |
| `vectorize(text, dims=256)` | Generate a vector from text (CPU-only, no model) |
| `sentences(text)` | Split text into sentences |
| `extract(text, max_chars=None, max_sentences=None, ratio=None)` | Keep the most informative sentences within a bound (CPU-only, no model) |

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

### `cosine_similarity(a, b)`

Compute the cosine of the angle between two numeric vectors. Returns a score from -1.0 (opposite) to 1.0 (identical direction); 0.0 means orthogonal. Works with embedding vectors from [`scriptling.ai`](https://scriptling.dev/okf/scriptling-libraries/ai.md)'s `client.embedding()` or with vectors from `vectorize()`.

**Parameters:**
- `a` (`list[float]`): First vector.
- `b` (`list[float]`): Second vector (same length as `a`).

**Returns:** `float`: similarity score from -1.0 to 1.0.

```python
import scriptling.similarity as sim

v1 = sim.vectorize("the quick brown fox")
v2 = sim.vectorize("the quick red fox")
score = sim.cosine_similarity(v1, v2)  # high — shares most words
```

### `most_similar(query, vectors, top_k=5)`

Rank a list of vectors by cosine similarity to a query vector, returning the top results.

**Parameters:**
- `query` (`list[float]`): Query vector.
- `vectors` (`list[list[float]]`): Candidate vectors to search.
- `top_k` (`int`, keyword-only): Maximum results to return. Default: `5`.

**Returns:** `list[dict]`: `[{"index": int, "score": float}, ...]` sorted by descending score.

```python
import scriptling.similarity as sim

docs = ["hello world", "quick fox", "goodbye world"]
vectors = [sim.vectorize(d) for d in docs]
results = sim.most_similar(sim.vectorize("hi world"), vectors, top_k=2)
for r in results:
    print(f"  {docs[r['index']]}: {r['score']:.3f}")
```

### `vectorize(text, dims=256)`

Generate a fixed-dimensional vector from text using the feature-hashing trick (CPU-only, no model or API call). Each word is hashed to a dimension with a +1/−1 sign, then the vector is L2-normalised so it can be compared directly with `cosine_similarity()`. Similar texts (sharing words) produce similar vectors.

**Parameters:**
- `text` (`str`): Text to vectorise.
- `dims` (`int`, keyword-only): Output dimension. Default: `256`.

**Returns:** `list[float]`: normalised vector of length `dims`.

```python
import scriptling.similarity as sim

v = sim.vectorize("hello world", dims=128)
print(len(v))  # 128
```

### `sentences(text)`

Split text into sentences. A sentence ends at `". "`, `"! "` or `"? "` when the next character is a capital letter, digit or opening quote, so `"e.g. this"` and `"3.5 mm"` stay whole, and at every line break, so transcripts, chat logs and pasted output split one line per sentence. Sentences are trimmed and empty ones dropped.

**Parameters:**
- `text` (`str`): Text to split.

**Returns:** `list[str]`: sentences in order; an empty list for blank text, never `None`.

```python
import scriptling.similarity as sim

sim.sentences("Hello world. This is a test! Is it?\nA new line here")
# ["Hello world.", "This is a test!", "Is it?", "A new line here"]
```

### `extract(text, max_chars=None, max_sentences=None, ratio=None)`

Keep the most informative sentences of a text, in their original order, within the given bounds. CPU-only: no model or API call.

Sentences are scored with TextRank. Each sentence is a node, edges are weighted by the cosine similarity of the sentences' hashed word vectors (the same vectors as `vectorize()`), and the stationary distribution ranks them, so the sentences most representative of the text as a whole score highest. A sentence that repeats, such as a signature carried through a thread, is ranked once and kept at most once, so repetition cannot make it look like the main point. The similarity matrix is built in parallel across CPUs. Text that already fits the bounds is returned unchanged.

Repetitive line-oriented text, such as a log or a stack trace where most lines repeat with only numbers changing, is handled differently: there the rare lines carry the information, so the leading and trailing lines are kept together with the first occurrence of each distinct line, in order, and ranking is not used.

Use `extract` where you would otherwise cut a long text at a fixed length before sending it to a model. The result is the same size but keeps what the text is about rather than whatever happened to come first.

**Parameters:**
- `text` (`str`): The text to shorten.
- `max_chars` (`int`, keyword-only): Keep sentences while the result fits in this many characters.
- `max_sentences` (`int`, keyword-only): Keep at most this many sentences.
- `ratio` (`float`, keyword-only): Keep this fraction of the sentences (`0 < ratio <= 1`).

With no bounds, `ratio` defaults to `0.3`. When several bounds are given, the tightest applies. A single sentence longer than `max_chars` is cut to fit rather than dropped, so the result is never empty for non-empty input.

**Returns:** `str`: the selected sentences, joined with spaces, or with newlines when the input was line-oriented.

```python
import scriptling.similarity as sim

# A long transcript down to roughly 20,000 characters of its most representative lines.
short = sim.extract(transcript, max_chars=20000)

# The gist of a verbose reply.
gist = sim.extract(reply, ratio=0.25)

# Everything but the noise from a pasted log.
log = sim.extract(pasted_log, max_sentences=40)
```

## Notes

- `search`, `best`, and `score` are the home for the fuzzy-matching API.
- `extract` is extractive, not abstractive: it only ever returns sentences that appear in the input, unchanged apart from trimming, so it cannot invent content. Pair it with a model for the summary itself.
- `minhash` uses 64 hashes by default, which is a good balance for lightweight similarity estimation.
- `tokenize` and `minhash` are useful for memory stores, semantic recall, and approximate deduplication.

## See Also

- [scriptling.toon](https://scriptling.dev/okf/scriptling-libraries/utilities/toon.md) - Compact data encoding, often paired with similarity search over decoded records
