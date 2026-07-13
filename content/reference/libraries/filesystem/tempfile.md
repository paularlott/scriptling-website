---
title: tempfile
description: Temporary file and directory creation with security restrictions.
weight: 6
---

The `tempfile` library creates temporary files and directories, similar to Python's `tempfile` module. All temporary paths are created with restrictive permissions (0600 for files, 0700 for directories) and are subject to the same `allowedPaths` restrictions as other filesystem libraries.

## Available Functions

| Function | Description |
|----------|-------------|
| `mkstemp(suffix="", prefix="tmp", dir=None)` | Create a temporary file and return its path. |
| `mkdtemp(suffix="", prefix="tmp", dir=None)` | Create a temporary directory and return its path. |
| `gettempdir()` | Return the default temporary directory. |
| `gettempprefix()` | Return the default prefix (`"tmp"`). |

## Functions

### `mkstemp(suffix="", prefix="tmp", dir=None)`

Creates a new temporary file and returns its path. The file is created with mode `0600` (owner read/write only) and immediately closed — unlike Python's `mkstemp`, which returns a file descriptor, this returns just the path.

**Parameters:**
- `suffix` (`str`, keyword-only): Suffix for the filename. Default: `""`.
- `prefix` (`str`, keyword-only): Prefix for the filename. Default: `"tmp"`.
- `dir` (`str` or `None`, keyword-only): Directory to create the file in. Default: the system temp directory.

**Returns:** `str`: the absolute path to the created file.

```python
import tempfile

# Simple temp file
path = tempfile.mkstemp()

# With a specific prefix and suffix
config = tempfile.mkstemp(prefix="app_", suffix=".toml")
# e.g. /tmp/app_4827361.toml
```

### `mkdtemp(suffix="", prefix="tmp", dir=None)`

Creates a new temporary directory and returns its path. The directory is created with mode `0700` (owner only).

**Parameters:** Same as `mkstemp`.

**Returns:** `str`: the absolute path to the created directory.

```python
import tempfile

scratch = tempfile.mkdtemp(prefix="build_")
# e.g. /tmp/build_9182736

# ... use scratch for intermediate files ...

import shutil
shutil.rmtree(scratch)  # clean up
```

### `gettempdir()`

Returns the system's default temporary directory. When `allowedPaths` restricts access and the system temp directory is outside the allowed set, the first allowed path is returned instead.

**Returns:** `str`: the temp directory path.

### `gettempprefix()`

Returns the default prefix used for temporary names.

**Returns:** `str`: `"tmp"`.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

Temporary files and directories are subject to the same `allowedPaths` restrictions as other filesystem libraries. When embedding in Go, access is restricted to the `allowedPaths` passed to `RegisterTempfileLibrary(p, allowedPaths)`:

- If `dir` is specified and outside `allowedPaths`, the operation is denied.
- If `dir` is omitted and the system temp directory is outside `allowedPaths`, the library falls back to the first allowed path.
- The created path is verified against `allowedPaths` after creation; if it somehow resolves outside the allowed set, it is immediately removed and an error is raised.

See [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries) and the [Security Guide](/docs/security/#file-system-security).

## See Also

- [shutil](../shutil/): High-level file operations (including `rmtree` for cleanup)
- [os](../os/): Operating system interfaces
- [pathlib](../pathlib/): Object-oriented filesystem paths
