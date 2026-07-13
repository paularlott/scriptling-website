---
title: Utilities Libraries
linkTitle: Utilities
description: General purpose utility libraries for Scriptling.
weight: 1
---

General purpose utility libraries for common scripting tasks.

## Libraries

| Library | Description |
|---------|-------------|
| [scriptling.console](console/) | Console input/output functions (TUI) |
| [scriptling.container](container/) | Container lifecycle management for Docker, Podman, and Apple Containers |
| [scriptling.nomad](nomad/) | HashiCorp Nomad client covering CSI volumes and jobs |
| [scriptling.grep](grep/) | Fast file content search with regex or literal patterns |
| [scriptling.find](find/) | Find files and directories by name, type, mtime, and size |
| [scriptling.sed](sed/) | In-place file content replacement with literal strings or regex patterns |
| [scriptling.secret](secret/) | Resolve secrets through host-configured provider aliases |
| [scriptling.wait_for](wait_for/) | Wait for resources to become available |
| [scriptling.toon](toon/) | TOON (Token-Oriented Object Notation) encoding/decoding |
| [scriptling.similarity](similarity/) | Text similarity utilities including fuzzy search and MinHash |
| [scriptling.template](template/) | Go-powered template rendering (HTML and text) |
| [scriptling.markdown](markdown/) | Markdown to HTML conversion (GitHub Flavored Markdown) |

## Quick Start

```python
import scriptling.grep as grep

# Find all TODO comments in Python files
matches = grep.pattern(r"\bTODO\b", "./src", recursive=True, glob="*.py")
for m in matches:
    print(f"{m['file']}:{m['line']}: {m['text']}")
```

## See Also

- [Provisioning](../provisioning/) - File and directory provisioning libraries
- [Runtime](../runtime/) - Background tasks, HTTP, and storage
- [Libraries](../../) - Full library reference index
- [Security Guide](/docs/security/) - Security guidance for host-provided libraries
