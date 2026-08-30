---
description: Download files over HTTP/HTTPS and optionally unpack zip archives, idempotently.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/provisioning/provision-fetch/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/provisioning/provision-fetch/
status: stable
tags:
    - libraries
    - provisioning
    - http
title: scriptling.provision.fetch
type: API Reference
---
# scriptling.provision.fetch

## Overview

The `scriptling.provision.fetch` library downloads remote files to local paths in an idempotent way. If the destination already contains the fetched bytes, the call returns `fetch.UNCHANGED`; otherwise it writes the new content and returns `fetch.CREATED` or `fetch.UPDATED`. When `unpack_zip=True`, the destination is treated as a directory and the response body is extracted as a zip archive, with entries constrained to that directory so path-traversal entries such as `../secret` are rejected.

## Available Functions

| Function | Description |
|----------|-------------|
| `file(url, dest, insecure=False, unpack_zip=False, timeout=30, max_bytes=0, mode=0o644, dir_mode=0o755, provides=None)` | Download a file, or download and unpack a zip archive |

## Constants

| Constant | Description |
|----------|-------------|
| `fetch.CREATED` | Destination file or extracted files were newly created (`"created"`) |
| `fetch.UPDATED` | Existing destination content changed (`"updated"`) |
| `fetch.UNCHANGED` | Existing destination content already matched (`"unchanged"`) |

## Functions

### `file(url, dest, insecure=False, unpack_zip=False, timeout=30, max_bytes=0, mode=0o644, dir_mode=0o755, provides=None)`

Downloads `url` using HTTP GET. The URL must use `http://` or `https://`.

When `unpack_zip=False`, `dest` is a file path and parent directories are created automatically. When `unpack_zip=True`, `dest` is a directory path: the fetched body is read as a zip archive and each file entry is written under that directory.

When unpacking a zip archive, `fetch.UPDATED` takes precedence over `fetch.CREATED`: if one entry updates existing content and another creates a new file, the overall status is `fetch.UPDATED`. Existing files whose bytes already match are still chmod'd to the requested mode. For zip entries, executable bits from the archive are OR'd into `mode`, so a `0o755` file in the archive remains executable even when the default `mode=0o644` is used. Directory entries create missing directories with `dir_mode`; existing directories are not re-chmod'd.

**Parameters:**
- `url` (`str`): `http://` or `https://` URL to fetch.
- `dest` (`str`): Destination file path, or destination directory when `unpack_zip=True`.
- `insecure` (`bool`, optional): Skip HTTPS certificate verification. Default: `False`.
- `unpack_zip` (`bool`, optional): Treat the response body as a zip archive and extract it. Default: `False`.
- `timeout` (`int`, optional): Request timeout in seconds. Default: `30`.
- `max_bytes` (`int`, optional): Maximum response size in bytes, or `0` for no cap. Default: `0`.
- `mode` (`int`, optional): File permission mode for written files. Default: `0o644`.
- `dir_mode` (`int`, optional): Directory permission mode for created directories. Default: `0o755`.
- `provides` (`list`, optional): List of file paths. If all paths exist, returns `fetch.UNCHANGED` without downloading or extracting. Default: `None`.

**Returns:** `dict`: with keys:

| Key | Description |
|-----|-------------|
| `status` | `fetch.CREATED`, `fetch.UPDATED`, or `fetch.UNCHANGED` |
| `url` | Source URL |
| `path` | Destination path |
| `bytes` | Size of the fetched response body |
| `unpacked` | `True` when `unpack_zip=True` |
| `files` | Written or checked file paths |

**Raises:** `Error`: if the URL scheme isn't `http`/`https`, the request fails or times out, the response exceeds `max_bytes`, or a zip entry would escape the destination directory or is not a regular file.

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
    print("All provided files already exist: skipped")
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.provision.fetch` makes outbound HTTP/HTTPS requests to arbitrary URLs and writes the downloaded bytes (or unpacked zip contents) to the local filesystem: so it combines network access with filesystem writes. Setting `insecure=True` disables HTTPS certificate verification entirely; only use it for trusted internal endpoints or bootstrap scenarios where certificate validation is genuinely impossible: passing it carelessly exposes downloads to interception and tampering. Zip extraction rejects absolute paths, `..` traversal, and non-regular entries (symlinks, device files), but the library otherwise writes wherever the host process has permission. For a full risk breakdown across all libraries, see the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md).

## See Also

- [scriptling.provision.file](https://scriptling.dev/okf/scriptling-libraries/scriptling/provisioning/provision-file.md): provision plain files and managed blocks without fetching them remotely
- [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries)
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md)
