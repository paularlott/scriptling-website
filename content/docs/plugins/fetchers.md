---
title: Plugin Fetchers
description: Serve scheme sources such as knot:// or demo:// from a plugin, on demand.
tags: [plugins]
weight: 4
---

A fetcher is a plugin that owns a URI scheme. The whole contract is one
registration call, `RegisterFetcher("knot", fetcher)`, and from that the
host knows everything it needs: `knot://` sources route to this plugin, its
library attaches automatically when it loads, and files are asked for only
when an import actually resolves. Nothing is transferred that nothing
imports.

There is no manifest and no declaration. One plugin serves one scheme, with
the standard layout hardcoded: modules live under `lib/`, and a bare
`scheme://name` source is a single script file. The plugin holds the
credentials, the discovery logic and the source of truth; scriptling only
speaks the fetch protocol.

Fetchers are keyed by URL scheme and are orthogonal to library names: the
scheme never passes through the plugin naming rules, and what a fetcher
returns is file content, nothing prefixed, nothing wrapped.

## How It Works

1. The plugin registers its one fetcher and scheme at startup, before
   `Run()` / serving, like every other plugin registration. A second
   registration is an error.
2. The plugin's handshake advertises the scheme; its presence is the whole
   advertisement.
3. The host routes `scheme://...` sources to that plugin and issues
   `fetch.read` / `fetch.glob` JSON-RPC requests for individual files and
   pattern matches. The library bundle the host attaches is synthesized
   from the handshake (name, version, `libs = ["lib"]`); the plugin never
   serves a manifest.
4. File content travels base64-encoded inside the JSON-RPC result, so binary
   assets (a `webroot/` image, a font) arrive intact.
5. The host keeps none of it. Every read is a fetch, and script sources are
   refetched on every run.

Fetch errors are typed, and the host treats each kind differently:
`-32001` (not found) is a plain miss, never fatal; `-32002` (denied)
surfaces as a permission error and is never retried; `-32003` (unavailable)
is retried a bounded number of times before failing. Any other failure (the
plugin process died, the backend it proxies is unreachable in a way the
fetcher cannot classify) is a different matter: the host aborts the import
with an error naming the package source, rather than silently skipping its
modules. A configured source you cannot reach should be an incident, not a
script that mysteriously runs without its libraries. Local files and
higher-priority packages still resolve without contacting the failed plugin
at all.

## Caching

The host does not cache what a plugin serves. Caching is the plugin's job: it knows its backend and how long
its answers stay valid, so a fetcher with a slow backend caches behind its own
`Read`. There is no conditional-read protocol; `Read` takes only `source` and
`path`, and always returns content.

Directory listings are the one thing held briefly, for 30 seconds by default,
because resolving a path consults its parent's listing. Content is never held.

## Using Fetcher Sources

```bash
# Load the plugin and run a local script: its libraries import with no
# --package at all, they attach with the plugin:
scriptling --plugin /usr/local/bin/knot \
           --plugin-arg scriptling-server --plugin-arg=--alias=testing \
           myscript.py

# Run a script served by the plugin itself (always refetched):
scriptling --plugin /usr/local/bin/knot knot://scripts/hello
```

A scheme source that serves its own `manifest.toml` is a whole app bundle:
main script, libs, serve list, MCP tools and webroot all arrive from the
plugin, and the server runs it exactly like a directory or zip bundle. A
source without one keeps the synthesized library layout.

A plugin's library attaches when the plugin is loaded, so nothing else is
needed. `--package` is for ordinary packages (a `.zip`, a directory, or a
URL) and does not take a plugin scheme source; there is no reason to name
one, since attachment is automatic.

