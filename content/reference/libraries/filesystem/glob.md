---
title: glob
description: Unix shell-style wildcard matching for filenames, similar to Python's glob module.
weight: 1
aliases:
  - /reference/libraries/extlib/glob/
  - /reference/libraries/glob/
---

The `glob` library provides Unix shell-style wildcards for filename matching, similar to Python's `glob` module. Reach for it when you need to find files and directories matching a pattern rather than walking a directory tree by hand.

## Available Functions

| Function | Description |
|----------|-------------|
| `glob(pattern, root_dir=".")` | Find all pathnames matching a pattern. |
| `iglob(pattern, root_dir=".")` | Iterator over pathnames matching a pattern. |
| `escape(pattern)` | Escape special characters so a pattern is matched literally. |

## Functions

### `glob(pattern, root_dir=".")`

Find all pathnames matching a pattern. Pattern syntax: `*` matches everything, `?` matches any single character, `[seq]` matches any character in `seq`, `[!seq]` matches any character not in `seq`, and `**` matches all files and directories recursively (when supported). Results are returned in arbitrary order, and an empty list is returned if there are no matches.

**Parameters:**
- `pattern` (`str`): Shell-style wildcard pattern to match.
- `root_dir` (`str`, optional): Directory to search from. Default: `"."`.

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

# Recursively find all markdown files
docs = glob.glob("**/*.md")

# Search from a specific directory
configs = glob.glob("*.json", "/etc/myapp")
```

### `iglob(pattern, root_dir=".")`

Find all pathnames matching a pattern, returned as an iterator instead of a list. This is more memory efficient for large result sets since matches are not all materialized at once.

**Parameters:**
- `pattern` (`str`): Shell-style wildcard pattern to match.
- `root_dir` (`str`, optional): Directory to search from. Default: `"."`.

**Returns:** `iterator`: yields matching pathnames as strings.

```python
import glob

# Process files one at a time
for filename in glob.iglob("**/*.py"):
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
