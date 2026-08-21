---
description: Fast file content search using regular expressions or literal strings.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/utilities/grep/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/utilities/grep/
status: stable
tags:
    - libraries
    - utilities
    - text
    - filesystem
title: scriptling.grep
type: API Reference
---
# scriptling.grep

The `scriptling.grep` library provides fast file content search. Use `pattern()` for regex searches and `string()` for literal string searches. Both accept a file or a directory as the path: if a directory is given, files are searched recursively or not depending on the options provided.

## Available Functions

| Function | Description |
|----------|-------------|
| `pattern(regex, path, **kwargs)` | Search using a regular expression |
| `string(text, path, **kwargs)` | Search for a literal string |

## Functions

### `pattern(regex, path, recursive=False, ignore_case=False, glob="", follow_links=False, max_size=1048576)`

Searches for a regular expression in a file or directory.

**Parameters:**
- `regex` (`str`): Regular expression pattern.
- `path` (`str`): File or directory to search.
- `recursive` (`bool`, optional): Recurse into subdirectories. Default: `False`.
- `ignore_case` (`bool`, optional): Case-insensitive matching. Default: `False`.
- `glob` (`str`, optional): Only search files whose name matches this glob pattern, e.g. `"*.py"`. Default: `""` (all files).
- `follow_links` (`bool`, optional): Follow symlinks if they resolve within allowed paths. Default: `False`.
- `max_size` (`int` or `None`, optional): Skip files larger than this many bytes. Default: `1048576` (1 MiB). Pass `None` to disable.

**Returns:** `list` of `dict`, each with keys:
- `file` (`str`): Path to the matched file.
- `line` (`int`): 1-based line number.
- `text` (`str`): Content of the matched line.

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

### `string(text, path, recursive=False, ignore_case=False, glob="", follow_links=False, max_size=1048576)`

Searches for a literal string in a file or directory. The text is treated exactly as written: no regex interpretation. Use this when the search term contains characters that have special meaning in regex (`.`, `(`, `)`, `*`, `+`, `?`, `[`, `]`, `^`, `$`, `|`, `\`) without needing to escape them.

**Parameters:**
- `text` (`str`): Literal string to search for.
- `path` (`str`): File or directory to search.
- `recursive` (`bool`, optional): Recurse into subdirectories. Default: `False`.
- `ignore_case` (`bool`, optional): Case-insensitive matching. Default: `False`.
- `glob` (`str`, optional): Only search files whose name matches this glob pattern, e.g. `"*.py"`. Default: `""` (all files).
- `follow_links` (`bool`, optional): Follow symlinks if they resolve within allowed paths. Default: `False`.
- `max_size` (`int` or `None`, optional): Skip files larger than this many bytes. Default: `1048576` (1 MiB). Pass `None` to disable.

**Returns:** `list` of `dict`, each with keys:
- `file` (`str`): Path to the matched file.
- `line` (`int`): 1-based line number.
- `text` (`str`): Content of the matched line.

```python
import scriptling.grep as grep

# Literal search: "." is not a wildcard here
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
grep.string("foo.bar", path)   # no match (looks for literal "foo.bar")
```

## Performance

Directory searches use a concurrent worker pool (bounded at `max(4, NumCPU/2)` goroutines). Files are scanned line-by-line with `bufio.Scanner` to keep memory usage flat regardless of file size. Binary files are automatically skipped by sniffing the first 8 KB for null bytes.

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

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](../../../scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.grep` has filesystem read access, restricted via the `allowedPaths` parameter to `RegisterGrepLibrary(p, allowedPaths)`. Any path outside the allowed directories returns a permission error, and symlinks are only followed if `follow_links=True` **and** the resolved target is within the allowed paths. See [Library Registration](../../../scriptling-docs/go-integration/library-registration.md#filesystem-libraries) for configuration details.

## See Also

- [scriptling.sed](sed.md) - Pair with grep to find-then-transform file content
- [Library Registration](../../../scriptling-docs/go-integration/library-registration.md) - Registering extended libraries when embedding in Go
- [Security Guide](../../../scriptling-docs/security.md) - Security guidance for host-provided libraries
