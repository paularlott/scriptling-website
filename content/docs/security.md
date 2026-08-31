---
title: Security Guide
description: Security best practices for embedding and running Scriptling in your applications.
tags: [docs, security]
weight: 6
---

Scriptling provides a sandboxed Python-like execution environment, but proper security practices are essential when embedding it in your applications.

## Overview

Scriptling's security boundary depends on how it is configured. **You are responsible for registering only the capabilities your scripts need and for applying process-level isolation where appropriate.**

## Bare Embedding vs CLI Defaults

A bare `scriptling.New()` interpreter starts without standard or extended libraries; the embedding host chooses what to register. It still provides the language runtime and `import` mechanism, but an import succeeds only after the host registers a library or configures a loader.

The `scriptling` CLI is intentionally more permissive. Unless disabled, its setup registers the standard libraries plus extended capabilities including `requests`, `os`, and `subprocess`:

- `requests` can reach the network unless `--network-policy` restricts it.
- `os` can access the filesystem unless `--allowed-paths` restricts its filesystem operations.
- `os.getenv()` reads the live process environment, and `os.environ()` exposes a snapshot of it. Filesystem allowlists do not filter environment variables.
- `subprocess` can execute host commands and bypass library-level filesystem and network controls.

Scriptling runs in a memory-safe Go environment without C extensions and does not directly expose the Go runtime, but the CLI capabilities above still provide host access. Do not describe the default CLI as a no-filesystem, no-network, or no-environment sandbox.

## Library Security

### Pure Standard Libraries

Embedding hosts can register these pure libraries without granting filesystem or network access. The CLI's normal setup includes them; a bare `scriptling.New()` does not register them automatically.

| Library       | Security Notes                               |
| ------------- | -------------------------------------------- |
| `math`        | Pure computation, no external access         |
| `json`        | Pure computation, no external access         |
| `datetime`    | Pure computation, no external access         |
| `time`        | Pure computation, no external access         |
| `string`      | Pure computation, no external access         |
| `base64`      | Pure computation, no external access         |
| `html`        | Pure computation, no external access         |
| `re`          | Regular expressions, no external access      |
| `random`      | Pseudo-random generation, no external access |
| `statistics`  | Pure computation, no external access         |
| `textwrap`    | Pure computation, no external access         |
| `functools`   | Pure computation, no external access         |
| `itertools`   | Pure computation, no external access         |
| `collections` | Pure computation, no external access         |
| `hashlib`     | Cryptographic hashing, no external access    |
| `hmac`        | Keyed hashing (HMAC), no external access     |
| `platform`    | Platform information, read-only              |
| `urllib`      | URL parsing only, no network access          |
| `uuid`        | UUID generation, no external access          |

### Scriptling-Specific Libraries

These libraries provide Scriptling-specific functionality. This is a capability inventory, not a list of libraries available in every runtime; embedding hosts register them explicitly and CLI availability varies by mode and build.

| Library               | Security Considerations                                       |
| --------------------- | ------------------------------------------------------------- |
| `scriptling.ai`       | **NETWORK ACCESS** - Makes HTTP requests to AI APIs           |
| `scriptling.ai.agent` | **NETWORK + CODE EXECUTION** - Agentic AI with tool execution |
| `scriptling.mcp`      | **NETWORK ACCESS** - MCP protocol communication               |
| `scriptling.net.*`    | **NETWORK ACCESS** - DNS, UDP/TCP, gossip, multicast, and WebSocket clients |
| `scriptling.messaging.*` | **NETWORK + REMOTE INPUT** - Bot clients receive events and send messages using script-supplied credentials |
| `scriptling.container` | **INFRASTRUCTURE CONTROL** - Manages Docker, Podman, and Apple Containers |
| `scriptling.nomad`    | **INFRASTRUCTURE CONTROL** - Registers/stops jobs and manages Nomad resources |
| `scriptling.plugin`   | **PROCESS OR NETWORK ACCESS** - Starts executable peers or connects to plugin servers |
| `scriptling.provision.*` | **FILESYSTEM + NETWORK ACCESS** - Changes files and can download remote content |
| `scriptling.secret`   | Host-controlled secret access; scripts see aliases, not provider credentials |
| `scriptling.console`  | Console I/O, including interactive input                       |
| `scriptling.similarity` | Pure computation, no external access                        |
| `scriptling.toon`     | Pure computation, no external access                          |

### Runtime Libraries

These libraries provide server and concurrency functionality:

| Library                      | Security Considerations                                     |
| ---------------------------- | ----------------------------------------------------------- |
| `scriptling.runtime`         | Background task execution (isolated and shared-env threads) |
| `scriptling.runtime.http`    | **HTTP SERVER** - Registers HTTP routes and handlers        |
| `scriptling.runtime.kv`      | In-memory key-value store - safe but unbounded memory       |
| `scriptling.runtime.sync`    | Concurrency primitives - safe but can cause deadlocks       |
| `scriptling.runtime.sandbox` | **CODE EXECUTION** - Executes code in isolated environments |

