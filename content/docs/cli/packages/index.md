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

# Load single Python file
scriptling --package ./helper.py script.py
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

Only `manifest.toml`, `lib/`, and `docs/` are included in the package.

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
scriptling manifest mylib.zip

# From URL
scriptling manifest https://example.com/lib.zip

# From source directory
scriptling manifest ./mylib

# JSON output
scriptling manifest mylib.zip --json
```

### Help Command

Query built-in help for functions:

```bash
# Help for package function
scriptling help mylib.utils.helper
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
