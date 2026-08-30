---
description: DNS resolution for hostname lookup, SRV records, and srv+http(s):// URLs.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/networking/resolve/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/networking/resolve/
status: stable
tags:
    - libraries
    - networking
title: scriptling.net.resolve
type: API Reference
---
# scriptling.net.resolve

DNS resolution library for hostname lookup, SRV record resolution, and `srv+http(s)://` URL resolution.

## Overview

The `scriptling.net.resolve` library provides DNS resolution utilities. It uses the system resolver by default, or custom nameservers when configured by the host application (e.g. [knot](https://github.com/paularlott/knot)). In the CLI, a [network policy](https://scriptling.dev/okf/scriptling-docs/cli/network-policy.md)'s `dns_servers` configure this resolver too — every script network path resolves through the same servers.

## Available Functions

| Function | Description |
|----------|-------------|
| `lookup_ip(host)` | Resolve a hostname to a list of IP addresses. |
| `lookup_srv(service)` | Resolve an SRV record to a list of addresses. |
| `resolve_srv_http(uri)` | Resolve a `srv+http(s)://` URI to a concrete URL. |

## Functions

### `lookup_ip(host)`

Resolves a hostname to a list of IP address strings (A and AAAA records).

**Parameters:**
- `host` (`str`): The hostname to resolve.

**Returns:** `list[str]`: list of IP address strings.

```python
import scriptling.net.resolve as resolve

ips = resolve.lookup_ip("example.com")
print(ips)  # ["93.184.216.34"]

for ip in ips:
    print(ip)
```

### `lookup_srv(service)`

Resolves an SRV service name to a list of address dicts, ordered by priority and weighted random selection per RFC 2782.

**Parameters:**
- `service` (`str`): The SRV service name, e.g. `"_myservice._tcp.example.com"`.

**Returns:** `list[dict]`: list of address dicts, each with `ip` (`str`, the resolved IP address) and `port` (`int`, the port number from the SRV record).

```python
import scriptling.net.resolve as resolve

addrs = resolve.lookup_srv("_myservice._tcp.example.com")
for addr in addrs:
    print(f"{addr['ip']}:{addr['port']}")
```

### `resolve_srv_http(uri)`

Resolves a `srv+http(s)://` URI to a concrete URL. Strips the `srv+` prefix, resolves the SRV record for the host, and substitutes the resolved port. The original hostname is preserved for SNI/TLS.

If `uri` does not start with `srv+`, it is returned unchanged, with an `https://` prefix added if no scheme is present.

**Parameters:**
- `uri` (`str`): The URI to resolve.

**Returns:** `str`: the resolved URL.

```python
import scriptling.net.resolve as resolve

url = resolve.resolve_srv_http("srv+https://api.example.com/v1")
print(url)  # "https://api.example.com:8443/v1"

# Non-SRV URIs pass through
url = resolve.resolve_srv_http("https://plain.example.com/path")
print(url)  # "https://plain.example.com/path"
```

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#extended-libraries).

`scriptling.net.resolve` performs DNS lookups against the system resolver, or against custom nameservers if the embedder injects one. DNS responses are not validated against any allowlist, so a script can trigger lookups for arbitrary hostnames, which can be used for network reconnaissance or to exfiltrate data via DNS queries. Host applications can restrict or monitor this by passing a custom resolver to `resolve.Register(env, resolver)`: see [Host Application Integration](#host-application-integration) below. See [Security Considerations](https://scriptling.dev/okf/scriptling-docs/security.md#network-security) for a full breakdown of network-enabled libraries.

## Host Application Integration

Host applications can inject a custom resolver by passing it to `resolve.Register(env, resolver)`. This allows applications like [knot](https://github.com/paularlott/knot) to configure custom nameservers, caching, and domain-specific routing. The `resolver` argument is required; `Register` panics if it is `nil`. When the host also registers a network policy, pass the policy's resolver (the `netsecurity` guard's `Resolver()`) so lookups and connections share one resolver — see the [library registration guide](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#network-policy).

## See Also

- [scriptling.net.unicast](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/unicast.md): direct point-to-point UDP/TCP messaging
- [scriptling.net.websocket](https://scriptling.dev/okf/scriptling-libraries/scriptling/networking/websocket.md): WebSocket client library
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md): full risk breakdown across all libraries
