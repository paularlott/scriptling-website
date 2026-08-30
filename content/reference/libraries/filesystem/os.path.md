---
title: os.path
description: Common pathname manipulations, similar to Python's os.path module.
tags: [libraries, filesystem]
weight: 2
aliases:
  - /reference/libraries/extlib/os.path/
  - /reference/libraries/os.path/
---

The `os.path` library provides common pathname manipulations: joining, splitting, normalizing, and inspecting paths: similar to Python's `os.path` module.

## Available Functions

| Function | Description |
|----------|-------------|
| `join(*paths)` | Join path components. |
| `exists(path)` | Check if a path exists. |
| `isfile(path)` | Check if a path is a regular file. |
| `isdir(path)` | Check if a path is a directory. |
| `basename(path)` | Get the final component of a path. |
| `dirname(path)` | Get the directory component of a path. |
| `split(path)` | Split a path into `(directory, filename)`. |
| `splitext(path)` | Split a path into `(root, extension)`. |
| `normpath(path)` | Normalize a path (collapse `.` and `..`). |
| `abspath(path)` | Get the absolute path. |
| `relpath(path, start=".")` | Get the relative path from `start`. |
| `isabs(path)` | Check if a path is absolute. |
| `getsize(path)` | Get a file's size in bytes. |
| `getmtime(path)` | Get a file's last modification time. |
| `islink(path)` | Check if a path is a symbolic link. |

## Functions

### `join(*paths)`

Join path components using the appropriate separator for the OS.

**Parameters:**
- `*paths` (`str`): Path components to join.

**Returns:** `str`: the joined path.

```python
import os.path

path = os.path.join("home", "user", "documents")
print(path)  # "home/user/documents" on Unix, "home\user\documents" on Windows

full = os.path.join("/", "home", "user", "documents", "file.txt")
print(full)  # "/home/user/documents/file.txt"
```

### `exists(path)`

Check if a path exists.

**Parameters:**
- `path` (`str`): Path to check.

**Returns:** `bool`: `True` if the path exists, `False` otherwise.

```python
import os.path

if os.path.exists("/tmp/file.txt"):
    print("File exists")
```

### `isfile(path)`

Check if a path is a regular file.

**Parameters:**
- `path` (`str`): Path to check.

**Returns:** `bool`: `True` if the path is a regular file, `False` otherwise.

```python
import os.path

if os.path.isfile("/tmp/data.txt"):
    print("It's a file")
```

### `isdir(path)`

Check if a path is a directory.

**Parameters:**
- `path` (`str`): Path to check.

**Returns:** `bool`: `True` if the path is a directory, `False` otherwise.

```python
import os.path

if os.path.isdir("/tmp/mydir"):
    print("It's a directory")
```

### `basename(path)`

Get the base name of a path (the final component).

**Parameters:**
- `path` (`str`): Path to process.

**Returns:** `str`: the final component of the path.

```python
import os.path

print(os.path.basename("/home/user/file.txt"))  # "file.txt"
print(os.path.basename("/home/user/mydir/"))    # "mydir"
```

### `dirname(path)`

Get the directory name of a path.

**Parameters:**
- `path` (`str`): Path to process.

**Returns:** `str`: the directory component of the path.

```python
import os.path

print(os.path.dirname("/home/user/file.txt"))  # "/home/user"
print(os.path.dirname("/home/user/mydir/"))    # "/home/user"
```

### `split(path)`

Split a path into a `(directory, filename)` tuple.

**Parameters:**
- `path` (`str`): Path to split.

**Returns:** `tuple`: `(directory, filename)`.

```python
import os.path

dir, file = os.path.split("/home/user/file.txt")
print(dir)   # "/home/user"
print(file)  # "file.txt"
```

### `splitext(path)`

Split a path into a `(root, extension)` tuple.

**Parameters:**
- `path` (`str`): Path to split.

**Returns:** `tuple`: `(root, extension)`.

```python
import os.path

root, ext = os.path.splitext("/home/user/file.txt")
print(root)  # "/home/user/file"
print(ext)   # ".txt"

root, ext = os.path.splitext("/home/user/archive.tar.gz")
print(root)  # "/home/user/archive.tar"
print(ext)   # ".gz"
```

### `normpath(path)`

