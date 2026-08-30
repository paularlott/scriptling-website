---
title: pathlib
description: Object-oriented filesystem paths, similar to Python's pathlib module.
tags: [libraries, filesystem]
weight: 3
aliases:
  - /reference/libraries/extlib/pathlib/
  - /reference/libraries/pathlib/
---

The `pathlib` library provides object-oriented filesystem path operations, similar to Python's `pathlib` module. It offers a more convenient and readable way to work with file paths than plain string manipulation, and is the recommended way to work with paths in new code.

## Available Functions

| Function | Description |
|----------|-------------|
| `Path(path)` | Create a new `Path` object. |
| `name` | Final path component (filename). |
| `stem` | Final component without its suffix. |
| `suffix` | File extension of the final component. |
| `parent` | Parent directory. |
| `parts` | Tuple of the path's components. |
| `joinpath(*other)` | Combine with other path components. |
| `exists()` | Check if the path exists. |
| `is_file()` | Check if the path is a regular file. |
| `is_dir()` | Check if the path is a directory. |
| `mkdir(mode=0o777, parents=False, exist_ok=False)` | Create a directory at this path. |
| `chmod(mode)` | Change file or directory permissions. |
| `rmdir()` | Remove an empty directory. |
| `unlink(missing_ok=False)` | Remove a file or symbolic link. |
| `read_text()` | Read file contents as a string. |
| `write_text(data)` | Write a string to a file. |
| `read_bytes()` | Read file contents as bytes. |
| `write_bytes(data)` | Write bytes to a file. |
| `copy(target)` | Copy this file or directory to a target path. |
| `rename(target)` | Rename/move this file or directory to a target path. |
| `iterdir()` | List directory contents as `Path` objects. |
| `glob(pattern)` | Match a pattern, returning a list of `Path` objects. |

## Functions

### `Path(path)`

Create a new `Path` object representing a filesystem path.

**Parameters:**
- `path` (`str`): The filesystem path.

**Returns:** `Path`: a new `Path` instance.

```python
import pathlib

p = pathlib.Path("/home/user/documents/file.txt")
print(p.name)      # "file.txt"
print(p.stem)      # "file"
print(p.suffix)    # ".txt"
print(p.parent)    # "/home/user/documents"
```

## Path Properties

### `name`

The final path component (file or directory name).

**Returns:** `str`: the final component of the path.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.name)  # "file.txt"

p2 = pathlib.Path("/home/user/myfolder/")
print(p2.name)  # "myfolder"
```

### `stem`

The final path component without its suffix.

**Returns:** `str`: the final component, with the suffix removed.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.stem)  # "file"

p2 = pathlib.Path("/home/user/README")
print(p2.stem)  # "README"
```

### `suffix`

The file extension of the final path component.

**Returns:** `str`: the suffix, including the leading `.`, or `""` if there is none.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.suffix)  # ".txt"

p2 = pathlib.Path("/home/user/README")
print(p2.suffix)  # ""
```

### `parent`

The parent directory of the path.

**Returns:** `str`: the parent directory.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.parent)  # "/home/user"
```

### `parts`

A tuple of the path's components.

**Returns:** `tuple`: the path components.

```python
p = pathlib.Path("/home/user/file.txt")
print(p.parts)  # ("/", "home", "user", "file.txt")
```

## Path Operations

### `joinpath(*other)`

Combine this path with other path components.

**Parameters:**
- `*other` (`str`): Path components to append.

**Returns:** `Path`: the combined path.

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

**Returns:** `bool`: `True` if the path exists, `False` otherwise.

```python
p = pathlib.Path("/home/user/file.txt")
if p.exists():
    print("File exists")
```

### `is_file()`

Check if the path is a regular file.

**Returns:** `bool`: `True` if the path is a regular file, `False` otherwise.

```python
p = pathlib.Path("/home/user/file.txt")
if p.is_file():
    print("Is a file")
```

### `is_dir()`

Check if the path is a directory.

**Returns:** `bool`: `True` if the path is a directory, `False` otherwise.

```python
p = pathlib.Path("/home/user/myfolder")
if p.is_dir():
    print("Is a directory")
```

## File Operations

### `read_text()`

Read the contents of the file as a string.

**Returns:** `str`: the file's contents.

**Raises:** `Error`: if the path is outside the allowed paths, or the file cannot be read.

```python
p = pathlib.Path("/home/user/file.txt")
content = p.read_text()
print(content)
```

### `write_text(data)`

Write a string to the file, creating or overwriting it.

**Parameters:**
- `data` (`str`): Content to write.

**Returns:** `None`

**Raises:** `Error`: if the path is outside the allowed paths.

```python
p = pathlib.Path("/home/user/newfile.txt")
p.write_text("Hello, World!")
```

### `read_bytes()`

Read the contents of the file as bytes.

**Returns:** [`bytes`](../../data-formats/bytes/): the file's raw bytes.

**Raises:** `Error`: if the path is outside the allowed paths, or the file cannot be read.

