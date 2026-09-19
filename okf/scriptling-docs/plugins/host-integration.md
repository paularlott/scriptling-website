---
description: Enable plugins in Go applications embedding Scriptling.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/plugins/host-integration/
sources:
    - resource: https://scriptling.dev/docs/plugins/host-integration/
status: stable
tags:
    - plugins
    - go
    - embedding
title: Plugin Manager
type: Guide
---
# Plugin Manager

Applications that embed Scriptling own a plugin manager. Load plugins once, then register plugin libraries with every Scriptling environment you create.

```go
package main

import (
    "context"
    "log"

    logslog "github.com/paularlott/logger/slog"

    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/plugin"
)

func main() {
    ctx := context.Background()

    appLogger := logslog.New(logslog.Config{
        Level:  "info",
        Format: "console",
    })

    manager := plugin.NewManager(appLogger, func(name string, err error) {
        log.Println("plugin crashed:", name, err)
        // Decide whether to terminate, restart, or mark this host unhealthy.
    })
    manager.AddDir("./plugins")
    if err := manager.Load(ctx); err != nil {
        log.Fatal(err)
    }
    defer manager.Close()

    for _, warning := range manager.Warnings() {
        log.Println("plugin warning:", warning)
    }

    p := scriptling.New()
    plugin.RegisterLibraries(p, manager)

    _, err := p.Eval(`
import plugin.hello
print(plugin.hello.greet("Ada"))
`)
    if err != nil {
        log.Fatal(err)
    }
}
```

## Multiple Environments

The manager starts each plugin executable once. Multiple Scriptling environments can share the same manager. Each environment must still be evaluated by only one Go thread at a time. The stdio JSON-RPC connection multiplexes overlapping calls by request id; connection pooling is intentionally not used because it would create multiple plugin process instances and violate the singleton plugin model:

```go
p1 := scriptling.New()
plugin.RegisterLibraries(p1, manager)

p2 := scriptling.New()
plugin.RegisterLibraries(p2, manager)
```

## Manager Scoping

For applications where each request or execution should have its own isolated set of plugins: without affecting other requests or the global manager: use `NewScope`. A scope is a lightweight child manager that inherits the parent's logger and connection pools but keeps its own plugin registry.

```go
// Application start-up: create a long-lived parent manager.
manager := plugin.NewManager(appLogger)
manager.AddDir("./plugins")
manager.Load(ctx)
defer manager.Close()

// Per-request execution: create an isolated scope and close it on exit.
// The scope inherits the parent's pooled HTTP transports so TLS connections
// to plugin endpoints are reused across requests.
scope := manager.NewScope()
defer scope.Close()

env := scriptling.New()
plugin.RegisterLibraries(env, scope)

// Scripts can now use scriptling.plugin.load() to register additional plugins
// that only exist for the lifetime of this scope.
```

### Restricting Transport Type

Pass `plugin.WithTransport` to control which plugin transports a scope permits. This is useful in security-sensitive contexts such as server-side script execution, where you want to allow HTTP(S) plugin endpoints but prevent scripts from launching arbitrary local executables.

```go
// HTTP/HTTPS only: scriptling.plugin.load() will refuse stdio executables.
scope := manager.NewScope(plugin.WithTransport(plugin.TransportHTTP))

// Stdio only: scriptling.plugin.load() will refuse http(s) URLs.
scope := manager.NewScope(plugin.WithTransport(plugin.TransportStdio))

// Default: both types permitted (same as not passing any option).
scope := manager.NewScope(plugin.WithTransport(plugin.TransportAll))

// Neither: scriptling.plugin.load() and .unload() both always fail.
scope := manager.NewScope(plugin.WithTransport(plugin.TransportNone))
```