`--plugin` takes an executable path, used literally (paths containing spaces
need no special handling), or the http(s) URL of a plugin server. Arguments come from `--plugin-arg`; see
[loading plugins](/docs/cli/command-line-options/#loading-plugins) for the
rules when several plugins are loaded at once.

| Source | Key |
| --- | --- |
| CLI | `--plugin /usr/local/bin/knot --plugin-arg scriptling-server` |
| Environment | `SCRIPTLING_PLUGIN=/usr/local/bin/knot` |
| Config file | `plugins.paths = ["/usr/local/bin/knot"]`, `plugins.args = ["scriptling-server"]` |

A scheme source can also be run directly as the positional script argument.
Plugin libraries compose with the ordinary loader chain (local files and
explicit `--package` bundles take precedence) and registered built-in modules
such as `json` and `os` are resolved before any loader, so a plugin library
can never shadow the standard library.

If no loaded plugin serves a source's scheme, the error says so and names the
scheme, rather than reporting a missing file:

```text
$ scriptling knot://scripts/hello
Error: failed to fetch script knot://scripts/hello: no plugin provides the
source scheme "knot" for knot://scripts/hello: load the plugin that serves it
with --plugin or --plugin-dir
```

When other fetcher plugins are loaded, the message also lists the schemes that
are available.

## Setup Scripts in Server Modes

The server modes take their setup script through the plugin too. A scheme
source as the script argument is fetched (always fresh) and handed to the
server as source text (nothing is written to a temporary file) and the
plugin's library attaches in those modes just as it does for plain script
execution:

```bash
scriptling --plugin /usr/local/bin/knot --plugin-arg scriptling-server \
           --json-rpc knot://scripts/setup
```

With the example fetcher plugin this serves the methods its setup script
registers, with every handler module arriving on demand from `demo://libs`:

```bash
printf '{"jsonrpc":"2.0","id":1,"method":"demo.add","params":{"a":2,"b":3}}\n' |
  scriptling --plugin /tmp/scriptling-plugins/fetcher-go --json-rpc demo://scripts/setup
```

## Go Plugins

Implement the `Fetcher` interface and make the one registration call; that
is the entire contract. The library bundle the host attaches takes its name
and version from the plugin's handshake:

```go
server := plugin.NewServer("myfetcher", "1.0.0", "serves mylib:// sources")
server.RegisterFetcher("mylib", myFetcher{})
if err := server.Run(); err != nil { panic(err) }
```

```go
type myFetcher struct{}

func (myFetcher) Read(ctx context.Context, source, path string) ([]byte, error) {
    // path == "" means the source itself is a single script file.
    content, ok := lookup(source, path)
    if !ok {
        return nil, fmt.Errorf("%w: %s", plugin.ErrFetchNotFound, path)
    }
    return []byte(content), nil
}

func (myFetcher) Glob(ctx context.Context, source, pattern string) ([]plugin.FetchEntry, error) {
    // Every path matching pattern, directories included, full paths.
    // Wrap plugin.ErrFetchDenied for refusals and
    // plugin.ErrFetchUnavailable for a backend that cannot answer (the
    // host retries those).
    entries := []plugin.FetchEntry{}
    for _, name := range knownPaths(source) {
        if plugin.MatchGlob(pattern, name) {
            entries = append(entries, plugin.FetchEntry{Name: name})
        }
    }
    return entries, nil
}
```

`Read` returns the file's bytes, or an error wrapping `plugin.ErrFetchNotFound`
for a miss. Data travels base64-encoded inside the JSON-RPC result, so binary
assets arrive intact. There are no validators to deal with: the host does not
cache, so every read reaches your handler. Cache inside `Read` if your backend
needs it. Serving from disk? `plugin.GlobDisk` implements `Glob` with the
root containment built in, so symlink escapes are not served.

`Glob` answers in one round trip what a directory walk would need one per
level for: existence is a wildcard-free pattern (the entry itself comes
back, so an empty directory is distinguishable from a missing one), a
listing is `<dir>/*`, a subtree is `<dir>/**`. No match is an empty result,
never an error. `MatchGlob` implements the pattern language; the C SDK
exposes the same matching as `sl_glob_match`.

There is no stat round trip either: `Open` and `Stat` read the file (a
directory is simply one whose glob answers its entry), so a plugin only ever
answers "here are the bytes" or "not found".

A complete example lives at `examples/plugins/fetcher-go` in the repository.

## C Plugins

The C SDK exposes the same feature:

```c
static sl_fetch_result *my_read(const char *source, const char *path, void *ctx) {
    return sl_fetch_data("# content\n", 10);  /* host does not cache */
}

static sl_fetch_entry *my_glob(const char *source, const char *pattern,
                               size_t *count, void *ctx) {
    /* keep the known paths sl_glob_match(pattern, name) accepts */
}

sl_register_fetcher(srv, "mylib", my_read, my_glob);
```

See [C Plugins](/docs/plugins/c-plugins/) for the handler contracts and the
`cdemo://` example in the `hello-c` plugin.

## Embedding Hosts

Go applications that embed Scriptling get the same behaviour by bridging their
plugin manager into a package scheme registry; see
[fetcher plugins in the plugin manager docs](/docs/plugins/host-integration/#fetcher-plugins)
for the wiring and reloading, and
`examples/embed-fetcher-plugin` for a runnable host.

## Wire Protocol

Fetch traffic is two host-to-plugin JSON-RPC methods, documented with the
rest of the [plugin protocol](/docs/plugins/protocol/): `fetch.read` and
`fetch.glob`. Both transports carry them; over HTTP the fetcher runs as a
plain request/response service, and stdio additionally allows logging from
inside handlers via `plugin.Logger(ctx)`.

`Glob` is required by the `Fetcher` interface: path resolution, listings and
enumeration all reduce to pattern matches, each answered in one call. Matches
are treated as advisory in the same spirit: a file a pattern match omits is
still readable, so a fetcher may keep its matching cheap.

Path safety has two halves, and the host owns only one of them. Before any
RPC is issued the host validates the virtual path with `fs.ValidPath`
semantics, so `..`, absolute paths and malformed components never reach the
plugin. What the host cannot do is sanitize the plugin's own filesystem: a
disk-backed fetcher maps virtual paths to real files, and a symlink inside
the served root (or a path component that resolves through one) can point
anywhere the plugin process can read. A fetcher serving files from disk must
defend its own root, typically by resolving the real path
(`filepath.EvalSymlinks`) and checking it stays inside the root before every
read.
