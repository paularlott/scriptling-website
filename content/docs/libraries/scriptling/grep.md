---
title: scriptling.grep
linkTitle: grep
weight: 1
---

The `scriptling.grep` library provides fast file content search. Use `pattern()` for regex searches and `string()` for literal string searches. Both accept a file or a directory as the path — if a directory is given, files are searched according to the options provided.

## Registration

```go
import "github.com/paularlott/scriptling/extlibs"

// No path restrictions
extlibs.RegisterGrepLibrary(p, nil)

// Restricted to specific directories
extlibs.RegisterGrepLibrary(p, []string{"/tmp", "/home/user/data"})
```

## Available Functions

| Function | Description |
| --- | --- |
| `pattern(regex, path, **kwargs)` | Search using a regular expression |
| `string(text, path, **kwargs)` | Search for a literal string |

## Return Value

Both functions return a list of match dicts:

```python
{"file": str, "line": int, "text": str}
```

- `file` — path to the matched file
- `line` — 1-based line number
- `text` — content of the matched line

## Functions

### scriptling.grep.pattern(regex, path, ...)

Search for a regular expression in a file or directory.

**Parameters:**

- `regex` (string): Regular expression pattern
- `path` (string): File or directory to search
- `recursive` (bool, optional): Recurse into subdirectories. Default: `False`
- `ignore_case` (bool, optional): Case-insensitive matching. Default: `False`
- `glob` (string, optional): Only search files whose name matches this glob pattern, e.g. `"*.py"`. Default: all files
- `follow_links` (bool, optional): Follow symlinks if they resolve within allowed paths. Default: `False`
- `max_size` (int or None, optional): Skip files larger than this many bytes. Default: `1048576` (1 MiB). Pass `None` to disable.

**Returns:** `list` of match dicts

**Example:**

```python
import scriptling.grep as grep

# Find all TODO comments in Python files
matches = grep.pattern(r"\bTODO\b", "./src", recursive=True, glob="*.py")
for m in matches:
    print(f"{m['file']}:{m['line']}: {m['text']}")

# Case-insensitive regex
matches = grep.pattern("error|warning", "./logs", ignore_case=True, recursive=True)

# Search a single file
matches = grep.pattern(r"def \w+\(", "/path/to/script.py")
```

### scriptling.grep.string(text, path, ...)

Search for a literal string in a file or directory. The text is treated exactly as written — no regex interpretation. Use this when the search term contains characters that have special meaning in regex (`.`, `(`, `)`, `*`, `+`, `?`, `[`, `]`, `^`, `$`, `|`, `\`) without needing to escape them.

**Parameters:**

- `text` (string): Literal string to search for
- `path` (string): File or directory to search
- `recursive` (bool, optional): Recurse into subdirectories. Default: `False`
- `ignore_case` (bool, optional): Case-insensitive matching. Default: `False`
- `glob` (string, optional): Only search files whose name matches this glob pattern, e.g. `"*.py"`. Default: all files
- `follow_links` (bool, optional): Follow symlinks if they resolve within allowed paths. Default: `False`
- `max_size` (int or None, optional): Skip files larger than this many bytes. Default: `1048576` (1 MiB). Pass `None` to disable.

**Returns:** `list` of match dicts

**Example:**

```python
import scriptling.grep as grep

# Literal search — "." is not a wildcard here
matches = grep.string("foo.bar()", "./src", recursive=True)

# Case-insensitive literal search
matches = grep.string("TODO:", "./src", ignore_case=True, recursive=True, glob="*.py")

# Search a single file
matches = grep.string("import os", "/path/to/script.py")
```

## Choosing Between pattern() and string()

| | `pattern()` | `string()` |
|---|---|---|
| Input | Regular expression | Literal string |
| `.` matches | Any character | Only a literal `.` |
| Special chars | Interpreted as regex | Treated as-is |
| Use when | You need regex syntax | You're searching for exact text |

```python
import scriptling.grep as grep

# These behave differently on a file containing "foo bar":
grep.pattern("foo.bar", path)  # matches "foo bar" (. = any char)
grep.string("foo.bar", path)     # no match (looks for literal "foo.bar")
```

## Performance

Directory searches use a concurrent worker pool (bounded at `max(4, NumCPU/2)` goroutines). Files are scanned line-by-line with `bufio.Scanner` to keep memory usage flat regardless of file size. Binary files are automatically skipped by sniffing the first 8 KB for null bytes.

## Security

`scriptling.grep` respects the path restrictions configured at registration time. Any path outside the allowed directories returns a permission error. Symlinks are only followed if `follow_links=True` **and** the resolved target is within the allowed paths.

## Regex Syntax

`pattern()` uses Go regular expressions. Key syntax:

| Pattern | Matches |
| --- | --- |
| `foo` | Literal `foo` anywhere on the line |
| `^foo` | Lines starting with `foo` |
| `foo$` | Lines ending with `foo` |
| `\bfoo\b` | Word boundary around `foo` |
| `foo\|bar` | `foo` or `bar` |
| `\d+` | One or more digits |
| `(?i)foo` | Case-insensitive `foo` (alternative to `ignore_case=True`) |
