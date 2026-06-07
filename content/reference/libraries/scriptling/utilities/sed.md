---
title: scriptling.sed
linkTitle: sed
weight: 2
---

The `scriptling.sed` library provides in-place file content replacement and capture group extraction. Both replace functions accept a file or a directory as the path. Files are modified atomically using a temp-file rename, so a partial write cannot corrupt a file. Binary files are skipped automatically.

## Available Functions

| Function | Description |
| --- | --- |
| `replace(old, new, path, **kwargs)` | Replace a literal string in a file or directory |
| `replace_pattern(regex, new, path, **kwargs)` | Replace a regex match in a file or directory |
| `extract(regex, path, **kwargs)` | Extract regex capture groups from a file or directory |

`replace` and `replace_pattern` return the number of files modified as an integer. `extract` returns a list of match dicts.

## Functions

### scriptling.sed.replace(old, new, path, ...)

Replace all occurrences of a literal string in a file or directory.

**Parameters:**

- `old` (string): Literal string to search for
- `new` (string): Replacement string
- `path` (string): File or directory to modify
- `recursive` (bool, optional): Recurse into subdirectories. Default: `False`
- `ignore_case` (bool, optional): Case-insensitive matching. Default: `False`
- `glob` (string, optional): Only modify files whose name matches this glob pattern, e.g. `"*.py"`. Default: all files
- `follow_links` (bool, optional): Follow symlinks if they resolve within allowed paths. Default: `False`
- `max_size` (int or None, optional): Skip files larger than this many bytes. Default: `1048576` (1 MiB). Pass `None` to disable.

**Returns:** `int` — number of files modified

**Example:**

```python
import scriptling.sed as sed

# Replace in a single file
n = sed.replace("old_func()", "new_func()", "/path/to/file.py")

# Replace across all Python files recursively
n = sed.replace("old_func()", "new_func()", "./src", recursive=True, glob="*.py")
print(f"{n} file(s) modified")

# Case-insensitive replace
n = sed.replace("TODO", "DONE", "./src", ignore_case=True, recursive=True)
```

### scriptling.sed.replace_pattern(regex, new, path, ...)

Replace all regex matches in a file or directory. Capture groups are referenced in the replacement string using `${1}`, `${2}`, or named groups `${name}`.

**Parameters:**

- `regex` (string): Regular expression pattern
- `new` (string): Replacement string (may reference capture groups as `${1}`, `${2}`, etc.)
- `path` (string): File or directory to modify
- `recursive` (bool, optional): Recurse into subdirectories. Default: `False`
- `ignore_case` (bool, optional): Case-insensitive matching. Default: `False`
- `glob` (string, optional): Only modify files whose name matches this glob pattern, e.g. `"*.py"`. Default: all files
- `follow_links` (bool, optional): Follow symlinks if they resolve within allowed paths. Default: `False`
- `max_size` (int or None, optional): Skip files larger than this many bytes. Default: `1048576` (1 MiB). Pass `None` to disable.

**Returns:** `int` — number of files modified

**Example:**

```python
import scriptling.sed as sed

# Rename a function across all Python files
n = sed.replace_pattern(
    r"def old_(\w+)\(",
    "def new_${1}(",
    "./src",
    recursive=True,
    glob="*.py"
)
print(f"{n} file(s) modified")

# Add a type annotation to all function definitions
n = sed.replace_pattern(
    r"def (\w+)\(self\):",
    "def ${1}(self) -> None:",
    "./src",
    recursive=True,
    glob="*.py"
)
```

### scriptling.sed.extract(regex, path, ...)

Extract regex capture groups from a file or directory. Returns a list of match dicts with the captured groups for each match.

**Parameters:**

- `regex` (string): Regular expression with capture groups
- `path` (string): File or directory to search
- `recursive` (bool, optional): Recurse into subdirectories. Default: `False`
- `ignore_case` (bool, optional): Case-insensitive matching. Default: `False`
- `glob` (string, optional): Only search files whose name matches this glob pattern, e.g. `"*.py"`. Default: all files
- `follow_links` (bool, optional): Follow symlinks if they resolve within allowed paths. Default: `False`
- `max_size` (int or None, optional): Skip files larger than this many bytes. Default: `1048576` (1 MiB). Pass `None` to disable.

**Returns:** `list` of match dicts:

```python
{"file": str, "line": int, "text": str, "groups": list}
```

- `file` — path to the matched file
- `line` — 1-based line number
- `text` — full content of the matched line
- `groups` — list of captured group strings (empty list if no capture groups)

**Example:**

```python
import scriptling.sed as sed

# Extract all function names from Python files
matches = sed.extract(r"def (\w+)\(", "./src", recursive=True, glob="*.py")
for m in matches:
    print(f"{m['file']}:{m['line']}: {m['groups'][0]}")

# Extract key=value pairs
matches = sed.extract(r"(\w+)=(\S+)", "./config.txt")
for m in matches:
    key, value = m["groups"]
    print(f"{key} -> {value}")

# Extract version strings
matches = sed.extract(r"version\s*=\s*[\"']([\d.]+)[\"']", "./src", recursive=True, glob="*.py")
versions = [m["groups"][0] for m in matches]
```

## Pairing with scriptling.grep

`scriptling.grep` and `scriptling.sed` are designed to work together — grep finds, sed transforms:

```python
import scriptling.grep as grep
import scriptling.sed as sed

# Find files containing the old API, then replace in them
matches = grep.string("old_func()", "./src", recursive=True, glob="*.py")
files = list({m["file"] for m in matches})
print(f"Found in {len(files)} file(s)")

# Replace across the whole directory at once
n = sed.replace("old_func()", "new_func()", "./src", recursive=True, glob="*.py")
print(f"Updated {n} file(s)")
```

## Capture Group Syntax

`replace_pattern` uses Go regular expression syntax for capture groups in the replacement string:

| Replacement | Meaning |
| --- | --- |
| `${1}` | First capture group |
| `${2}` | Second capture group |
| `${name}` | Named capture group `(?P<name>...)` |

```python
import scriptling.sed as sed

# Using numbered groups
sed.replace_pattern(r"(\w+)_old", "${1}_new", "./src", recursive=True)

# Using named groups
sed.replace_pattern(r"(?P<fn>\w+)\(self\)", "${fn}(self, ctx)", "./src", recursive=True)
```

## Security

`scriptling.sed` respects the path restrictions configured at registration time. Any path outside the allowed directories returns a permission error. Symlinks are only followed if `follow_links=True` **and** the resolved target is within the allowed paths.

## Performance

Directory operations use the same concurrent worker pool as `scriptling.grep` — bounded at `max(4, NumCPU/2)` goroutines. Each file is written atomically: content is written to a temp file in the same directory, then renamed over the original, which is an atomic operation on all supported platforms.
