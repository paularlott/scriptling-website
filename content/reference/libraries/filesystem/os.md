---
title: os
description: Operating system interfaces for file system operations and environment variables.
tags: [libraries, filesystem]
weight: 1
aliases:
  - /reference/libraries/extlib/os/
  - /reference/libraries/os/
---

The `os` library provides operating system interfaces for file system operations and environment variables, similar to Python's `os` module. Reach for it for reading/writing whole files, listing directories, and managing environment variables.

## Available Functions

| Function | Description |
|----------|-------------|
| `getenv(key, default=None)` | Get an environment variable. |
| `getcwd()` | Get the current working directory. |
| `listdir(path=".")` | List directory contents. |
| `read_file(path)` | Read entire file contents as a string. Use [read_bytes](#read_bytes) for binary files. |
| `read_bytes(path)` | Read entire file contents as a [`bytes`](../../data-formats/bytes/) value. |
| `read_lines(path)` | Iterate over lines in a file lazily (memory-efficient for large files). |
| `write_file(path, content, mode=0o644)` | Write `str` or `bytes` content to a file (creates/overwrites). |
| `append_file(path, content)` | Append `str` or `bytes` content to a file. |
| `remove(path)` | Remove a file. |
| `chmod(path, mode)` | Change file or directory permissions. |
| `mkdir(path, mode=0o777)` | Create a directory. |
| `makedirs(path, mode=0o777, exist_ok=False)` | Create directories recursively. |
| `rmdir(path)` | Remove an empty directory. |
| `removedirs(name)` | Remove an empty directory and its empty parents. |
| `rename(old, new)` | Rename a file or directory. |
| `symlink(src, dst)` | Create a symbolic link named `dst` pointing to `src`. |

## Constants

| Constant | Description |
|----------|-------------|
| `os.environ` | Dictionary of all environment variables, captured at registration/import time. |
| `os.sep` | The path separator used by the operating system (`"/"` on Unix, `"\"` on Windows). |
| `os.linesep` | The line separator used by the operating system (`"\n"` on Unix, `"\r\n"` on Windows). |
| `os.name` | The operating system name, Python-compatible (`"posix"` on Unix/Linux/macOS, `"nt"` on Windows). |
| `os.platform` | The specific platform identifier (`"darwin"`, `"linux"`, `"windows"`). |

## Functions

### `getenv(key, default=None)`

Get an environment variable.

**Parameters:**
- `key` (`str`): Name of the environment variable.
- `default` (`any`, optional): Value to return if the variable is not set. Default: `None`.

**Returns:** `str`: the variable's value, or `default` (or `None` if no default given) when unset.

```python
import os

# Get environment variable - returns None if not set
home = os.getenv("HOME")
if home:
    print(home)

# With default value
path = os.getenv("MY_PATH", "/default/path")
print(path)
```

### `os.environ`

Dictionary of all environment variables, captured when the library is registered/imported. Supports both direct indexing and the `.get()` method.

**Returns:** `dict`: all environment variables.

```python
import os

# Access as dictionary
print(os.environ["PATH"])

# Use .get() method with default (Python-compatible)
token = os.environ.get("API_TOKEN", "default_token")

# Iterate over all variables
for key, value in os.environ.items():
    print(f"{key} = {value}")
```

### `getcwd()`

Get the current working directory.

**Returns:** `str`: the absolute path to the current working directory.

```python
import os

cwd = os.getcwd()
print(cwd)  # e.g., "/home/user/projects"
```

### `listdir(path=".")`

List directory contents.

**Parameters:**
- `path` (`str`, optional): Directory path to list. Default: `"."`.

**Returns:** `list`: entry names in the directory.

**Raises:** `Error`: if `path` is outside the allowed paths, or cannot be read.

```python
import os

# List current directory
entries = os.listdir()
print(entries)  # ["file1.txt", "file2.py", "subdir"]

# List a specific directory
entries = os.listdir("/tmp")
```

### `read_file(path)`

Read entire file contents as a string. Use [`read_bytes()`](#read_bytes) for
binary files (msgpack, images, hashes) — `read_file` will corrupt non-UTF-8
data.

**Parameters:**
- `path` (`str`): Path to the file.

**Returns:** `str`: the file's contents.

**Raises:** `Error`: if `path` is outside the allowed paths, or the file cannot be read.

```python
import os

content = os.read_file("/tmp/data.txt")
print(content)
```

### `read_bytes(path)`

Read entire file contents as a [`bytes`](../../data-formats/bytes/) value,
preserving binary data byte-for-byte. Use this for msgpack/protobuf payloads,
images, hashes, and any other non-text data.

**Parameters:**
- `path` (`str`): Path to the file.

**Returns:** `bytes`: the file's raw contents.

**Raises:** `Error`: if `path` is outside the allowed paths, or the file cannot be read.

```python
import os, msgpack

data = msgpack.unpackb(os.read_bytes("/tmp/payload.msgpack"))
```

### `read_lines(path)`

Iterate over lines in a file lazily, yielding one `str` per line (without the
trailing newline). The file is read on-demand, so memory usage is proportional
to the longest line, not the file size. Use this for large files where
`read_file().splitlines()` would load everything into memory.

The file handle is closed when the iterator reaches EOF. If the loop exits
early (e.g. via `break`), the handle is closed when the iterator is
garbage-collected — the same behaviour as Python's bare `open()` without
`with`.

**Parameters:**
- `path` (`str`): Path to the file.

**Returns:** An iterator yielding `str`, one per line.

**Raises:** `Error`: if `path` is outside the allowed paths, or the file cannot be opened.

```python
import os

# Process a large log file without loading it all into memory
for line in os.read_lines("/var/log/app.log"):
    if "ERROR" in line:
        print(line)

# Equivalent one-liner for small files (loads everything):
# for line in os.read_file(path).splitlines():
#     ...
```

### `write_file(path, content, mode=0o644)`

Write content to a file, creating or overwriting it. Accepts a `str` (UTF-8
encoded) or [`bytes`](../../data-formats/bytes/) (raw binary).

**Parameters:**
- `path` (`str`): Path to the file.
- `content` (`str` or `bytes`): Content to write.
- `mode` (`int`, optional): Permission bits used when creating a new file. Default: `0o644`.

**Returns:** `None`

**Raises:** `Error`: if `path` is outside the allowed paths, or the file cannot be written.

```python
import os

os.write_file("/tmp/output.txt", "Hello, World!", mode=0o600)

# Binary — round-trips cleanly with read_bytes()
os.write_file("/tmp/data.msgpack", msgpack.packb({"k": 1}))
```

### `append_file(path, content)`

Append content to a file, creating it if it does not exist. Accepts a `str`
or [`bytes`](../../data-formats/bytes/).

**Parameters:**
- `path` (`str`): Path to the file.
- `content` (`str` or `bytes`): Content to append.

**Returns:** `None`

**Raises:** `Error`: if `path` is outside the allowed paths, or the file cannot be written.

```python
import os

os.append_file("/tmp/log.txt", "New log entry\n")
```

### `remove(path)`

Remove a file.

**Parameters:**
- `path` (`str`): Path to the file to remove.

**Returns:** `None`

**Raises:** `Error`: if `path` is outside the allowed paths, or the file cannot be removed.

```python
import os

os.remove("/tmp/old_file.txt")
```

### `chmod(path, mode)`

Change the permissions of a file or directory.

**Parameters:**
- `path` (`str`): Path to the file or directory.
- `mode` (`int`): Permission bits, such as `0o600`, `0o644`, or `0o755`.

**Returns:** `None`

**Raises:** `Error`: if `path` is outside the allowed paths.

```python
import os

os.chmod("/tmp/script.sh", 0o755)
```

### `mkdir(path, mode=0o777)`

Create a directory.

**Parameters:**
- `path` (`str`): Path to the directory to create.
- `mode` (`int`, optional): Permission bits. Default: `0o777` (still subject to the process umask).

**Returns:** `None`

**Raises:** `Error`: if `path` is outside the allowed paths, or the directory cannot be created.

```python
import os

os.mkdir("/tmp/newdir", 0o700)
```

### `makedirs(path, mode=0o777, exist_ok=False)`

Create directories recursively, creating all parent directories as needed.

**Parameters:**
- `path` (`str`): Path to the directory to create.
- `mode` (`int`, optional): Permission bits for created directories. Default: `0o777` (still subject to the process umask).
- `exist_ok` (`bool`, optional): If `True`, do not error when the target directory already exists. Default: `False`.

**Returns:** `None`

**Raises:** `Error`: if `path` is outside the allowed paths, or the directory already exists and `exist_ok` is `False`.

```python
import os

os.makedirs("/tmp/a/b/c", mode=0o755, exist_ok=True)
```

### `rmdir(path)`

Remove an empty directory.

**Parameters:**
- `path` (`str`): Path to the directory to remove.

**Returns:** `None`

**Raises:** `Error`: if `path` is outside the allowed paths, or the directory is not empty.

```python
import os

os.rmdir("/tmp/emptydir")
```

### `removedirs(name)`

Remove an empty directory, then remove empty parent directories until a parent cannot be removed.

**Parameters:**
- `name` (`str`): Path to the leaf directory to remove.

**Returns:** `None`

**Raises:** `Error`: if `name` is outside the allowed paths.

```python
import os

os.removedirs("/tmp/a/b/c")
```

### `rename(old, new)`

Rename a file or directory.

**Parameters:**
- `old` (`str`): Current path.
- `new` (`str`): New path.

**Returns:** `None`

**Raises:** `Error`: if either path is outside the allowed paths.

```python
import os

os.rename("/tmp/old.txt", "/tmp/new.txt")
```

### `symlink(src, dst)`

Create a symbolic link named `dst` that points to `src`. If `dst` already exists, an error is raised. The destination must be within the allowed paths configured at registration.

**Parameters:**
- `src` (`str`): The target the symlink points to (may be relative or absolute).
- `dst` (`str`): The path where the symlink is created.

**Returns:** `None`

```python
import os

# Create a symlink like node_modules/.bin entries
os.symlink("../eslint/bin/eslint.js", "node_modules/.bin/eslint")
```

## Special Variables

### `__file__`

When a script is run from a file (via `EvalFile`, `SetSourceFile`, or the CLI), `__file__` is set to the absolute path of the script file. This lets scripts locate resources relative to themselves, just like in Python. `__file__` is only set when running from a file: it is not available in `Eval()` calls without a source file set.

```python
import os.path

# Get the directory containing this script
script_dir = os.path.dirname(__file__)

# Load a data file next to the script
data_file = os.path.join(script_dir, "data.json")
content = os.read_file(data_file)
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`os` provides read/write access to the host filesystem and to the embedder's environment variables (via `os.environ`/`os.getenv`). When embedding in Go, file access is restricted to the `allowedPaths` passed to `RegisterOSLibrary(p, allowedPaths)`: path traversal (`../`) and symlink attacks are blocked automatically. Passing `nil` removes all restrictions, which is dangerous for untrusted scripts. See [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries) and the [Security Guide](/docs/security/#file-system-security).

## Python Compatibility

This library implements a subset of Python's `os` module:

| Function | Supported |
|----------|-----------|
| `getenv` | Yes (returns `None` when unset, matching Python) |
| `environ` | Yes |
| `getcwd` | Yes |
| `listdir` | Yes |
| `chmod` | Yes |
| `mkdir` | Yes (`mode` supported) |
| `makedirs` | Yes (`mode` and `exist_ok` supported) |
| `rmdir` | Yes |
| `removedirs` | Yes |
| `remove` | Yes |
| `rename` | Yes |
| `symlink` | Yes |
| `read_file` | Yes (Scriptling-specific) |
| `write_file` | Yes (Scriptling-specific) |
| `append_file` | Yes (Scriptling-specific) |
| `stat` | No |
| `walk` | No |
| `utime` | No |

Caveats on the supported subset:

- `os.getenv()` returns `None` when the variable is not set and no default is given (matches Python).
- File operations use `read_file()`, `write_file()`, and `append_file()` instead of `open()`: there are no file object handles, only direct functions.
- All file operations are subject to security restrictions when `allowedPaths` is configured.
- There is no combined `os.path` module import: use `import os.path` separately for path operations.
- `__file__` is set automatically when running from a file, enabling `os.path.dirname(__file__)` to work as in Python.

## See Also

- [os.path](../os.path/): Path manipulation functions
- [pathlib](../pathlib/): Object-oriented filesystem paths
- [fs](../fs/): Binary file I/O
