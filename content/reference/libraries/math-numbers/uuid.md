---
title: uuid
description: UUID generation, matching Python's uuid module.
tags: [libraries, math]
weight: 7

aliases:
  - /reference/libraries/stdlib/uuid/
  - /reference/libraries/uuid/
---

The `uuid` library generates universally unique identifiers (UUIDs) using time-based, random, name-based or sortable timestamp-based schemes. Each function returns a `UUID` object; `str(u)` gives the canonical form such as `"550e8400-e29b-41d4-a716-446655440000"`.

## Available Functions

| Function | Description |
|----------|-------------|
| `uuid1()` | Version 1 UUID from the current time and MAC address. |
| `uuid4()` | Version 4 (random) UUID; the usual general-purpose choice. |
| `uuid3(namespace, name)` | Version 3 (MD5, name-based) UUID; the same inputs always give the same UUID. |
| `uuid5(namespace, name)` | Version 5 (SHA-1, name-based) UUID; the same inputs always give the same UUID. |
| `uuid7()` | Version 7 UUID from a millisecond timestamp; sorts in creation order, which suits database keys. |
| `UUID(string)` | Parse a UUID from its hyphenated, bare-hex or URN string form. |

The namespace constants `NAMESPACE_DNS`, `NAMESPACE_URL`, `NAMESPACE_OID` and `NAMESPACE_X500` are `UUID` objects that can be passed to `uuid3()`/`uuid5()`.

## UUID Objects

A `UUID` supports `str()`, `repr()`, `==`/`!=`, ordering (`<`, `<=`, `>`, `>=`) and hashing, so it works as a dict key, set member and `sorted()` item. Attributes: `hex` (32 hex digits), `version`, `variant`, `bytes` (16 `bytes`) and `urn`.

## UUID Versions Comparison

| Version | Based On | Sortable | Use Case |
|---------|----------|----------|----------|
| `uuid1()` | Time + MAC | Partially | Legacy systems, audit trails |
| `uuid4()` | Random | No | General purpose, most common |
| `uuid7()` | Timestamp | Yes | Database keys, distributed systems |

## Example

```python
import uuid

request_id = uuid.uuid4()
print(str(request_id), len(str(request_id)))   # 550e8400-... 36
print(request_id.version, request_id.hex[:8])  # 4 ...

a = uuid.uuid7()                  # time-ordered: later IDs sort after earlier ones
b = uuid.uuid7()
print(a < b, a.version)           # True 7

# Name-based UUIDs are deterministic
print(uuid.uuid5(uuid.NAMESPACE_DNS, "example.com"))
# cfbff0d1-9375-5685-968c-48ce8b15ae17

seen = {request_id: "first"}      # hashable
print(uuid.UUID(str(request_id)) == request_id)   # True
```

## Differences from Python

- `.int` is not available: a UUID is a 128-bit integer and scriptling integers are 64-bit.
- `uuid.UUID(s)` takes one positional string (hyphenated, bare hex or `urn:uuid:` form), not the `hex=`, `bytes=`, `int=` or `fields=` keywords; `.fields`, `.time` and the other less common attributes are not provided.
- `uuid7()` matches Python 3.14+.

## See Also

- [random](../random/): random number generation.
- [hashlib](../hashlib/): cryptographic hash functions.
