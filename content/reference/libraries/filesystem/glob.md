---
title: glob
description: Unix shell-style wildcard matching for filenames, similar to Python's glob module.
tags: [libraries, filesystem]
weight: 1
aliases:
  - /reference/libraries/extlib/glob/
  - /reference/libraries/glob/
---

The `glob` library provides Unix shell-style wildcards for filename matching, similar to Python's `glob` module. Reach for it when you need to find files and directories matching a pattern rather than walking a directory tree by hand.

## Available Functions

| Function | Description |
|----------|-------------|
| `glob(pattern, root_dir=".", *, recursive=False, include_hidden=False)` | Find all pathnames matching a pattern. |
| `iglob(pattern, root_dir=".", *, recursive=False, include_hidden=False)` | Iterator over pathnames matching a pattern. |
| `escape(pattern)` | Escape special characters so a pattern is matched literally. |

## Functions

### `glob(pattern, root_dir=".", *, recursive=False, include_hidden=False)`

Find all pathnames matching a pattern. Pattern syntax: `*` matches everything except a path separator, `?` matches any single character, `[seq]` matches any character in `seq`, `[!seq]` matches any character not in `seq`, and `**` matches all files and directories recursively when `recursive=True`. Results are returned in arbitrary order, and an empty list is returned if there are no matches.

By default entries whose name starts with `.` (dot-files and dot-directories) are skipped. Pass `include_hidden=True` to match them.

When `recursive=True`, the directory walk runs as a bounded parallel search using the same worker model as [`scriptling.grep`](../../scriptling/utilities/grep/), so deep trees are scanned concurrently.

**Parameters:**
- `pattern` (`str`): Shell-style wildcard pattern to match.
- `root_dir` (`str`, optional): Directory to search from. Default: `"."`.
- `recursive` (`bool`, keyword-only): When `True`, `**` matches files and directories recursively, descending into every subdirectory. When `False` (the default), `**` is treated as `*`.
- `include_hidden` (`bool`, keyword-only): When `True`, entries whose name starts with `.` are matched; when `False` (the default) they are skipped.

**Returns:** `list`: matching pathnames as strings.

**Raises:** `Error`: if `root_dir` is outside the allowed paths (see [Security Considerations](#security-considerations)).

```python
import glob

# Match all files ending in .txt
txt_files = glob.glob("*.txt")

# Match files starting with "test"
test_files = glob.glob("test*")

# Match single character variations
files = glob.glob("file?.txt")  # file1.txt, filea.txt, etc.

# Match character ranges
logs = glob.glob("log[0-9].txt")  # log0.txt, log1.txt, etc.

# Recursively find all markdown files (descends into subdirectories)
docs = glob.glob("**/*.md", recursive=True)

# Same search, but also descend into dot-directories such as .github
all_docs = glob.glob("**/*.md", recursive=True, include_hidden=True)

# Search from a specific directory
configs = glob.glob("*.json", "/etc/myapp")
```

### `iglob(pattern, root_dir=".", *, recursive=False, include_hidden=False)`

Find all pathnames matching a pattern, returned as an iterator instead of a list. This is more memory efficient for large result sets since matches are not all materialized at once. Accepts the same parameters as [`glob()`](#globpattern-root_dir-recursive-include_hidden).

**Parameters:**
- `pattern` (`str`): Shell-style wildcard pattern to match.
- `root_dir` (`str`, optional): Directory to search from. Default: `"."`.
- `recursive` (`bool`, keyword-only): When `True`, `**` matches recursively (default: `False`).
- `include_hidden` (`bool`, keyword-only): When `True`, dot-entries are matched (default: `False`).

**Returns:** `iterator`: yields matching pathnames as strings.

```python
import glob

# Process files one at a time
for filename in glob.iglob("**/*.py", recursive=True):
    print(f"Found: {filename}")
```

### `escape(pattern)`

Escape all special characters (`*`, `?`, `[`, `]`) in a pattern so they are treated as literal characters rather than wildcards.

**Parameters:**
- `pattern` (`str`): Pattern containing characters to escape.

**Returns:** `str`: the escaped pattern.

```python
import glob

# Escape special characters to search for a literal filename
pattern = glob.escape("file*.txt")
# Returns "file[*].txt" which matches the literal "file*.txt"
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`glob` provides read access to the host filesystem (directory listings and path matching). When embedding in Go, access is restricted to the `allowedPaths` passed to `RegisterGlobLibrary(p, allowedPaths)`: path traversal (`../`) is blocked automatically. See [Library Registration](/docs/go-integration/library-registration/#filesystem-libraries) and the [Security Guide](/docs/security/#file-system-security).

## See Also

- [os](../os/): Operating system interfaces
- [pathlib](../pathlib/): Object-oriented filesystem paths, including a `Path.glob()` method
- [fs](../fs/): Binary file I/O
