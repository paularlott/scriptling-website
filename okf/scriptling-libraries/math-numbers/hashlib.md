---
description: Cryptographic hash functions.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/math-numbers/hashlib/
sources:
    - resource: https://scriptling.dev/reference/libraries/math-numbers/hashlib/
status: stable
tags:
    - libraries
    - math
    - security
title: hashlib
type: API Reference
---
# hashlib

The `hashlib` library provides cryptographic hash functions (MD5, SHA-1, SHA-256). Its constructors return **hash objects** rather than raw strings: call `.hexdigest()` (lowercase hex) or `.digest()` (raw binary as a [`bytes`](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md) value) on the returned object to get the result.

## Available Functions

| Function | Description |
|----------|-------------|
| `md5([data])` | Create an MD5 hash object. |
| `sha1([data])` | Create a SHA-1 hash object. |
| `sha256([data])` | Create a SHA-256 hash object. |

## Functions

### `sha256([data])`

Creates a SHA-256 hash object, optionally seeded with `data`.

**Parameters:**
- `data` (`str`, `bytes`, or `list`, optional): Initial data to hash: a string (encoded as UTF-8), a `bytes` value, or a list of byte values (as returned by `str.encode()`).

**Returns:** `Hash`: an instance supporting `.update()`, `.hexdigest()`, `.digest()`, and `.copy()` (see Hash Object Methods below).

```python
import hashlib

h = hashlib.sha256("hello")
print(h.hexdigest())  # "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
print(h.name)         # "sha256"
print(h.digest_size)  # 32
```

### `sha1([data])`

Creates a SHA-1 hash object, optionally seeded with `data`.

**Parameters:**
- `data` (`str` or `list`, optional): Initial data to hash.

**Returns:** `Hash`: `.hexdigest()` is 40 hex characters.

```python
import hashlib

print(hashlib.sha1("hello").hexdigest())  # "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
```

### `md5([data])`

Creates an MD5 hash object, optionally seeded with `data`.

**Parameters:**
- `data` (`str` or `list`, optional): Initial data to hash.

**Returns:** `Hash`: `.hexdigest()` is 32 hex characters.

```python
import hashlib

print(hashlib.md5("hello").hexdigest())  # "5d41402abc4b2a76b9719d911017c592"
```

## Hash Object Methods

Objects returned by `md5()`, `sha1()`, and `sha256()` support:

| Method / Field | Description |
|----------------|-------------|
| `.update(data)` | Feed more data into the hash. Returns `None`. |
| `.hexdigest()` | Return the digest as a lowercase hex string. |
| `.digest()` | Return the digest as a [`bytes`](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md) value. |
| `.copy()` | Return an independent copy of the hash object. |
| `.name` | Algorithm name, e.g. `"sha256"`. |
| `.digest_size` | Digest size in bytes (`md5` 16, `sha1` 20, `sha256` 32). |
| `.block_size` | Block size in bytes (`64` for all supported algorithms). |

```python
import hashlib

# Build a hash incrementally
h = hashlib.sha256()
h.update("foo")
h.update("bar")
assert h.hexdigest() == hashlib.sha256("foobar").hexdigest()

# copy() is independent
c = h.copy()
h.update("baz")
assert c.hexdigest() == hashlib.sha256("foobar").hexdigest()
assert h.hexdigest() == hashlib.sha256("foobarbaz").hexdigest()
```

## See Also

- [hmac](https://scriptling.dev/okf/scriptling-libraries/math-numbers/hmac.md): message authentication codes, often paired with `hashlib` constructors.
- [base64](https://scriptling.dev/okf/scriptling-libraries/math-numbers/base64.md): Base64 encoding and decoding.
- [bytes](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md): the binary type returned by `.digest()`.
