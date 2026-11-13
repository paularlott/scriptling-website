---
title: Library Registration
description: How to register standard and extension libraries when embedding Scriptling in Go.
tags: [go-integration, embedding, go]
weight: 2
---

When embedding Scriptling in a Go application, you control which libraries are available to scripts. A bare `scriptling.New()` interpreter has no importable libraries: a library exists for scripts only once you register it.

Libraries come in two tiers, and the tier tells you both what a library can reach and what it costs to include.

| Tier | Go package | What it may do | How to register |
|------|------------|----------------|-----------------|
| **Standard libraries** | `github.com/paularlott/scriptling/stdlib` | Pure computation. No filesystem, network, process, environment or host access, and no third-party dependency beyond what the interpreter core already links | `stdlib.RegisterAll(p)`, or `p.RegisterLibrary(stdlib.XLibrary)` one at a time |
| **Extension libraries** | One package per library or family, under `github.com/paularlott/scriptling/extlibs/...` | Anything the host grants: files, network, processes, host information, credentials, or simply a large dependency | Import the package and call its `Register` function |

## Why Two Tiers

**Capability.** Every standard library is safe by construction: it can compute, but it cannot touch the world outside the interpreter. You can register the whole set for untrusted scripts, which are then bounded by the interpreter's resource limits. Each extension library is a capability you grant deliberately, usually with a path or network policy attached.

**Binary size and dependencies.** The interpreter core depends on the `stdlib` package, so the standard libraries are compiled into every application that embeds Scriptling whether or not you register them; registering them costs no extra binary size. Extension libraries are the opposite: each lives in its own Go package, and an application that does not import a package does not link it or its dependencies. You only ship, and only have to audit, the extensions you register.

The split was driven by measurement. Before it, the extension libraries shared one Go package, so registering only YAML produced a 13.7 MB binary: it linked every library in that package, including the WebSocket client, the Markdown renderer, process inspection, the KV store, the HTTP client and subprocess. Today the same embedder is 6.83 MB.

Measured on stripped darwin/arm64 embedder binaries, the interpreter plus every standard library is 6.52 MB. Adding one extension gives:

| Registered on top of the standard libraries | Binary | Added |
|---------------------------------------------|--------|-------|
| `toml` | 6.73 MB | 0.21 MB |
| `os` (filesystem) | 6.81 MB | 0.29 MB |
| `yaml` | 6.83 MB | 0.31 MB |
| `scriptling.net.multicast` | 7.86 MB | 1.34 MB |
| `scriptling.template.*` | 7.96 MB | 1.44 MB |
| `requests` | 9.96 MB | 3.44 MB |
| `scriptling.mercure` | 10.04 MB | 3.52 MB |

The runtime family is split the same way, so a server pays only for the pieces it registers:

| Runtime libraries registered | Added |
|------------------------------|-------|
| Core: `scriptling.runtime` (background tasks), `.sync`, `.sandbox`, `.jsonrpc`, `.mcp`, `.plugin` | 0.34 MB |
| `scriptling.runtime.kv` only | 0.46 MB |
| `scriptling.runtime.http` (links the core) | 1.92 MB |
| All of the runtime libraries | 2.40 MB |

When the tiers were drawn, the candidate libraries were measured in isolation:

| Library | Size | Tier |
|---------|------|------|
| `shlex` | 16 KB | Standard |
| `secrets` | 16 KB | Standard |
| `html.parser` | 64 KB | Standard |
| `csv` | 65 KB | Standard |
| `xml` | 68 KB | Standard |
| `toml` | 197 KB | Extension |
| `yaml` | 296 KB | Extension |
| `scriptling.template.*` | 1.4 MB | Extension |

The first five meet the standard-library rule and are small (229 KB together), so they are standard libraries. YAML, TOML and the template engine stay opt-in because of their weight, even though they have no host access.

## Minimal Embedder

An interpreter with the standard libraries and nothing else. Scripts can compute, parse and format data, but cannot reach files, the network, processes or the host:

```go
package main

import (
    "fmt"

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    _, err := p.Eval(`
import csv, io, json, statistics

rows = list(csv.DictReader(io.StringIO("name,score\nada,92\nalan,87\n")))
print(json.dumps({"rows": len(rows), "mean": statistics.mean([int(r["score"]) for r in rows])}))
`)
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

## Pick What You Need

Add extension libraries one at a time, each with the narrowest policy that works. Only the packages imported here are linked into the binary:

```go
package main

import (
    "fmt"

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/extlibs/filesystem"
    "github.com/paularlott/scriptling/extlibs/logging"
    "github.com/paularlott/scriptling/extlibs/netsecurity"
    "github.com/paularlott/scriptling/extlibs/requests"
    "github.com/paularlott/scriptling/extlibs/yaml"
    "github.com/paularlott/scriptling/stdlib"
)

func main() {
    p := scriptling.New()
    stdlib.RegisterAll(p)

    // No host access, just a parser: no policy needed.
    yaml.Register(p)

    // Log through the default logger (stdout).
    logging.RegisterDefault(p)

    // os, os.path and pathlib, confined to one directory.
    filesystem.RegisterOS(p, []string{"/srv/app/data"})
    filesystem.RegisterPathlib(p, []string{"/srv/app/data"})

    // Outbound HTTPS to a single API host.
    requests.Register(p, &netsecurity.Config{
        RequireHTTPS: true,
        AllowHosts:   []string{"api.example.com"},
    })

    if _, err := p.Eval(`import yaml, os, requests`); err != nil {
        fmt.Println("Error:", err)
    }
}
```

## Standard Libraries

### Register All at Once

```go
import "github.com/paularlott/scriptling/stdlib"

