---
title: shutil
description: High-level file and directory operations — copy, move, rmtree, disk_usage.
weight: 7
---

The `shutil` library provides high-level file and directory operations, similar to Python's `shutil` module. It complements [`os`](../os/) and [`pathlib`](../pathlib/) with operations like recursive tree deletion (`rmtree`), directory copying (`copytree`), and disk usage queries that are awkward to implement by hand.

## Available Functions

| Function | Description |
|----------|-------------|
| `copy(src, dst)` | Copy a file or directory tree. |
| `copy2(src, dst)` | Same as `copy` (file mode is always preserved). |
| `copytree(src, dst)` | Recursively copy a directory tree. |
| `rmtree(path)` | Recursively delete a directory tree. |
| `move(src, dst)` | Move or rename a file or directory. |
| `disk_usage(path)` | Return total, used, and free disk space. |

## Functions

### `copy(src, dst)`

Copies `src` to `dst`, preserving file modes. If `src` is a directory, the entire tree is copied recursively. Returns `dst`.

**Parameters:**
- `src` (`str`): Source file or directory.
- `dst` (`str`): Destination path.

**Returns:** `str`: the destination path.

```python
import shutil

shutil.copy("config.toml", "config.toml.bak")
shutil.copy("/opt/app/", "/opt/app-backup/")
```

### `copy2(src, dst)`

Identical to `copy()` — file mode is always preserved. Provided for Python compatibility.

### `copytree(src, dst)`

Recursively copies the directory tree rooted at `src` to `dst`. File modes are preserved. Returns `dst`.

**Parameters:**
- `src` (`str`): Source directory (must exist and be a directory).
- `dst` (`str`): Destination path (must not exist).

**Returns:** `str`: the destination path.

**Raises:** `Error` if `src` is not a directory.

```python
import shutil

shutil.copytree("templates/", "templates-backup/")
```

### `rmtree(path)`

Recursively deletes the directory at `path` and all of its contents (files, subdirectories, symlinks). Unlike [`os.removedirs`](../os/), the directory does not need to be empty.

**Parameters:** `path` (`str`): Directory to remove.

**Returns:** `None`.

```python
import shutil, tempfile

scratch = tempfile.mkdtemp(prefix="build_")
# ... do work ...
shutil.rmtree(scratch)  # clean up everything
```

### `move(src, dst)`

Atomically moves `src` to `dst` (same as `os.rename`). Returns `dst`.

**Parameters:**
- `src` (`str`): Source path.
- `dst` (`str`): Destination path.

**Returns:** `str`: the destination path.

```python
import shutil

shutil.move("output.tmp", "output.final")
```

### `disk_usage(path)`

Returns disk usage statistics for the file system containing `path`.

**Parameters:** `path` (`str`): Any path on the file system to query.

**Returns:** `dict` with keys:
- `total` (`int`): Total space in bytes.
- `used` (`int`): Used space in bytes (includes reserved blocks).
- `free` (`int`): Free space available to non-privileged users.

```python
import shutil

du = shutil.disk_usage("/")
print(f"{du['used'] / du['total'] * 100:.1f}% used")
# e.g. "67.3% used"
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

All operations are subject to the `allowedPaths` passed to `RegisterShutilLibrary(p, allowedPaths)`. Both `src` and `dst` (or `path`) must be within the allowed directories; path traversal (`../`) is blocked automatically and symlinks resolving outside the allowed set are rejected. See [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries) and the [Security Guide](/docs/security/#file-system-security).

## See Also

- [tempfile](../tempfile/): Temporary file and directory creation
- [os](../os/): Operating system interfaces
- [pathlib](../pathlib/): Object-oriented filesystem paths
