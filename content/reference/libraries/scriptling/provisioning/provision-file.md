---
title: scriptling.provision.file
linkTitle: provision.file
weight: 5
---

File provisioning library for creating and updating files with correct permissions.

## Overview

The `scriptling.provision.file` library writes files only when their content differs from what's already on disk, making it safe to call repeatedly without unnecessary writes. It also supports managing **marker-delimited blocks** inside a larger file so you can maintain just a region (for example, a managed section inside a shell rc file) without touching the rest.

## Available Functions

| Function | Description |
|----------|-------------|
| `ensure(path, content, mode=0o644, create_only=False)` | Ensure a file exists with the given content |
| `absent(path)` | Remove a file if it exists |
| `ensure_directory(path, mode=0o755)` | Ensure a directory exists |
| `absent_directory(path)` | Remove an empty directory if it exists |
| `ensure_block(path, content, id="managed", comment="#", position="end", insert_after="", mode=0o644, create_only=False)` | Maintain a marker-delimited block within a file |
| `absent_block(path, id="managed", comment="#")` | Remove a managed block |

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

## ensure_block

```python
ensure_block(
    path: str,
    content: str,
    id: str = "managed",
    comment: str = "#",
    position: str = "end",
    insert_after: str = "",
    mode: int = 0o644,
    create_only: bool = False,
) -> str
```

Maintains a **managed block** inside a file. The block is wrapped in distinctive markers and only the text between them is replaced on each run — everything outside the markers is left byte-for-byte untouched. If the markers are not present, the block is inserted at the chosen position.

The markers are generated from `comment` and `id` and look like this:

```
# >>> scriptling managed: myid >>>
<content>
# <<< scriptling managed: myid <<<
```

A unique `id` lets multiple independent blocks coexist in the same file. Use a different `comment` prefix for non-shell file types (for example `"//"`).

### Placement

When the markers are not yet present in the file, the block is inserted according to:

- `position="end"` (default) — append the block to the end of the file.
- `position="start"` — prepend the block at the start of the file.
- `insert_after="<substring>"` — insert the block immediately after the first line containing the substring. `insert_after` takes precedence over `position`. If the anchor is not found, an error is returned and the file is left unchanged.

Once a block exists, subsequent calls only swap the content between the markers; the block is **not** moved, regardless of `position` / `insert_after`.

If the file does not exist, it is created (including parent directories) containing just the managed block, with a trailing newline.

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `path` | — | Path to the file (supports `~` expansion) |
| `content` | — | Block contents maintained between the markers |
| `id` | `"managed"` | Block identifier embedded in the markers |
| `comment` | `"#"` | Comment prefix used to build the markers |
| `position` | `"end"` | Where to insert a new block: `"end"` or `"start"` |
| `insert_after` | `""` | Substring anchor; new block inserted after first match (overrides `position`) |
| `mode` | `0o644` | File permission mode used when creating the file |
| `create_only` | `False` | If `True`, never modify an existing block |

### Returns

`str` — one of `file.CREATED`, `file.UPDATED`, `file.UNCHANGED`.

### Content rules

- A single trailing newline in `content` is normalized, so `"foo\n"` and `"foo"` produce the same block.
- Empty `content` is allowed and reserves a region with just the two markers.
- An error is raised if `content` itself contains a marker line, or if the file contains **orphaned** markers (a begin without a matching end, or duplicate markers).

### Example

```python
import scriptling.provision.file as file

# Append a managed section to ~/.bashrc
status = file.ensure_block("~/.bashrc", "export EDITOR=vim\n", id="editor")

# Insert after a specific anchor line
file.ensure_block("/etc/hosts", "127.0.0.1 myapp\n", insert_after="localhost")

# Multiple independent blocks in the same file
file.ensure_block("~/.bashrc", "alias ll='ls -la'\n", id="aliases")
```

## absent_block

```python
absent_block(path: str, id: str = "managed", comment: str = "#") -> str
```

Removes the managed block (both markers and all content between them) for the given `id`. Everything else in the file is left untouched. The existing file's permission mode is preserved. If no such block exists, nothing happens.

### Returns

`str` — `file.REMOVED` if the block was deleted, `file.UNCHANGED` if the block was not present. An error is raised on orphaned markers.

### Example

```python
import scriptling.provision.file as file

status = file.absent_block("~/.bashrc", id="editor")
if status == file.REMOVED:
    print("Block removed")
```
