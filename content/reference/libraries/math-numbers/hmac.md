---
title: hmac
weight: 2

aliases:
  - /reference/libraries/stdlib/hmac/
  - /reference/libraries/hmac/
---

Keyed-Hashing for Message Authentication (HMAC).

The `hmac` library is used to compute and verify message authentication codes,
most commonly to verify webhook signatures. Scriptling has no dedicated `bytes`
type, so strings are used as byte buffers; the list of byte values returned by
`str.encode()` is also accepted anywhere a byte buffer is expected.

## Available Functions

| Function                              | Description                                        |
| ------------------------------------- | -------------------------------------------------- |
| `new(key, msg=None, digestmod=None)`  | Create an HMAC object                               |
| `digest(key, msg, digestmod)`         | One-shot HMAC, returns the raw digest byte string   |
| `compare_digest(a, b)`                | Constant-time string comparison (timing-safe)       |

## HMAC Object Methods

| Method / Field  | Description                                                          |
| --------------- | ------------------------------------------------------------------- |
| `.update(data)` | Feed more data into the message; returns `None`                      |
| `.hexdigest()`  | Return the MAC as a lowercase hex string                            |
| `.digest()`     | Return the MAC as a raw byte string                                 |
| `.copy()`       | Return an independent copy of the HMAC object                       |
| `.name`         | Algorithm name, e.g. `"hmac-sha256"`                                |
| `.digest_size`  | Digest size in bytes                                                |
| `.block_size`   | Block size in bytes                                                 |

## Functions

### hmac.new(key, msg=None, digestmod=None)

Creates an HMAC object.

**Parameters:**

- `key`: Secret key (string as bytes, or a list of byte values)
- `msg` (optional): Initial message data
- `digestmod` (optional): `"sha256"` (default), `"sha1"`, `"md5"`, or a
  `hashlib` constructor such as `hashlib.sha256`

**Returns:** HMAC object

```python
import hmac

sig = hmac.new("secret", "payload", "sha256").hexdigest()
print(sig)
```

### hmac.digest(key, msg, digestmod)

One-shot HMAC returning the raw digest as a byte string.

```python
import hmac

mac = hmac.digest("secret", "payload", "sha256")
```

### hmac.compare_digest(a, b)

Constant-time comparison of two strings, to be used when comparing signature
values so that timing differences do not leak information.

**Returns:** `True` if equal, `False` otherwise

```python
import hmac

ok = hmac.compare_digest(expected, received)
```

## Verifying a Webhook Signature

This is the canonical use case — recomputing the HMAC of a request body with a
shared secret and comparing it against the signature header:

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

print(verify(body, good_sig, secret))      # True
print(verify(body, "sha256=tampered", secret))  # False
```

> **Note:** Scriptling does not support parameter type annotations, so write
> `def verify(body, signature, secret):` rather than
> `def verify(body: bytes, ...) -> bool:`.

## Generating a Secret Key

To generate a new random secret, use the [`secrets`](../) library:

```python
import secrets

secret = secrets.token_hex(32)  # 64-character hex string
```
