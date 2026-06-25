---
title: hashlib
weight: 1

aliases:
  - /reference/libraries/stdlib/hashlib/
  - /reference/libraries/hashlib/
---

Cryptographic hash functions.

The `hashlib` constructors return **hash objects** rather than raw strings.
Call `.hexdigest()` (lowercase hex) or `.digest()` (raw bytes as a string) on
the returned object to get the result. Scriptling has no dedicated `bytes`
type, so strings are used as byte buffers throughout.

## Available Functions

| Function             | Description                                |
| -------------------- | ------------------------------------------ |
| `md5([data])`        | Create an MD5 hash object                  |
| `sha1([data])`       | Create a SHA-1 hash object                 |
| `sha256([data])`     | Create a SHA-256 hash object               |

## Hash Object Methods

| Method / Field  | Description                                                        |
| --------------- | ----------------------------------------------------------------- |
| `.update(data)` | Feed more data into the hash; returns `None`                       |
| `.hexdigest()`  | Return the digest as a lowercase hex string                       |
| `.digest()`     | Return the digest as a raw byte string                            |
| `.copy()`       | Return an independent copy of the hash object                     |
| `.name`         | Algorithm name, e.g. `"sha256"`                                   |
| `.digest_size`  | Digest size in bytes (`md5` 16, `sha1` 20, `sha256` 32)           |
| `.block_size`   | Block size in bytes (`64` for all supported algorithms)           |

## Functions

### hashlib.sha256([data])

Creates a SHA-256 hash object, optionally seeded with `data`.

**Parameters:**

- `data` (optional): A string (treated as bytes) or a list of byte values
  (as returned by `str.encode()`)

**Returns:** Hash object

**Example:**

```python
import hashlib

h = hashlib.sha256("hello")
print(h.hexdigest())  # "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
print(h.name)         # "sha256"
print(h.digest_size)  # 32
```

### hashlib.sha1([data])

Creates a SHA-1 hash object.

**Returns:** Hash object (`.hexdigest()` is 40 hex chars)

```python
import hashlib

print(hashlib.sha1("hello").hexdigest())  # "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
```

### hashlib.md5([data])

Creates an MD5 hash object.

**Returns:** Hash object (`.hexdigest()` is 32 hex chars)

```python
import hashlib

print(hashlib.md5("hello").hexdigest())  # "5d41402abc4b2a76b9719d911017c592"
```

## Updating and Copying

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

## Usage Example

```python
import hashlib

text = "Hello, World!"

print("MD5:   ", hashlib.md5(text).hexdigest())
print("SHA-1: ", hashlib.sha1(text).hexdigest())
print("SHA-256:", hashlib.sha256(text).hexdigest())

# Consistent results
a = hashlib.sha256("test").hexdigest()
b = hashlib.sha256("test").hexdigest()
print("Consistent:", a == b)  # True
```