stdlib.RegisterAll(p)
```

`stdlib.LibraryNames()` returns the name of every library `RegisterAll` registers, in registration order, which is useful for building allow or deny lists.

### Register Individually

```go
p.RegisterLibrary(stdlib.JSONLibrary)
p.RegisterLibrary(stdlib.MathLibrary)
p.RegisterLibrary(stdlib.ReLibrary)
p.RegisterLibrary(stdlib.TimeLibrary)
```

Registering a subset changes what scripts can import, not what is compiled in: the whole `stdlib` package is part of every embedding binary.

`stdlib.RegisterAll` registers every library in this table. Each library variable has a matching name constant (`stdlib.JSONLibraryName` and so on) where one is declared in `stdlib`.

| Import name | Go variable |
|-------------|-------------|
| `base64` | `stdlib.Base64Library` |
| `collections` | `stdlib.CollectionsLibrary` |
| `contextlib` | `stdlib.ContextlibLibrary` |
| `copy` | `stdlib.CopyLibrary` |
| `csv` | `stdlib.CSVAliasLibrary` |
| `dataclasses` | `stdlib.DataclassesLibrary` |
| `datetime` | `stdlib.DatetimeLibrary` |
| `difflib` | `stdlib.DifflibLibrary` |
| `enum` | `stdlib.EnumLibrary` |
| `functools` | `stdlib.FunctoolsLibrary` |
| `hashlib` | `stdlib.HashlibLibrary` |
| `hmac` | `stdlib.HmacLibrary` |
| `html` | `stdlib.HTMLLibrary` |
| `html.parser` | `stdlib.HTMLParserLibrary` |
| `io` | `stdlib.IOLibrary` |
| `itertools` | `stdlib.ItertoolsLibrary` |
| `json` | `stdlib.JSONLibrary` |
| `math` | `stdlib.MathLibrary` |
| `msgpack` | `stdlib.MsgpackLibrary` |
| `random` | `stdlib.RandomLibrary` |
| `re` | `stdlib.ReLibrary` |
| `scriptling.csv` | `stdlib.CSVLibrary` |
| `scriptling.xml` | `stdlib.XMLLibrary` |
| `secrets` | `stdlib.SecretsLibrary` |
| `shlex` | `stdlib.ShlexLibrary` |
| `statistics` | `stdlib.StatisticsLibrary` |
| `string` | `stdlib.StringLibrary` |
| `textwrap` | `stdlib.TextwrapLibrary` |
| `time` | `stdlib.TimeLibrary` |
| `typing` | `stdlib.TypingLibrary` |
| `urllib` | `stdlib.URLLibLibrary` |
| `urllib.parse` | `stdlib.URLParseLibrary` |
| `uuid` | `stdlib.UUIDLibrary` |
| `xml` | `stdlib.XMLAliasLibrary` |

`csv` and `xml` are the same libraries as `scriptling.csv` and `scriptling.xml`, registered under their Python names as well. `secrets` draws from the operating system's cryptographic random source, which is not host access in the sense above: it reveals nothing about the host and changes nothing.

`platform` is not a standard library: it reports the host name, so it is an extension (`platform.Register(p)`, see [Utilities](#utilities)).

## Extension Libraries

Each extension lives in its own package under `github.com/paularlott/scriptling/extlibs/`. Import the package, then call its registration function. Every package also exports its import name as a constant (`yaml.LibraryName`, `filesystem.OSLibraryName`, `runtime.RuntimeSyncLibraryName`, `kv.LibraryName` and so on).

In the tables below, the package column is relative to `github.com/paularlott/scriptling/`, and *Grants* is the reason to think before registering: filesystem, network, process, host information, credentials, code execution, inbound (a server entry point), or none (no host access, opt-in only because of its size or dependencies).

### Filesystem Libraries

Package `extlibs/filesystem`. Every function takes `allowedPaths []string`, the directories the library may touch (see [Path Policy](#path-policy)).

```go
import "github.com/paularlott/scriptling/extlibs/filesystem"

// Everything in the family, under one path policy
filesystem.RegisterAll(p, []string{"/tmp", "/data"})

