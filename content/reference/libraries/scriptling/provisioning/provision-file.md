---
title: scriptling.provision.file
linkTitle: provision.file
weight: 5
---

File provisioning library for creating and updating files with correct permissions.

## Overview

The `scriptling.provision.file` library provides a single `ensure` function that writes a file only if its content differs from what's already on disk. This makes it safe to call repeatedly without unnecessary writes.

## Available Functions

| Function | Description |
|----------|-------------|
| `ensure(path, content, mode=0o644, create_only=False)` | Ensure a file exists with the given content |
| `absent(path)` | Remove a file if it exists |
| `ensure_directory(path, mode=0o755)` | Ensure a directory exists |
| `absent_directory(path)` | Remove an empty directory if it exists |

## Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| `file.CREATED` | `"created"` | File or directory was newly created |
| `file.UPDATED` | `"updated"` | File existed but content differed |
| `file.UNCHANGED` | `"unchanged"` | File existed with identical content |
| `file.REMOVED` | `"removed"` | File or directory was deleted |
| `file.ABSENT` | `"absent"` | File or directory did not exist |
| `file.EXISTS` | `"exists"` | Directory already existed |

## ensure

```python
ensure(path: str, content: str, mode: int = 0o644, create_only: bool = False) -> str
```

Creates parent directories if needed. If the file already exists with the same content, it is left unchanged. Otherwise the file is written with the specified mode.

### create_only

When `create_only=True`, an existing file is never modified — the call returns `file.UNCHANGED` without writing, even if the content on disk differs. New files are still written normally. This is useful for seeding configuration files that should only be created once and left alone on subsequent runs.

### Constants

The return values can be compared using library constants:

| Constant | Value |
|----------|-------|
| `file.CREATED` | `"created"` |
| `file.UPDATED` | `"updated"` |
| `file.UNCHANGED` | `"unchanged"` |

### Returns

`str` — one of `file.CREATED`, `file.UPDATED`, `file.UNCHANGED`.

### Example

```python
import scriptling.provision.file as file

# Create a git config file
status = file.ensure("~/.gitconfig", """[user]
    name = Jane Doe
    email = jane@example.com
""", mode=0o600)

if status == file.CREATED:
    print("Git config created")
elif status == file.UPDATED:
    print("Git config updated")
```

Seed a file only on first run, leaving any later edits intact:

```python
import scriptling.provision.file as file

status = file.ensure("~/.config/myapp/defaults.toml", DEFAULTS, create_only=True)
```

## absent

```python
absent(path: str) -> str
```

Removes a file if it exists. Does nothing if the file is already absent.

### Returns

`str` — `file.REMOVED` or `file.ABSENT`.

### Example

```python
import scriptling.provision.file as file

status = file.absent("~/.old_config")
if status == file.REMOVED:
    print("File removed")
```

## ensure_directory

```python
ensure_directory(path: str, mode: int = 0o755) -> str
```

Creates a directory and all parent directories if needed.

### Returns

`str` — `file.CREATED` or `file.EXISTS`.

### Example

```python
import scriptling.provision.file as file

status = file.ensure_directory("~/.config/myapp", mode=0o700)
if status == file.CREATED:
    print("Directory created")
```

## absent_directory

```python
absent_directory(path: str) -> str
```

Removes an empty directory if it exists. Returns an error if the directory is not empty.

### Returns

`str` — `file.REMOVED` or `file.ABSENT`.

### Example

```python
import scriptling.provision.file as file

status = file.absent_directory("~/old/empty/dir")
if status == file.REMOVED:
    print("Directory removed")
```
