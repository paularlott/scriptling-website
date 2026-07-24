---
title: hmac
description: Keyed-hashing for message authentication (HMAC).
tags: [libraries, math, security]
weight: 2

aliases:
  - /reference/libraries/stdlib/hmac/
  - /reference/libraries/hmac/
---

The `hmac` library computes and verifies message authentication codes, most commonly to verify webhook signatures. Keys and messages may be passed as strings (UTF-8 encoded), [`bytes`](../../data-formats/bytes/) values, or lists of byte values (as returned by `str.encode()`).

## Available Functions

| Function | Description |
|----------|-------------|
| `new(key, msg=None, digestmod=None)` | Create an HMAC object. |
| `digest(key, msg, digestmod)` | One-shot HMAC, returning the raw digest as a [`bytes`](../../data-formats/bytes/) value. |
| `compare_digest(a, b)` | Constant-time string comparison (timing-safe). |

## Functions

### `new(key, msg=None, digestmod=None)`

Creates an HMAC object.

**Parameters:**
- `key` (`str`, `bytes`, or `list`): Secret key (string encoded as UTF-8, a `bytes` value, or a list of byte values).
- `msg` (`str`, `bytes`, or `list`, optional): Initial message data. Default: `None`.
- `digestmod` (`str` or callable, optional): `"sha256"` (default), `"sha1"`, `"md5"`, or a `hashlib` constructor such as `hashlib.sha256`.

**Returns:** `HMAC`: an instance supporting `.update()`, `.hexdigest()`, `.digest()`, and `.copy()` (see HMAC Object Methods below).

```python
import hmac

sig = hmac.new("secret", "payload", "sha256").hexdigest()
print(sig)
```

### `digest(key, msg, digestmod)`

One-shot HMAC, computing the digest directly without creating a reusable object.

**Parameters:**
- `key` (`str`, `bytes`, or `list`): Secret key.
- `msg` (`str`, `bytes`, or `list`): Message data.
- `digestmod` (`str` or callable): `"sha256"`, `"sha1"`, `"md5"`, or a `hashlib` constructor.

**Returns:** [`bytes`](../../data-formats/bytes/): the raw digest.

```python
import hmac

mac = hmac.digest("secret", "payload", "sha256")
```

### `compare_digest(a, b)`

Compares two strings in constant time, so that timing differences do not leak information about how many leading bytes matched. Use this instead of `==` when comparing signature values.

**Parameters:**
- `a` (`str`): First string.
- `b` (`str`): Second string.

**Returns:** `bool`: `True` if equal, `False` otherwise.

```python
import hmac

ok = hmac.compare_digest(expected, received)
```

## HMAC Object Methods

Objects returned by `new()` support:

| Method / Field | Description |
|----------------|-------------|
| `.update(data)` | Feed more data into the message. Returns `None`. |
| `.hexdigest()` | Return the MAC as a lowercase hex string. |
| `.digest()` | Return the MAC as a [`bytes`](../../data-formats/bytes/) value. |
| `.copy()` | Return an independent copy of the HMAC object. |
| `.name` | Algorithm name, e.g. `"hmac-sha256"`. |
| `.digest_size` | Digest size in bytes. |
| `.block_size` | Block size in bytes. |

## Verifying a Webhook Signature

This is the canonical use case: recomputing the HMAC of a request body with a shared secret and comparing it against the signature header:

```python
import hmac
import hashlib

def verify(body, signature, secret):
    expected = "sha256=" + hmac.new(
        secret.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

body = "the raw request body"
secret = "your-webhook-secret"
good_sig = "sha256=" + hmac.new(secret.encode(), body, "sha256").hexdigest()

print(verify(body, good_sig, secret))           # True
print(verify(body, "sha256=tampered", secret))  # False
```

> **Note:** Scriptling does not support parameter type annotations, so write
> `def verify(body, signature, secret):` rather than
> `def verify(body: bytes, ...) -> bool:`.

## See Also

- [hashlib](../hashlib/): cryptographic hash functions, including the constructors accepted as `digestmod`.
- [secrets](../../http-process/secrets/): `token_hex()` for generating a new random secret key.
- [base64](../base64/): Base64 encoding and decoding.
- [bytes](../../data-formats/bytes/): the binary type returned by `.digest()` and `digest()`.