// Or only what scripts need
filesystem.RegisterOS(p, []string{"/tmp", "/data"})
filesystem.RegisterGlob(p, []string{"/data"})
```

| Import name | Registration | Grants |
|-------------|--------------|--------|
| `os`, `os.path` | `filesystem.RegisterOS(p, allowedPaths)` | Filesystem read/write; environment variables (`os.environ`, `os.getenv`) |
| `pathlib` | `filesystem.RegisterPathlib(p, allowedPaths)` | Filesystem read/write |
| `glob` | `filesystem.RegisterGlob(p, allowedPaths)` | Filesystem read (listings) |
| `fs` | `filesystem.RegisterFS(p, allowedPaths)` | Filesystem read/write |
| `shutil` | `filesystem.RegisterShutil(p, allowedPaths)` | Filesystem read/write |
| `tempfile` | `filesystem.RegisterTempfile(p, allowedPaths)` | Filesystem write |
| `zipfile` | `filesystem.RegisterZipfile(p, allowedPaths)` | Filesystem read/write |
| `tarfile` | `filesystem.RegisterTarfile(p, allowedPaths)` | Filesystem read/write |
| `scriptling.grep` | `filesystem.RegisterGrep(p, allowedPaths)` | Filesystem read |
| `scriptling.find` | `filesystem.RegisterFind(p, allowedPaths)` | Filesystem read |
| `scriptling.sed` | `filesystem.RegisterSed(p, allowedPaths)` | Filesystem read/write |
| all of the above | `filesystem.RegisterAll(p, allowedPaths)` | |

The constructors (`filesystem.NewOSLibrary`, `NewPathlibLibrary`, `NewGlobLibrary`, `NewShutilLibrary`, `NewTempfileLibrary`, `NewZipfileLibrary`, `NewTarfileLibrary`, `NewGrepLibrary`, `NewFindLibrary`, `NewSedLibrary`) take an `fssecurity.Config` and return the library without registering it. The package also exports a plain Go API (`filesystem.Grep`, `filesystem.Find`, `filesystem.SedReplace`, `filesystem.EditFile` and their option types) that needs no interpreter.

### Path Policy

Every library that touches files takes the same policy, either as `allowedPaths []string` or as an `fssecurity.Config{AllowedPaths: ...}` (package `extlibs/fssecurity`):

| Value | Meaning |
|-------|---------|
| `nil` (or a zero `fssecurity.Config`) | No restriction: the whole filesystem the process can reach |
| `[]string{}` | Deny all paths |
| `[]string{"/srv/data", ...}` | Only these directories and everything below them |

Relative entries are made absolute against the process's working directory. Every check resolves symbolic links and `..` before comparing, so a link or traversal that leads outside the allowed directories is refused, and `/allowed` does not match `/allowed-other`. A refused path raises `PermissionError`.

The same policy confines the file access of libraries outside the filesystem family:

| Library | Registration | What the paths confine |
|---------|--------------|------------------------|
| `requests` | `requests.RegisterConfigured(p, paths, policy)` | The CA bundle a script names with `verify="path"` |
| `scriptling.oauth` | `oauth.RegisterConfigured(p, paths, policy)` | CA bundle files |
| `scriptling.mercure` | `mercure.RegisterConfigured(p, paths, policy, opts...)` | CA bundle files |
| `scriptling.wait_for` | `waitfor.RegisterConfigured(p, allowedPaths, policy...)` | `file()`, `dir()` and `file_content()` |
| `scriptling.container` | `container.RegisterConfigured(...)` or `container.RegisterWithOptions(p, opts)` | Unix sockets and bind-mounted volumes a script names |
| Slack, Discord, Telegram | `slack.RegisterConfigured(p, logger, allowedPaths, policy...)` (same for `discord`, `telegram`) | Local files `send_file()` reads |
| `scriptling.runtime.http` | `http.Register(p, allowedPaths)` (`extlibs/runtime/http`) | Directories `static()` may serve; the server serves only files that resolve inside them |
| `scriptling.runtime.kv` | `kv.Register(p, allowedPaths)` (`extlibs/runtime/kv`) | Persistent stores `kv.open()` creates or opens (in-memory `:memory:` stores are always allowed) |
| `scriptling.runtime.sandbox` | `runtime.RegisterSandbox(p, allowedPaths)` | Scripts `exec_file()` reads |
| `scriptling.provision.file`, `.fetch` | `file.RegisterConfigured(p, paths, ...)`, `fetch.RegisterConfigured(p, paths, guard, ...)` | Files they create, change or download to |

Each plain `Register` in that table registers the library without a path restriction. The runtime libraries have no such variant: `http.Register`, `kv.Register` and `runtime.RegisterSandbox` always take `allowedPaths`, so an unconfined `static()`, `kv.open()` or `exec_file()` means passing `nil` explicitly. A path they refuse raises the same uncatchable `PermissionError` as the filesystem libraries. The CLI registers all of these libraries with its `--allowed-paths` list.

### Network and HTTP

| Import name | Package | Registration | Grants |
|-------------|---------|--------------|--------|
| `requests` | `extlibs/requests` | `requests.Register(p, policy...)` or `requests.RegisterConfigured(p, paths, policy)` | Network (outbound HTTP); reads CA bundle files |
| `scriptling.oauth` | `extlibs/oauth` | `oauth.Register(p, policy...)` or `oauth.RegisterConfigured(p, paths, policy)` | Network |
| `scriptling.net.websocket` | `extlibs/net/websocket` | `websocket.Register(p, policy...)` | Network |
| `scriptling.net.unicast` | `extlibs/net/unicast` | `unicast.Register(p, policy...)` | Network |
| `scriptling.net.multicast` | `extlibs/net/multicast` | `multicast.Register(p, policy...)` | Network |
| `scriptling.net.gossip` | `extlibs/net/gossip` | `gossip.Register(p, logger, policy...)` (a nil logger is a null logger) | Network |
| `scriptling.net.resolve` | `extlibs/net/resolve` | `resolve.Register(p, resolver)` (your `resolve.Resolver`) | DNS lookups through the resolver you supply |
| `scriptling.mercure` | `extlibs/mercure` | `mercure.Register(p, policy...)` or `mercure.RegisterConfigured(p, paths, policy, opts...)` | Network |
| `scriptling.wait_for` | `extlibs/waitfor` | `waitfor.Register(p, policy...)` or `waitfor.RegisterConfigured(p, allowedPaths, policy...)` | Network (ports, HTTP), filesystem (file checks), process list (`process_name()`) |

`mercure.WithoutSubscribe()` is an option for `RegisterConfigured` that lets scripts publish but not receive. The interpreter closes the Mercure clients a script leaves open ([lifecycle](../basics/#what-a-script-leaves-open)).

`requests.Register` with a policy but no paths leaves the CA bundle unconfined; use `requests.RegisterConfigured(p, fssecurity.Config{AllowedPaths: paths}, policy)` to confine it too (outside the paths it raises an uncatchable `PermissionError`, as in `os`). The CLI registers it this way with `--allowed-paths` and `--network-policy`.

### Network Policy

The outbound networking libraries (`requests`, `scriptling.wait_for`, `scriptling.net.websocket`, `scriptling.net.unicast`, `scriptling.net.multicast`, `scriptling.net.gossip`, `scriptling.nomad`, `scriptling.oauth`, `scriptling.mercure`, `scriptling.ai`, `scriptling.mcp`, and the Slack, Discord and Telegram messaging libraries) accept an optional `*netsecurity.Config` (package `extlibs/netsecurity`) that restricts where scripts may connect. `scriptling.container` takes one through `container.RegisterConfigured` or `container.Options.Policy` (it checks the endpoints a script supplies), and `scriptling.provision.fetch` takes a `*netsecurity.Guard` through `fetch.RegisterConfigured`. Pass `nil` (or omit the argument) for no restrictions; a non-nil policy blocks loopback, link-local (cloud metadata), private, unspecified, and multicast addresses, and IP-literal URLs, by default. An invalid policy fails closed: the library refuses every connection rather than falling back to unrestricted access.

```go
import (
    "github.com/paularlott/scriptling/extlibs/ai"
    scriptlingmcp "github.com/paularlott/scriptling/extlibs/mcp"
    "github.com/paularlott/scriptling/extlibs/net/websocket"
    "github.com/paularlott/scriptling/extlibs/netsecurity"
    "github.com/paularlott/scriptling/extlibs/requests"
    "github.com/paularlott/scriptling/extlibs/waitfor"
)

policy := &netsecurity.Config{
    RequireHTTPS: true,
    AllowHosts:   []string{"api.example.com"},
}

requests.Register(p, policy)
waitfor.Register(p, policy)
websocket.Register(p, policy)
ai.Register(p, policy)
scriptlingmcp.Register(p, policy)

