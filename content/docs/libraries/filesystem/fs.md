---
title: fs
weight: 1

aliases:
  - /docs/libraries/extlib/fs/
  - /docs/libraries/fs/
requires_registration: true
---

Binary I/O library for reading and unpacking binary file formats. Requires explicit registration with allowed paths.

## Available Functions

| Function | Description |
| -------- | ----------- |
| `read_bytes(path, offset, length)` | Read a range of bytes from a file |
| `write_bytes(path, offset, data[, mode])` | Write raw bytes at an offset |
| `unpack(format, data)` | Unpack binary data using format strings |
| `pack(format, values)` | Pack values into a binary string |
| `byte_at(data, index)` | Return the unsigned byte value (0-255) at an index |
| `len(data)` | Return the byte length of a binary string |
| `slice(data, start[, end])` | Byte-safe slicing of binary data |

## Functions

### fs.read_bytes(path, offset, length)

Read a range of bytes from a file.

**Parameters:**

- `path` (str): File path to read
- `offset` (int): 0-based byte position to start reading
- `length` (int): Number of bytes to read (max 64 MiB per call)

**Returns:** String (raw bytes)

**Example:**

```python
import fs

data = fs.read_bytes("/tmp/data.bin", 0, 16)
```

### fs.write_bytes(path, offset, data[, mode])

Write raw bytes at an offset. Creates the file if it does not exist.

**Parameters:**

- `path` (str): File path to write
- `offset` (int): 0-based byte position to start writing
- `data` (str): Raw bytes to write
- `mode` (int, optional): Permission bits used when creating a new file. Defaults to `0o644`.

**Returns:** None

**Example:**

```python
import fs

fs.write_bytes("/tmp/output.bin", 0, "\x00\x01\x02\x03", mode=0o600)
```

### fs.unpack(format, data)

Unpack binary data using format strings.

**Parameters:**

- `format` (str): Format string describing the binary layout
- `data` (str): Binary data to unpack

**Returns:** List of values

**Format Characters:**

| Char | Type | Size |
| ---- | ---- | ---- |
| `b` | int8 (signed) | 1 byte |
| `B` | uint8 (unsigned) | 1 byte |
| `h` | int16 (signed) | 2 bytes |
| `H` | uint16 (unsigned) | 2 bytes |
| `i` | int32 (signed) | 4 bytes |
| `I` | uint32 (unsigned) | 4 bytes |
| `q` | int64 (signed) | 8 bytes |
| `Q` | uint64 (unsigned) | 8 bytes |
| `f` | float32 | 4 bytes |
| `d` | float64 | 8 bytes |
| `e` | float16 | 2 bytes |

**Byte Order:**

- `<` — Little-endian (default)
- `>` — Big-endian

A number before a format character acts as a repeat count (e.g. `"<4f"` reads 4 float32 values).

**Example:**

```python
import fs

data = fs.read_bytes("/tmp/points.bin", 0, 12)

# Unpack 3 little-endian float32 values
values = fs.unpack("<3f", data)
print(values)  # [1.0, 2.0, 3.0]

# Unpack a single big-endian uint16
num = fs.unpack(">H", data[:2])
```

### fs.pack(format, values)

Pack values into a binary string. Uses the same format strings as `unpack()`.

**Parameters:**

- `format` (str): Format string describing the binary layout
- `values` (list): Values to pack

**Returns:** String (binary data)

**Example:**

```python
import fs

# Pack 3 floats in little-endian
data = fs.pack("<3f", [1.0, 2.0, 3.0])
fs.write_bytes("/tmp/points.bin", 0, data)
```

### fs.byte_at(data, index)

Return the unsigned byte value (0-255) at the given index.

**Parameters:**

- `data` (str): Binary data
- `index` (int): Byte index

**Returns:** Integer (0-255)

**Example:**

```python
import fs

data = fs.read_bytes("/tmp/file.bin", 0, 4)
b = fs.byte_at(data, 0)  # First byte value
```

### fs.len(data)

Return the byte length of a binary string. Unlike the builtin `len()`, this counts bytes, not Unicode code points.

**Parameters:**

- `data` (str): Binary data

**Returns:** Integer

**Example:**

```python
import fs

data = fs.read_bytes("/tmp/file.bin", 0, 100)
size = fs.len(data)  # Up to 100
```

### fs.slice(data, start[, end])

Byte-safe slicing of binary data. Unlike string slicing, this operates on byte offsets, not Unicode code points.

**Parameters:**

- `data` (str): Binary data
- `start` (int): Start byte offset
- `end` (int, optional): End byte offset (default: end of data)

**Returns:** String (binary slice)

**Example:**

```python
import fs

data = fs.read_bytes("/tmp/file.bin", 0, 256)
header = fs.slice(data, 0, 4)    # First 4 bytes
body = fs.slice(data, 4)         # Everything after
```

## Usage Example

```python
import fs

# Read a PNG file header
data = fs.read_bytes("/tmp/image.png", 0, 29)

# Check PNG signature (first 8 bytes)
signature = fs.slice(data, 0, 8)

# Read width and height (big-endian uint32 at offsets 16 and 20)
width = fs.unpack(">I", fs.slice(data, 16, 20))[0]
height = fs.unpack(">I", fs.slice(data, 20, 24))[0]

print("Width:", width)
print("Height:", height)
```

## Security

The `fs` library is restricted to explicitly allowed paths. Attempts to access files outside the configured directories will result in a permission error.

## See Also

- [os](os/) — Operating system interfaces
- [pathlib](pathlib/) — Object-oriented filesystem paths
