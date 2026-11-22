---
description: Enable libraries, allow paths and hosts, and set resource limits, secrets and plugins for FrankenScriptling.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/frankenscriptling/configuration/
sources:
    - resource: https://scriptling.dev/docs/frankenscriptling/configuration/
status: stable
tags:
    - frankenscriptling
    - security
    - configuration
title: Configuration
type: Guide
---
# Configuration

FrankenScriptling is configured with environment variables and optional TOML
files that only the operator controls. PHP code cannot read or loosen the
policy: it can only lower the resource limits for one VM.

The settings are read once, when the first VM is created, and apply to the
whole FrankenPHP process. Set them on the container (`docker run -e`, Compose
`environment:`) or in your own image's `ENV`. They are not read per site from
the Caddyfile's `env` directive.

With nothing set, scripts get the computation-only libraries and no access to
files, the network or other processes.

## Libraries

Libraries fall into these groups:

| Group | Registered when | Libraries |
| --- | --- | --- |
| Always on | Always | The standard library, `toml`, `yaml`, `html.parser`, `logging`, `sys`, `secrets`, `shlex`, `scriptling.csv`, `scriptling.xml`, `scriptling.markdown`, `scriptling.similarity`, `scriptling.template.html`, `scriptling.template.text`, `scriptling.ai.memory` |
| Filesystem | Enabled, and `SCRIPTLING_ALLOWED_PATHS` grants directories | `pathlib`, `os`, `os.path`, `fs`, `glob`, `shutil`, `tempfile`, `tarfile`, `zipfile`, `scriptling.find`, `scriptling.grep`, `scriptling.sed` |
| Network | Enabled, and a network policy is set | `requests`, `scriptling.net.websocket`, `scriptling.net.resolve`, `scriptling.ai`, `scriptling.mcp` (with `scriptling.toon`), `scriptling.mercure` |
| Processes | Enabled | `subprocess` |
| Secrets | Enabled, and a secret provider is set | `scriptling.secret` |
| Plugins | Enabled, and plugins are preloaded | `scriptling.plugin` |

`scriptling.ai.agent` and `scriptling.ai.agent.interact` are in the image but
import `scriptling.ai`, so they work once `scriptling.ai` is enabled and the
model's host is allowed. Some
libraries are not in the image at all, whatever the configuration: container
control, the database and key-value stores, messaging, `scriptling.wait_for`
and the gossip, multicast and unicast networking libraries.

| Variable | Meaning |
| --- | --- |
| `SCRIPTLING_ENABLED_LIBRARIES` | Comma-separated libraries to enable from the gated groups. Unset enables none. |
| `SCRIPTLING_ALLOWED_PATHS` | Colon-separated absolute directories the filesystem libraries may use. Unset or `-` allows none, so the filesystem libraries stay closed even when enabled. |
| `SCRIPTLING_NETWORK_POLICY_FILE` | Comma-separated paths to network policy files (below). Unset keeps the network libraries closed even when enabled. Later files override earlier ones. |

```bash
docker run --rm -p 8080:80 \
  -e SCRIPTLING_ENABLED_LIBRARIES=pathlib,requests \
  -e SCRIPTLING_ALLOWED_PATHS=/app/data \
  -e SCRIPTLING_NETWORK_POLICY_FILE=/etc/scriptling/network.toml \
  -v "$PWD/network.toml:/etc/scriptling/network.toml:ro" \
  -v "$PWD/data:/app/data" \
  -v "$PWD/public:/app/public" \
  paularlott/frankenscriptling:php8.6
```

Scripts can now read and write under `/app/data` and call the hosts the policy
allows. `pathlib.Path("/etc/passwd").read_text()` fails with a policy error,
and `import subprocess` fails because it was not enabled.

A stdio MCP server (`mcp.Client("/path/to/server")`) starts a process, so
`scriptling.mcp` refuses it unless `subprocess` is enabled too.

## Network policy file