```python
p = pathlib.Path("/home/user/data.bin")
data = p.read_bytes()
```

### `write_bytes(data)`

Write bytes to the file, creating or overwriting it.

**Parameters:**
- `data` ([`bytes`](../../data-formats/bytes/) or `str`): Raw bytes to write. Strings are UTF-8 encoded.

**Returns:** `None`

**Raises:** `Error`: if the path is outside the allowed paths.

```python
p = pathlib.Path("/home/user/data.bin")
p.write_bytes("raw bytes")
```

### `mkdir(mode=0o777, parents=False, exist_ok=False)`

Create a directory at this path. The `mode` argument uses permission bits such as `0o700` or `0o755`. As in Python, the final permissions are still subject to the process umask.

**Parameters:**
- `mode` (`int`, optional): Permission bits. Default: `0o777`.
- `parents` (`bool`, optional): If `True`, create any missing parent directories. Default: `False`.
- `exist_ok` (`bool`, optional): If `True`, do not error when the directory already exists. Default: `False`.

**Returns:** `None`

**Raises:** `Error`: if the path is outside the allowed paths, or the directory already exists and `exist_ok` is `False`.

```python
# Create a single directory
p = pathlib.Path("/home/user/newfolder")
p.mkdir(0o700)

# Create nested directories
p2 = pathlib.Path("/home/user/a/b/c")
p2.mkdir(parents=True, exist_ok=True)
```

### `chmod(mode)`

Change the permissions of the file or directory.

**Parameters:**
- `mode` (`int`): Permission bits, such as `0o600`, `0o644`, or `0o755`.

**Returns:** `None`

**Raises:** `Error`: if the path is outside the allowed paths.

```python
p = pathlib.Path("/home/user/script.sh")
p.chmod(0o755)
```

### `rmdir()`

Remove the empty directory.

**Returns:** `None`

**Raises:** `Error`: if the path is outside the allowed paths, or the directory is not empty.

```python
p = pathlib.Path("/home/user/emptyfolder")
p.rmdir()
```

### `unlink(missing_ok=False)`

Remove this file or symbolic link.

**Parameters:**
- `missing_ok` (`bool`, optional): If `True`, do not error if the file does not exist. Default: `False`.

**Returns:** `None`

**Raises:** `Error`: if the path is outside the allowed paths, or the file does not exist and `missing_ok` is `False`.

```python
p = pathlib.Path("/home/user/file.txt")
p.unlink()

# Don't error if file doesn't exist
p.unlink(missing_ok=True)
```

### `copy(target)`

Copy this file or directory to the target path.

**Parameters:**
- `target` (`str`): Destination path.

**Returns:** `Path`: a new `Path` pointing to `target`.

**Raises:** `Error`: if either path is outside the allowed paths.

```python
p = pathlib.Path("/home/user/file.txt")
new_path = p.copy("/home/user/file_backup.txt")
print(new_path)  # "/home/user/file_backup.txt"

# Copy a directory tree
src = pathlib.Path("/home/user/project")
src.copy("/home/user/project_backup")
```

### `rename(target)`

Rename or move this file or directory to the target path.

**Parameters:**
- `target` (`str`): Destination path.

**Returns:** `Path`: a new `Path` pointing to `target`.

**Raises:** `Error`: if either path is outside the allowed paths.

```python
p = pathlib.Path("/home/user/old_name.txt")
new_path = p.rename("/home/user/new_name.txt")
print(new_path)  # "/home/user/new_name.txt"
```

### `iterdir()`

Return a list of `Path` objects for the contents of this directory. The path must point to an existing directory.

**Returns:** `list`: `Path` objects for each directory entry.

**Raises:** `Error`: if the path is outside the allowed paths, or cannot be read.

```python
p = pathlib.Path("/home/user/documents")
for child in p.iterdir():
    if child.is_file():
        print(f"File: {child.name}")
    elif child.is_dir():
        print(f"Dir: {child.name}")
```

### `glob(pattern)`

Return a list of `Path` objects matching the given pattern in this directory. Supports `*`, `?`, and `**` (recursive) wildcards.

**Parameters:**
- `pattern` (`str`): Shell-style wildcard pattern.

**Returns:** `list`: matching `Path` objects.

**Raises:** `Error`: if the path is outside the allowed paths.

```python
p = pathlib.Path("/home/user/documents")

# Find all text files
txt_files = p.glob("*.txt")

# Find all Python files recursively
all_py = p.glob("**/*.py")
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`pathlib` provides read/write access to the host filesystem. When embedding in Go, access is restricted to the `allowedPaths` passed to `RegisterPathlibLibrary(p, allowedPaths)`: path traversal (`../`) is blocked automatically. See [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries) and the [Security Guide](/docs/security/#file-system-security).

## See Also

- [os](../os/): Operating system interfaces and file operations
- [os.path](../os.path/): Path manipulation functions
- [glob](../glob/): Standalone shell-style wildcard matching