### Extended Libraries (Require Explicit Registration)

These libraries extend functionality but require explicit registration:

| Library       | Security Considerations                                                     |
| ------------- | --------------------------------------------------------------------------- |
| `requests`    | **NETWORK ACCESS** - Allows HTTP/HTTPS requests to external URLs            |
| `os`          | **FILE SYSTEM ACCESS** - Controlled by allowed paths                        |
| `os.path`     | **FILE SYSTEM ACCESS** - Path operations, controlled by allowed paths       |
| `pathlib`     | **FILE SYSTEM ACCESS** - Object-oriented paths, controlled by allowed paths |
| `glob`        | **FILE SYSTEM ACCESS** - Pattern matching, controlled by allowed paths      |
| `subprocess`  | **CRITICAL RISK** - Allows arbitrary command execution                      |
| `sys`         | **SYSTEM ACCESS** - Provides access to system internals                     |
| `secrets`     | Cryptographically secure random generation                                  |
| `logging`     | File and console logging - may write to disk                                |
| `scriptling.wait_for` | Network/resource polling - may access network                               |
| `scriptling.provision.fetch` | HTTP/HTTPS downloads and filesystem writes; `insecure=True` skips TLS verification |
| `yaml`        | YAML parsing - safe but watch for large files                               |
| `toml`        | TOML parsing - safe but watch for large files                               |
| `html.parser` | HTML parsing - safe but watch for large files                               |

### Never Register in Untrusted Environments

**Do NOT register these libraries when executing untrusted code:**

- `subprocess` - Allows arbitrary command execution
- `sys` - Provides access to system internals and environment
- `scriptling.runtime.sandbox` - Can execute arbitrary code
- `scriptling.ai.agent` - Can execute AI-generated code with tools

## File System Security

### Restricting File Access

When registering filesystem libraries, you **must** specify allowed paths:

```go
// Safe: Only allows access to specific directories
extlibs.RegisterOSLibrary(p, []string{
    "/tmp/myapp/data",
    "/home/user/documents",
})
extlibs.RegisterPathlibLibrary(p, []string{
    "/tmp/myapp/data",
    "/home/user/documents",
})
extlibs.RegisterTempfileLibrary(p, []string{"/tmp/myapp"})
extlibs.RegisterShutilLibrary(p, []string{
    "/tmp/myapp/data",
    "/home/user/documents",
})

// Dangerous: Allows access to entire file system
extlibs.RegisterOSLibrary(p, nil)        // Nil = no restriction (full read/write access)
extlibs.RegisterOSLibrary(p, []string{}) // Empty = deny all (no paths allowed)
```

All filesystem libraries (`os`, `pathlib`, `fs`, `glob`, `tempfile`, `shutil`, `zipfile`, `tarfile`, `scriptling.grep`, `scriptling.find`, `scriptling.sed`) accept `allowedPaths` and enforce the same path traversal and symlink protections. Archive libraries (`zipfile`, `tarfile`) additionally block zip-slip / tar-slip attacks (path traversal via crafted entry names).

### Path Traversal Protection

Scriptling's file system libraries automatically prevent path traversal attacks:

```python
# User tries to escape allowed directory
import os
import pathlib

allowed_path = "/tmp/myapp/data"
# Trying to access parent directories
os.read_file("/tmp/myapp/data/../../etc/passwd")  # BLOCKED
os.read_file("/tmp/myapp/data/secrets.txt")        # ALLOWED

path = pathlib.Path("/tmp/myapp/data/../../../etc/passwd")  # BLOCKED
```

## Network Security

### Network-Enabled Libraries

These libraries can make network requests:

