---
description: Find files and directories by name, type, modification time, and size.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/utilities/find/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/utilities/find/
status: stable
tags:
    - libraries
    - utilities
    - filesystem
title: scriptling.find
type: API Reference
---
# scriptling.find

The `scriptling.find` library finds files and directories under a path by name, type, modification time, and size — similar in spirit to the Unix `find` command. It fills the gap between `glob` (which matches names but cannot filter on metadata) and a hand-rolled `os.walk` loop.

When searching recursively, entries are stat'd and filtered concurrently using the same bounded worker-pool model as [`scriptling.grep`](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/grep.md), so large trees are scanned in parallel.

The library exposes two functions: `path()` returns matching paths as a list of strings, and `entries()` returns the same matches as a list of dicts carrying `size`, `mtime`, and `is_dir` per entry. Use `entries()` when you need the metadata (e.g. comparing two trees without re-reading bytes); use `path()` when only the strings are needed, since it skips the per-entry `stat` in the no-filter common case.

## Available Functions

| Function | Description |
|----------|-------------|
| `path(path, **kwargs)` | Find files/directories matching the given filters; returns `list[str]`. |
| `entries(path, **kwargs)` | Same filters as `path()`, but returns `list[dict]` with `path`, `size`, `mtime`, and `is_dir` per match; opt-in hash, link_target, metadata fields. |

## Functions

### `path(path, *, recursive=True, type="any", name="", mtime_min=None, mtime_max=None, size_min=None, size_max=None, include_hidden=False, follow_links=False, max_depth=None)`

Finds files and directories under `path` matching the supplied filters and returns their paths as a list of strings. Results are in arbitrary order; an empty list is returned when nothing matches.

If `path` is a single file, it is checked directly against the filters and returned (as a single-element list) when it matches.

**Parameters:**
- `path` (`str`): Directory (or file) to search under.
- `recursive` (`bool`, keyword-only): Descend into subdirectories. Default: `True`. When `False`, only the immediate children of `path` are examined.
- `type` (`str`, keyword-only): Restrict to `"file"` (regular files), `"dir"` (directories), or `"any"`. Default: `"any"`.
- `name` (`str`, keyword-only): Shell-style glob pattern matched against each entry's base name, e.g. `"*.md"`. Empty matches everything. Default: `""`.
- `mtime_min` (`float` or `None`, keyword-only): Include only entries modified at or after this epoch time (seconds). `None` = no lower bound. Default: `None`.
- `mtime_max` (`float` or `None`, keyword-only): Include only entries modified at or before this epoch time (seconds). `None` = no upper bound. Default: `None`.
- `size_min` (`int` or `None`, keyword-only): Include only entries whose size in bytes is `>=` this value. `None` = no lower bound. Default: `None`.
- `size_max` (`int` or `None`, keyword-only): Include only entries whose size in bytes is `<=` this value. `None` = no upper bound. Default: `None`.
- `include_hidden` (`bool`, keyword-only): When `True`, entries whose name starts with `.` are matched; when `False` (the default) they are skipped along with their subtrees.
- `follow_links` (`bool`, keyword-only): Follow symlinks if they resolve within allowed paths. Default: `False`.
- `max_depth` (`int` or `None`, keyword-only): Maximum recursion depth (`1` = immediate children only). `None` = unlimited. Default: `None`.

**Returns:** `list[str]`: matching paths.

**Raises:** `Error`: if `path` is outside the allowed paths (see [Security Considerations](#security-considerations)).

```python
import scriptling.find as find
import time

# All markdown files under /docs (recursive by default)
docs = find.path("/docs", name="*.md", type="file")

# Markdown files modified in the last 24 hours
recent = find.path("/docs", name="*.md", type="file",
                   mtime_min=time.time() - 86400)

# Large log files (> 100 MiB)
big_logs = find.path("/var/log", name="*.log", type="file",
                     size_min=100 * 1024 * 1024)

# All directories named "node_modules" (descend into dot-dirs too)
dirs = find.path("/project", type="dir", name="node_modules",
                 include_hidden=True)

# Only immediate children, no descent
top = find.path("/data", recursive=False)
```

### `entries(path, *, recursive=True, type="any", name="", mtime_min=None, mtime_max=None, size_min=None, size_max=None, include_hidden=False, follow_links=False, max_depth=None, include_metadata=False, include_hash=False, include_symlinks=False)`

Like `path()` — same filters, same semantics — but returns a `list[dict]` with one dict per match, so the caller can compare trees without re-reading bytes. Every matching entry is stat'd; use `path()` instead when only the strings are needed.

**Additional parameters** (beyond those shared with `path()`):

| Parameter | Type | Description |
|-----------|------|-------------|
| `include_metadata` | `bool` | When `True`, `file_perm` is populated (extracted from the entry stat, no extra syscall). |
| `include_hash` | `bool` | When `True`, each file is crc64-hashed and the hex checksum is returned in `hash`. Use for definitive change detection — two entries with matching `hash` have identical bytes. |
| `include_symlinks` | `bool` | When `True`, symbolic link entries are yielded with their `link_target` set to the symlink target string, instead of following the link. |

Each entry dict has the keys:

| Key | Type | Description |
|------|------|-------------|
| `path` | `str` | The matching entry's path. |
| `size` | `int` | Size in bytes. `0` for directories. |
| `mtime` | `float` | Modification time as epoch seconds (matches the unit used by `mtime_min`/`mtime_max`). |
| `is_dir` | `bool` | `True` when the entry is a directory. |
| `file_perm` | `int` or `None` | File permission bits. `None` unless `include_metadata=True`. |
| `hash` | `str` or `None` | Hex-encoded crc64 checksum of file content. `None` unless `include_hash=True`. |
| `link_target` | `str` or `None` | Symlink target path. `None` unless `include_symlinks=True`. |

**Parameters:** identical to [`path()`](#path), plus the three above. The root itself is never included in the result, and entries are returned in arbitrary order.

**Returns:** `list[dict]`: one dict per match.

**Raises:** `Error`: if `path` is outside the allowed paths.

```python
import scriptling.find as find
import time

# Sync-relevant metadata: every markdown file with its size and mtime
for e in find.entries("/docs", name="*.md", type="file"):
    print(e["path"], e["size"], e["mtime"])

# Build a {path: mtime} index for differential sync
mtimes = {e["path"]: e["mtime"] for e in find.entries("/site", type="file")}

# Directories only — is_dir is always True here, but size and mtime are
# still populated for the directory itself.
dirs = find.entries("/project", type="dir", name="node_modules")

# Hash-based change detection — only upload when bytes differ
for e in find.entries("/site", include_hash=True, type="file"):
    print(e["path"], e["hash"])

# Detect symbolic links without following them
for e in find.entries("/project", include_symlinks=True):
    if e["link_target"]:
        print(e["path"], "->", e["link_target"])
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`find` provides read access to the host filesystem (directory listings and `stat` calls). When embedding in Go, access is restricted to the `allowedPaths` passed to `RegisterFindLibrary(p, allowedPaths)`: path traversal (`../`) is blocked automatically and symlinks resolving outside the allowed paths are skipped. See [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#filesystem-libraries) and the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md#file-system-security).

## See Also

- [glob](https://scriptling.dev/okf/scriptling-libraries/filesystem/glob.md): Shell-style wildcard matching by name
- [pathlib](https://scriptling.dev/okf/scriptling-libraries/filesystem/pathlib.md): Object-oriented filesystem paths
- [scriptling.grep](https://scriptling.dev/okf/scriptling-libraries/scriptling/utilities/grep.md): File content search, using the same parallel worker model
