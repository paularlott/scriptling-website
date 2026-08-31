---
title: Provisioning Libraries
linkTitle: Provisioning
description: File and directory provisioning libraries for Scriptling.
tags: [libraries, provisioning]
weight: 15

aliases:
  - /reference/libraries/scriptling/provisioning/
---

Provisioning libraries for managing files and directories within the Scriptling environment.

## Libraries

| Library | Description |
|---------|-------------|
| [scriptling.provision.file](provision-file/) | File and directory provisioning: create, update, and remove with correct permissions, plus marker-delimited managed blocks for maintaining a region within a file |
| [scriptling.provision.fetch](provision-fetch/) | HTTP/HTTPS file fetching with optional insecure TLS and safe zip unpacking |

## Quick Start

```python
import scriptling.provision.file as file

# Idempotently ensure a config file exists
status = file.ensure("~/.gitconfig", "[user]\n    name = Jane Doe\n", mode=0o600)
print(status)  # file.CREATED, file.UPDATED, or file.UNCHANGED

# Ensure a directory exists
file.ensure_directory("~/.config/myapp")
```

## See Also

- [Utilities](../utilities/) - General purpose utility libraries
- [Libraries](../) - Full library reference index
- [Security Guide](/docs/security/) - Filesystem risk breakdown
