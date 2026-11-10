---
description: Install and remove system packages with apt, dnf, yum, apk or Homebrew, skipping those already in place.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/provisioning/provision-package/
sources:
    - resource: https://scriptling.dev/reference/libraries/provisioning/provision-package/
status: stable
tags:
    - libraries
    - provisioning
title: scriptling.provision.package
type: API Reference
---
# scriptling.provision.package

## Overview

`scriptling.provision.package` installs and removes system packages. It asks which of the packages are installed first and runs the package manager only when something needs doing, so a script that has already run once does not touch apt at all.

It finds the package manager itself: apt, dnf, yum, apk or Homebrew, in that order.

apt, dnf, yum and apk need root, which the library uses on its own through `sudo`; you don't pass `become=True`. The scriptling CLI refuses it with `--deny-become` (see [Running as Root](https://scriptling.dev/okf/scriptling-libraries/provisioning.md#running-as-root)). Homebrew always runs as the user.

The library is registered only where the `subprocess` library is.

## Available Functions

| Function | Description |
|----------|-------------|
| `ensure(packages, update=False, manager=None)` | Install the packages not yet installed |
| `absent(packages, manager=None)` | Remove the packages that are installed |
| `installed(packages, manager=None)` | Whether every package is installed |
| `manager()` | The package manager in use |

## Constants

| Constant | Description |
|----------|-------------|
| `package.CREATED` | Something was installed (`"created"`) |
| `package.UNCHANGED` | Everything was already installed (`"unchanged"`) |
| `package.REMOVED` | Something was removed (`"removed"`) |
| `package.ABSENT` | Nothing was installed to remove (`"absent"`) |

## Functions

### `ensure(packages, update=False, manager=None)`

Installs those of `packages` that are not installed.

A new machine (a fresh container, say) often has no package lists, and an old one may have stale lists. Either way the install fails, so `ensure()` then refreshes the lists and tries once more. apt also waits up to five minutes for another apt to finish (unattended-upgrades on a new machine, for example) rather than failing at its lock.

**Parameters:**
- `packages` (`str` or `list`): A package name, or a list of them.
- `update` (`bool`, optional): Refresh the package lists before installing. Default: `False`.
- `manager` (`str`, optional): `"apt"`, `"dnf"`, `"yum"`, `"apk"` or `"brew"`. Default: the first of these found.

**Returns:** `str`: `package.CREATED` or `package.UNCHANGED`.

**Raises:** `Error` when the package manager fails, with the command and the last lines it wrote. `PermissionError`, which the script cannot catch, where root is needed and running as root is not allowed.

```python
import scriptling.provision.package as package

if package.ensure(["nginx", "curl"]) == package.CREATED:
    print("installed")
```

### `absent(packages, manager=None)`

Removes those of `packages` that are installed.

**Returns:** `str`: `package.REMOVED` or `package.ABSENT`.

```python
import scriptling.provision.package as package

package.absent("telnet")
```

### `installed(packages, manager=None)`

**Returns:** `bool`: `True` when every one of `packages` is installed. Asking needs no root.

### `manager()`

**Returns:** `str` or `None`: `"apt"`, `"dnf"`, `"yum"`, `"apk"` or `"brew"`; `None` when there is none.

## See Also

- [Provisioning Libraries](https://scriptling.dev/okf/scriptling-libraries/provisioning.md) - Running as root
- [scriptling.provision.command](https://scriptling.dev/okf/scriptling-libraries/provisioning/provision-command.md) - Run commands
