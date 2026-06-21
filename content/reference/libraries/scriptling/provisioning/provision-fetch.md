---
title: scriptling.provision.fetch
linkTitle: provision.fetch
weight: 6
---

Fetch provisioning library for downloading files over HTTP/HTTPS and optionally unpacking zip archives.

## Overview

The `scriptling.provision.fetch` library downloads remote files to local paths in an idempotent way. If the destination already contains the fetched bytes, the call returns `fetch.UNCHANGED`; otherwise it writes the new content and returns `fetch.CREATED` or `fetch.UPDATED`.

When `unpack_zip=True`, the destination is treated as a directory and the response body is extracted as a zip archive. Zip entries are constrained to the destination directory, so path traversal entries such as `../secret` are rejected.

## Available Functions

| Function | Description |
|----------|-------------|
| `file(url, dest, insecure=False, unpack_zip=False, timeout=30, max_bytes=0, mode=0o644, dir_mode=0o755, provides=None)` | Download a file or unpack a fetched zip archive |

## Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| `fetch.CREATED` | `"created"` | Destination file or extracted files were newly created |
| `fetch.UPDATED` | `"updated"` | Existing destination content changed |
| `fetch.UNCHANGED` | `"unchanged"` | Existing destination content already matched |

## file

```python
file(
    url: str,
    dest: str,
    insecure: bool = False,
    unpack_zip: bool = False,
    timeout: int = 30,
    max_bytes: int = 0,
    mode: int = 0o644,
    dir_mode: int = 0o755,
    provides: list[str] = None,
) -> dict
```

Downloads `url` using HTTP GET. The URL must use `http://` or `https://`.

When `unpack_zip=False`, `dest` is a file path. Parent directories are created automatically.

When `unpack_zip=True`, `dest` is a directory path. The fetched body is read as a zip archive and each file entry is written under that directory.

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `url` | — | `http://` or `https://` URL to fetch |
| `dest` | — | Destination file, or destination directory when `unpack_zip=True` |
| `insecure` | `False` | Skip HTTPS certificate verification |
| `unpack_zip` | `False` | Treat the response body as a zip archive and extract it |
| `timeout` | `30` | Request timeout in seconds |
| `max_bytes` | `0` | Maximum response size in bytes, or `0` for no cap |
| `mode` | `0o644` | File permission mode for written files |
| `dir_mode` | `0o755` | Directory permission mode for created directories |
| `provides` | `None` | List of file paths. If all paths exist, returns `UNCHANGED` without downloading or extracting |

### Returns

`dict` with:

| Key | Description |
|-----|-------------|
| `status` | `fetch.CREATED`, `fetch.UPDATED`, or `fetch.UNCHANGED` |
| `url` | Source URL |
| `path` | Destination path |
| `bytes` | Size of the fetched response body |
| `unpacked` | `True` when `unpack_zip=True` |
| `files` | Written or checked file paths |

When unpacking a zip archive, `fetch.UPDATED` takes precedence over `fetch.CREATED`: if one entry updates existing content and another creates a new file, the overall status is `fetch.UPDATED`. Existing files whose bytes already match are still chmod'd to the requested mode. For zip entries, executable bits from the archive are OR'd into `mode`, so a `0o755` file in the archive remains executable when the default `mode=0o644` is used. Directory entries create missing directories with `dir_mode`; existing directories are not re-chmod'd.

### Examples

Download a file:

```python
import scriptling.provision.fetch as fetch

result = fetch.file(
    "https://example.com/app.conf",
    "~/.config/app/app.conf",
    mode=0o600,
)

if result["status"] != fetch.UNCHANGED:
    print("Fetched " + result["path"])
```

Fetch and unpack a zip archive:

```python
import scriptling.provision.fetch as fetch

result = fetch.file(
    "https://example.com/site.zip",
    "/srv/site",
    unpack_zip=True,
)

print("Extracted " + str(len(result["files"])) + " files")
```

Use insecure TLS only for trusted internal endpoints:

```python
import scriptling.provision.fetch as fetch

fetch.file(
    "https://internal.example.test/bootstrap.zip",
    "/opt/bootstrap",
    insecure=True,
    unpack_zip=True,
)
```

Skip fetching when all expected files are already present:

```python
import scriptling.provision.fetch as fetch

result = fetch.file(
    "https://example.com/site.zip",
    "/srv/site",
    unpack_zip=True,
    provides=["/srv/site/bin/app", "/srv/site/config.yaml"],
)

if result["status"] == fetch.UNCHANGED:
    print("All provided files already exist — skipped")
```

## Security Notes

- `insecure=True` disables HTTPS certificate verification. Use it only for trusted internal endpoints or bootstrapping environments where certificate validation is impossible.
- Zip extraction rejects absolute paths and `..` traversal paths.
- Zip extraction rejects non-regular file entries such as symlinks and device files.
- Use `max_bytes` when fetching from endpoints where a large or misconfigured response could exhaust memory.
- This library performs network and filesystem writes. Avoid registering it for untrusted scripts unless the host environment is otherwise constrained.
