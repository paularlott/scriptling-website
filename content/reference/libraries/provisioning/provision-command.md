---
title: scriptling.provision.command
linkTitle: provision.command
description: Run commands while provisioning a machine, as the script's user or as root.
tags: [libraries, provisioning, process]
weight: 7
---

## Overview

`scriptling.provision.command` runs a command, waits for it and captures its output. It differs from `subprocess` in two ways: it can run the command as root (`become=True`), and it raises an error when the command fails unless you pass `check=False`.

It is registered only where the `subprocess` library is: `--disable-lib subprocess` (or `--no-subprocess`) removes it too.

## Available Functions

| Function | Description |
|----------|-------------|
| `run(cmd, become=False, cwd=None, env=None, input=None, timeout=None, check=True)` | Run a command |
| `is_root()` | Whether the script runs as root |
| `require_root()` | Stop the script unless it runs as root |

## Functions

### `run(cmd, become=False, cwd=None, env=None, input=None, timeout=None, check=True)`

Runs `cmd` and waits for it. A list is a program and its arguments, run as they are. A string is a command line for `/bin/sh`, so it may use pipes, `&&` and the like.

**Parameters:**
- `cmd` (`list` or `str`): The command.
- `become` (`bool`, optional): Run as root. See [Running as Root](../#running-as-root). Default: `False`.
- `cwd` (`str`, optional): Working directory (supports `~` expansion). Default: the current one.
- `env` (`dict`, optional): Environment variables added to the inherited environment.
- `input` (`str`, optional): Text for the command's standard input. Default: none.
- `timeout` (`float`, optional): Seconds to allow. The command is stopped after that and an error raised.
- `check` (`bool`, optional): Raise an error when the command exits with a non-zero status. Default: `True`.

**Returns:** a `Result` with:

| Field | Description |
|-------|-------------|
| `returncode` | The exit status |
| `stdout` | What it wrote to standard output |
| `stderr` | What it wrote to standard error |
| `ok` | `True` when `returncode` is `0` |
| `args` | The command as given (a shell command line is one element) |

**Raises:** `Error` when the command cannot start, times out, or (with `check=True`) exits non-zero; the message ends with the last lines it wrote. `PermissionError`, which the script cannot catch, for `become=True` where running as root is not allowed.

```python
import scriptling.provision.command as command

command.run(["systemctl", "enable", "--now", "nginx"], become=True)

r = command.run("id -un")
print("running as", r.stdout.strip())

r = command.run(["grep", "-q", "docker", "/etc/group"], check=False)
if not r.ok:
    command.run(["groupadd", "docker"], become=True)
```

A failure says what failed and why:

```text
run: apt-get install -y no-such-package exited with status 100:
E: Unable to locate package no-such-package
```

### `is_root()`

**Returns:** `bool`: `True` when the script itself runs as root (with `sudo scriptling`, say).

### `require_root()`

Stops the script with an error unless it runs as root. Use it in scripts meant to run as a whole with `sudo`. A script that runs as a user and needs root for a few steps passes `become=True` to those steps instead.

```python
import scriptling.provision.command as command

command.require_root()
```

## See Also

- [Provisioning Libraries](../) - Running as root
- [subprocess](/reference/libraries/http-process/subprocess/) - Python's subprocess