```

To load the same TOML file the CLI's `--network-policy` flag uses, import `extlibs/netsecurity/policyfile`. It is a separate package so that the network libraries do not link a TOML parser; only an application that reads policy files imports it:

```go
import "github.com/paularlott/scriptling/extlibs/netsecurity/policyfile"

policy, err := policyfile.LoadConfig("policy.toml") // *netsecurity.Config
if err != nil {
    return err // invalid policies are an error, never an open policy
}
requests.Register(p, policy)
```

`ai.Register`'s policy also guards `remote_servers`, the MCP servers an `ai.Client()` instance can attach for tool use, so a script cannot reach a policy-blocked endpoint by routing through `ai.Client(..., remote_servers=[...])` instead of `mcp.Client(...)` directly. Stdio-transport `mcp.Client()` instances (a local subprocess) are unaffected: the policy only governs network access.

`Config` options (all optional; the zero value behind a non-nil pointer is a safe default policy):

| Option | Type | Default | Meaning |
|---|---|---|---|
| `RequireHTTPS` | `bool` | `false` | Reject plain `http://` and `ws://` URLs |
| `AllowIPLiterals` | `bool` | `false` | Permit URLs that name an IP directly; granted addresses still face the address rules |
| `AllowLoopback` | `bool` | `false` | Permit `127.0.0.0/8` and `::1` |
| `AllowPrivateIPs` | `bool` | `false` | Permit RFC1918 and IPv6 unique-local ranges |
| `AllowReservedIPs` | `bool` | `false` | Permit reserved ranges that are neither private nor publicly routable: CGNAT `100.64.0.0/10`, `0.0.0.0/8`, documentation and benchmarking ranges, `240.0.0.0/4`, IPv4-compatible/NAT64/6to4/Teredo IPv6 and more; the full list is `netsecurity.ReservedCIDRs`. Policy files set it as `allow_reserved_ips = true` |
| `AllowHosts` | `[]string` | `nil` | Host allowlist; when set, only these hosts may be contacted. Listed hosts are trusted: they may resolve to loopback, private and reserved addresses; `DeniedCIDRs` still applies to them, and a link-local answer still needs an `AllowedCIDRs` entry. Exact names match themselves; a leading dot (`.corp.example.com`) matches the domain and all subdomains |
| `DenyHosts` | `[]string` | `nil` | Host denylist; always wins, even over `AllowHosts`. Same syntax |
| `AllowedCIDRs` | `[]string` | `nil` | Address ranges permitted explicitly, overriding the built-in blocks (how you grant one slice of a LAN) |
| `DeniedCIDRs` | `[]string` | `nil` | Address ranges blocked explicitly; wins over everything, including `AllowedCIDRs` |
| `DNSServers` | `[]string` | `nil` | Resolve through these servers (`"1.1.1.1"` or `"8.8.8.8:53"`, plain DNS) instead of the host resolver; the same resolver then serves `scriptling.net.resolve` too |
| `AllowAll` | `bool` | `false` | Host-use only (not settable from policy files): disable every address and host check, leaving only the shared DNS resolver; the way to configure nameservers without imposing a policy |
| `ClientTimeout` | `time.Duration` | `0` | Optional end-to-end cap on each HTTP request (dial, TLS, redirects, reading the body) for the client the guard hands to script libraries. `0` enforces no cap: requests run as long as their own per-request timeout allows, which long-running calls such as LLM APIs need. Policy files set it as `client_timeout = "45s"` |

An invalid config (bad CIDR, malformed DNS server) fails `netsecurity.NewGuard` / `policyfile.LoadConfig` with an error: treat it as a startup failure. `netsecurity.FailClosed(err)` returns a guard that rejects every request if you need to keep serving after a config error.

### Process and System

| Import name | Package | Registration | Grants |
|-------------|---------|--------------|--------|
| `subprocess` | `extlibs/subprocess` | `subprocess.Register(p)` | Process execution |
| `sys` | `extlibs/sys` | `sys.Register(p, argv, stdin)` | Host information (platform, executable path), `argv`, the standard streams, `exit()`, and an `input()` builtin reading `stdin` when it is non-nil |
| `platform` | `extlibs/platform` | `platform.Register(p)` | Host information (host name, OS, architecture) |
| `logging` | `extlibs/logging` | `logging.Register(p, logger)` or `logging.RegisterDefault(p)` | Writes to your logger; `RegisterDefault` (or a nil logger) logs to stdout |
| `scriptling.secret` | `extlibs/secret` | `secret.Register(p, registry)` | Credentials from the `*secretprovider.Registry` you supply |

```go
import (
    "os"

    "github.com/paularlott/scriptling/extlibs/logging"
    "github.com/paularlott/scriptling/extlibs/secret"
    "github.com/paularlott/scriptling/extlibs/sys"
)

sys.Register(p, []string{"script.py"}, os.Stdin) // argv and stdin
logging.Register(p, myLogger)                   // or logging.RegisterDefault(p)
secret.Register(p, registry)                    // *secretprovider.Registry
```

`sys.NewLibrary(argv, stdin)` and `secret.NewLibrary(registry)` build the library without registering it.

#### Secret Providers

`scriptling.secret` reads from a `*secretprovider.Registry` (package `extlibs/secretprovider`). That package is only the core: the `Provider` interface, the alias `Registry`, provider `Config` blocks and a table of provider-type factories (`RegisterFactory`, `RegisteredTypes`). It holds no concrete provider, so it links no HTTP client. Either register your own `Provider` with `registry.Register(provider, alias, cacheTTL)`, or enable the built-in provider types you want and build providers from config:

| `provider =` | Package | Enable with | Construct directly |
|--------------|---------|-------------|--------------------|
| `"vault"` (HashiCorp Vault) | `extlibs/secretprovider/vault` | `vault.Register()` | `vault.New(cfg)` |
| `"onepassword"` (1Password Connect) | `extlibs/secretprovider/onepassword` | `onepassword.Register()` | `onepassword.New(cfg)` |

```go
import (
    "github.com/paularlott/scriptling/extlibs/secret"
    "github.com/paularlott/scriptling/extlibs/secretprovider"
    "github.com/paularlott/scriptling/extlibs/secretprovider/onepassword"
    "github.com/paularlott/scriptling/extlibs/secretprovider/vault"
)

if err := vault.Register(); err != nil { // provider = "vault"
    return err
}
if err := onepassword.Register(); err != nil { // provider = "onepassword" (Connect)
    return err
}

registry := secretprovider.NewRegistry()
if err := secretprovider.RegisterConfigs(registry, configs); err != nil { // []secretprovider.Config
    return err
}
secret.Register(p, registry)
```

