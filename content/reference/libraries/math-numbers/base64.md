---
title: base64
description: Base64 encoding and decoding.
tags: [libraries, math]
weight: 6

aliases:
  - /reference/libraries/stdlib/base64/
  - /reference/libraries/base64/
---

The `base64` library encodes and decodes data using standard Base64, with Python-compatible function names. Inputs may be a [`bytes`](../../data-formats/bytes/) value or a string (UTF-8 encoded); decoding always returns a [`bytes`](../../data-formats/bytes/) value, so call `.decode()` on the result if you need a string.

## Available Functions

| Function | Description |
|----------|-------------|
| `b64encode(s)` | Encode a `bytes` or `str` value to Base64. |
| `b64decode(s)` | Decode a Base64 string, returning `bytes`. |

## Functions

### `b64encode(s)`

Encodes a value to standard Base64.

**Parameters:**
- `s` (`bytes` or `str`): Value to encode. Strings are encoded as UTF-8 first.

**Returns:** `str`: the Base64-encoded result.

```python
import base64

encoded = base64.b64encode("hello world")
print(encoded)  # "aGVsbG8gd29ybGQ="

# Bytes input is also accepted
encoded = base64.b64encode(bytes("hello world"))
```

### `b64decode(s)`

Decodes a standard Base64 string.

**Parameters:**
- `s` (`str`): Base64-encoded string to decode.

**Returns:** [`bytes`](../../data-formats/bytes/): the decoded binary data. Call `.decode()` to convert to a string when the underlying data is text.

**Raises:** `Error`: if `s` is not valid Base64.

```python
import base64

decoded = base64.b64decode("aGVsbG8gd29ybGQ=")
print(decoded.decode())  # "hello world"
```

## See Also

- [hashlib](../hashlib/): cryptographic hash functions.
- [hmac](../hmac/): message authentication codes.
- [bytes](../../data-formats/bytes/): the binary type returned by `b64decode()`.
