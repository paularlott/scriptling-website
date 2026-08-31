---
title: scriptling.package
linkTitle: package
description: Read metadata and files from app and plugin bundles loaded by the host.
tags: [libraries, packages, bundles]
weight: 19
---

## Overview

`scriptling.package` provides read-only access to app and plugin bundles already loaded by the host. It can enumerate package names, inspect versions, and read or list packaged files without exposing the loader itself.

```python
import scriptling.package as package

for name in package.names():
    print(name, package.version(name))

if package.file_exists("myapp", "config/defaults.toml"):
    defaults = package.read_file("myapp", "config/defaults.toml")
```

## Availability

This library is conditional. Ordinary CLI and server execution register it only when a package loader has app bundles, explicitly configured bundles, or plugin-declared bundles. It is absent when no loader is configured. Embedders using the CLI package loader can call `RegisterPackageLibrary(p, loader)`; registration is a no-op for a nil loader.

## Available Functions

| Function | Description |
|----------|-------------|
| `names()` | Return loaded package names |
| `version(name)` | Return a package's manifest version |
| `exists(name)` | Test whether a package is loaded |
| `file_exists(name, path)` | Test whether a file or directory path exists in a package |
| `read_file(name, path)` | Read a package file as text |
| `read_bytes(name, path)` | Read a package file as `bytes` |
| `list(name, path)` | List direct children beneath a package path |
| `glob(name, pattern)` | List files matching a package-relative glob |

## Functions

### `names()`

Returns loaded package names.

**Returns:** `list[str]`

### `version(name)`

Returns the `version` from the named package's manifest.

**Returns:** `str`

**Raises:** `Error` if the package is not loaded.

### `exists(name)`

Returns `True` if the named package is loaded and `False` otherwise.

### `file_exists(name, path)`

Returns `True` if `path` names an existing file or directory in the package. Unknown packages and missing paths return `False`.

### `read_file(name, path)` / `read_bytes(name, path)`

Read a packaged file as `str` or [`bytes`](data-formats/bytes/) respectively. Paths are package-relative; a leading slash is removed and path traversal is cleaned before access.

**Raises:** `Error` if the package or file is not available.

### `list(name, path)`

Lists direct children under `path`. Directory names end in `/`.

```python
entries = package.list("myapp", "templates")
```

### `glob(name, pattern)`

Returns package-relative files matching `pattern`. `*` and `?` stay within one path segment; `**` crosses path separators.

```python
python_files = package.glob("myapp", "lib/**/*.py")
```

## Security Considerations

The API is read-only, but it makes host-selected bundle contents visible to the script. Do not put credentials or other data in a loaded bundle unless every script with this library may read them. Package registration does not grant access to arbitrary host files; it is limited to the loader's bundle filesystems.

## See Also

- [Runtime MCP](runtime/mcp/): tools packaged in app bundles
- [Libraries](./): library availability and registration overview