Normalize a path by collapsing redundant separators and up-level references.

**Parameters:**
- `path` (`str`): Path to normalize.

**Returns:** `str`: the normalized path.

```python
import os.path

print(os.path.normpath("home//user/../user/./docs"))
# "home/user/docs"

print(os.path.normpath("/a/b/c/../../d"))
# "/a/d"
```

### `abspath(path)`

Get the absolute path.

**Parameters:**
- `path` (`str`): Path to convert.

**Returns:** `str`: the absolute path.

```python
import os.path

print(os.path.abspath("file.txt"))           # e.g., "/home/user/project/file.txt"
print(os.path.abspath("../other/file.txt"))  # e.g., "/home/user/other/file.txt"
```

### `relpath(path, start=".")`

Get a relative path to `path`.

**Parameters:**
- `path` (`str`): Path to convert to relative.
- `start` (`str`, optional): Starting directory. Default: `"."` (current directory).

**Returns:** `str`: the relative path.

```python
import os.path

# From current directory
print(os.path.relpath("/home/user/project/file.txt"))
# e.g., "file.txt" if cwd is /home/user/project

# From a specific start directory
print(os.path.relpath("/home/user/project/file.txt", "/home/user"))
# "project/file.txt"
```

### `isabs(path)`

Check if a path is absolute.

**Parameters:**
- `path` (`str`): Path to check.

**Returns:** `bool`: `True` if the path is absolute, `False` otherwise.

```python
import os.path

print(os.path.isabs("/home/user/file.txt"))  # True
print(os.path.isabs("file.txt"))              # False
print(os.path.isabs("../parent/file.txt"))    # False
```

### `getsize(path)`

Get the size of a file in bytes.

**Parameters:**
- `path` (`str`): Path to the file.

**Returns:** `int`: file size in bytes.

**Raises:** `Error`: if `path` is outside the allowed paths, or does not exist.

```python
import os.path

size = os.path.getsize("/tmp/data.txt")
print(f"File size: {size} bytes")
```

### `getmtime(path)`

Get the time of last modification of a file.

**Parameters:**
- `path` (`str`): Path to the file.

**Returns:** `float`: modification time as a Unix timestamp (seconds since epoch).

**Raises:** `Error`: if `path` is outside the allowed paths, or does not exist.

```python
import os.path

mtime = os.path.getmtime("/tmp/data.txt")
print(f"Last modified: {mtime}")
```

### `islink(path)`

Check if a path is a symbolic link. Unlike `os.path.isfile` and `os.path.isdir` (which follow symlinks), this function uses `Lstat` under the hood, so it reports whether the path itself is a symlink — regardless of what the target is.

**Parameters:**
- `path` (`str`): Path to check.

**Returns:** `bool`: `True` if the path is a symbolic link, `False` otherwise.

```python
import os.path

# symlink check doesn't follow links: returns True for the link itself
if os.path.islink("node_modules/.bin/eslint"):
    print("It's a symlink")
```

## Security Considerations

This is an extended library, requiring registration in Go (registered together with the `os` library by `RegisterOSLibrary`, see [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries)).

`os.path` provides read access to filesystem metadata (`exists`, `isfile`, `isdir`, `getsize`, `getmtime`). Access is restricted to the `allowedPaths` passed to `RegisterOSLibrary(p, allowedPaths)`, path traversal (`../`) is blocked automatically. See the [Security Guide](/docs/security/#file-system-security).

## Python Compatibility

This library implements a subset of Python's `os.path` module:

| Function | Supported |
|----------|-----------|
| `join` | Yes |
| `exists` | Yes |
| `isfile` | Yes |
| `isdir` | Yes |
| `basename` | Yes |
| `dirname` | Yes |
| `split` | Yes |
| `splitext` | Yes |
| `abspath` | Yes |
| `normpath` | Yes |
| `relpath` | Yes |
| `isabs` | Yes |
| `getsize` | Yes |
| `getmtime` | Yes |
| `getatime` | No |
| `getctime` | No |
| `islink` | Yes |
| `ismount` | No |
| `samefile` | No |

## See Also

- [os](../os/): Operating system interfaces and file operations
- [pathlib](../pathlib/): Object-oriented filesystem paths (recommended for new code)
