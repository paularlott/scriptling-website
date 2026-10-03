---
description: Base64 encoding and decoding.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/math-numbers/base64/
sources:
    - resource: https://scriptling.dev/reference/libraries/math-numbers/base64/
status: stable
tags:
    - libraries
    - math
title: base64
type: API Reference
---
# base64

The `base64` library encodes and decodes data using standard Base64, with Python-compatible function names. Inputs may be a [`bytes`](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md) value or a string (UTF-8 encoded); decoding always returns a [`bytes`](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md) value, so call `.decode()` on the result if you need a string.

## Available Functions

| Function | Description |
|----------|-------------|
| `b64encode(s)` | Encode a `bytes` or `str` value to a Base64 `str`. |
| `b64decode(s)` | Decode a Base64 `str`, returning `bytes`; raises if `s` is not valid Base64. |

## Example

```python
import base64

encoded = base64.b64encode("hello world")      # str input is UTF-8 encoded first
print(encoded)                                 # aGVsbG8gd29ybGQ=
print(base64.b64encode(b"hello world") == encoded)  # True

decoded = base64.b64decode(encoded)            # always bytes
print(decoded)                                 # b'hello world'
print(decoded.decode())                        # hello world
```

## Differences from Python

- `b64encode()` accepts a `str` (encoded as UTF-8) and returns a `str`, where Python requires and returns `bytes`.
- `b64decode()` requires a `str` and raises on invalid input (Python silently discards invalid characters by default).
- Only standard Base64 is provided; there is no `urlsafe_b64encode`, `b32encode`, `b16encode` or `a85encode`.

## See Also

- [hashlib](https://scriptling.dev/okf/scriptling-libraries/math-numbers/hashlib.md): cryptographic hash functions.
- [hmac](https://scriptling.dev/okf/scriptling-libraries/math-numbers/hmac.md): message authentication codes.
- [bytes](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md): the binary type returned by `b64decode()`.
