---
title: uuid
description: UUID generation, matching Python's uuid module.
tags: [libraries, math]
weight: 7

aliases:
  - /reference/libraries/stdlib/uuid/
  - /reference/libraries/uuid/
---

The `uuid` library generates universally unique identifiers (UUIDs) using time-based, random, or sortable timestamp-based schemes.

## Available Functions

| Function | Description |
|----------|-------------|
| `uuid1()` | Generate UUID version 1 (time-based). |
| `uuid4()` | Generate UUID version 4 (random). |
| `uuid7()` | Generate UUID version 7 (timestamp-based, sortable). |

## Functions

### `uuid1()`

Generates a UUID version 1, based on the current time and MAC address. Useful for unique IDs where time ordering matters (the timestamp can be partially recovered from the value, though it isn't lexicographically sortable as a string).

**Returns:** `str`: a UUID in the form `xxxxxxxx-xxxx-1xxx-yxxx-xxxxxxxxxxxx`.

**Raises:** `Error`: if UUID generation fails.

```python
import uuid

id = uuid.uuid1()
print(id)  # e.g., "f47ac10b-58cc-1e4c-a26f-e3fc32165abc"
```

### `uuid4()`

Generates a UUID version 4, fully random. The most commonly used form for general-purpose unique identifiers.

**Returns:** `str`: a UUID in the form `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`.

```python
import uuid

id = uuid.uuid4()
print(id)  # e.g., "550e8400-e29b-41d4-a716-446655440000"
```

### `uuid7()`

Generates a UUID version 7, based on the Unix timestamp in milliseconds. UUIDs generated in sequence sort in chronological order as strings, making this ideal for database primary keys.

**Returns:** `str`: a UUID in the form `xxxxxxxx-xxxx-7xxx-yxxx-xxxxxxxxxxxx`.

**Raises:** `Error`: if UUID generation fails.

```python
import uuid

id = uuid.uuid7()
print(id)  # e.g., "018f6b1c-4e5d-7abc-8def-0123456789ab"
```

## UUID Versions Comparison

| Version | Based On | Sortable | Use Case |
|---------|----------|----------|----------|
| `uuid1()` | Time + MAC | Partially | Legacy systems, audit trails |
| `uuid4()` | Random | No | General purpose, most common |
| `uuid7()` | Timestamp | Yes | Database keys, distributed systems |

## Examples

### Generate a Unique Request ID

```python
import uuid

def make_request():
    request_id = uuid.uuid4()
    print("Request ID:", request_id)

make_request()
```

### Database Record ID

```python
import uuid

def create_record(data):
    record = {
        "id": uuid.uuid7(),  # Sortable by creation time
        "data": data
    }
    return record

record = create_record({"name": "Test"})
print(record["id"])
```

## Python Compatibility

| Function | Supported |
|----------|-----------|
| `uuid1()` | Yes |
| `uuid4()` | Yes |
| `uuid7()` | Yes (Python 3.12+) |
| `uuid3()` | No (name-based, MD5) |
| `uuid5()` | No (name-based, SHA-1) |

## See Also

- [random](../random/): random number generation.
- [hashlib](../hashlib/): cryptographic hash functions.
