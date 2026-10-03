---
title: uuid
description: UUID generation, matching Python's uuid module.
tags: [libraries, math]
weight: 7

aliases:
  - /reference/libraries/stdlib/uuid/
  - /reference/libraries/uuid/
---

The `uuid` library generates universally unique identifiers (UUIDs) using time-based, random, or sortable timestamp-based schemes. Each function returns the UUID as a string such as `"550e8400-e29b-41d4-a716-446655440000"`.

## Available Functions

| Function | Description |
|----------|-------------|
| `uuid1()` | Version 1 UUID from the current time and MAC address. |
| `uuid4()` | Version 4 (random) UUID; the usual general-purpose choice. |
| `uuid7()` | Version 7 UUID from a millisecond timestamp; sorts in creation order as a string, which suits database keys. |

## UUID Versions Comparison

| Version | Based On | Sortable | Use Case |
|---------|----------|----------|----------|
| `uuid1()` | Time + MAC | Partially | Legacy systems, audit trails |
| `uuid4()` | Random | No | General purpose, most common |
| `uuid7()` | Timestamp | Yes | Database keys, distributed systems |

## Example

```python
import uuid

request_id = uuid.uuid4()         # a str, e.g. "550e8400-e29b-41d4-a716-446655440000"
print(len(request_id), request_id[14])   # 36 4  (the version digit)

a = uuid.uuid7()                  # time-ordered: later IDs sort after earlier ones
b = uuid.uuid7()
print(a < b, a[14])               # True 7

print(uuid.uuid1()[14])           # 1
```

## Differences from Python

- The functions return the UUID as a lowercase hyphenated `str`, not a `uuid.UUID` object: there is no `.hex`, `.int` or `.bytes`, and no `uuid.UUID` class for parsing.
- `uuid7()` matches Python 3.14+. `uuid3()` and `uuid5()` (name-based) are not available.

## See Also

- [random](../random/): random number generation.
- [hashlib](../hashlib/): cryptographic hash functions.
