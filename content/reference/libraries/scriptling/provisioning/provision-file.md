---
title: scriptling.provision.file
linkTitle: provision.file
description: Create, update, and remove files and directories idempotently, including marker-delimited managed blocks.
weight: 5
---

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

| Constant | Description |
|----------|-------------|
| `file.CREATED` | File or directory was newly created (`"created"`) |
| `file.UPDATED` | File existed but content differed (`"updated"`) |
| `file.UNCHANGED` | File existed with identical content (`"unchanged"`) |
| `file.REMOVED` | File or directory was deleted (`"removed"`) |
| `file.ABSENT` | File or directory did not exist (`"absent"`) |
| `file.EXISTS` | Directory already existed (`"exists"`) |

## Functions

### `ensure(path, content, mode=0o644, create_only=False)`

Ensures a file exists with the given content. Creates parent directories if needed. If the file already exists with the same content, it is left unchanged; otherwise the file is written with the specified mode.

When `create_only=True`, an existing file is never modified: the call returns `file.UNCHANGED` without writing, even if the content on disk differs. New files are still written normally. This is useful for seeding configuration files that should only be created once and left alone on subsequent runs.

**Parameters:**
- `path` (`str`): Path to the file (supports `~` expansion).
- `content` (`str`): File contents.
- `mode` (`int`, optional): File permission mode. Default: `0o644`.
- `create_only` (`bool`, optional): If `True`, never modify an existing file. Default: `False`.

**Returns:** `str`: one of `file.CREATED`, `file.UPDATED`, `file.UNCHANGED`.

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

### `absent(path)`

Removes a file if it exists. Does nothing if the file is already absent.

**Parameters:**
- `path` (`str`): Path to the file (supports `~` expansion).

**Returns:** `str`: `file.REMOVED` or `file.ABSENT`.

```python
import scriptling.provision.file as file

status = file.absent("~/.old_config")
if status == file.REMOVED:
    print("File removed")
```

### `ensure_directory(path, mode=0o755)`

Creates a directory and all parent directories if needed.

**Parameters:**
- `path` (`str`): Path to the directory (supports `~` expansion).
- `mode` (`int`, optional): Directory permission mode. Default: `0o755`.

**Returns:** `str`: `file.CREATED` or `file.EXISTS`.

**Raises:** `Error`: if the path exists but is not a directory.

```python
import scriptling.provision.file as file

status = file.ensure_directory("~/.config/myapp", mode=0o700)
if status == file.CREATED:
    print("Directory created")
```

### `absent_directory(path)`

Removes an empty directory if it exists.

**Parameters:**
- `path` (`str`): Path to the directory (supports `~` expansion).

**Returns:** `str`: `file.REMOVED` or `file.ABSENT`.

**Raises:** `Error`: if the directory is not empty, or the path exists but is not a directory.

```python
import scriptling.provision.file as file

status = file.absent_directory("~/old/empty/dir")
if status == file.REMOVED:
    print("Directory removed")
```

### `ensure_block(path, content, id="managed", comment="#", position="end", insert_after="", mode=0o644, create_only=False)`

Maintains a **managed block** inside a file. The block is wrapped in distinctive markers and only the text between them is replaced on each run: everything outside the markers is left byte-for-byte untouched. If the markers are not present, the block is inserted at the chosen position.

The markers are generated from `comment` and `id` and look like this:

```
# >>> scriptling managed: myid >>>
<content>
# <<< scriptling managed: myid <<<
```

A unique `id` lets multiple independent blocks coexist in the same file. Use a different `comment` prefix for non-shell file types (for example `"//"`).

When the markers are not yet present in the file, the block is inserted according to:

- `position="end"` (default): append the block to the end of the file.
- `position="start"`: prepend the block at the start of the file.
- `insert_after="<substring>"`: insert the block immediately after the first line containing the substring. `insert_after` takes precedence over `position`. If the anchor is not found, an error is returned and the file is left unchanged.

Once a block exists, subsequent calls only swap the content between the markers; the block is **not** moved, regardless of `position` / `insert_after`. If the file does not exist, it is created (including parent directories) containing just the managed block, with a trailing newline.

A single trailing newline in `content` is normalized, so `"foo\n"` and `"foo"` produce the same block. Empty `content` is allowed and reserves a region with just the two markers.

**Parameters:**
- `path` (`str`): Path to the file (supports `~` expansion).
- `content` (`str`): Block contents maintained between the markers.
- `id` (`str`, optional): Block identifier embedded in the markers. Default: `"managed"`.
- `comment` (`str`, optional): Comment prefix used to build the markers. Default: `"#"`.
- `position` (`str`, optional): Where to insert a new block: `"end"` or `"start"`. Default: `"end"`.
- `insert_after` (`str`, optional): Substring anchor; new block inserted after first match (overrides `position`). Default: `""`.
- `mode` (`int`, optional): File permission mode used when creating the file. Default: `0o644`.
- `create_only` (`bool`, optional): If `True`, never modify an existing block. Default: `False`.

**Returns:** `str`: one of `file.CREATED`, `file.UPDATED`, `file.UNCHANGED`.

**Raises:** `Error`: if `content` itself contains a marker line, if the file contains orphaned markers (a begin without a matching end, or duplicate markers), or if `insert_after` is set but no matching line is found.

```python
import scriptling.provision.file as file

# Append a managed section to ~/.bashrc
status = file.ensure_block("~/.bashrc", "export EDITOR=vim\n", id="editor")

# Insert after a specific anchor line
file.ensure_block("/etc/hosts", "127.0.0.1 myapp\n", insert_after="localhost")

# Multiple independent blocks in the same file
file.ensure_block("~/.bashrc", "alias ll='ls -la'\n", id="aliases")
```

### `absent_block(path, id="managed", comment="#")`

Removes the managed block (both markers and all content between them) for the given `id`. Everything else in the file is left untouched. The existing file's permission mode is preserved. If no such block exists, nothing happens.

**Parameters:**
- `path` (`str`): Path to the file (supports `~` expansion).
- `id` (`str`, optional): Block identifier embedded in the markers. Default: `"managed"`.
- `comment` (`str`, optional): Comment prefix used to build the markers. Default: `"#"`.

**Returns:** `str`: `file.REMOVED` if the block was deleted, `file.UNCHANGED` if the block was not present.

**Raises:** `Error`: on orphaned markers.

```python
import scriptling.provision.file as file

status = file.absent_block("~/.bashrc", id="editor")
if status == file.REMOVED:
    print("Block removed")
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.provision.file` writes, modifies, and deletes files and directories on the local filesystem wherever the embedding process's own OS-level permissions allow. Unlike `os`, `fs`, or `pathlib`, it does not take an `allowedPaths` restriction: there is no per-library sandboxing of which paths it can touch. If you need to confine where provisioning writes can land, restrict it at the OS/process level (e.g. running under a dedicated user, container, or chroot) rather than relying on library-level controls. For a full risk breakdown across all libraries, see the [Security Guide](/docs/security/).

## See Also

- [scriptling.provision.fetch](../provision-fetch/): download remote files and unpack zip archives to disk
- [Library Registration](/docs/go-integration/library-registration/#extended-libraries)
- [Security Guide](/docs/security/)
