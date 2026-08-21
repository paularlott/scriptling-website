---
description: Parse and generate MessagePack binary data.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/data-formats/msgpack/
sources:
    - resource: https://scriptling.dev/reference/libraries/data-formats/msgpack/
status: stable
tags:
    - libraries
    - data-formats
title: msgpack
type: API Reference
---
# msgpack

The `msgpack` library serialises Scriptling values to [MessagePack](https://msgpack.org/) binary form and parses MessagePack payloads back into Scriptling values. It is the binary counterpart to [`json`](json.md) — more compact and faster, at the cost of human readability.

`packb` returns a [`bytes`](bytes.md) value; `unpackb` takes one.

## Available Functions

| Function | Description |
|----------|-------------|
| `packb(obj)` | Serialise a Scriptling value to MessagePack `bytes`. |
| `unpackb(packed)` | Parse MessagePack `bytes` into a Scriptling value. |
| `pack(obj)` | Alias for `packb()`. |
| `unpack(packed)` | Alias for `unpackb()`. |

## Functions

### `packb(obj)`

Converts a Scriptling value (`dict`, `list`, `tuple`, `str`, `int`, `float`, `bool`, `None`, or `bytes`) to its MessagePack binary representation.

**Parameters:**
- `obj`: Value to serialise. `bytes` round-trips as msgpack `bin`; `str` as msgpack `str`; tuples and lists both encode as msgpack arrays.

**Returns:** [`bytes`](bytes.md): the MessagePack-encoded payload.

```python
import msgpack

payload = msgpack.packb({"user": "alice", "id": 42})
# payload is a bytes value
```

### `unpackb(packed)`

Parses MessagePack bytes back into a Scriptling value. msgpack `bin` decodes to [`bytes`](bytes.md); msgpack `str` decodes to `str`; integers are clamped to Scriptling's int64.

**Parameters:**
- `packed` (`bytes`): A `bytes` value containing a MessagePack payload.

**Returns:** `dict`, `list`, `str`, `int`, `float`, `bool`, `None`, or `bytes`: the decoded value.

**Raises:** `Error`: if `packed` is not a `bytes` value or the payload is malformed.

```python
import msgpack

payload = msgpack.packb({"name": "alice"})
data = msgpack.unpackb(payload)
print(data["name"])  # "alice"
```

## Round-tripping

Every supported value type round-trips losslessly:

```python
import msgpack

values = [
    None, True, False,
    0, -5, 12345,
    3.14,
    "hello",
    [1, 2, 3],
    {"a": 1, "b": [2, 3]},
]

for v in values:
    assert msgpack.unpackb(msgpack.packb(v)) == v
```

Binary data round-trips as `bytes`:

```python
import msgpack
import bytes

binary = bytes([0, 128, 255, 1, 254])
assert msgpack.unpackb(msgpack.packb(binary)) == binary
```

## Limitations

- **`ext` types** (msgpack timestamp, application-defined extensions) are not supported.
- **Streaming `Packer` / `Unpacker` classes** are intentionally omitted — `packb` / `unpackb` cover the one-shot use case.
- **Large integers** clamp to Scriptling's int64 range, matching [`json`](json.md)'s behaviour.

## Choosing a backing codec (Go embedders)

The msgpack library is codec-backed: the `stdlib.MsgpackCodec` interface is

```go
type MsgpackCodec interface {
    Name() string
    Marshal(v interface{}) ([]byte, error)
    Unmarshal(data []byte, v interface{}) error
}
```

This is **structurally identical** to [`gossip`'s `codec.Serializer`](https://pkg.go.dev/github.com/paularlott/gossip/codec#Serializer) — any gossip codec satisfies it without an adapter, so a single driver instance can be shared between Scriptling's msgpack library and a gossip cluster, guaranteeing both sides use the same wire format.

```go
import (
    "github.com/paularlott/gossip/codec"
    "github.com/paularlott/scriptling/stdlib"
)

// One codec instance, used by both gossip and Scriptling.
shared := codec.NewShamatonMsgpackCodec() // or Vmihailenco, Hashicorp, etc.

// Hand it to gossip:
cfg := gossip.DefaultConfig() // already defaults to shamaton
cfg.MsgCodec = shared

// And to Scriptling — register a library built from the shared codec:
p.RegisterLibrary(stdlib.NewMsgpackLibrary(shared))
```

The default package-level library is `stdlib.MsgpackLibrary` and defaults to gossip's `codec.NewShamatonMsgpackCodec()` (matching `gossip.DefaultConfig`), which is what `stdlib.RegisterAll` registers. Embedders who want to override that globally can reassign the var before calling `RegisterAll`:

```go
stdlib.MsgpackLibrary = stdlib.NewMsgpackLibrary(myCodec)
stdlib.RegisterAll(p)
```

## See Also

- [json](json.md): the text counterpart — human-readable, larger payloads.
- [bytes](bytes.md): the binary type returned by `packb()`.
- [toml](toml.md) / [yaml](yaml.md): other structured data formats.
