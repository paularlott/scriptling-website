---
title: sys
description: System-specific parameters and functions, similar to Python's sys module.
tags: [libraries, runtime]
weight: 1
aliases:
  - /reference/libraries/extlib/sys/
  - /reference/libraries/sys/
---

The `sys` library provides access to system-specific parameters and functions: platform identification, command-line arguments, stdin, and interpreter exit: similar to Python's `sys` module.

## Available Functions

| Function | Description |
|----------|-------------|
| `exit(code=0)` | Raise a `SystemExit` exception to exit the interpreter. |
| `input(prompt=None)` | Read a line from stdin, stripping the trailing newline. |

## Constants

| Constant | Description |
|----------|-------------|
| `platform` | Operating system platform string (`"darwin"`, `"linux"`, `"win32"`). |
| `version` | Scriptling interpreter version string. |
| `maxsize` | Maximum signed integer value (`9223372036854775807`). |
| `path_sep` | Path separator for the OS (`"/"` on Unix, `"\"` on Windows). |
| `argv` | List of command-line arguments passed to the script. |
| `stdin` | Standard input stream object, only present when stdin is configured. |

## Functions

### `exit(code=0)`

Raise a `SystemExit` exception to exit the interpreter. Unlike most exceptions, `SystemExit` **cannot be caught** by `try`/`except` blocks: it bypasses all `except` clauses and propagates to the caller (CLI, REPL, etc.). `finally` blocks still execute before it propagates. To handle errors gracefully instead of exiting, use `raise()` with a message.

**Parameters:**
- `code` (`int`/`str`, optional): Exit status. Default: `0`. An integer produces the message `"SystemExit: <code>"`; a string is used as the message directly (and implies exit code `1`).

**Returns:** `None`: does not return; propagates a `SystemExit` exception to the caller.

```python
import sys

# Exit successfully (raises SystemExit: 0)
sys.exit()

# Exit with error code (raises SystemExit: 1)
sys.exit(1)

# Exit with a custom message
sys.exit("Fatal error occurred")

# except does NOT catch sys.exit(), but finally still runs:
try:
    sys.exit(42)
except Exception as e:
    print("This will never print - except is bypassed!")
finally:
    print("This WILL print - finally executes")
```

### `input(prompt=None)`

Read a line from stdin, stripping the trailing newline. Only available when the environment is configured with a stdin reader (piped input via the CLI, or an `io.Reader` passed to `RegisterSysLibrary` in Go). The optional `prompt` argument is accepted but not printed: there is no interactive terminal in remote/server environments.

**Parameters:**
- `prompt` (`str`, optional): Ignored placeholder for Python compatibility. Default: `None`.

**Returns:** `str`: the line read from stdin, without its trailing newline. Returns `""` at EOF.

```python
line = input()
print("You typed:", line)
```

### `stdin`

A file-like object connected to standard input. Only available when stdin is configured: either when running via the CLI with piped input, or when an input reader is supplied during registration of the `sys` library via the Go API.

| Method | Description |
|--------|-------------|
| `read()` | Read all remaining data from stdin. |
| `readline()` | Read one line including the newline character; returns `""` at EOF. |

`sys.stdin` is also iterable: each iteration yields one line including its trailing newline.

```python
import sys

# Read all at once
data = sys.stdin.read()

# Read line by line
line = sys.stdin.readline()

# Iterate over lines
for line in sys.stdin:
    print("Got:", line.rstrip())
```

### `platform`

A string identifying the operating system platform.

```python
import sys
print(sys.platform)  # "darwin", "linux", or "win32"
```

### `version`

A string containing the version of the Scriptling interpreter.

```python
import sys
print(sys.version)  # "Scriptling 1.0"
```

### `maxsize`

The maximum value of a signed integer (`int64`).

```python
import sys
print(sys.maxsize)  # 9223372036854775807
```

### `path_sep`

The path separator used by the operating system.

```python
import sys
print(sys.path_sep)  # "/" on Unix, "\" on Windows
```

### `argv`

A list of command-line arguments passed to the script.

```python
import sys

if len(sys.argv) < 2:
    print("Usage: script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
print(f"Processing {input_file}")
```

In server modes (`--server`, `--json-rpc`, `--mcp-tools`, `--package`), `sys.argv` is available in every evaluator — the setup script, MCP tool handlers, HTTP route handlers, and JSON-RPC method handlers. Positional arguments after `--` on the CLI are included, so app bundles can accept their own flags:

```sh
# --bundles is not a scriptling flag; it passes through to sys.argv
scriptling --package ./myapp -- --bundles /data
```

```python
# Inside a tool or handler — each call resolves sys.argv fresh
import sys
bundles = "/data"
for i in range(len(sys.argv) - 1):
    if sys.argv[i] == "--bundles":
        bundles = sys.argv[i + 1]
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`sys` exposes whatever `argv` and `stdin` the embedder passes to `RegisterSysLibrary(p, argv, stdin)`: if those contain secrets, a script can read them. Never register this library (or pass sensitive argv/env) for untrusted code. See the [Security Guide](/docs/security/#environment-variables).

## Python Compatibility

This library implements a subset of Python's `sys` module:

| Feature | Supported |
|---------|-----------|
| `argv` | Yes |
| `exit()` | Yes |
| `platform` | Yes |
| `version` | Yes (simplified) |
| `maxsize` | Yes |
| `path` | No |
| `modules` | No |
| `stdin` / `stdout` / `stderr` | `stdin` yes (when available), `stdout`/`stderr` no |
| `executable` | No |
| `version_info` | No |

## See Also

- [subprocess](../subprocess/): Spawn external commands
- [os](../../filesystem/os/): Environment variables and filesystem access
