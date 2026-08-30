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

Lists keys at a path using the provider alias registered by the host. For Vault, returns the key names at a secret path. For 1Password, returns item titles in a vault.

**Parameters:**
- `alias` (`str`): Registered provider alias, such as `"prod_vault"` or `"op"`.
- `path` (`str`): Provider-specific path. For Vault, a secret engine path (e.g. `"secret/data/app"`). For 1Password, a vault name or UUID.

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

Run a script with the config file:

```bash
scriptling --secret-config ./secrets.toml script.py
```

The built-in CLI loader currently supports `vault` and `onepassword`. Embedded applications can construct and register providers directly in Go.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.secret` grants access to credentials, but the risk is mitigated by design: scripts only ever see a provider alias and a logical path/field name, never the actual secret value's source, provider URL, or access token. The host application owns the real `secretprovider.Registry` passed to `RegisterSecretLibrary(p, registry)`, and resolution fails closed when an alias is missing or the provider errors. See [Secret Provider Security](https://scriptling.dev/okf/scriptling-docs/security.md#secret-provider-security) for the full model.

## See Also

- [CLI Guide](https://scriptling.dev/okf/scriptling-docs/./cli.md) - Command-line flags and runtime behavior
- [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) - Registering extended libraries when embedding in Go
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md) - Security guidance for host-provided libraries
