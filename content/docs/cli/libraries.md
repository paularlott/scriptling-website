---
title: CLI Libraries
description: Loading, disabling, and controlling library and filesystem access.
tags: [cli]
weight: 4
---

## Library Loading

Scriptling automatically searches for libraries in the same directory as the running script: matching Python's behaviour. For interactive mode or stdin, the current working directory is used.

```bash
# Libraries in ./myproject/ are found automatically
scriptling ./myproject/script.py

# Interactive mode: libraries in cwd are found automatically
scriptling --interactive
```

Use `--libpath` (repeatable, alias `-L`) to add extra search directories. The script directory (or cwd) is always searched first:

```bash
# Search script dir first, then /shared/libs
scriptling --libpath /shared/libs script.py

# Multiple extra directories
scriptling --libpath /shared/libs --libpath /company/libs script.py

# Via environment variable
SCRIPTLING_LIBPATH=/shared/libs scriptling script.py
```

Libraries follow Python-style folder organisation:

```
myproject/
  script.py
  utils.py              # import utils
  knot/
    groups.py           # import knot.groups
    roles.py            # import knot.roles
```

```python
# In script.py: no --libpath needed, same directory is searched automatically
import utils           # Loads from myproject/utils.py
import knot.groups     # Loads from myproject/knot/groups.py
```

For nested imports like `knot.groups`, the loader checks:
1. `dir/knot/groups.py` (folder structure: preferred)
2. `dir/knot.groups.py` (flat file: legacy fallback)

## Disabling and Listing Libraries

### List Available Libraries

Use `--list-libs` to print the CLI's built-in library inventory and exit:

```bash
scriptling --list-libs
```

The current inventory is not exhaustive: it omits some helper and contextual libraries that CLI setup registers. In particular, `msgpack` is available in the default no-disable CLI setup but is currently omitted from `--list-libs`. Supplying any `--disable-lib` also takes a selective registration path that currently omits `msgpack`.

When combined with `--disable-lib`, named libraries are excluded from the reported inventory:

```bash
scriptling --disable-lib subprocess --list-libs
```

### Disable Specific Libraries

Use `--disable-lib` (repeatable) to prevent specific built-in libraries from loading:

```bash
# Disable a single library
scriptling --disable-lib subprocess script.py

# Disable multiple libraries, and also stop scripts loading executable plugins
scriptling --disable-lib subprocess --disable-lib os script.py

# Via environment variable
SCRIPTLING_DISABLE_LIB=subprocess scriptling script.py
```

If a script attempts to import a disabled library, it raises `ImportError`, which can be caught with `try` / `except`.

## Script Filesystem Controls

`--allowed-paths` constrains filesystem operations made through participating Scriptling libraries. It is not a complete filesystem sandbox: subprocesses, plugin processes, setup scripts, TLS files, `--web-root` static assets, and other host-side operations are outside this library-level allowlist. Library loading is covered in one respect: the directories you name with `--libpath` (and the script's own directory) are trusted, but a library reached through a **symlink** in one of them is only loaded if the resolved file lies inside a library directory or an allowed path, so a link planted in a library directory cannot pull in a file from elsewhere. With no `--allowed-paths` the loader follows symlinks as it always has.

| Mode                 | Flag                            | Participating library access |
| -------------------- | ------------------------------- | ---------------------------- |
| **Unrestricted**     | (default)                       | Any path                     |
| **Allowlisted**      | `--allowed-paths /path1,/path2` | Only specified paths         |
| **Deny library I/O** | `--allowed-paths -`             | No paths                     |

### Unrestricted Mode (default)

The CLI registers its broad library set without filesystem restrictions:

```bash
scriptling script.py
```

### Allowlisted Mode

Participating library filesystem operations are restricted to specified paths:

```bash
# Restrict to specific directories
scriptling --allowed-paths "/tmp/data,./uploads" script.py

# Relative paths resolve from the working directory, not the script's directory
scriptling --allowed-paths "./data,../shared" script.py

# Via environment variable
SCRIPTLING_ALLOWED_PATHS="/var/www,./public" scriptling script.py
```

Paths are checked the way the kernel opens them: symlinks are resolved, dangling ones and ones that climb out with `..` included, so a link inside an allowed directory cannot reach a file outside it. `os.symlink()` also refuses a target outside the allowed paths, resolving a relative target from the link's directory.

### Deny Participating Library File Access

Deny filesystem access through the libraries wired to the allowlist:

```bash
scriptling --allowed-paths - script.py
```

This denies operations such as `os.read_file`, `os.write_file`, `pathlib`, `glob`, and `sandbox.exec_file`, along with `scriptling.wait_for` `file()`, `dir()` and `file_content()`, messaging `send_file()`, `scriptling.container` bind mounts, `runtime.http.static`, `runtime.kv.open`, `scriptling.provision.fetch` and `scriptling.provision.file`; it does not prevent an enabled `subprocess`, `scriptling.provision.command` or `scriptling.provision.package` from reading files with host commands. Disable that capability explicitly with `--disable-lib subprocess` in every mode, which removes all three.

When a script tries to access a path outside the allowed directories:

```python
import os
# Stops the script if /etc/passwd is not in the allowed paths
content = os.read_file("/etc/passwd")
```

The denial is a `PermissionError` that no `try`/`except` or `with` block can catch, so the run stops (after any `finally` blocks) with:

```
Error: access denied: path '/etc/passwd' is outside allowed directories
```

**Common libraries (not an exhaustive inventory):**

- Standard libraries: `json`, `msgpack`, `math`, `random`, `re`, `time`, `base64`, `hashlib`, `hmac`, `urllib`
- `datetime` - Date and time operations
- `yaml`, `toml` - YAML and TOML parsing
- `html.parser` - HTML parsing
- `requests` - HTTP client
- `os` - Environment variables and file operations (path-restricted)
- `pathlib`, `glob` - File system access (path-restricted)
- `secrets` - Cryptographic random number generation
- `scriptling.runtime` - Runtime utilities including sandbox and background tasks
- `subprocess` - Process execution
- `scriptling.wait_for` - Process monitoring
- AI, agent, and MCP libraries
