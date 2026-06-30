---
title: base64
description: Base64 encoding and decoding.
weight: 1

aliases:
  - /reference/libraries/stdlib/base64/
  - /reference/libraries/base64/
---

The `base64` library encodes and decodes strings using standard Base64, with Python-compatible function names. Scriptling has no dedicated `bytes` type, so strings are used as byte buffers throughout.

## Available Functions

| Function | Description |
|----------|-------------|
| `b64encode(s)` | Encode a string to Base64. |
| `b64decode(s)` | Decode a Base64 string. |

## Functions

### `b64encode(s)`

Encodes a string to standard Base64.

**Parameters:**
- `s` (`str`): String to encode (treated as raw bytes).

**Returns:** `str`: the Base64-encoded result.

```python
import base64

encoded = base64.b64encode("hello world")
print(encoded)  # "aGVsbG8gd29ybGQ="
```

### `b64decode(s)`

Decodes a standard Base64 string.

**Parameters:**
- `s` (`str`): Base64-encoded string to decode.

**Returns:** `str`: the decoded result.

**Raises:** `Error`: if `s` is not valid Base64.

```python
import base64

decoded = base64.b64decode("aGVsbG8gd29ybGQ=")
print(decoded)  # "hello world"
```

## See Also

- [hashlib](../hashlib/): cryptographic hash functions.
- [hmac](../hmac/): message authentication codes.
