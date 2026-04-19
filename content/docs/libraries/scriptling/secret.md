---
title: scriptling.secret
linkTitle: secret
weight: 1
---

Resolve secrets through host-configured provider aliases without exposing provider credentials to scripts.

## Overview

The `scriptling.secret` library gives scripts a single provider-agnostic API:

```python
import scriptling.secret as secret

db_password = secret.get("prod_vault", "secret/data/app", "password")
api_key = secret.get("op", "Engineering/api-key", "credential")
```

The host application owns the provider configuration. Scripts only see:

- A provider `alias`
- A provider-specific `path`
- An optional `field`

This keeps provider URLs, access tokens, namespaces, and similar private data out of Scriptling code.

## Library Function

| Function | Description |
| -------- | ----------- |
| `scriptling.secret.get(alias, path, field="")` | Resolve a secret using a host-configured provider alias |
| `scriptling.secret.list(alias, path)` | List keys/items at a path |

## Functions

### scriptling.secret.get(alias, path, field="")

Resolve a secret using the provider alias registered by the host.

**Parameters:**

- `alias` (string): Registered provider alias such as `prod_vault` or `op`.
- `path` (string): Provider-specific secret path or identifier.
- `field` (string, optional): Field to extract from a multi-value secret. Default: `""`.

**Returns:** `string` - The resolved secret value.

**Example:**

```python
import scriptling.secret as secret

db_password = secret.get("prod_vault", "secret/data/app", "password")
api_key = secret.get("op", "Engineering/api-key", "credential")
```

### scriptling.secret.list(alias, path)

List keys at a path using the provider alias registered by the host. For Vault, returns the key names at a secret path. For 1Password, returns item titles in a vault.

**Parameters:**

- `alias` (string): Registered provider alias such as `prod_vault` or `op`.
- `path` (string): Provider-specific path. For Vault, a secret engine path (e.g., `secret/data/app`). For 1Password, a vault name or UUID.

**Returns:** `list[string]` - List of key or item name strings.

**Example:**

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

Run a script with the config file:

```bash
scriptling --secret-config ./secrets.toml script.py
```

## Go Integration

Hosts can register providers programmatically instead of using a config file.

```go
package main

import (
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/extlibs"
    "github.com/paularlott/scriptling/extlibs/secretprovider"
)

func main() {
    p := scriptling.New()

    registry := secretprovider.NewRegistry()
    provider, err := secretprovider.NewProvider(secretprovider.Config{
        Provider: "vault",
        Alias:    "prod_vault",
        Address:  "https://vault.internal:8200",
        Token:    "hvs.example",
    })
    if err != nil {
        panic(err)
    }
    if err := registry.Register(provider, "prod_vault", 0); err != nil {
        panic(err)
    }

    extlibs.RegisterSecretLibrary(p, registry)
}
```

## Supported CLI Providers

The built-in CLI loader currently supports:

- `vault`
- `onepassword`

Embedded applications can construct and register providers directly in Go.

## Security Considerations

- Provider credentials stay in the host application or CLI config file.
- Scripts only see aliases and logical secret paths.
- Secret resolution fails closed when an alias is missing or the provider returns an error.
- Cache TTL is configured by the host, not by the script.

## See Also

- [CLI Reference](../../cli/) - Command-line flags and runtime behavior
- [Security Guide](../../security/) - Security guidance for host-provided libraries
- [Scriptling Libraries](../) - Other Scriptling-specific libraries