The network policy is a TOML file in the same format as the CLI's
[network policy](https://scriptling.dev/okf/scriptling-docs/cli/network-policy.md):

```toml
https_only = true
allow_hosts = ["api.example.com", ".internal.example.com"]
deny_hosts = []
allow_cidrs = []
deny_cidrs = []
allow_ip_literals = false
allow_loopback = false
allow_private_ips = false
dns_servers = ["1.1.1.1"]
client_timeout = "30s"
```

Every key is optional. Loopback, link-local (cloud metadata endpoints
included), private and multicast addresses are refused unless allowed, and a
URL with an IP address is refused unless `allow_ip_literals` is set or the
address is in `allow_cidrs`. There is no setting that turns the checks off.

A policy cannot name a port, so allowing loopback or a private range opens
everything listening there, including Caddy's admin API on `localhost:2019`.
Allow the narrowest `allow_cidrs` you can instead.

## One policy file

`SCRIPTLING_POLICY_FILE` takes one or more comma-separated TOML files that
hold the libraries, paths, network policy and limits together:

```toml
[libraries]
enabled = ["pathlib", "requests"]

[filesystem]
allowed_paths = ["/app/data"]

[network]
https_only = true
allow_hosts = ["api.example.com"]

[limits]
memory_bytes = 67108864
max_value_bytes = 1048576
```

When the separate variables are set too, they are the base and the file
overrides what it sets.

## Resource limits

| Variable | `[limits]` key | Meaning |
| --- | --- | --- |
| `SCRIPTLING_MEMORY_LIMIT` | `memory_bytes` | Estimated memory one VM may hold. Going over cancels the running call with an error containing `memory limit exceeded`; the VM stays usable. |
| `SCRIPTLING_MAX_VALUE_BYTES` | `max_value_bytes` | Largest string, bytes value or container one operation may create. Going over raises `MemoryError` in the script. |

Both are in bytes; unset or `0` means no limit. The limits apply to each VM,
not to the process. PHP can lower them for one VM with `setMemoryLimit()` and
`setMaxValueBytes()` but cannot raise or remove them. Limit running time per
call with `evalWithTimeout()`.

A malformed setting (an unreadable policy file, a limit that is not a
number) fails closed: VMs report the error instead of running with a looser
policy.

## Secrets

`scriptling.secret` reads secrets from Vault or 1Password, configured from
the environment so credentials stay out of policy files. It also needs
`scriptling.secret` in `SCRIPTLING_ENABLED_LIBRARIES`.

| Variable | Meaning |
| --- | --- |
| `SCRIPTLING_SECRET_PROVIDER` | `vault` or `onepassword` |
| `SCRIPTLING_SECRET_ALIAS` | The name scripts pass to `secret.get(alias, path, field)`; defaults to the provider's name |
| `SCRIPTLING_SECRET_ADDRESS` | The provider's address (Vault's URL) |
| `SCRIPTLING_SECRET_TOKEN` | Vault token or 1Password service account token |
| `SCRIPTLING_SECRET_APP_ROLE_ID`, `SCRIPTLING_SECRET_APP_ROLE_SECRET` | Vault AppRole login, instead of a token |
| `SCRIPTLING_SECRET_NAMESPACE` | Vault Enterprise namespace |
| `SCRIPTLING_SECRET_KV_VERSION` | Vault KV engine version, `1` or `2` |
| `SCRIPTLING_SECRET_CACHE_TTL` | How long a value is cached, such as `5m` (the default) |
| `SCRIPTLING_SECRET_DEFAULT_FIELD` | The field used when a script names none |
| `SCRIPTLING_SECRET_INSECURE_SKIP_TLS` | `true` skips TLS verification; for testing only |

For several providers, point `SCRIPTLING_SECRET_PROVIDERS_FILE` at TOML files
with one `[[providers]]` table each, using the same settings in snake_case
(`provider`, `alias`, `address`, `token`, ...). See
[`scriptling.secret`](https://scriptling.dev/okf/scriptling-libraries/utilities/secret.md) for the script side.

## Plugins

`scriptling.plugin` gives scripts the [plugins](https://scriptling.dev/okf/scriptling-docs/plugins.md) the operator
loads at startup. Scripts cannot load their own unless HTTP loading is turned
on, and they can never start a plugin executable.

| Variable | Meaning |
| --- | --- |
| `SCRIPTLING_PLUGIN` | Comma-separated plugin executables or `http(s)://` URLs to load at startup |
| `SCRIPTLING_PLUGIN_DIR` | Comma-separated directories of plugin executables to load at startup |
| `SCRIPTLING_PLUGIN_HTTP_ENABLED` | `true` lets scripts `load()` HTTP(S) plugins within the network policy, and `unload()` only those |

A plugin that fails to load fails the policy closed rather than leaving
scripts with fewer plugins than intended. `scriptling.plugin` also has to be
in `SCRIPTLING_ENABLED_LIBRARIES`.

```bash
SCRIPTLING_ENABLED_LIBRARIES=scriptling.plugin
SCRIPTLING_PLUGIN=https://billing.internal/rpc
SCRIPTLING_PLUGIN_DIR=/etc/frankenscriptling/plugins
```

## Compose example

```yaml
services:
  app:
    image: paularlott/frankenscriptling:php8.6
    ports:
      - "8080:80"
    environment:
      SCRIPTLING_POLICY_FILE: /etc/scriptling/policy.toml
      SCRIPTLING_SECRET_PROVIDER: vault
      SCRIPTLING_SECRET_ADDRESS: https://vault.internal:8200
      SCRIPTLING_SECRET_TOKEN: ${VAULT_TOKEN}
    volumes:
      - ./public:/app/public
      - ./policy.toml:/etc/scriptling/policy.toml:ro
```
