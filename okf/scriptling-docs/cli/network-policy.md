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

`--network-policy` restricts where the `requests`, `scriptling.wait_for`, `scriptling.net.websocket`, `scriptling.net.unicast`, `scriptling.net.multicast`, `scriptling.net.gossip`, `scriptling.nomad`, `scriptling.ai`, `scriptling.mcp`, and `scriptling.provision.fetch` libraries, the Slack, Discord and Telegram libraries, and container endpoints a script supplies may connect — the tool for letting scripts reach the internet without letting them reach your private network or cloud metadata endpoints. Enforcement happens at connect time: hostnames are resolved through the configured DNS servers, every resolved address is checked, and the connection is made to the validated address — so DNS rebinding, redirects, and IP-notation tricks don't get through.

For `scriptling.ai`, the policy also covers `remote_servers` — the MCP servers an AI client can attach for tool use — so a script cannot reach an internal MCP endpoint by routing through `ai.Client(..., remote_servers=[...])` instead of `mcp.Client(...)` directly.

```bash
scriptling --network-policy=policy.toml --disable-lib subprocess script.py
```

A missing or invalid policy file aborts startup rather than running scripts unrestricted. Combine the policy with `--disable-lib subprocess` in any mode so code cannot bypass it by shelling out to `curl`; `scriptling.container` checks only endpoints a script passes as `socket=`; the configured `--docker-host` / `--podman-host` endpoints are trusted. The Slack, Discord and Telegram libraries send every request and gateway connection through the policy, their platforms' own hosts included, since a script supplies the bot token and could otherwise post data to a bot it controls; the bot token itself is only ever sent to the platform's hosts. Under a strict `allow_hosts`, list the hosts of the platforms you use: `api.telegram.org`; `slack.com` and its subdomains (for example `.slack.com`, which covers `wss-primary.slack.com` and `files.slack.com`); `discord.com` plus `gateway.discord.gg` (and `.discordapp.com` / `.discordapp.net` for media). `scriptling.net.gossip` checks every connection a cluster makes, to joined peers and to peers it learns from the cluster, and carries all traffic over TCP; grant a private cluster with `allow_cidrs`. With `allow_hosts` set, gossip peers are limited to the listed names, and a peer given by IP must be granted by `allow_cidrs` or `allow_ip_literals`. `scriptling.provision.fetch` downloads through the policy. A connection the policy denies raises a `network policy: …` error, including from `wait_for.http()` and `wait_for.port()`, which fail immediately rather than waiting out their timeout. A network policy constrains only the libraries wired to it; it is not a process-level network sandbox, and plugin processes are outside it.

With a policy active, these address categories are blocked by default:

- Loopback (`127.0.0.0/8`, `::1`)
- Link-local (`169.254.0.0/16` including cloud metadata endpoints, `fe80::/10`)
- Private (`10/8`, `172.16/12`, `192.168/16`, `fc00::/7`)
- Reserved: ranges that are neither private nor publicly routable — shared address space / CGNAT (`100.64/10`, home to some cloud metadata endpoints), `0/8`, `192.0.0/24`, documentation (`192.0.2/24`, `198.51.100/24`, `203.0.113/24`, `2001:db8::/32`, `3fff::/20`), benchmarking (`198.18/15`, `2001:2::/48`), `240/4` and broadcast, and the IPv6 forms that embed or translate IPv4 (IPv4-compatible `::/96`, NAT64 `64:ff9b::/96` and `64:ff9b:1::/48`, 6to4 `2002::/16`, Teredo `2001::/32`), plus discard `100::/64` and deprecated site-local `fec0::/10`
- Unspecified (`0.0.0.0`, `::`) and multicast addresses
- URLs that name an IP directly (e.g. `http://10.0.0.1/`)

## Policy File Reference

A TOML file; every key is optional.

```toml
# Require https:// and wss:// URLs only
https_only = false

# Permit URLs that name an IP directly (http://1.2.3.4/). Blocked by
# default unless the address is already granted by allow_cidrs; every
# literal still faces the address-category and deny_cidrs rules.
# Non-canonical forms count as literals too: a host whose last label is a
# number (2130706433, 0x7f.1, 127.1) or that contains a colon.
allow_ip_literals = false

# Permit loopback addresses (e.g. for local testing)
allow_loopback = false

# Permit private network addresses (10/8, 172.16/12, 192.168/16, fc00::/7)
allow_private_ips = false

# Permit reserved addresses: CGNAT 100.64/10, 0/8, documentation and
# benchmarking ranges, 240/4, IPv4-compatible/NAT64/6to4/Teredo IPv6 and
# similar non-public ranges. To reach just one of them (e.g. a CGNAT
# overlay network), prefer allow_cidrs.
allow_reserved_ips = false

# Host allowlist: when set, ONLY these hosts may be contacted. Listed
# hosts are trusted — they may resolve to loopback, private and reserved
# addresses. deny_cidrs still applies to them, and a link-local answer
# (169.254.0.0/16, fe80::/10 — where cloud metadata lives) still needs an
# allow_cidrs entry: a suffix entry trusts every name under it, and
# wildcard-DNS names can be pointed at any address. An exact name matches
# itself; a leading dot matches the domain and all subdomains.
# Matching ignores case and a trailing dot ("api.example.com." is the
# same host as "api.example.com"), in entries and in requests alike.
allow_hosts = ["api.example.com", ".internal.corp"]

# Host denylist: always wins, even over the allowlist. Same syntax.
deny_hosts = ["tracker.example"]

# Address range exceptions. allow_cidrs overrides the built-in address
# blocks (how you grant one slice of your LAN); deny_cidrs wins over
# everything, allowlisted hosts included. Multicast is always denied unless granted here, e.g. SSDP
# for scriptling.net.multicast: "239.255.255.250/32".
allow_cidrs = ["10.1.0.0/16"]
deny_cidrs  = ["10.66.0.0/16"]

# Resolve hostnames through these servers instead of the host's resolver
# (plain DNS, port 53). One resolver then serves every script network path,
# including scriptling.net.resolve, so lookups and connections always agree.
dns_servers = ["1.1.1.1", "8.8.8.8:53"]

# Cap each HTTP request end to end - dial, TLS, redirects, reading the
# body - e.g. "30s" or "2m". Off by default: requests run as long as
# their own per-request timeout allows, which long-running calls such as
# LLM APIs need.
client_timeout = "30s"
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
# One slice of the LAN granted, https only. IP-literal URLs inside this
# range are accepted without setting allow_ip_literals.
https_only = true
allow_cidrs = ["10.1.0.0/16"]
```

Note that in the CLI, custom DNS always comes with the policy's address checks — a policy file cannot turn them off. Embedding hosts that want nameservers without any blocking can construct a resolver-only configuration in Go (see `AllowAll` in the [library registration guide](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#network-policy)).

Go hosts configure the same policy in code — see the [library registration guide](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md) for the `netsecurity.Config` reference, and the [security guide](https://scriptling.dev/okf/scriptling-docs/security.md) for the broader sandboxing model.
