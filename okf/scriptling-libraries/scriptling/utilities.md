---
description: General purpose utility libraries for Scriptling.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/utilities/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/utilities/
status: stable
tags:
    - libraries
    - utilities
title: Utilities Libraries
type: API Reference
---
# Utilities Libraries

General purpose utility libraries for common scripting tasks.

## Libraries

| Library | Description |
|---------|-------------|
| [scriptling.console](utilities/console.md) | Console input/output functions (TUI) |
| [scriptling.container](utilities/container.md) | Container lifecycle management for Docker, Podman, and Apple Containers |
| [scriptling.nomad](utilities/nomad.md) | HashiCorp Nomad client covering CSI volumes and jobs |
| [scriptling.grep](utilities/grep.md) | Fast file content search with regex or literal patterns |
| [scriptling.find](utilities/find.md) | Find files and directories by name, type, mtime, and size |
| [scriptling.csv](utilities/csv.md) | CSV parsing and formatting (string-based) |
| [scriptling.xml](utilities/xml.md) | XML parsing and formatting (dict-based, string-only) |
| [scriptling.sed](utilities/sed.md) | In-place file content replacement with literal strings or regex patterns |
| [scriptling.secret](utilities/secret.md) | Resolve secrets through host-configured provider aliases |
| [scriptling.wait_for](utilities/wait_for.md) | Wait for resources to become available |
| [scriptling.toon](utilities/toon.md) | TOON (Token-Oriented Object Notation) encoding/decoding |
| [scriptling.similarity](utilities/similarity.md) | Text similarity utilities including fuzzy search and MinHash |
| [scriptling.template](utilities/template.md) | Go-powered template rendering (HTML and text) |
| [scriptling.markdown](utilities/markdown.md) | Markdown to HTML conversion (GitHub Flavored Markdown) |

## Quick Start

```python
import scriptling.grep as grep

# Find all TODO comments in Python files
matches = grep.pattern(r"\bTODO\b", "./src", recursive=True, glob="*.py")
for m in matches:
    print(f"{m['file']}:{m['line']}: {m['text']}")
```

## See Also

- [Provisioning](provisioning.md) - File and directory provisioning libraries
- [Runtime](runtime.md) - Background tasks, HTTP, and storage
- [Libraries](../scriptling-libraries.md) - Full library reference index
- [Security Guide](../../scriptling-docs/security.md) - Security guidance for host-provided libraries
