---
title: Packages
description: Create, distribute, and load Scriptling packages.
tags: [cli]
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
# Output includes: sha256=abc123def456...
```

Or use the `manifest` command to print a package's metadata:

```bash
scriptling pack manifest mylib.zip
# Shows: Name, Version, Description, and Main fields from the manifest
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

The SHA256 hash is printed on success: use it with `#sha256=...` to verify integrity on load.

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

Remote packages (http:// and https://) are cached locally to avoid redundant downloads. Scriptling uses HTTP conditional requests to check for updates efficiently.

### How Caching Works

When loading a remote package:

1. **First download** - Package is cached to disk along with its `ETag` and `Last-Modified` headers
2. **Subsequent loads** - Scriptling sends a conditional `GET` request with:
   - `If-None-Match: <etag>` - if the server provided an ETag
   - `If-Modified-Since: <last-modified>` - if the server provided Last-Modified
3. **If server responds `304 Not Modified`** - Uses cached copy (no body transferred)
4. **If server responds `200 OK`** - Downloads and caches the updated package

This means:
- **Single request** - One GET request, whether cached or not
- **Automatic updates** - New versions are fetched immediately when available
- **Bandwidth efficient** - No body transferred when unchanged

### Cache Location

Default cache directory:

| Platform | Location |
|----------|----------|
| macOS | `~/Library/Caches/scriptling/packages/` |
| Linux | `~/.cache/scriptling/packages/` |
| Windows | `%LOCALAPPDATA%\scriptling\packages\` |

Override with `--cache-dir` or `SCRIPTLING_CACHE_DIR` environment variable.

### Cache Commands

```bash
# Clear all cached packages
scriptling cache clear
```

### Cache TTL

Cached packages are automatically pruned after 7 days of non-use. Each access resets the TTL, so frequently used packages stay cached indefinitely.

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

## App Bundles

A package whose manifest declares `serve` becomes an **app bundle** — a complete
application shipped as one artifact. The manifest owns all path and registration
config; the CLI only picks the transport.

### Manifest

```toml
name = "myapp"
version = "1.0.0"
main = "setup.py"           # .py file (runs top-level) or "module.function"
libs = ["lib", "vendor"]    # module search dirs (default ["lib"])
serve = ["http", "mcp"]     # "http", "mcp", "json-rpc" — any combination
```

| Field | Description |
|-------|-------------|
| `main` | Entry point: a `.py` file path (runs top-level) or `module.function`. If absent, no setup script runs. |
| `libs` | Module search dirs inside the package, searched in order. Default `["lib"]`. |
| `serve` | Protocols to enable. Presence of `serve` makes the package an app bundle. |

### Transport

The `serve` list declares **what** the app provides, not how it's reached.
The CLI flags decide the transport:

| CLI flags | What happens |
|-----------|-------------|
| `--package .` (no `--server`) | MCP or JSON-RPC over **stdio** (whichever is in `serve`) |
| `--server :8000 --package .` | All declared protocols over **HTTP**: MCP at `/mcp`, JSON-RPC at `/json-rpc`, HTTP routes at their registered paths |

So `serve = ["mcp"]` works for both `scriptling --package .` (stdio) and `scriptling --server :8000 --package .` (HTTP at `/mcp`).

### Convention Dirs

These top-level dirs are auto-discovered when present:

| Dir | Protocol | Contents |
|-----|----------|----------|
| `tools/` | mcp | `.py` + `.toml` pairs (MCP tools) |
| `resources/` | mcp | Resource tree (static files and `{var}` templates) |
| `prompts/` | mcp | `.toml` + `.py` pairs or `.md`/`.txt` (MCP prompts) |
| `webroot/` | http | Static assets served at the HTTP root |
| `docs/` | — | Documentation viewer |

### Running

```bash
# Development — run from a folder (hot-reloadable)
scriptling --server :8000 --package ./myapp          # HTTP (all serve protocols)
scriptling --package ./myapp                           # stdio (MCP or JSON-RPC)

# Production — run from a zip
scriptling pack ./myapp myapp.zip
scriptling --server :8000 --package myapp.zip
scriptling --server :8000 --package https://host/myapp.zip#sha256=...
```

In app-bundle mode the CLI rejects path/registration flags (`-L`, `--script`,
`--mcp-tools`, `--mcp-resources`, `--mcp-prompts`, `--web-root`, `--code`,
`--interactive`) because the manifest owns them. Deployment flags (`--server`,
`--tls-*`, `--bearer-token`, secrets) remain valid.

### main Resolution

`main` accepts two forms, resolved at boot by lookup order:

1. Ends in `.py` **and the file exists** → run the file top-level (the bundle
   analogue of `--script`).
2. Otherwise → `module.function` (eval `import mod` + `mod.fn()`).
3. Neither resolves → boot error.

So `main = "setup.py"` runs the file; `main = "demo.run"` calls the function.
`main = "foo.py"` with no such file falls back to module `foo`, function `py`.

### Library Packs (without serve)

A package without `serve` is a **library pack** — it provides importable modules
only, exactly as before. The `--package` flag accepts multiple library packs
alongside one app bundle:

```bash
scriptling --server :8000 --package ./myapp --package ./vendor-deps.zip
```

### Build Inclusion

`pack build` includes exactly: `manifest.toml`, every `libs` dir, the `main`
script file, and the convention dirs when present. Dotfiles are excluded
silently; anything else at the top level produces a warning. Missing declared
`libs` dirs or `main` scripts are build errors.

### Examples

- `examples/app-bundle/` — reference HTTP + MCP app with routes, tools and
  webroot.
- `examples/jsonrpc-package/` — JSON-RPC server shipped as a package (stdio +
  HTTP).
- `examples/sample-package/` — classic library pack (no `serve`, proves
  backward compatibility).

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
