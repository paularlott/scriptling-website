---
title: scriptling.net.resolve
linkTitle: resolve
weight: 3
---

DNS resolution library for IP lookup, SRV record resolution, and srv+http URL resolution.

## Overview

The `scriptling.net.resolve` library provides DNS resolution utilities. It uses the system resolver by default, or custom nameservers when configured by the host application (e.g. knot).

## Available Functions

| Function | Description |
|----------|-------------|
| `lookup_ip(host)` | Resolve a hostname to a list of IP addresses |
| `lookup_srv(service)` | Resolve an SRV record to a list of addresses |
| `resolve_srv_http(uri)` | Resolve a srv+http(s):// URI to a concrete URL |

## lookup_ip

```python
lookup_ip(host: str) -> list[str]
```

Resolves a hostname to a list of IP address strings (A and AAAA records).

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `host` | `str` | The hostname to resolve |

### Returns

`list[str]` — List of IP address strings.

### Example

```python
import scriptling.net.resolve as resolve

ips = resolve.lookup_ip("example.com")
print(ips)  # ["93.184.216.34"]

for ip in ips:
    print(ip)
```

## lookup_srv

```python
lookup_srv(service: str) -> list[dict]
```

Resolves an SRV service name to a list of address dicts, ordered by priority and weighted random selection per RFC 2782.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `service` | `str` | The SRV service name (e.g. `_myservice._tcp.example.com`) |

### Returns

`list[dict]` — List of address dicts, each with:

| Key | Type | Description |
|-----|------|-------------|
| `ip` | `str` | Resolved IP address |
| `port` | `int` | Port number from the SRV record |

### Example

```python
import scriptling.net.resolve as resolve

addrs = resolve.lookup_srv("_myservice._tcp.example.com")
for addr in addrs:
    print(f"{addr['ip']}:{addr['port']}")
```

## resolve_srv_http

```python
resolve_srv_http(uri: str) -> str
```

Resolves a `srv+http(s)://` URI to a concrete URL. Strips the `srv+` prefix, resolves the SRV record for the host, and substitutes the resolved port. The original hostname is preserved for SNI/TLS.

If the URI does not start with `srv+`, it is returned unchanged (with an `https://` prefix added if no scheme is present).

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `uri` | `str` | The URI to resolve |

### Returns

`str` — The resolved URL.

### Example

```python
import scriptling.net.resolve as resolve

url = resolve.resolve_srv_http("srv+https://api.example.com/v1")
print(url)  # "https://api.example.com:8443/v1"

# Non-SRV URIs pass through
url = resolve.resolve_srv_http("https://plain.example.com/path")
print(url)  # "https://plain.example.com/path"
```

## Host Application Integration

Host applications can inject a custom resolver by passing it to `resolve.Register(env, resolver)`. This allows applications like knot to configure custom nameservers, caching, and domain-specific routing. Passing `nil` uses the default system DNS resolver.
