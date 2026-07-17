---
title: io
description: In-memory text I/O streams, providing StringIO as a buffer that behaves like a text file.
tags: [libraries, text]
weight: 3

aliases:
  - /reference/libraries/stdlib/io/
  - /reference/libraries/io/
---

The `io` library provides in-memory I/O streams. It currently exposes `StringIO`, an in-memory string buffer that behaves like a text file: useful for building up strings incrementally or capturing output that would otherwise go to stdout.

## Available Classes

| Class | Description |
|-------|-------------|
| `StringIO(initial_value="")` | In-memory text buffer that behaves like a file opened for text I/O. |

## StringIO

`io.StringIO(initial_value="")` creates an in-memory text buffer. An optional string pre-fills the buffer. `StringIO` supports the `with` statement: the buffer is closed automatically on exit.

### Methods

| Method | Description |
|--------|-------------|
| `write(s)` | Write a string to the buffer. |
| `getvalue()` | Return the entire buffer contents as a string. |
| `read(n=None)` | Read up to `n` characters from the current position. |
| `readline()` | Read one line (including the newline) from the current position. |
| `seek(pos)` | Set the read position. |
| `tell()` | Return the current read position. |
| `truncate(pos=None)` | Truncate the buffer to `pos` characters. |
| `close()` | Close the buffer. |

### `StringIO(initial_value="")`

Creates a new in-memory text buffer. If `initial_value` is given, the buffer starts pre-filled with that string and the read position starts at `0`.

**Parameters:**
- `initial_value` (`str`, optional): Text to pre-fill the buffer with. Default: `""`.

**Returns:** `StringIO`: a new buffer instance.

```python
import io

buf = io.StringIO()
empty = buf.getvalue()  # ""

prefilled = io.StringIO("hello world")
print(prefilled.getvalue())  # "hello world"
```

### `write(s)`

Writes a string to the buffer at the current position.

**Parameters:**
- `s` (`str`): Text to write.

**Returns:** `int`: the number of characters written.

**Raises:** `Exception`: if the buffer has been closed.

```python
import io

buf = io.StringIO()
n = buf.write("hello")  # 5
buf.write(" world")
print(buf.getvalue())  # "hello world"
```

### `getvalue()`

Returns the entire contents of the buffer as a string, regardless of the current read position.

**Parameters:** None

**Returns:** `str`: the full buffer contents.

**Raises:** `Exception`: if the buffer has been closed.

```python
import io

buf = io.StringIO()
for i in range(5):
    buf.write(f"item {i}\n")

result = buf.getvalue()
print(result)
# item 0
# item 1
# item 2
# item 3
# item 4
```

### `read(n=None)`

Reads characters from the current position and advances the position by the number of characters read.

**Parameters:**
- `n` (`int`, optional): Maximum number of characters to read. If omitted, reads all remaining characters. Default: `None`.

**Returns:** `str`: the characters read; an empty string if already at the end of the buffer.

**Raises:** `Exception`: if the buffer has been closed.

```python
import io

buf = io.StringIO("hello world")

first = buf.read(5)   # "hello"
buf.seek(6)
rest = buf.read()     # "world"

buf.seek(0)
all_text = buf.read()  # "hello world"
```

### `readline()`

Reads one line from the current position, including the trailing newline character if present, and advances the position past it.

**Parameters:** None

**Returns:** `str`: the line read, including its newline if present; an empty string at the end of the buffer.

**Raises:** `Exception`: if the buffer has been closed.

```python
import io

buf = io.StringIO("line1\nline2\nline3")
while True:
    line = buf.readline()
    if line == "":
        break
    print(line.strip())
```

### `seek(pos)`

Sets the read position used by `read()` and `readline()`. Values outside the buffer's bounds are clamped.

**Parameters:**
- `pos` (`int`): New read position, clamped to `[0, len(buffer)]`.

**Returns:** `int`: the resulting position.

**Raises:** `Exception`: if the buffer has been closed.

```python
import io

buf = io.StringIO("hello world")
buf.seek(6)
print(buf.read())  # "world"
```

### `tell()`

Returns the current read position.

**Parameters:** None

**Returns:** `int`: the current read position.

**Raises:** `Exception`: if the buffer has been closed.

```python
import io

buf = io.StringIO("hello")
buf.read(2)
print(buf.tell())  # 2
```

### `truncate(pos=None)`

Truncates the buffer so it contains only the first `pos` characters. If the read position is beyond the new end, it is moved back to the new end.

**Parameters:**
- `pos` (`int`, optional): Number of characters to keep. Default: the current read position.

**Returns:** `int`: the resulting buffer size.

**Raises:** `Exception`: if the buffer has been closed.

```python
import io

buf = io.StringIO("hello world")
buf.truncate(5)
print(buf.getvalue())  # "hello"
```

### `close()`

Closes the buffer. Any further read/write operations on the buffer raise an exception.

**Parameters:** None

**Returns:** `None`

```python
import io

buf = io.StringIO("data")
buf.close()

try:
    buf.write("more")
except Exception as e:
    print(e)  # I/O operation on closed file
```

## Usage Examples

### Using as a context manager

```python
import io

with io.StringIO() as buf:
    buf.write("line one\n")
    buf.write("line two\n")
    content = buf.getvalue()

# buf is closed after the with block
print(content)
```

### Capturing print output

The built-in `print()` function accepts a `file` keyword argument. Passing a `StringIO` instance redirects output into the buffer instead of stdout.

```python
import io

buf = io.StringIO()
print("a", "b", "c", sep=",", end="!\n", file=buf)
print(buf.getvalue())  # a,b,c!
```

## See Also

- [datetime](../datetime/) - Date and time types
- [time](../time/) - Time access and conversions
- [urllib](../urllib/) - URL parsing and encoding
