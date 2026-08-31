---
description: Read and write ZIP archives.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/filesystem/zipfile/
sources:
    - resource: https://scriptling.dev/reference/libraries/filesystem/zipfile/
status: stable
tags:
    - libraries
    - filesystem
title: zipfile
type: API Reference
---
# zipfile

The `zipfile` library provides ZIP archive reading and writing, similar to Python's `zipfile` module.

## Available Functions

| Function | Description |
|----------|-------------|
| `ZipFile(path, mode="r")` | Open a ZIP archive for reading or writing. |
| `is_zipfile(path)` | Check if a file is a valid ZIP archive. |

## ZipFile Methods

| Method | Description |
|-------|-------------|
| `namelist()` | Return a list of archive member names. |
| `read(name)` | Read a member as a string. |
| `extract(member, path=".")` | Extract a single member. |
| `extractall(path=".")` | Extract all members. |
| `write(filename, arcname=None)` | Add a file to the archive (write mode). |
| `writestr(name, data)` | Write a string as a member (write mode). |
| `close()` | Close the archive. |

## Usage

### Reading

```python
import zipfile

zf = zipfile.ZipFile("archive.zip")
for name in zf.namelist():
    print(name, len(zf.read(name)))
zf.close()
```

### Extracting

```python
import zipfile

with zipfile.ZipFile("archive.zip") as zf:  # close() is called automatically
    zf.extractall("/tmp/output")
```

### Creating

```python
import zipfile

zf = zipfile.ZipFile("output.zip", "w")
zf.writestr("readme.txt", "hello world")
zf.write("/etc/hostname", "config/hostname")
zf.close()
```

### Checking

```python
import zipfile

if zipfile.is_zipfile("maybe.zip"):
    print("valid zip")
```

## Security Considerations

This is an extended library, requiring registration in Go. Both the archive path and extraction destination must be within `allowedPaths`. Zip-slip (path traversal via crafted entry names) is blocked automatically. See [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#filesystem-libraries) and the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md#file-system-security).