A scope created with no `WithTransport` option at all inherits its parent's
transport mode rather than defaulting to `TransportAll` — see
[Nested Scopes](#nested-scopes) below. An explicit `WithTransport` on the
child always overrides whatever the parent has, in either direction: a
child of a `TransportNone` parent may reopen `TransportHTTP`, and a child of
a `TransportAll` parent may narrow to `TransportNone`.

### Restricting Which Paths Scripts May Load Executables From

`WithExecPaths` restricts *new* stdio/exec loads a scope may perform to a
set of allowed directories, independently of transport mode. This is the
exec-side counterpart to `WithHTTPTransport` below: it doesn't change
whether stdio loading is permitted at all (that's still `WithTransport`),
only which paths a permitted stdio load may spawn from.

This matters because a host application's own boot-time preloading and a
script's later dynamic loading are different trust levels. During startup,
the host itself may load plugins from anywhere on the filesystem it has
access to — there's no script involved, so there's nothing to restrict.
Later, if the host wants to let scripts load *additional* plugins
dynamically, it may still want to confine those loads to a known-safe
directory rather than anywhere the process can reach.

```go
// Startup: the host loads from wherever it trusts, unrestricted — this
// manager has no exec-path restriction at all.
manager := plugin.NewManager(appLogger)
manager.LoadPlugin(ctx, "/opt/vendor/widgets/widget", nil)
defer manager.Close()

// Script-facing scope: stdio loading is permitted (TransportAll, the
// default), but only from this one directory. The startup-preloaded
// plugin above stays fully usable regardless — WithExecPaths only gates
// where a *new* load may spawn its executable from.
scope := manager.NewScope(
    plugin.WithExecPaths(&fssecurity.Config{AllowedPaths: []string{"/etc/myapp/scoped-plugins"}}),
)
defer scope.Close()

p := scriptling.New()
plugin.RegisterLibraries(p, scope)
p.Eval(`
import scriptling.plugin as plugin
plugin.call_function("widgets", "build", ["chair"])                       # preloaded, always works
plugin.load("extra", "/etc/myapp/scoped-plugins/extra")                   # allowed: inside the allowlist
plugin.load("evil", "/usr/bin/whoami")                                    # error: not in the allowed paths
`)
```

An `fssecurity.Config` with a `nil` `AllowedPaths` is unrestricted (the
default when `WithExecPaths` isn't used at all); an explicit empty slice
denies every stdio load. `WithExecPaths` combines freely with
`WithHTTPTransport` on the same scope — one governs which executables may
be spawned, the other which HTTP(S) endpoints may be dialed, and neither
affects the other.

Like transport mode, `execPaths` is inherited by a child scope created with
no explicit `WithExecPaths` option, and an explicit option on the child
always overrides the inherited value.

### Exposing Admin-Trusted Plugins Without Letting Scripts Load Their Own

A host that pre-loads specific plugins and wants scripts to use them — but
never to load a *different* plugin the host didn't choose — should register
`scriptling.plugin` against a `TransportNone` scope. `list`, `describe`,
`call_function`, `batch_call`, and `call_method` all keep working against
whatever the parent manager already loaded (scopes chain to their parent for
lookups, as above); `load` and `unload` return an error unconditionally.
This is the safe way to hand scripts a plugin control library at all —
registering `scriptling.plugin` against an unrestricted manager gives any
script `load(name, path)`, and `path` is *script-supplied*: for a filesystem
path that's an arbitrary local executable, for an `http(s)://` URL that's an
arbitrary outbound fetch, neither checked against anything. `TransportNone`
is what makes "plugins are admin-supplied and therefore trusted" actually
true, rather than true only until the first script calls `load`.

```go
// Startup: admin loads whatever this host trusts, on an unrestricted
// manager — a directory of stdio executables and/or specific plugins by
// path or URL, exactly like the CLI's --plugin-dir and --plugin.
manager := plugin.NewManager(appLogger)
manager.AddDir("/etc/myapp/plugins")           // stdio executables in this dir
manager.Load(ctx)
manager.LoadPlugin(ctx, "/opt/widgets/widget", nil)              // one specific executable
manager.LoadURL(ctx, "billing", "https://billing.internal/rpc", false, false) // one specific https endpoint
defer manager.Close()

// Every script environment gets a TransportNone scope: full use of every
// plugin loaded above, however it was loaded, no ability to load or unload
// anything new.
scope := manager.NewScope(plugin.WithTransport(plugin.TransportNone))
defer scope.Close()

p := scriptling.New()
plugin.RegisterLibraries(p, scope)
p.Eval(`
import scriptling.plugin as plugin
print(plugin.list())          # shows the admin-loaded plugins
plugin.call_function("widgets", "build", ["chair"])  # works
plugin.load("evil", "/bin/sh")  # error: plugin loading is disabled in this scope
`)
```

If a plugin registered a generated script proxy (a `scriptling=True`
handshake peer whose schema declares script-language sources for its
functions/classes), that proxy's own source does `import scriptling.plugin`
internally — so registering only the individual client library via
`plugin.RegisterClientLibrary` (skipping the control library entirely) is
*not* a substitute for this pattern unless every loaded plugin is a plain
`scriptling=False` JSON-RPC peer. `TransportNone` works uniformly for both.

### Allowing Scripts to Load New Plugins Only Over a Policy-Enforced Transport

`WithHTTPTransport` overrides the `http.RoundTripper` a scope uses for every
HTTP(S) plugin call — the `LoadURL` handshake and every later
`call_function`/`batch_call`/`call_method` RPC alike, since both draw from
the same pooled transport. Combine it with `TransportHTTP` to let scripts
load *new* plugins, but only over a transport you control — for example one
that enforces a network allow/deny list, so a script can't use
`scriptling.plugin.load()` as a way around restrictions you've placed on
`requests` or other network-facing libraries.

Pass the guard's own `HTTPClient().Transport`, not a bare dial-level
transport: `HTTPClient()` wraps every request in `CheckURL` (scheme, host
allow/deny lists, IP-literal handling) *and* validates every dialed address,
which is the same two-layer enforcement `requests`/`scriptling.ai`/
`scriptling.mcp` get. A dial-only transport alone would silently skip the
allow_hosts/deny_hosts checks — connections to plain public hosts would go
through unchecked, and only the loopback/private/link-local categories
would still be caught at dial time.

This combines with startup preloading exactly the same way `TransportNone`
does above — the parent manager can still `AddDir`/`Load`/`LoadPlugin`/
`LoadURL` whatever it trusts before the scope is ever created, and every one
of those stays fully usable through the scope regardless of the scope's own
transport mode; the mode only governs *new* loads scripts attempt through
the scope itself:

```go
manager := plugin.NewManager(appLogger)
manager.LoadPlugin(ctx, "/opt/widgets/widget", nil) // trusted, preloaded at startup
defer manager.Close()

guard, err := netsecurity.NewGuard(myNetworkPolicy) // *netsecurity.Config
if err != nil {
    log.Fatal(err)
}

scope := manager.NewScope(
    plugin.WithTransport(plugin.TransportHTTP),
    plugin.WithHTTPTransport(guard.HTTPClient().Transport),
)
defer scope.Close()

p := scriptling.New()
plugin.RegisterLibraries(p, scope)
p.Eval(`
import scriptling.plugin as plugin
plugin.call_function("widgets", "build", ["chair"])         # the startup-preloaded plugin, always available
plugin.load("remote", "https://plugins.example.com/rpc")   # a *new* load — allowed if the policy allows this host
plugin.load("evil", "http://169.254.169.254/")              # fails: blocked by the policy's own checks
plugin.load("evil", "/usr/bin/whoami")                       # fails: stdio still isn't permitted, preloaded or not
`)
```

The same transport governs a request regardless of `insecure_skip_tls`: a
script asking to skip TLS verification still goes through the transport you
supplied, not the manager's own separate skip-verify transport. This is a
one-way ratchet — `WithHTTPTransport` can only make a scope's HTTP plugin
traffic more constrained than the default, never less.

### Visibility and Name Isolation

`scope.Get` and `scope.List` chain to the parent: a scope sees its own plugins plus all ancestor plugins. A child scope may only add plugin names that do not already exist anywhere in the ancestry chain: attempting to load a name that a parent already owns returns an error. This prevents name collisions and the subtle env-binding bugs that shadow-then-overwrite would cause.

Loading the exact same endpoint under the same name is idempotent: `LoadPath` and `LoadURL` return the ancestor's client unchanged without creating a new connection.

```go
// Parent has plugin.tools loaded at startup.
// Scope can see plugin.tools via the parent chain but cannot load a competing
// endpoint under the same name: that would return an error.
scope := manager.NewScope()

// Loading the exact same URL is idempotent and returns parent's client:
client, _ := scope.LoadURL(ctx, "tools", "https://plugins.example.com/rpc", true, false)
// client == parentClient (same pointer)

// scope.Get("tools") → parent's client (via chain)
// manager.Get("tools") → parent's client (unchanged)
```

`scope.Unload(name)` only removes scope-local plugins. Attempting to unload a plugin that lives in the parent returns an error, which prevents accidental removal of shared resources from within an isolated request.

### Connection Pooling Across Scopes

The parent manager holds two shared `*http.Transport` instances (one TLS-verified, one skip-verify). `NewScope` inherits the same transport pointers, so all scopes derived from the same manager share a single HTTP/2 connection pool per endpoint. Connections established in one request are reused in the next, even though each request uses its own scope and its own Scriptling environment.

When a scope is closed, its `http.Client` instances are dropped, but the connections remain warm inside the shared transport's pool. The parent's `Close` tears down the transports.

### Nested Scopes

Scopes can themselves be scoped. The same rules apply at every level: lookup chains to the immediate parent, close affects only the local level, and all levels share the root manager's transports.

A child scope created with no options inherits its parent's transport mode
and `execPaths` — it is never more permissive than its parent by default.
An explicit `WithTransport`/`WithExecPaths` on the child overrides the
inherited value for that scope (and everything scoped from it, unless they
override it again).

```go
tenantScope := manager.NewScope(plugin.WithTransport(plugin.TransportHTTP))
defer tenantScope.Close()
// Load tenant-specific plugins into tenantScope…

requestScope := tenantScope.NewScope()
defer requestScope.Close()
// requestScope has no explicit WithTransport, so it inherits tenantScope's
// TransportHTTP — stdio loading stays refused, it does not silently widen
// to TransportAll.
// requestScope sees its own plugins + tenantScope's + manager's.
// requestScope.Close() leaves tenantScope fully intact.
```

### Plugin Logs

Pass a logger to `plugin.NewManager(appLogger, crashHandler)` to install the manager-lifetime host logger used for records emitted by Go plugins through `plugin.Logger(ctx)`. Pass the same `github.com/paularlott/logger.Logger` your application already uses; the example above uses `github.com/paularlott/logger/slog` so plugin logs are visible during development. `manager.SetLogger()` is also available for late wiring. If no logger is configured, plugin log records are acknowledged and dropped.

## Crash Handling

Pass a crash handler to `plugin.NewManager(appLogger, crashHandler)` to handle plugin processes that exit unexpectedly after loading. `manager.SetCrashHandler()` is also available for late wiring. Long-running applications can log the failure, terminate, restart the process, or mark themselves unhealthy.

```go
manager.SetCrashHandler(func(name string, err error) {
    log.Println("plugin crashed:", name, err)
})
```

`manager.Health()` is still available for polling or health endpoints. It returns a map of unhealthy plugin library names to errors and is empty when all loaded plugins are healthy.

## Server Applications

For long-running servers, create the manager during application startup and close it during shutdown. Register plugin libraries in every request environment.

Scriptling's CLI server mode does this for `--plugin-dir` automatically.

## Loading JSON-RPC Peers on Demand

`Manager.LoadPath` spawns a single executable at runtime without scanning a
directory. `Manager.LoadURL` connects to an HTTP(S) JSON-RPC endpoint.
`Manager.Unload` closes one and removes it. These are safe to call while the
manager is also serving `--plugin-dir` plugins.

```go
// Plugin protocol peer (scriptling.handshake + function.call etc.)
client, err := manager.LoadPath(ctx, "widgets", "/opt/widgets/widget", true, nil)
if err != nil { log.Fatal(err) }
defer manager.Unload("widgets")

// Typed plugin call: ints stay ints, etc.
result, err := client.CallFunction(ctx, "build",
    []plugin.Value{{Type: "string", Value: "chair"}}, nil)

// Pass command-line arguments, e.g. loading scriptling itself in raw JSON-RPC mode.
client, err = manager.LoadPath(ctx, "rpc", "scriptling", false,
    []string{"--json-rpc", "./setup.py"})
if err != nil { log.Fatal(err) }
defer manager.Unload("rpc")

// HTTP JSON-RPC endpoint. The last argument skips TLS verification for
// local/self-signed HTTPS servers.
client, err = manager.LoadURL(ctx, "remote", "https://127.0.0.1:8443/json-rpc", false, true)
if err != nil { log.Fatal(err) }
defer manager.Unload("remote")
```

HTTP plugin transport is request/response only. It supports calls, objects, and
batches, but the server cannot initiate callbacks back to the client. Use stdio
plugins when host callbacks or `plugin.Logger(ctx)` are required.

`LoadPath` is idempotent on absolute path + name; `LoadURL` is idempotent on
URL + name. A second call with the same peer and name returns the existing
client. Loading an already-loaded peer under a different name, or loading a new
peer under a name already in use, returns an error.

The CLI always constructs a manager (even without `--plugin-dir`) so that
`scriptling.plugin.load` / `unload` / `call` are available to scripts in run,
server, and `--json-rpc` modes. Constructing a manager starts no processes; it
only becomes expensive when directories are scanned or executables launched, so
the CLI skips that work for `--lint`, `--list-libs` and the package
subcommands. Embedded applications get the same behaviour as long as they
construct a manager and call `plugin.RegisterLibraries` on each environment.

## Fetcher Plugins

Plugins that own a URI scheme (see [plugin fetchers](https://scriptling.dev/okf/scriptling-docs/plugins/fetchers.md))
serve scripts and libraries on demand. A host opts in by bridging its manager
into a package scheme registry with `pluginpack`. After that, `knot://libs`
resolves like any other package source and `knot://scripts/hello` can be
fetched and run.

```go
import (
    "github.com/paularlott/scriptling/scriptling-cli/bootstrap"
    "github.com/paularlott/scriptling/scriptling-cli/pack"
    "github.com/paularlott/scriptling/scriptling-cli/pluginpack"
)

// After manager.Load(ctx), and before opening any scheme:// source.
bridge := pluginpack.New(pluginpack.Options{
    Manager: manager,
    Context: ctx,      // cancelling this aborts in-flight fetches
})
if err := bridge.Register(); err != nil {
    log.Fatal(err)
}
defer bridge.Close() // releases the schemes this bridge claimed

// The library bundle of every fetcher plugin, for automatic attachment.
bundles, err := bridge.Bundles()
if err != nil {
    log.Fatal(err)
}

loader := pack.NewLoader()
for _, b := range bundles {
    if err := loader.AddBundle(b); err != nil {
        log.Fatal(err)
    }
}

p := scriptling.New()
stdlib.RegisterAll(p)
plugin.RegisterLibraries(p, manager)
bootstrap.ApplyPackLoader(p, loader)

// Modules now import straight out of the plugin.
p.EvalWithContext(ctx, "import mylib")
```

`Register` must run before any scheme source is opened, because it is what
makes the scheme resolvable. A partial failure (two plugins claiming one
scheme) rolls back, so the bridge is left owning nothing.

A source whose scheme no loaded plugin serves fails with an error wrapping
`pack.ErrUnknownScheme`, so a host can tell "the plugin was never loaded" apart
from any other failure and add advice that fits its own configuration:

```go
if errors.Is(err, pack.ErrUnknownScheme) {
    return fmt.Errorf("%w; add it to plugins.d and restart", err)
}
```

The library message ends with "load the plugin that serves it" for exactly this
reason: it stays true whether plugins arrive from a CLI flag, a config file, or
a desktop integration. The CLI extends the same sentence with
`with --plugin or --plugin-dir`.

To run a script that lives in the plugin, fetch it as source text. Scripts are
never cached and never staged to a file:

```go
source, err := bridge.FetchScript(ctx, "knot://scripts/hello")
if err != nil {
    log.Fatal(err)
}
p.SetSourceFile("knot://scripts/hello")
p.EvalWithContext(ctx, string(source))
```

Server hosts pass the same bytes through `ServerConfig.ScriptSource` (with
`ScriptName` for error messages) instead of `ScriptFile`.

### Reloading Plugins

`Close` releases the schemes the bridge registered, which is what makes runtime
plugin reloads possible: close the old bridge, load the new plugins, register a
new bridge over them. Bundles opened through a closed bridge stop working.

```go
bridge.Close()
manager.Close()

manager = plugin.NewManager(appLogger, crashHandler)
manager.AddDir("./plugins")
manager.Load(ctx)

bridge = pluginpack.New(pluginpack.Options{Manager: manager, Context: ctx})
bridge.Register()
```

### Isolated Scheme Registries

By default a bridge registers into the process-wide registry, so one scheme has
one owner per process. Multi-tenant hosts that need independent routing tables
pass their own:

```go
registry := pack.NewSchemeRegistry()
bridge := pluginpack.New(pluginpack.Options{
    Manager:  manager,
    Context:  ctx,
    Registry: registry,
})
bridge.Register()

// Resolve through the private registry rather than pack.FetchBundle.
b, err := registry.FetchBundle("knot://libs", false, cacheDir)
```

Two tenants can then each own a `knot` scheme pointing at different plugins.

### Caching and Freshness

Plugin-served content is not cached, not on disk and not in memory between
reads. See [caching](https://scriptling.dev/okf/scriptling-docs/plugins/fetchers.md#caching): the compile is already
cached upstream by source text, and the plugin is the only side that knows its
backend's freshness rules, so any persistence belongs behind its own `Read`.

Directory listings are reused for `Options.DirTTL` (30 seconds by default),
because resolving a path consults its parent's listing and walking an app bundle
would otherwise re-list a directory per entry. Set a negative `DirTTL` to fetch
every listing fresh.

A complete runnable host lives at `examples/embed-fetcher-plugin` in the
repository.