Call each provider's `Register()` before `secretprovider.RegisterConfigs` or `secretprovider.NewProvider`; a config block whose type was not registered fails with an error naming the type. `Register()` is safe to call more than once. A `onepassword` block with `service_account_token` (a 1Password service account instead of Connect) also needs the `github.com/paularlott/scriptling-onepassword` extension linked in with a blank import; see [scriptling.secret](/reference/libraries/utilities/secret/).

### Runtime Libraries

The runtime family is three packages, so an application links only what it registers:

| Package | Go package name | Libraries | Links |
|---------|-----------------|-----------|-------|
| `extlibs/runtime` | `runtime` (alias it if you also import Go's `runtime`) | `scriptling.runtime` (background tasks, server lifecycle) and `.sync`, `.sandbox`, `.jsonrpc`, `.mcp`, `.plugin` | No KV store, no WebSocket server, no `net/http` |
| `extlibs/runtime/kv` | `kv` | `scriptling.runtime.kv` | The KV store; independent of the rest of the family |
| `extlibs/runtime/http` | `http` (alias it if you also import Go's `net/http`) | `scriptling.runtime.http` | The WebSocket server; imports the core package |

There is no register-everything call: register each library you want. The CLI registers them in this order (`scriptling.runtime.plugin` later, with the other libraries):

```go
import (
    scriptlingruntime "github.com/paularlott/scriptling/extlibs/runtime"
    rthttp "github.com/paularlott/scriptling/extlibs/runtime/http"
    "github.com/paularlott/scriptling/extlibs/runtime/kv"
)

allowedPaths := []string{"/srv/app/data"}

rthttp.Register(p, allowedPaths)                    // scriptling.runtime.http
kv.Register(p, allowedPaths)                        // scriptling.runtime.kv
scriptlingruntime.RegisterSync(p)                   // scriptling.runtime.sync
scriptlingruntime.RegisterSandbox(p, allowedPaths)  // scriptling.runtime.sandbox
scriptlingruntime.RegisterJSONRPC(p)                // scriptling.runtime.jsonrpc
scriptlingruntime.RegisterMCP(p)                    // scriptling.runtime.mcp
scriptlingruntime.Register(p)                       // scriptling.runtime (background tasks)
scriptlingruntime.RegisterPlugin(p)                 // scriptling.runtime.plugin
```

| Import name | Registration | Grants |
|-------------|--------------|--------|
| `scriptling.runtime` | `runtime.Register(p)` | Background tasks (concurrent execution) |
| `scriptling.runtime.http` | `http.Register(p, allowedPaths)` | Inbound: HTTP and WebSocket routes your server exposes; `static()` serves files within `allowedPaths` |
| `scriptling.runtime.kv` | `kv.Register(p, allowedPaths)` | In-memory stores; filesystem for persistent stores within `allowedPaths` |
| `scriptling.runtime.jsonrpc` | `runtime.RegisterJSONRPC(p)` | Inbound: JSON-RPC methods |
| `scriptling.runtime.mcp` | `runtime.RegisterMCP(p)` | Inbound: MCP tools, resources and prompts |
| `scriptling.runtime.sync` | `runtime.RegisterSync(p)` | None (shared concurrency primitives) |
| `scriptling.runtime.sandbox` | `runtime.RegisterSandbox(p, allowedPaths)` | Code execution in an isolated environment; `exec_file()` reads scripts within `allowedPaths` |
| `scriptling.runtime.plugin` | `runtime.RegisterPlugin(p)` | Inbound: serves this script as a plugin |

`allowedPaths` follows the [path policy](#path-policy): `nil` is unrestricted, `[]string{}` denies every path. Each sub-library registered with the same interpreter, before or after `runtime.Register`, is also reachable as an attribute of the parent, so `import scriptling.runtime as rt; rt.kv.open(...)` works when `scriptling.runtime.kv` is registered and `rt.kv` is absent when it is not.

For a `kv.default` store, call `kv.InitStore(path, logger)` before `kv.Register` (an empty path is memory-only; a nil logger keeps the default stderr logger) and `kv.CloseStore()` on shutdown. `kv.DefaultDB()` returns that store's `*snapshotkv.DB`, and `kv.StoreDB(obj)` returns the DB behind any store object a script hands back. Route registrations live in `http.State` (types `http.RouteInfo`, `http.WebSocketRouteInfo`, `http.WebSocketServerConn`), guarded by `runtime.RuntimeState`'s lock. Other exported names keep their meaning: `runtime.RuntimeState`, `runtime.ResetRuntime` (which also clears the routes and closes the KV stores), `runtime.SetSandboxFactory` and so on. Request-scoped context and the transport name live in `extlibs/reqctx` (`reqctx.SetTransport`, `reqctx.Transport`, `reqctx.WithRequestContext`).

### AI & Agent

```go
import (
    "github.com/paularlott/scriptling/extlibs/agent"
    "github.com/paularlott/scriptling/extlibs/ai"
    aimemory "github.com/paularlott/scriptling/extlibs/ai/memory"
    aitools "github.com/paularlott/scriptling/extlibs/ai/tools"
)

ai.Register(p)            // scriptling.ai (optional *netsecurity.Config)
agent.Register(p)         // scriptling.ai.agent (returns error)
agent.RegisterInteract(p) // scriptling.ai.agent.interact (returns error)
aimemory.Register(p)      // scriptling.ai.memory (optional logger)
aitools.Register(p)       // scriptling.ai.tools
```

| Import name | Package | Registration | Grants |
|-------------|---------|--------------|--------|
| `scriptling.ai` | `extlibs/ai` | `ai.Register(p, policy...)` | Network (LLM APIs and remote MCP servers) |
| `scriptling.ai.agent` | `extlibs/agent` | `agent.Register(p)` | Runs model-chosen tool calls with the libraries you have registered |
| `scriptling.ai.agent.interact` | `extlibs/agent` | `agent.RegisterInteract(p)` | Interactive terminal agent loop |
| `scriptling.ai.memory` | `extlibs/ai/memory` | `memory.Register(p, logger...)` | Memory stored in a `scriptling.runtime.kv` store |
| `scriptling.ai.tools` | `extlibs/ai/tools` | `tools.Register(p)` | None (tool schema builder) |

`agent.Register` and `agent.RegisterInteract` register script libraries and take a registrar with `RegisterScriptLibrary`, such as `*scriptling.Scriptling`.

### MCP Protocol & TOON

```go
import "github.com/paularlott/scriptling/extlibs/mcp"

mcp.Register(p)             // scriptling.mcp
mcp.RegisterToolHelpers(p)  // scriptling.mcp.tool
mcp.RegisterToon(p)         // scriptling.toon
```

| Import name | Registration | Grants |
|-------------|--------------|--------|
| `scriptling.mcp` | `mcp.Register(p, policy...)` or `mcp.RegisterConfigured(p, policy, allowProcesses)` | Network (HTTP MCP servers); process execution (stdio MCP servers) |
| `scriptling.mcp.tool` | `mcp.RegisterToolHelpers(p)` | None (helpers for writing MCP tools) |
| `scriptling.toon` | `mcp.RegisterToon(p)` | None (TOON encoding) |

`mcp.Register` allows stdio servers, which `mcp.Client()` starts as subprocesses. Hosts that disable subprocesses use `mcp.RegisterConfigured(p, policy, false)`, which refuses any target that is not an `http(s)` URL.

### Networking

| Import name | Package | Call |
|-------------|---------|------|
| `scriptling.net.resolve` | `extlibs/net/resolve` | `resolve.Register(p, resolver)` |
| `scriptling.net.multicast` | `extlibs/net/multicast` | `multicast.Register(p, policy...)` |
| `scriptling.net.unicast` | `extlibs/net/unicast` | `unicast.Register(p, policy...)` |
| `scriptling.net.gossip` | `extlibs/net/gossip` | `gossip.Register(p, logger, policy...)` |
| `scriptling.net.websocket` | `extlibs/net/websocket` | `websocket.Register(p, policy...)` |
| `scriptling.mercure` | `extlibs/mercure` | `mercure.Register(p, policy...)` or `mercure.RegisterConfigured(p, paths, policy, opts...)` |

```go
import (
    "github.com/paularlott/scriptling/extlibs/mercure"
    "github.com/paularlott/scriptling/extlibs/net/gossip"
    "github.com/paularlott/scriptling/extlibs/net/multicast"
    "github.com/paularlott/scriptling/extlibs/net/resolve"
    "github.com/paularlott/scriptling/extlibs/net/unicast"
    "github.com/paularlott/scriptling/extlibs/net/websocket"
)

resolve.Register(p, myResolver) // requires a resolve.Resolver implementation
multicast.Register(p)
unicast.Register(p)
gossip.Register(p, nil)         // nil = null logger
websocket.Register(p)
mercure.Register(p)
```

All of these grant network access; see [Network Policy](#network-policy).

### Messaging

```go
import (
    "github.com/paularlott/scriptling/extlibs/messaging/console"
    "github.com/paularlott/scriptling/extlibs/messaging/discord"
    "github.com/paularlott/scriptling/extlibs/messaging/slack"
    "github.com/paularlott/scriptling/extlibs/messaging/telegram"
)

console.Register(p)        // scriptling.messaging.console
telegram.Register(p, nil)  // scriptling.messaging.telegram (logger, optional *netsecurity.Config)
discord.Register(p, nil)   // scriptling.messaging.discord (logger, optional *netsecurity.Config)
slack.Register(p, nil)     // scriptling.messaging.slack (logger, optional *netsecurity.Config)
```

| Import name | Package | Call | Grants |
|-------------|---------|------|--------|
| `scriptling.messaging.console` | `extlibs/messaging/console` | `console.Register(p)` | Terminal input and output |
| `scriptling.messaging.telegram` | `extlibs/messaging/telegram` | `telegram.Register(p, logger, policy...)` | Network; inbound bot messages; local files for `send_file()` |
| `scriptling.messaging.discord` | `extlibs/messaging/discord` | `discord.Register(p, logger, policy...)` | Network; inbound bot messages; local files for `send_file()` |
| `scriptling.messaging.slack` | `extlibs/messaging/slack` | `slack.Register(p, logger, policy...)` | Network; inbound bot messages; local files for `send_file()` |

Each of `telegram`, `discord` and `slack` also has `RegisterConfigured(p, logger, allowedPaths, policy...)`, which confines the local files `send_file()` reads to `allowedPaths`; plain `Register` leaves them unconfined.

### Utilities

```go
import (
    "github.com/paularlott/scriptling/extlibs/console"
    "github.com/paularlott/scriptling/extlibs/container"
    "github.com/paularlott/scriptling/extlibs/markdown"
    "github.com/paularlott/scriptling/extlibs/nomad"
    "github.com/paularlott/scriptling/extlibs/oauth"
    "github.com/paularlott/scriptling/extlibs/platform"
    "github.com/paularlott/scriptling/extlibs/similarity"
    "github.com/paularlott/scriptling/extlibs/template"
    "github.com/paularlott/scriptling/extlibs/toml"
    "github.com/paularlott/scriptling/extlibs/yaml"
)

yaml.Register(p)              // yaml
toml.Register(p)              // toml
template.RegisterHTML(p)      // scriptling.template.html
template.RegisterText(p)      // scriptling.template.text
markdown.Register(p)          // scriptling.markdown
similarity.Register(p)        // scriptling.similarity
platform.Register(p)          // platform
console.Register(p)           // scriptling.console
container.Register(p, "", "") // scriptling.container (empty = default sockets)
nomad.Register(p)             // scriptling.nomad (optional *netsecurity.Config)
oauth.Register(p)             // scriptling.oauth (optional *netsecurity.Config)
```

| Import name | Package | Call | Grants |
|-------------|---------|------|--------|
| `yaml` | `extlibs/yaml` | `yaml.Register(p)` | None (YAML parser, 296 KB) |
| `toml` | `extlibs/toml` | `toml.Register(p)` | None (TOML parser, 197 KB) |
| `scriptling.template.html` | `extlibs/template` | `template.RegisterHTML(p)` | None (Go template engine, 1.4 MB with `.text`) |
| `scriptling.template.text` | `extlibs/template` | `template.RegisterText(p)` | None (Go template engine) |
| `scriptling.markdown` | `extlibs/markdown` | `markdown.Register(p)` | None (Markdown renderer) |
| `scriptling.similarity` | `extlibs/similarity` | `similarity.Register(p)` | None |
| `platform` | `extlibs/platform` | `platform.Register(p)` | Host information (host name, OS, architecture) |
| `scriptling.console` | `extlibs/console` | `console.Register(p)` | Terminal user interface |
| `scriptling.container` | `extlibs/container` | `container.Register(p, dockerSock, podmanSock)`, `container.RegisterConfigured(p, dockerSock, podmanSock, paths, policy)` or `container.RegisterWithOptions(p, opts)` | Control of Docker, Podman or Apple containers on the host |
| `scriptling.nomad` | `extlibs/nomad` | `nomad.Register(p, policy...)` | Network; control of a Nomad cluster |
| `scriptling.oauth` | `extlibs/oauth` | `oauth.Register(p, policy...)` or `oauth.RegisterConfigured(p, paths, policy)` | Network |

`container.Options` adds `Paths` (the filesystem jail for sockets and volumes), `Policy` (network policy for script-supplied endpoints; also refuses `network="host"`), `AppleCLI` and `DenyPrivileged` (refuses `run(privileged=True)`).

The provisioning libraries, `scriptling.provision.file`, `.fetch`, `.command` and `.package`, are covered in the next section.

### Provisioning

| Import name | Package | Call | Grants |
|-------------|---------|------|--------|
| `scriptling.provision.file` | `extlibs/provision/file` | `file.Register(p)` or `file.RegisterConfigured(p, paths, opts...)` | Filesystem write |
| `scriptling.provision.fetch` | `extlibs/provision/fetch` | `fetch.Register(p)` or `fetch.RegisterConfigured(p, paths, guard, opts...)` | Network; filesystem write |
| `scriptling.provision.command` | `extlibs/provision/command` | `command.Register(p)` or `command.RegisterConfigured(p, opts...)` | Process execution |
| `scriptling.provision.package` | `extlibs/provision/packages` | `packages.Register(p)` or `packages.RegisterConfigured(p, opts...)` | Process execution (system package manager) |

### Provisioning as Root

The provisioning libraries run `become=True` steps as root only when you give them a `become.Become`. Without one, such a step fails with a `PermissionError` (unless the process already runs as root). The first root step starts your own program again through `sudo` as a helper, so your program must serve it: call `become.ServeIfHelper()` first thing in `main`.

```go
import "github.com/paularlott/scriptling/extlibs/provision/become"

func main() {
    become.ServeIfHelper() // started as the root helper: serve it and exit

    // ...
    b := become.New(become.Config{Paths: paths}) // the same allowed paths as the libraries
    defer b.Close()

    file.RegisterConfigured(p, paths, file.WithBecome(b))
    fetch.RegisterConfigured(p, paths, guard, fetch.WithBecome(b))
    command.RegisterConfigured(p, command.WithBecome(b))
    packages.RegisterConfigured(p, packages.WithBecome(b))
}
```

`become.Config` also takes `Command`, the helper's command line (default: this program with `become.HelperArg`), and `Sudo` (default `sudo`; `doas` works too). One helper serves every interpreter that shares the `Become`.

### Executable Plugins

`scriptling.plugin` (the control library for executable plugins, listing/calling/loading them at runtime) lives in the top-level `plugin` package, not under `extlibs`, and needs a `*plugin.Manager` rather than just the interpreter:

```go
import (
    "github.com/paularlott/scriptling/plugin"
)

manager := plugin.NewManager(myLogger, func(name string, err error) {
    myLogger.Error("plugin process exited", "plugin", name, "error", err)
})
manager.AddDir("./plugins")
if err := manager.Load(ctx); err != nil {
    // handle error
}

plugin.RegisterLibraries(p, manager)  // scriptling.plugin, plus plugin.<name> for each loaded executable
```

| Import name | Package | Call |
|-------------|---------|------|
| `scriptling.plugin` | `plugin` | `plugin.RegisterLibraries(p, manager, policy...)` or `plugin.RegisterLibrariesConfigured(p, manager, policy, allowProcesses)` |

A plugin whose name the interpreter already has, a registered library or a module its library loader supplies, is skipped with a manager warning rather than shadowing it, so set the library loader before calling `plugin.RegisterLibraries`. `plugin.RegisterLibrariesConfigured` with `allowProcesses` false refuses script-driven `load()` of an executable while HTTP(S) plugins still load; `plugin.ProcessesAllowed(disabledLibs)` derives the flag from your disabled-library list, as the CLI's `--no-subprocess` does.

See [Plugin Manager](/docs/plugins/host-integration/) for the full plugin embedding guide.

## Migrating from v0.39

v0.40.0 removed the single `extlibs` package. There is no compatibility layer; replace each old name with the new one.

| Old | New |
|-----|-----|
| `extlibs.RegisterCsvLibrary`, `RegisterXmlLibrary`, `RegisterHTMLParserLibrary`, `RegisterShlexLibrary`, `RegisterSecretsLibrary` | `stdlib.RegisterAll(p)`, or `p.RegisterLibrary(stdlib.CSVLibrary)` and so on |
| `platform` from `stdlib.RegisterAll` | `platform.Register(p)` (`extlibs/platform`) |
| `extlibs.RegisterYAMLLibrary`, `RegisterTOMLLibrary`, `RegisterMarkdownLibrary` | `yaml.Register`, `toml.Register`, `markdown.Register` |
| `extlibs.RegisterTemplateHTMLLibrary`, `RegisterTemplateTextLibrary` | `template.RegisterHTML`, `template.RegisterText` |
| `extlibs.RegisterOSLibrary(p, paths)` and the other filesystem `Register…Library` calls | `filesystem.RegisterOS(p, paths)`, `filesystem.RegisterPathlib`, … or `filesystem.RegisterAll(p, paths)` |
| `extlibs.RegisterRequestsLibrary`, `RegisterRequestsLibraryConfigured`, `SetRequestsMaxParallelLimit` | `requests.Register`, `requests.RegisterConfigured`, `requests.SetRequestsMaxParallelLimit` |
| `extlibs.RegisterWebSocketLibrary` | `websocket.Register` (`extlibs/net/websocket`) |
| `extlibs.RegisterWaitForLibrary`, `RegisterWaitForLibraryConfigured` | `waitfor.Register`, `waitfor.RegisterConfigured` |
| `extlibs.RegisterSubprocessLibrary`, `RegisterSysLibrary`, `NewSysLibrary` | `subprocess.Register`, `sys.Register`, `sys.NewLibrary` |
| `extlibs.RegisterLoggingLibrary`, `RegisterLoggingLibraryDefault` | `logging.Register`, `logging.RegisterDefault` |
| `extlibs.RegisterSecretLibrary`, `NewSecretLibrary` | `secret.Register`, `secret.NewLibrary` |
| `extlibs.RegisterRuntimeLibrary` | `runtime.Register` (`extlibs/runtime`) |
| `extlibs.RegisterRuntime{JSONRPC,MCP,Sync,Plugin}Library`, `RegisterRuntimeSandboxLibrary(p, paths)` | `runtime.Register{JSONRPC,MCP,Sync,Plugin}`, `runtime.RegisterSandbox(p, paths)` |
| `extlibs.RegisterRuntimeLibraryAll(p, paths)` | One call per library: `http.Register(p, paths)`, `kv.Register(p, paths)`, `runtime.RegisterSync`, `runtime.RegisterSandbox(p, paths)`, `runtime.RegisterJSONRPC`, `runtime.RegisterMCP`, `runtime.Register` |
| `extlibs.RegisterRuntimeKVLibrary`, `RegisterRuntimeKVLibraryWithSecurity(p, paths)`, `NewKVSubLibrary`, `NewKVSubLibraryWithSecurity` | `kv.Register(p, paths)` (`extlibs/runtime/kv`); pass `nil` for unrestricted |
| `extlibs.InitKVStore`, `CloseKVStore`, `KVStoreDB`, `RuntimeState.KVDB` | `kv.InitStore`, `kv.CloseStore`, `kv.StoreDB`, `kv.DefaultDB()` |
| `extlibs.RegisterRuntimeHTTPLibrary`, `HTTPSubLibrary`, `NewHTTPSubLibrary(paths)` | `http.Register(p, paths)` (`extlibs/runtime/http`); pass `nil` for unrestricted |
| `extlibs.RouteInfo`, `WebSocketRouteInfo`, `WebSocketServerConn`; `RuntimeState.Routes`, `.WebSocketRoutes`, `.WebSocketConnections` | The same types in `extlibs/runtime/http`; `http.State.Routes` and so on, under `runtime.RuntimeState`'s lock |
| `extlibs.SetSandboxFactory`, `extlibs.RuntimeState` and the other runtime names | The same names in `extlibs/runtime` |
| `extlibs.RuntimeState.Transport` | `reqctx.SetTransport`, `reqctx.Transport` (`extlibs/reqctx`) |
| `secretprovider.NewVaultProvider(cfg)` | `vault.Register()`, or `vault.New(cfg)` (`extlibs/secretprovider/vault`) |
| `secretprovider.NewOnePasswordProvider(cfg)` | `onepassword.Register()`, or `onepassword.New(cfg)` (`extlibs/secretprovider/onepassword`) |
| `netsecurity.LoadConfig(path)` | `policyfile.LoadConfig(path)` (`extlibs/netsecurity/policyfile`) |
| `extlibs.XLibraryName` constants | Each package's own constant: `yaml.LibraryName`, `filesystem.OSLibraryName`, `kv.LibraryName`, `http.LibraryName`, `runtime.RuntimeSyncLibraryName`, … |

## Security Considerations

When embedding Scriptling, you have full control over what scripts can access. The standard libraries are safe to expose to untrusted scripts under the interpreter's resource limits; every extension library is a capability you grant. See the [Security Guide](../../security/) for best practices.

**Never register these libraries when running untrusted code:**

- `subprocess`: allows arbitrary command execution
- `sys`: exposes host details and process control (`exit`)
- `scriptling.container`: controls Docker/Podman containers on the host
- `scriptling.nomad`: grants full control over a Nomad cluster (CSI volumes, jobs)
- `scriptling.runtime.sandbox`: can execute arbitrary code
- `scriptling.ai.agent`: can execute AI-generated code with tools
- `scriptling.provision.command` and `scriptling.provision.package`: run commands, possibly as root

Register filesystem and network libraries for untrusted code only with a [path policy](#path-policy) and a [network policy](#network-policy). Even `platform` reveals the host name, which is why it is an extension rather than a standard library.

## See Also

- [Basics](../basics/): creating interpreters and exchanging variables
- [Security Guide](../../security/): security best practices for embedding
- [Libraries](../../../reference/libraries/): usage reference for all libraries

## Database Drivers in Embedded Hosts

Scriptling is the library; your application is the host, and the database drivers are optional at every level: you may compile them in, load them as external plugin binaries, or have neither. One call covers all three cases:

```go
import scriptlingplugin "github.com/paularlott/scriptling/plugin"

// On every interpreter your host spins up: main instances, HTTP request
// environments, MCP sessions, sandbox/background factories:
scriptlingplugin.RegisterLibraries(p, pluginManager, scriptlingplugin.PolicyFromSecurity(netPolicy, allowedPaths))
```

- **Compiled in** (build tags `plugin_sqlite` / `plugin_sql` / `plugin_valkey` / `plugin_badgerdb`, or import the plugin packages and call `sqlite.RegisterInProcess(p, policy)`): registers regardless of the manager; a nil `pluginManager` is fine.
- **External plugin binaries**: pass your `*plugin.Manager` (see [Plugin Manager](../../plugins/host-integration/)) and the proxy libraries register per instance.
- **Neither**: nothing registers; scripts importing `scriptling.sqlite` fail with a named `unknown library` error.

The CLI is exactly this pattern: its `--plugin-dir` handling, exe-relative discovery and per-mode wiring are host choices, not library behaviour. Inside handler scripts, open a connection per run and let the environment's teardown collect it (`Connection` closes itself when instances are collected; explicit `conn.close()` is still good manners).
