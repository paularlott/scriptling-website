---
description: Restricting script outbound network access with a policy file.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/cli/network-policy/
sources:
    - resource: https://scriptling.dev/docs/cli/network-policy/
status: stable
tags:
    - cli
    - security
title: Network Policy
type: Guide
---
# Network Policy

`--network-policy` restricts where the `requests`, `scriptling.wait_for`, and `scriptling.net.websocket` libraries may connect — the tool for letting scripts reach the internet without letting them reach your private network or cloud metadata endpoints. Enforcement happens at connect time: hostnames are resolved through the configured DNS servers, every resolved address is checked, and the connection is made to the validated address — so DNS rebinding, redirects, and IP-notation tricks don't get through.

```bash
scriptling --network-policy=policy.toml --no-subprocess script.py
```

A missing or invalid policy file aborts startup rather than running scripts unrestricted. Combine with `--no-subprocess` so scripts can't bypass the policy by shelling out to `curl`.

With a policy active, these address categories are blocked by default:

- Loopback (`127.0.0.0/8`, `::1`)
- Link-local (`169.254.0.0/16` including cloud metadata endpoints, `fe80::/10`)
- Private (`10/8`, `172.16/12`, `192.168/16`, `fc00::/7`)
- Unspecified (`0.0.0.0`, `::`) and multicast addresses
- URLs that name an IP directly (e.g. `http://10.0.0.1/`)

## Policy File Reference

A TOML file; every key is optional.

```toml
# Require https:// and wss:// URLs only
https_only = false

# Permit URLs that name an IP directly (http://1.2.3.4/). Blocked by
# default; granted addresses still face the address rules above.
allow_ip_literals = false

# Permit loopback addresses (e.g. for local testing)
allow_loopback = false

# Permit private network addresses (10/8, 172.16/12, 192.168/16, fc00::/7)
allow_private_ips = false

# Host allowlist: when set, ONLY these hosts may be contacted. Listed
# hosts are trusted — they may resolve to internal addresses. An exact
# name matches itself; a leading dot matches the domain and all subdomains.
allow_hosts = ["api.example.com", ".internal.corp"]

# Host denylist: always wins, even over the allowlist. Same syntax.
deny_hosts = ["tracker.example"]

# Address range exceptions. allow_cidrs overrides the built-in address
# blocks (how you grant one slice of your LAN); deny_cidrs wins over
# everything.
allow_cidrs = ["10.1.0.0/16"]
deny_cidrs  = ["10.66.0.0/16"]

# Resolve hostnames through these servers instead of the host's resolver
# (plain DNS, port 53). One resolver then serves every script network path,
# including scriptling.net.resolve, so lookups and connections always agree.
dns_servers = ["1.1.1.1", "8.8.8.8:53"]
```

Common recipes:

```toml
# Internet-only: no internal access at all (the default policy — an empty file)
```

```toml
# API allowlist: scripts may call one API and nothing else
allow_hosts = ["api.example.com"]
```

```toml
# One slice of the LAN granted, https only
https_only = true
allow_cidrs = ["10.1.0.0/16"]
```

Note that in the CLI, custom DNS always comes with the policy's address checks — a policy file cannot turn them off. Embedding hosts that want nameservers without any blocking can construct a resolver-only configuration in Go (see `AllowAll` in the [library registration guide](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#network-policy)).

Go hosts configure the same policy in code — see the [library registration guide](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) for the `netsecurity.Config` reference, and the [security guide](https://scriptling.dev/okf/scriptling-docs/security.md) for the broader sandboxing model.
