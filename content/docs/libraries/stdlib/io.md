---
title: io
weight: 3
---

In-memory I/O streams. Currently provides `StringIO` — an in-memory string buffer that behaves like a text file.

## Available Classes

| Class | Description |
| ----- | ----------- |
| `StringIO([initial_value])` | In-memory string buffer |

## StringIO

`io.StringIO([initial_value=""])` creates an in-memory text buffer. An optional string pre-fills the buffer.

### Methods

| Method | Description |
| ------ | ----------- |
| `write(s)` | Write string `s` to the buffer; returns number of characters written |
| `getvalue()` | Return the entire buffer contents as a string |
| `read([n])` | Read up to `n` characters from the current position; reads all if `n` is omitted |
| `readline()` | Read one line (including the newline character) from the current position |
| `seek(pos)` | Set the read position to `pos` |
| `tell()` | Return the current read position |
| `truncate([pos])` | Truncate the buffer to `pos` characters (default: current position) |
| `close()` | Close the buffer; further I/O raises an error |

`StringIO` supports the `with` statement — the buffer is closed automatically on exit.

## Usage Examples

### Building strings incrementally

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

### Capturing print output

```python
import io

buf = io.StringIO()
print("hello", file=buf)
print("world", file=buf)
captured = buf.getvalue()  # "hello\nworld\n"
```

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

### Pre-filled buffer with read/seek

```python
import io

buf = io.StringIO("hello world")

first = buf.read(5)   # "hello"
buf.seek(6)
rest  = buf.read()    # "world"

buf.seek(0)
all   = buf.read()    # "hello world"
```

### Reading line by line

```python
import io

buf = io.StringIO("line1\nline2\nline3")
while True:
    line = buf.readline()
    if line == "":
        break
    print(line.strip())
```

### Truncating a buffer

```python
import io

buf = io.StringIO("hello world")
buf.truncate(5)
print(buf.getvalue())  # "hello"
```

## print(file=buf)

The built-in `print()` function accepts a `file` keyword argument. Passing a `StringIO` instance redirects output into the buffer instead of stdout.

```python
import io

buf = io.StringIO()
print("a", "b", "c", sep=",", end="!\n", file=buf)
print(buf.getvalue())  # a,b,c!
```

## Error Handling

Operations on a closed buffer raise an exception:

```python
import io

buf = io.StringIO("data")
buf.close()

try:
    buf.write("more")
except Exception as e:
    print(e)  # I/O operation on closed file
```
