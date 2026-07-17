---
title: subprocess
description: Spawn and manage subprocesses, similar to Python's subprocess module.
tags: [libraries, subprocess]
weight: 1
aliases:
  - /reference/libraries/extlib/subprocess/
  - /reference/libraries/subprocess/
---

The `subprocess` library provides functions for spawning and managing external commands, similar to Python's `subprocess` module.

## Available Functions

| Function | Description |
|----------|-------------|
| `run(args, **options)` | Run a command and return a `CompletedProcess`. |

## Functions

### `run(args, **options)`

Run a command and return a `CompletedProcess` instance.

**Parameters:**
- `args` (`str`/`list`): Command to run. A string is split on spaces (unless `shell` is `True`, in which case it is passed to the shell as-is); a list is used as the literal argument vector.
- The following options are passed as keyword arguments:
  - `capture_output` (`bool`): Capture stdout and stderr. Default: `False`.
  - `shell` (`bool`): Run the command through the shell. Default: `False`.
  - `cwd` (`str`): Working directory for the command.
  - `timeout` (`int`/`float`): Timeout in seconds.
  - `check` (`bool`): Raise an exception if `returncode` is non-zero. Default: `False`.
  - `text` (`bool`): Return stdout/stderr as strings. Default: `False`.
  - `encoding` (`str`): Encoding for stdout/stderr. Default: `"utf-8"`.
  - `input` (`str`): String to pipe to stdin.
  - `env` (`dict`): Environment variables for the command.

**Returns:** `CompletedProcess`: see [CompletedProcess Class](#completedprocess-class).

**Raises:** `Error`: if the command cannot be executed, or if `check` is `True` and the command exits non-zero.

```python
import subprocess

# Simple command execution
result = subprocess.run("echo hello")
print(result.returncode)  # 0

# Capture output (options are keyword arguments)
result = subprocess.run("echo hello world", capture_output=True)
print(result.stdout.strip())  # "hello world"

# Run with arguments as a list
result = subprocess.run(["echo", "test"])

# Use the shell
result = subprocess.run("echo 'hello' && echo 'world'", shell=True)

# Check for errors
try:
    result = subprocess.run("false", check=True)
except Exception:
    print("Command failed")
```

## CompletedProcess Class

`subprocess.run()` returns a `CompletedProcess` instance with the following attributes:

- `args` (`list`): Command arguments.
- `returncode` (`int`): Exit code of the process.
- `stdout` (`str`): Captured standard output (empty string if not captured).
- `stderr` (`str`): Captured standard error (empty string if not captured).

### `CompletedProcess.check_returncode()`

Check that the process returned successfully.

**Returns:** `CompletedProcess`: the instance itself, if `returncode` is `0`.

**Raises:** `Error`: if `returncode` is non-zero.

```python
import subprocess

result = subprocess.run("true")
result.check_returncode()  # OK

try:
    result = subprocess.run("false")
    result.check_returncode()  # Raises
except Exception:
    print("Process failed")
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`subprocess` allows arbitrary OS command execution on the host. This is a **critical risk**: there is no built-in mitigation, sandboxing, or allowlisting. Never register this library when running untrusted scripts, and be careful with user-provided command strings or the `shell` option to avoid command injection. See [Library Registration](/docs/go-integration/library-registration/#security-considerations) and the [Security Guide](/docs/security/).

## Platform Compatibility

- Works on all platforms supported by Go's `os/exec` package.
- Command syntax may vary between operating systems.
- Use the `sys` library's `platform` constant to detect the current platform if your script needs to branch on OS.

## See Also

- [sys](../sys/): Detect the current platform and access environment/argv
- [requests](../requests/): Make HTTP requests without spawning a process