- `requests` - HTTP client library
- `scriptling.sql` - MySQL, MariaDB and PostgreSQL client (see [Database Drivers](#database-drivers))
- `scriptling.valkey` - Valkey/Redis client (see [Database Drivers](#database-drivers))
- `scriptling.ai` - AI API client
- `scriptling.ai.agent` - Agentic AI with tool execution
- `scriptling.mcp` - MCP protocol client
- `scriptling.wait_for` - Resource polling (may check network endpoints)
- `scriptling.provision.fetch` - HTTP/HTTPS downloads and optional zip unpacking

### Disabling Network Access

To keep the sandbox network-free, don't register network-enabled libraries:

```go
// Safe: Only register standard libraries (no network access)
stdlib.RegisterAll(p)

// Unsafe: Registers network-enabled library
extlibs.RegisterRequestsLibrary(p)
```

### Network Policies

For scripts that *should* reach the internet but must never reach your private network, register a network policy. A policy governs the `requests`, `scriptling.wait_for`, and `scriptling.net.websocket` libraries and is enforced at connect time: the hostname is resolved through the configured DNS servers, every resolved address is checked against the policy, and the connection is made to the validated address directly. That closes the usual bypasses — DNS rebinding (the answer changing between check and connect), redirects to internal hosts, and IP-notation tricks.

With a policy active, loopback, link-local (including cloud metadata endpoints like `169.254.169.254`), private, unspecified, and multicast addresses are all blocked by default, as are URLs that name an IP directly. Host allow/deny lists, CIDR exceptions, https-only, and custom DNS servers grant exactly the access you intend — allowlisted hosts are trusted to resolve internally, and deny rules always win.

- **CLI**: `--network-policy=policy.toml` — the full policy file reference is in the [network policy guide](/docs/cli/network-policy/). Combine it with `--disable-lib subprocess` in any mode so code cannot bypass the policy by shelling out.
- **Embedding**: pass a `*netsecurity.Config` (or load the same TOML file with `netsecurity.LoadConfig`) when registering the governed libraries — the `Config` options are documented in the [library registration guide](/docs/go-integration/library-registration/#network-policy). No policy means no restrictions.

```go
policy, err := netsecurity.LoadConfig("policy.toml")
if err != nil {
    return err // an invalid policy must never degrade into an open one
}
extlibs.RegisterRequestsLibrary(p, policy)
extlibs.RegisterWaitForLibrary(p, policy)
extlibs.RegisterWebSocketLibrary(p, policy)
```

The policy governs the three libraries above. `scriptling.ai`, `scriptling.mcp`, and `scriptling.provision.fetch` make network calls too, but to endpoints configured by the host rather than chosen by the script; if scripts can configure those endpoints in your integration, keep them unregistered in untrusted environments.

## Database Drivers

The database plugins enforce the host security policy on every operation, in both compiled-in and external-plugin form (the policy travels in the plugin handshake):

- **`scriptling.sqlite` and `scriptling.badgerdb` (file-backed)** — the database path must fall inside `--allowed-paths` / the embedder's allowed paths. `":memory:"` sqlite databases are always allowed.
- **`scriptling.sql` and `scriptling.valkey` (network)** — connections dial through the same guard as the `requests` library, so a network policy applies in full. This answers the common question for MySQL/MariaDB/PostgreSQL DSNs: **connecting by hostname or by IP are both covered.** A hostname is resolved through the policy's DNS servers and every resolved address is checked; an IP literal is checked directly — and IP literals are denied by default, so `mysql://user@10.0.0.5/db` needs the address allowed explicitly:

  - `allow_private_ips = true` together with `allow_ip_literals = true` for arbitrary private IP literals, or
  - the address inside `allow_cidrs` (an explicit CIDR grant permits that IP literal without `allow_ip_literals`), or
  - the hostname inside `allow_hosts` (allowlisted hosts are trusted to resolve internally — the recommended way to grant access to `db.internal.corp`).

  Loopback (`postgres://localhost` on the same machine) needs `allow_loopback = true`. The same rules apply to `valkey://` URLs.

When no policy is configured the drivers connect without restriction, exactly like the other network libraries.

The same holds for any plugin that advertises the `policy` capability, and it
is worth being precise about what that means: the policy is **delivered to the
plugin and enforced by it**. It is not a sandbox around a plugin process, so
`--allowed-paths` and `--network-policy` bound what a *cooperative* plugin
does, never what a malicious one could. Treat third-party plugin binaries
like any other executable you choose to run. For plugins that do cooperate
the protection is real, and the network guard in particular carries genuine
SSRF and DNS-rebinding defences to every dial the plugin makes.

```toml
# policy.toml — a script that may reach the database subnet
allow_private_ips = true
allow_hosts = ["db.internal.corp"]
```

## Secret Provider Security

Use `scriptling.secret` when scripts need secrets but should not receive provider URLs, tokens, or other private configuration.

**Recommended pattern:** Register providers in the host application and expose only aliases to scripts.

```python
import scriptling.secret as secret

db_password = secret.get("prod_vault", "secret/data/app", "password")
```

The script only sees `prod_vault`, the logical path, and the optional field name. The host owns the real provider configuration.

## Resource Limits

### Execution Timeout

Always set timeouts for script execution:

```go
import "time"

ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

result, err := p.EvalWithContext(ctx, code)
if err == context.DeadlineExceeded {
    // Script was terminated due to timeout
}
```

### Memory Limits

Scriptling runs within Go's memory management, but consider:

1. **Large allocations** can cause memory pressure
2. **Infinite loops** can consume CPU indefinitely
3. **Recursion depth** is limited by Go's stack

## Code Injection Prevention

### Never Execute Untrusted Input Directly

```python
# DANGEROUS: Never do this with scriptling.runtime.sandbox
import scriptling.runtime.sandbox as sandbox

user_input = get_user_code()  # e.g., "os.remove('/important/file')"
sandbox.eval(user_input)      # Executes arbitrary code!
```

**Note**: The `scriptling.runtime.sandbox` library allows executing arbitrary code strings. Never pass untrusted user input directly to it.

### Safe Patterns

```python
# SAFE: Use structured data and predefined functions
user_config = get_user_config()  # Returns validated dict
name = user_config.get("name", "Anonymous")
greet(name)  # Controlled execution

# SAFE: Whitelist allowed operations
allowed_operations = {"add", "subtract", "multiply"}
operation = user_config.get("operation")
if operation in allowed_operations:
    result = perform_operation(operation, x, y)
```

## Environment Variables

The CLI registers `os` by default: `os.getenv()` reads the live process environment and `os.environ()` returns the snapshot captured when the library was registered. `--allowed-paths` does not filter either API. For untrusted CLI code, sanitize the host process environment and disable `os`; embedding hosts can omit the library and expose only selected values:

```go
// A bare scriptling.New() has no libraries; pass only approved values.
p.SetVar("APP_VERSION", "1.0.0")
p.SetVar("API_ENDPOINT", apiEndpoint)
```

Do not rely on omitting `sys` alone: it is not the CLI's only environment-access path.

## Security Checklist

Use this checklist when deploying Scriptling in production:

- [ ] File system access is restricted to specific paths (`os`, `pathlib`, `glob`)
- [ ] Network access is disabled or restricted per client (`requests`, databases, networking, messaging, AI, MCP)
- [ ] Execution timeout is configured
- [ ] `subprocess` library is NOT registered
- [ ] `sys` and `os` are omitted or carefully controlled for untrusted code
- [ ] Container, Nomad, plugin, messaging, and provisioning libraries are omitted unless explicitly required
- [ ] `scriptling.runtime.sandbox` is NOT registered for untrusted code
- [ ] `scriptling.ai.agent` is NOT registered for untrusted code
- [ ] Environment variables are filtered
- [ ] Untrusted user input is validated
- [ ] Scripts run with minimal privileges
- [ ] Error messages don't leak sensitive information
- [ ] Logs are sanitized before display
- [ ] Runtime KV store size is monitored (unbounded memory)
- [ ] Background tasks are properly managed and terminated

## Common Attack Vectors

### 1. Resource Exhaustion

```python
# Consumes all memory
big_list = []
while True:
    big_list = big_list + ["x" * 1000000]
```

**Mitigation**: Use execution timeouts.

### 2. Infinite Loops

```python
# Consumes all CPU
while True:
    pass
```

**Mitigation**: Use execution timeouts.

### 3. Path Traversal (Protected)

```python
# Attempt to escape allowed directory
import os
os.read_file("../../etc/passwd")
```

**Mitigation**: Scriptling's `os` library validates paths against allowed directories.

### 4. Information Disclosure

```python
# Read a host secret when the CLI's default os library is enabled
import os
secret = os.getenv("SECRET_TOKEN")
```

**Mitigation**: Sanitize the process environment and disable or omit `os` for untrusted code; filesystem path restrictions do not filter environment variables.

## Best Practices

1. **Principle of Least Privilege**: Only register the libraries that are absolutely necessary
2. **Validate All Input**: Never trust user-provided code or data
3. **Use Timeouts**: Always set execution time limits
4. **Restrict File Access**: Explicitly whitelist allowed directories for `os`, `pathlib`, `glob`
5. **Disable Network**: Unless needed, keep the sandbox offline (don't register `requests`, `scriptling.ai`, `scriptling.mcp`)
6. **Monitor Resource Usage**: Watch for unusual memory/CPU consumption
7. **Sanitize Errors**: Don't expose internal paths or stack traces to users
8. **Keep Updated**: Update Scriptling regularly for security patches
9. **Limit Runtime State**: Monitor `scriptling.runtime.kv` store size and use TTLs
10. **Control Concurrency**: Be aware that `scriptling.runtime.sync` primitives can cause deadlocks
11. **Sandbox Isolation**: Use `scriptling.runtime.sandbox` carefully - it executes code in isolated environments but still runs in the same process

## Reporting Security Issues

If you discover a security vulnerability in Scriptling, please report it responsibly:

1. Do **NOT** create a public issue
2. Submit details via our [Security Report Form](https://forms.gle/86ckNpahQWPP5xRLA)
3. Include steps to reproduce
4. Allow time for a fix to be released before disclosure

## Additional Resources

- [Go Integration Basics](../go-integration/basics/) - Setting up Scriptling in Go
- [Sandbox Library](../../reference/libraries/runtime/sandbox/) - Runtime sandbox configuration
- [Library Registration](../go-integration/library-registration/) - How to register libraries in Go
