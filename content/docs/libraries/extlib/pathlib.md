---
title: pathlib
weight: 1
---

The pathlib library provides object-oriented filesystem path operations, similar to Python's pathlib module. It offers a more convenient and readable way to work with file paths compared to string manipulation.

## Available Properties & Methods

| Property/Method    | Description                        |
| ------------------ | ---------------------------------- |
| `name`             | Final path component (filename)    |
| `stem`             | Final component without suffix     |
| `suffix`           | File extension                     |
| `parent`           | Parent directory                   |
| `parts`            | Tuple of path components           |
| `joinpath(*other)` | Combine with other path components |
| `exists()`         | Check if path exists               |
| `is_file()`        | Check if path is a file            |
| `is_dir()`         | Check if path is a directory       |
| `mkdir(mode=0o777, parents=False, exist_ok=False)` | Create directory |
| `chmod(mode)`      | Change file or directory permissions |
| `rmdir()`          | Remove empty directory             |
| `unlink(missing_ok=False)` | Remove file or link        |
| `read_text()`      | Read file contents as string       |
| `write_text(data)` | Write string to file               |
| `read_bytes()`     | Read file contents as bytes        |
| `write_bytes(data)` | Write bytes to file               |

## Basic Usage

```python
import pathlib

# Create a Path object
p = pathlib.Path("/home/user/documents/file.txt")

# Access path components
print(p.name)      # "file.txt"
print(p.stem)      # "file"
print(p.suffix)    # ".txt"
print(p.parent)    # "/home/user/documents"
```

## Path Properties

### `name`

The final path component (file or directory name).

```python
p = pathlib.Path("/home/user/file.txt")
print(p.name)  # "file.txt"

p2 = pathlib.Path("/home/user/myfolder/")
print(p2.name)  # "myfolder"
```

### `stem`

The final path component without its suffix.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.stem)  # "file"

p2 = pathlib.Path("/home/user/README")
print(p2.stem)  # "README"
```

### `suffix`

The file extension of the final path component.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.suffix)  # ".txt"

p2 = pathlib.Path("/home/user/README")
print(p2.suffix)  # ""
```

### `parent`

The parent directory of the path.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.parent)  # "/home/user"

p2 = pathlib.Path("/home/user/folder/")
print(p2.parent)  # "/home/user"
```

### `parts`

A tuple of the path's components.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.parts)  # ("/", "home", "user", "file.txt")
```

## Path Operations

### `joinpath(*other)`

Combine this path with other path components.

```python
p = pathlib.Path("/home/user")
p2 = p.joinpath("documents", "file.txt")
print(p2)  # "/home/user/documents/file.txt"

# Method chaining
p3 = pathlib.Path("a").joinpath("b").joinpath("c")
print(p3)  # "a/b/c"
```

### `exists()`

Check if the path exists.

```python
p = pathlib.Path("/home/user/file.txt")
if p.exists():
    print("File exists")
else:
    print("File does not exist")
```

### `is_file()`

Check if the path is a regular file.

```python
p = pathlib.Path("/home/user/file.txt")
if p.is_file():
    print("Is a file")
```

### `is_dir()`

Check if the path is a directory.

```python
p = pathlib.Path("/home/user/myfolder")
if p.is_dir():
    print("Is a directory")
```

## File Operations

### `read_text()`

Read the contents of a file as a string.

```python
p = pathlib.Path("/home/user/file.txt")
content = p.read_text()
print(content)
```

### `write_text(data)`

Write a string to a file.

```python
p = pathlib.Path("/home/user/newfile.txt")
p.write_text("Hello, World!")
```

### `read_bytes()`

Read the contents of a file as bytes.

```python
p = pathlib.Path("/home/user/data.bin")
data = p.read_bytes()
```

### `write_bytes(data)`

Write bytes to a file.

```python
p = pathlib.Path("/home/user/data.bin")
p.write_bytes("raw bytes")
```

### `mkdir(mode=0o777, parents=False, exist_ok=False)`

Create a directory.

```python
# Create a single directory
p = pathlib.Path("/home/user/newfolder")
p.mkdir(0o700)

# Create nested directories
p2 = pathlib.Path("/home/user/a/b/c")
p2.mkdir(parents=True, exist_ok=True)
```

The `mode` argument uses permission bits such as `0o700` or `0o755`. Like Python, the final permissions are still subject to the process umask when creating directories.

### `chmod(mode)`

Change the permissions of a file or directory.

```python
p = pathlib.Path("/home/user/script.sh")
p.chmod(0o755)
```

### `rmdir()`

Remove an empty directory.

```python
p = pathlib.Path("/home/user/emptyfolder")
p.rmdir()
```

### `unlink(missing_ok=False)`

Remove a file or symbolic link.

```python
p = pathlib.Path("/home/user/file.txt")
p.unlink()

# Don't error if file doesn't exist
p.unlink(missing_ok=True)
```

## Security

The pathlib library respects filesystem security restrictions. If the Scriptling interpreter is configured with allowed paths, all pathlib operations are restricted to those directories. Attempting to access files outside the allowed directories will result in security errors.

## Examples

### Reading and Writing Files

```python
import pathlib

# Write to a file
file_path = pathlib.Path("/tmp/example.txt")
file_path.write_text("This is some content")

# Read from the file
content = file_path.read_text()
print(content)  # "This is some content"

# Clean up
file_path.unlink()
```

### Directory Operations

```python
import pathlib

# Create a directory structure
base_dir = pathlib.Path("/tmp/myproject")
base_dir.mkdir()

src_dir = base_dir.joinpath("src")
src_dir.mkdir()

# Check what we created
print(src_dir.exists())  # True
print(src_dir.is_dir())  # True

# List would show the directory, but pathlib doesn't have it yet
```

### Path Manipulation

```python
import pathlib

# Parse a path
p = pathlib.Path("/var/log/apache2/access.log")

print(f"Name: {p.name}")        # "access.log"
print(f"Stem: {p.stem}")        # "access"
print(f"Suffix: {p.suffix}")    # ".log"
print(f"Parent: {p.parent}")    # "/var/log/apache2"

# Build new paths
config_path = p.parent.joinpath("apache2.conf")
print(config_path)  # "/var/log/apache2/apache2.conf"
```

## Error Handling

All pathlib operations that can fail return errors as Scriptling error objects. Always check for errors in production code:

```python
import pathlib

p = pathlib.Path("/tmp/myfile.txt")
try:
    content = p.read_text()
    print("Content:", content)
except:
    print("Could not read file")
```

## Performance Notes

- Path objects are lightweight and can be created frequently
- File operations involve actual filesystem access and may be slow
- Use `exists()`, `is_file()`, and `is_dir()` before operations when appropriate
