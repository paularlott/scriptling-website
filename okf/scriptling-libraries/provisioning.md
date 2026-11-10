---
description: Set up a machine from a script - files, downloads, commands and packages, as the user or as root.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/provisioning/
sources:
    - resource: https://scriptling.dev/reference/libraries/provisioning/
status: stable
tags:
    - libraries
    - provisioning
title: Provisioning Libraries
type: API Reference
---
# Provisioning Libraries

The provisioning libraries set up a machine: write config files, download tools, run commands and install packages. Each step checks first and changes only what needs changing, so a script can run again and again and only fix what has drifted.

## Libraries

| Library | Description |
|---------|-------------|
| [scriptling.provision.file](https://scriptling.dev/okf/scriptling-libraries/provisioning/provision-file.md) | Files and directories with the right content, mode and owner, plus managed blocks inside a larger file |
| [scriptling.provision.fetch](https://scriptling.dev/okf/scriptling-libraries/provisioning/provision-fetch.md) | Download files over HTTP/HTTPS, optionally unpacking zip archives |
| [scriptling.provision.command](https://scriptling.dev/okf/scriptling-libraries/provisioning/provision-command.md) | Run commands, as the user or as root |
| [scriptling.provision.package](https://scriptling.dev/okf/scriptling-libraries/provisioning/provision-package.md) | Install and remove packages with apt, dnf, yum, apk or Homebrew |

## Quick Start

```python
import scriptling.provision.file as file
import scriptling.provision.package as package
import scriptling.provision.command as command

package.ensure(["nginx", "curl"])

if file.ensure("/etc/nginx/conf.d/app.conf", NGINX_CONF, become=True) != file.UNCHANGED:
    command.run(["systemctl", "reload", "nginx"], become=True)

file.ensure("~/.config/app/app.toml", APP_CONF)   # in your own home, as you
```

```bash
scriptling setup.py
```

## Running as Root

A provisioning script usually runs as you and needs root for a few steps: installing packages, writing under `/etc`, restarting a service. Pass `become=True` to those steps; everything else runs as you.

- **Allowed where `subprocess` is:** `become=True` runs `sudo`, which a script could already run with `subprocess`, so the scriptling CLI allows it by default. `--deny-become` (or `SCRIPTLING_DENY_BECOME=1`, or `security.deny_become = true` in its config) refuses it, and so does disabling the subprocess library. A refused step fails with a `PermissionError` the script cannot catch.
- **The user must be able to sudo:** root comes from `sudo`, so it is only as available as sudo is to the user running the script.
- **sudo is asked once:** the first `become=True` step starts one helper through `sudo`, and every later root step in the script goes to it.
- **Passwordless sudo just works:** the helper starts with `sudo -n` first, so where sudo needs no password (a knot space, a cloud image, CI) nothing is asked. Where sudo wants a password, it asks once on the terminal. With no terminal, the step fails at once with an error saying so, rather than hanging.
- **Already root:** when scriptling itself runs as root (`sudo scriptling setup.py`), `become=True` steps simply run, even with `--deny-become`.
- **Packages need no `become`:** `package.ensure()` uses root by itself where the package manager needs it (apt, dnf, yum, apk) and never with Homebrew, which refuses root.
- **Files keep sensible owners:** a new file written with `become=True` belongs to root unless you pass `owner=`/`group=`. An existing file keeps its owner when its content is updated.
- **Downloads run as you:** with `fetch.file(..., become=True)` only the final write is done as root.
- **`--allowed-paths` still holds:** the root helper enforces the same allowed paths as the script.

## See Also

- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - What provisioning can change
- [Command-Line Options](https://scriptling.dev/okf/scriptling-docs/cli/command-line-options.md) - `--deny-become`
- [Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling-libraries.md) - Full library reference index
