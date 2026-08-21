---
description: Read and write TAR archives (uncompressed and gzipped).
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/filesystem/tarfile/
sources:
    - resource: https://scriptling.dev/reference/libraries/filesystem/tarfile/
status: stable
tags:
    - libraries
    - filesystem
title: tarfile
type: API Reference
---
# tarfile

The `tarfile` library provides TAR archive reading and writing with optional gzip compression, similar to Python's `tarfile` module.

## Available Functions

| Function | Description |
|----------|-------------|
| `TarFile(path, mode="r")` | Open a TAR archive. Modes: `"r"`, `"r:gz"`, `"w"`, `"w:gz"`. |
| `is_tarfile(path)` | Check if a file is a valid TAR archive. |

## TarFile Methods

| Method | Description |
|-------|-------------|
| `getnames()` | Return a list of archive member names. |
| `read(name)` | Read a member as a string. |
| `extract(member, path=".")` | Extract a single member. |
| `extractall(path=".")` | Extract all members. |
| `add(filename, arcname=None)` | Add a file to the archive (write mode). |
| `addstr(name, data)` | Write a string as a member (write mode). |
| `close()` | Close the archive. |

## Usage

### Reading and Extracting

```python
import tarfile

tf = tarfile.TarFile("archive.tar")
for name in tf.getnames():
    print(name, len(tf.read(name)))

# Extract everything
tf.extractall("/tmp/output")
tf.close()
```

### Gzipped Archives

```python
import tarfile

# Read .tar.gz
tf = tarfile.TarFile("archive.tar.gz", "r:gz")
tf.extractall("/tmp/output")
tf.close()

# Write .tar.gz
tf = tarfile.TarFile("output.tar.gz", "w:gz")
tf.addstr("file.txt", "compressed content")
tf.close()
```

### Creating

```python
import tarfile

tf = tarfile.TarFile("output.tar", "w")
tf.add("/var/log/app.log", "logs/app.log")
tf.addstr("metadata.json", '{"version": "1.0"}')
tf.close()
```

## Security Considerations

This is an extended library, requiring registration in Go. Both the archive path and extraction destination must be within `allowedPaths`. Tar-slip (path traversal via crafted entry names) is blocked automatically. See [Library Registration](../../scriptling-docs/go-integration/library-registration.md#filesystem-libraries) and the [Security Guide](../../scriptling-docs/security.md#file-system-security).
