---
description: File and directory provisioning libraries for Scriptling.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/provisioning/
sources:
    - resource: https://scriptling.dev/reference/libraries/provisioning/
status: stable
tags:
    - libraries
    - provisioning
title: Provisioning Libraries
type: API Reference
---
# Provisioning Libraries

Provisioning libraries for managing files and directories within the Scriptling environment.

## Libraries

| Library | Description |
|---------|-------------|
| [scriptling.provision.file](https://scriptling.dev/okf/scriptling-libraries/provisioning/provision-file.md) | File and directory provisioning: create, update, and remove with correct permissions, plus marker-delimited managed blocks for maintaining a region within a file |
| [scriptling.provision.fetch](https://scriptling.dev/okf/scriptling-libraries/provisioning/provision-fetch.md) | HTTP/HTTPS file fetching with optional insecure TLS and safe zip unpacking |

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

- [Utilities](https://scriptling.dev/okf/scriptling-libraries/./utilities.md) - General purpose utility libraries
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Full library reference index
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Filesystem risk breakdown
