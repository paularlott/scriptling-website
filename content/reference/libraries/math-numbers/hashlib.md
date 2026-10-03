---
title: hashlib
description: Cryptographic hash functions.
tags: [libraries, math, security]
weight: 4

aliases:
  - /reference/libraries/stdlib/hashlib/
  - /reference/libraries/hashlib/
---

The `hashlib` library provides cryptographic hash functions (MD5, SHA-1, SHA-256). Its constructors return **hash objects** rather than raw strings: call `.hexdigest()` (lowercase hex) or `.digest()` (raw binary as a [`bytes`](../../data-formats/bytes/) value) on the returned object to get the result.

## Available Functions

| Function | Description |
|----------|-------------|
| `md5([data])` | MD5 hash object, optionally seeded with `data`. |
| `sha1([data])` | SHA-1 hash object, optionally seeded with `data`. |
| `sha256([data])` | SHA-256 hash object, optionally seeded with `data`. |

`data` (and the argument to `.update()`) may be a `str`, which is hashed as UTF-8, a `bytes` value, or a list of byte values.

## Hash Object Methods

Objects returned by `md5()`, `sha1()`, and `sha256()` support:

| Method / Field | Description |
|----------------|-------------|
| `.update(data)` | Feed more data into the hash. Returns `None`. |
| `.hexdigest()` | Return the digest as a lowercase hex string. |
| `.digest()` | Return the digest as a [`bytes`](../../data-formats/bytes/) value. |
| `.copy()` | Return an independent copy of the hash object. |
| `.name` | Algorithm name, e.g. `"sha256"`. |
| `.digest_size` | Digest size in bytes (`md5` 16, `sha1` 20, `sha256` 32). |
| `.block_size` | Block size in bytes (`64` for all supported algorithms). |

```python
import hashlib

print(hashlib.sha256("hello").hexdigest())  # 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
print(hashlib.sha1("hello").hexdigest())    # aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
print(hashlib.md5(b"hello").hexdigest())    # 5d41402abc4b2a76b9719d911017c592

h = hashlib.sha256()
h.update("foo")
h.update("bar")
print(h.hexdigest() == hashlib.sha256("foobar").hexdigest())  # True
print(h.name, h.digest_size, len(h.digest()))  # sha256 32 32

c = h.copy()                    # independent of h from here on
h.update("baz")
print(c.hexdigest() == hashlib.sha256("foobar").hexdigest())  # True
```

## Differences from Python

- Strings are accepted directly and hashed as UTF-8 (Python requires `bytes`).
- Only `md5`, `sha1`, and `sha256` exist; there is no `hashlib.new()`, `sha512`, `blake2b`, or other algorithm.

## See Also

- [hmac](../hmac/): message authentication codes, often paired with `hashlib` constructors.
- [base64](../base64/): Base64 encoding and decoding.
- [bytes](../../data-formats/bytes/): the binary type returned by `.digest()`.
