---
title: fs
description: Binary I/O for reading, writing, and unpacking binary file formats.
tags: [libraries, filesystem]
weight: 4
aliases:
  - /reference/libraries/extlib/fs/
  - /reference/libraries/fs/
---

The `fs` library provides binary I/O for reading and writing raw bytes, plus `pack`/`unpack` helpers for working with structured binary file formats (similar to Python's `struct` module combined with raw file access).

## Available Functions

| Function | Description |
|----------|-------------|
| `read_bytes(path, offset, length)` | Read a range of bytes from a file. |
| `write_bytes(path, offset, data, mode=0o644)` | Write raw bytes at an offset, creating the file if needed. |
| `unpack(format, data)` | Unpack binary data using a format string. |
| `pack(format, values)` | Pack values into a binary string using a format string. |
| `byte_at(data, index)` | Return the unsigned byte value (0-255) at an index. |
| `len(data)` | Return the byte length of a binary string. |
| `slice(data, start, end=None)` | Byte-safe slicing of binary data. |

## Functions

### `read_bytes(path, offset, length)`

Read a range of bytes from a file. `length` is capped at 64 MiB per call.

**Parameters:**
- `path` (`str`): File path to read.
- `offset` (`int`): 0-based byte position to start reading.
- `length` (`int`): Number of bytes to read (max 64 MiB per call).

**Returns:** `str`: the raw bytes read from the file.

```python
import fs

data = fs.read_bytes("/tmp/data.bin", 0, 16)
```

### `write_bytes(path, offset, data, mode=0o644)`

Write raw bytes at an offset. Creates the file if it does not exist.

**Parameters:**
- `path` (`str`): File path to write.
- `offset` (`int`): 0-based byte position to start writing.
- `data` (`str`): Raw bytes to write.
- `mode` (`int`, optional): Permission bits used when creating a new file. Default: `0o644`.

**Returns:** `None`

```python
import fs

fs.write_bytes("/tmp/output.bin", 0, "\x00\x01\x02\x03", mode=0o600)
```

### `unpack(format, data)`

Unpack binary data using a format string.

Supported format characters: `b`/`B` int8/uint8 (1 byte), `h`/`H` int16/uint16 (2 bytes), `i`/`I` int32/uint32 (4 bytes), `q`/`Q` int64/uint64 (8 bytes), `f` float32 (4 bytes), `d` float64 (8 bytes), `e` float16 (2 bytes). Prefix the format with `<` for little-endian (default) or `>` for big-endian. A number before a format character is a repeat count (e.g. `"<4f"` reads four float32 values).

**Parameters:**
- `format` (`str`): Format string describing the binary layout.
- `data` (`str`): Binary data to unpack.

**Returns:** `list`: the unpacked values.

**Raises:** `Error`: if `data` is shorter than the format requires, or `format` contains an unsupported character.

```python
import fs

data = fs.read_bytes("/tmp/points.bin", 0, 12)

# Unpack 3 little-endian float32 values
values = fs.unpack("<3f", data)
print(values)  # [1.0, 2.0, 3.0]

# Unpack a single big-endian uint16
num = fs.unpack(">H", data[:2])
```

### `pack(format, values)`

Pack values into a binary string. Uses the same format strings as `unpack()`.

**Parameters:**
- `format` (`str`): Format string describing the binary layout.
- `values` (`list`): Values to pack.

**Returns:** `str`: the packed binary data.

**Raises:** `Error`: if the number of values does not match the format, or a value is out of range for its format character.

```python
import fs

# Pack 3 floats in little-endian
data = fs.pack("<3f", [1.0, 2.0, 3.0])
fs.write_bytes("/tmp/points.bin", 0, data)
```

### `byte_at(data, index)`

Return the unsigned byte value (0-255) at the given index.

**Parameters:**
- `data` (`str`): Binary data.
- `index` (`int`): Byte index.

**Returns:** `int`: the byte value, `0`-`255`.

**Raises:** `Error`: if `index` is out of range.

```python
import fs

data = fs.read_bytes("/tmp/file.bin", 0, 4)
b = fs.byte_at(data, 0)  # First byte value
```

### `len(data)`

Return the byte length of a binary string. Unlike the builtin `len()`, this counts bytes, not Unicode code points.

**Parameters:**
- `data` (`str`): Binary data.

**Returns:** `int`: the number of bytes in `data`.

```python
import fs

data = fs.read_bytes("/tmp/file.bin", 0, 100)
size = fs.len(data)  # Up to 100
```

### `slice(data, start, end=None)`

Byte-safe slicing of binary data. Unlike string slicing, this operates on byte offsets, not Unicode code points.

**Parameters:**
- `data` (`str`): Binary data.
- `start` (`int`): Start byte offset.
- `end` (`int`, optional): End byte offset. Default: `None` (end of data).

**Returns:** `str`: the byte slice.

```python
import fs

data = fs.read_bytes("/tmp/file.bin", 0, 256)
header = fs.slice(data, 0, 4)    # First 4 bytes
body = fs.slice(data, 4)         # Everything after
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`fs` provides direct read/write access to the host filesystem at the byte level. When embedding in Go, access is restricted to the `allowedPaths` passed to `RegisterFSLibrary(p, allowedPaths)`: path traversal (`../`) is blocked automatically. See [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries) and the [Security Guide](/docs/security/#file-system-security).

## See Also

- [os](../os/): Operating system interfaces and simple text file I/O
- [pathlib](../pathlib/): Object-oriented filesystem paths
