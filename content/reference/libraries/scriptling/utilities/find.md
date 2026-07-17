---
title: scriptling.find
linkTitle: find
description: Find files and directories by name, type, modification time, and size.
tags: [libraries, utilities, filesystem]
weight: 1
---

The `scriptling.find` library finds files and directories under a path by name, type, modification time, and size — similar in spirit to the Unix `find` command. It fills the gap between `glob` (which matches names but cannot filter on metadata) and a hand-rolled `os.walk` loop.

When searching recursively, entries are stat'd and filtered concurrently using the same bounded worker-pool model as [`scriptling.grep`](./grep/), so large trees are scanned in parallel.

## Available Functions

| Function | Description |
|----------|-------------|
| `path(path, **kwargs)` | Find files/directories matching the given filters. |

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

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`find` provides read access to the host filesystem (directory listings and `stat` calls). When embedding in Go, access is restricted to the `allowedPaths` passed to `RegisterFindLibrary(p, allowedPaths)`: path traversal (`../`) is blocked automatically and symlinks resolving outside the allowed paths are skipped. See [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries) and the [Security Guide](/docs/security/#file-system-security).

## See Also

- [glob](../../filesystem/glob/): Shell-style wildcard matching by name
- [pathlib](../../filesystem/pathlib/): Object-oriented filesystem paths
- [scriptling.grep](./grep/): File content search, using the same parallel worker model
