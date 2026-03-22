---
title: Packages
description: Create, distribute, and load Scriptling packages.
weight: 4
---

Packages are ZIP archives containing Scriptling libraries that can be loaded from local files or URLs. They enable easy distribution and reuse of code.

## Overview

A package is a ZIP file containing:

```
mylib.zip
├── manifest.toml    # Required - package metadata
├── lib/             # Required - Python modules
│   ├── __init__.py
│   └── utils.py
└── docs/            # Optional - documentation
    └── guide.md
```

## Package Manifest

The `manifest.toml` file describes the package:

```toml
name = "mylib"
version = "1.0.0"
description = "A useful library"
main = "app.main"    # Optional: entry point for running
```

**Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Package name |
| `version` | Yes | Version string |
| `description` | No | Brief description |
| `main` | No | Entry point as `module.function` for running |

## Loading Packages

Use the `--package` (or `-p`) flag to load packages:

```bash
# Load from local file
scriptling --package ./libs/mylib.zip script.py

# Load from URL
scriptling --package https://example.com/libs/mylib.zip script.py

# Load multiple packages
scriptling --package core.zip --package utils.zip script.py
```

### Package Priority

When loading multiple packages, the last one has highest priority. Later packages can override modules from earlier ones:

```bash
# override.zip can shadow modules from core.zip
scriptling --package core.zip --package override.zip script.py
```

### Self-Signed Certificates

Use `--insecure` (or `-k`) to allow self-signed HTTPS certificates:

```bash
scriptling --insecure --package https://self-signed.local/lib.zip script.py
```

### Hash Verification

Verify package integrity by specifying an expected SHA256 hash:

```bash
# Verify package hash before loading
scriptling --package mylib.zip#sha256=abc123... script.py

# With URL (download and verify)
scriptling --package https://example.com/lib.zip#sha256=abc123... script.py
```

**How it works:**
- Append `#sha256=<hash>` to the package path or URL
- Scriptling computes the SHA256 hash after fetching
- If the hash doesn't match, loading fails with an error
- For local files, the hash is optional (no hash = no verification)
- For remote URLs, this ensures the package hasn't been tampered with

**Getting the hash:**

When you create a package, the hash is printed:

```bash
scriptling pack ./mylib -o mylib.zip
# Output includes: SHA256: abc123def456...
```

Or use the `manifest` command:

```bash
scriptling manifest mylib.zip
# Shows: Hash: abc123def456...
```

### Custom Cache Directory

Remote packages are cached locally. Override the cache location with `--cache-dir`:

```bash
scriptling --cache-dir ./cache --package https://example.com/lib.zip script.py
```

Or set the `SCRIPTLING_CACHE_DIR` environment variable.

## Running Packages

If a package defines a `main` entry point in its manifest, you can run it directly:

```bash
# Run the package's main function
scriptling --package mylib.zip

# With arguments
scriptling --package mylib.zip -- arg1 arg2
```

**Execution order:**
1. If `-c` given → execute inline code
2. Else if `--interactive` → start REPL
3. Else if script file or stdin → execute script
4. Else if packages with `main` → run entry point from last package
5. Else → error

## Inline Code

Use `-c` to execute inline code with packages loaded:

```bash
scriptling --package mylib.zip -c "import utils; print(utils.hello('World'))"
```

## Creating Packages

### Package Structure

Create a directory with your code:

```
mylib/
├── manifest.toml
├── lib/
│   ├── __init__.py
│   ├── utils.py
│   └── submodule/
│       ├── __init__.py
│       └── helpers.py
└── docs/
    └── guide.md
```

### Pack Command

Create a package from a directory:

```bash
# Create package
scriptling pack ./mylib -o mylib.zip

# Overwrite existing
scriptling pack ./mylib -o mylib.zip -f
```

The SHA256 hash is printed on success — use it with `#sha256=...` to verify integrity on load.

### Unpack Command

Extract a package for development:

```bash
# Unpack to current directory
scriptling unpack mylib.zip

# Unpack to specific directory
scriptling unpack mylib.zip -d ./mylib-dev

# List contents without extracting
scriptling unpack mylib.zip --list

# From URL
scriptling unpack https://example.com/lib.zip -d ./lib
```

## Viewing Package Information

### Manifest Command

View package metadata:

```bash
# From local package
scriptling pack manifest mylib.zip

# From URL
scriptling pack manifest https://example.com/lib.zip

# From source directory
scriptling pack manifest ./mylib

# JSON output
scriptling pack manifest mylib.zip --json
```

### Docs Command

Browse package documentation interactively:

```bash
# Launch TUI browser
scriptling pack docs mylib.zip

# From URL
scriptling pack docs https://example.com/lib.zip

# From unpacked directory
scriptling pack docs ./mylib-dev

# List docs without TUI
scriptling pack docs mylib.zip --list
```

## Cache Management

Remote packages are cached with ETag/Last-Modified validation:

```bash
# Clear all cached packages
scriptling cache clear
```

## Using Packages in Code

Once loaded, packages work like any other module:

```python
# Import from package
import utils
from submodule import helpers

# Use functions
result = utils.process("data")
helpers.format(result)
```

## Distribution

Share packages via any HTTP server:

```bash
# Create and upload
scriptling pack ./mylib -o mylib.zip
scp mylib.zip server:/var/www/libs/

# Others can use directly
scriptling --package https://yourserver.com/libs/mylib.zip app.py
```

## See Also

- [Basic Usage](../basic-usage/) - Running scripts and interactive mode
- [HTTP Server Mode](../http-server/) - Running as an HTTP server
- [MCP Server Mode](../mcp-server/) - Model Context Protocol integration
