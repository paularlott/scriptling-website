---
description: Resolve secrets through host-configured provider aliases without exposing provider credentials to scripts.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/utilities/secret/
sources:
    - resource: https://scriptling.dev/reference/libraries/utilities/secret/
status: stable
tags:
    - libraries
    - utilities
    - security
title: scriptling.secret
type: API Reference
---
# scriptling.secret

The `scriptling.secret` library resolves secrets through host-configured provider aliases. The host application owns the provider configuration (Vault, 1Password, etc.): scripts only ever see a provider `alias`, a provider-specific `path`, and an optional `field`, which keeps provider URLs, access tokens, namespaces, and similar private data out of Scriptling code.

## Available Functions

| Function | Description |
|----------|-------------|
| `get(alias, path, field="")` | Resolve a secret using a host-configured provider alias |
| `list(alias, path)` | List keys/items at a path |

## Functions

### `get(alias, path, field="")`

Resolves a secret using the provider alias registered by the host.

**Parameters:**
- `alias` (`str`): Registered provider alias, such as `"prod_vault"` or `"op"`.
- `path` (`str`): Provider-specific secret path or identifier.
- `field` (`str`, optional): Field to extract from a multi-value secret. Default: `""`.

**Returns:** `str`: the resolved secret value.

**Raises:** `Error`: when the alias is unknown or the underlying provider returns an error.

```python
import scriptling.secret as secret

db_password = secret.get("prod_vault", "secret/data/app", "password")
api_key = secret.get("op", "Engineering/api-key", "credential")
```

### `list(alias, path)`

Lists keys at a path using the provider alias registered by the host. For Vault, returns the key names at a secret path. For 1Password, returns the item titles in a vault, or the field names of an item for `vault/item`.

**Parameters:**
- `alias` (`str`): Registered provider alias, such as `"prod_vault"` or `"op"`.
- `path` (`str`): Provider-specific path. For Vault, a secret engine path (e.g. `"secret/data/app"`). For 1Password, a vault name or ID, or `vault/item` to list an item's fields.

**Returns:** `list` of `str`: key or item name strings.

**Raises:** `Error`: when the alias is unknown or the underlying provider returns an error.

```python
import scriptling.secret as secret

keys = secret.list("prod_vault", "secret/data/app")
for key in keys:
    print(key, "=", secret.get("prod_vault", "secret/data/app/" + key))

items = secret.list("op", "Engineering")
for item in items:
    print(item)
```

## CLI Usage

The Scriptling CLI can load provider aliases from a TOML config file:

```toml
[[secrets.provider]]
provider = "vault"
alias = "prod_vault"
address = "https://vault.internal:8200"
token = "hvs.example"
cache_ttl = "5m"

[[secrets.provider]]
provider = "onepassword"
alias = "op"
address = "http://op-connect:8080"
token = "example-token"
```

### 1Password service accounts

With the [scriptling-onepassword](https://github.com/paularlott/scriptling-onepassword) extension, the `onepassword` provider can use a [1Password service account](https://developer.1password.com/docs/service-accounts/) instead of 1Password Connect. Give `service_account_token` in place of `address` and `token`; no Connect server is needed:

```toml
[[secrets.provider]]
provider = "onepassword"
alias = "op"
service_account_token = "ops_..."
```

Paths and fields work the same way in both modes: `vault/item` by name or ID, the field defaulting to `password`, falling back to `credential` and the item's notes. A provider uses one mode or the other; giving both is an error.

Service accounts use the 1Password Go SDK, which adds about 14 MB, so they live in the separate extension. Install the `scriptling-onepassword` or `scriptling-slim-onepassword` build (see [1Password Builds](https://scriptling.dev/okf/scriptling-docs/quick-start/cli.md#1password-builds)), or make a [custom build](#service-accounts-in-embedded-applications-and-custom-builds). In the standard `scriptling` and `scriptling-slim` builds, a `service_account_token` config fails with an error naming the extension.

A service account can only read the vaults it was given when it was created, and can't be given your built-in Personal, Private or Employee vault, or the default Shared vault. 1Password also limits how many requests a service account makes; `cache_ttl` keeps repeated reads from counting against it.

#### Service account or Connect?

A service account needs nothing but its token, and replaces passwords kept in environment variables with one read-only token you can revoke. Each new `scriptling` process starts cold, though: its first secret read loads 1Password's engine and signs in (about a second), and each secret is fetched from 1Password once per process, counting against the service account's limits. `cache_ttl` only helps within a process.

1Password Connect keeps a synced copy of your vaults on your own server, so every run reads from it directly. Use a service account for interactive use, occasional scripts and CI jobs. Use Connect when scriptling starts many times a minute, or reads many secrets per run, where the start-up cost or the rate limits would get in the way.

Run a script with the config file:

```bash
scriptling --secret-config ./secrets.toml script.py
```

The built-in CLI loader currently supports `vault` and `onepassword` (1Password Connect, or a service account in the `-onepassword` builds). Embedded applications can construct and register providers directly in Go.

### Service accounts in embedded applications and custom builds

An embedded application enables service accounts by importing the extension for its side effect:

```go
import _ "github.com/paularlott/scriptling-onepassword"
```

Every `secretprovider.Config` with `ServiceAccountToken` then builds a service account provider. Set `onepassword.IntegrationName` and `IntegrationVersion` before first use to identify your application to 1Password.

A CLI with service accounts is a module whose `main.go` calls `scriptlingcmd.Main()` with the extension imported:

```go
package main

import (
	"github.com/paularlott/scriptling/scriptling-cli/scriptlingcmd"
	_ "github.com/paularlott/scriptling-onepassword"
)

func main() { scriptlingcmd.Main() }
```

Build it with `go mod tidy && go build`. To include the database drivers too, build with the same tags as the released CLI, e.g. `-tags plugin_sqlite,plugin_sql,plugin_valkey,plugin_badgerdb`.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.secret` grants access to credentials, but the risk is mitigated by design: scripts only ever see a provider alias and a logical path/field name, never the actual secret value's source, provider URL, or access token. The host application owns the real `secretprovider.Registry` passed to `RegisterSecretLibrary(p, registry)`, and resolution fails closed when an alias is missing or the provider errors. See [Secret Provider Security](https://scriptling.dev/okf/scriptling-docs/security.md#secret-provider-security) for the full model.

## See Also

- [CLI Guide](https://scriptling.dev/okf/scriptling-docs/cli.md) - Command-line flags and runtime behavior
- [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) - Registering extended libraries when embedding in Go
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security guidance for host-provided libraries
