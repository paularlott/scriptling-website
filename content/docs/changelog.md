---
title: Changelog
description: Scriptling release history.
tags: [docs, changelog]
layout: changelog
nav-skip: true
---

## August 2026

{{< version "v0.23.0" >}}
{{< changelog-item "added" >}}
**Database support.** New first-party plugins bring SQLite, MySQL/MariaDB, PostgreSQL, Valkey/Redis and BadgerDB to scripts. The relational libraries `scriptling.sqlite` and `scriptling.sql` share one API: `connect()` hands you a connection with `query()`, `execute()` and `close()`, and rows come back as dicts. The key/value libraries `scriptling.valkey` and `scriptling.badgerdb` agree on `get`, `set`, `delete`, `expire`, `ttl` and `incr`, plus hashes, so code moves between a shared cache and local storage unchanged. The valkey client also speaks to clusters and sentinels, can flush a database, and adds sets, queues and database selection. All pure Go. Take it either way: `scriptling-full` is the same CLI with every driver compiled in (`brew install paularlott/tap/scriptling-full`), or the `plugins-<os>-<arch>.zip` from the releases page — installed as `brew install paularlott/tap/scriptling-plugins` — provides all four binaries to point `--plugin-dir` at. See the new [Database Libraries](/reference/libraries/databases/) reference and the runnable [examples](https://github.com/paularlott/scriptling/tree/main/examples/databases).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`get_orm()`.** Relational connections grow an ORM, the same one for all four backends. Chain `.where(...)` calls and `.order_by(...)` onto a `select`, `update` or `delete`, or use the quick `insert(table, dict)` form for a single row. A mutation without a where is refused, so a mistake can't wipe a whole table. `orm.table()` opens a model gateway that maps rows onto your objects, taking its write columns from the table's schema on first read, and table builders handle the schema side.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`--plugin` loads a single plugin.** Point `--plugin` at one executable instead of scanning a directory. The flag repeats, `--plugin-arg` carries per-plugin arguments, and `--plugin-env KEY=VALUE` layers environment entries onto an executable plugin, binding the same way: bare with one plugin, `<plugin>=` qualified with several. Explicit entries load before `--plugin-dir` scans and win on a clash.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Plugin servers over HTTP.** A `--plugin` value can be the `http://` or `https://` URL of a remote JSON-RPC plugin server instead of an executable. URLs authenticate with `--plugin-header KEY=VALUE`, a bearer token say, or with `user:pass@` in the URL as Basic auth; `--plugin-insecure <url>` marks the URLs allowed to use self-signed certificates. A [plain-PHP example server](https://github.com/paularlott/scriptling/tree/main/examples/plugins/php-server) shows the whole protocol in another language (see [PHP Plugins](/docs/plugins/php-plugins/)).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Namespaced plugin names.** A plugin that declares a dotted name is imported under exactly that name, so the database plugins can declare `scriptling.sqlite` and match their compiled-in builds. A name that would shadow a registered library is refused.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Plugins receive the security policy.** The handshake now carries the `--allowed-paths` filesystem roots and the network policy, and first-party plugins enforce both: file-based plugins check database paths, network plugins dial through the same guards as `requests`. Older plugins ignore the new field.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Plugin peers know who spawned them.** Every executable spawned as a plugin peer gets `SCRIPTLING_PLUGIN_PEER` set to the host's version, so a multi-role executable can divert a bare invocation into plugin mode.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Fetcher plugins: scripts and libraries over custom schemes.** A plugin can register a fetcher with a single call, `RegisterFetcher("knot", fetcher)` in Go or `sl_register_fetcher` in C, and serve its own `knot://` scheme. `knot://scripts/hello` runs a plugin-served script, `knot://libs` libraries attach on import, and files are fetched only when something actually asks for them. A scheme source that serves its own `manifest.toml` is a whole app bundle: setup script, routes, MCP tools and webroot. In server modes, background tasks resolve handler modules from packages through the same loader request handlers use. See the [Plugin Fetchers](/docs/plugins/fetchers/) page.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`fetch.glob`: every match in one round trip.** A fetcher's second operation matches a pattern — `*` and `?` within a segment, `[class]` for a choice of characters, `**` across segments — and the plugin, which knows its backend, does the matching instead of the host walking the tree level by level. Existence is a wildcard-free pattern, a listing is `<dir>/*`, a subtree is `<dir>/**`. No match is an empty result rather than an error, and errors are typed as not found, denied or unavailable, so the host can retry unavailable backends (and transport failures) a bounded number of times on idempotent reads. Go fetchers get `plugin.MatchGlob` and `plugin.GlobDisk` with root containment built in; the C SDK gets `sl_glob_match`.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Fetcher plugins for embedders.** `pluginpack.New(...)` brings the same `knot://` resolution to Go hosting applications, with cancellation of in-flight fetches and reloadable schemes; server hosts can hand a fetched setup script straight to `ServerConfig.ScriptSource`. See `examples/embed-fetcher-plugin`.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Per-user MCP tools, resources and prompts.** Middleware can register entries that exist for the life of a single request (e.g. `mcp.register_request_tool("restart", ...)`), so each caller's `tools/list` shows exactly what their middleware registered — hand an admin their `restart` tool without anyone else ever seeing it.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Scripts can ask how they are served.** `mcp.transport()` and `runtime.jsonrpc.transport()` return `"http"`, `"stdio"` or `None`, so one setup script works in every mode.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Middleware can pass data to handlers.** The middleware gets `request.context`, a fresh dict on every request: authenticate, write `request.context["user"] = name`, and the handler reads it back — via `request.context` on HTTP routes, or `tool.request_context()` / `runtime.jsonrpc.request_context()` in MCP tools and JSON-RPC methods. `get_request()` goes further and returns the whole HTTP request, or `None` over stdio.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**WebSocket routes are now guarded.** WebSocket upgrades now run through the middleware (and the static `--bearer-token` when no middleware is registered) like every other endpoint, so a `websocket("/ws", ...)` handler can't be reached without the token.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`package.glob` recursive patterns matched nothing.** `scriptling.package`'s `glob` handled `**` by matching literal prefix and suffix halves, so the common `**/*.md` form returned an empty list for every package kind. It now speaks the same pattern language as `fetch.glob`, where `**` crosses any number of segments (including none, so a file at the package root still matches).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`runtime.background()` no longer races the caller's environment.** A spawned task read the calling script's variables from its own goroutine, racing any concurrent evaluation of the same environment — intermittent and unreproducible under concurrent handlers. Task setup now runs on the caller's goroutine before the task starts.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Subcommands honor their flags.** `--cache-dir`, `--package`, `--allowed-paths`, `--network-policy`, `--docker-host` and `--podman-host` are now global flags, so `cache clear` and `help` accept them in any position instead of ignoring or rejecting them.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`plugins.dirs` config key works.** `--plugin-dir` now reads the documented nested `[plugins] dirs = [...]` config key instead of the wrong alternative keys, and `--plugin` reads `plugins.paths` alongside it.
{{< /changelog-item >}}

---

{{< version "v0.22.0" >}}

{{< changelog-item "added" >}}
**Per-user keys for MCP and JSON-RPC.** The middleware registered with `runtime.http.middleware(...)` now guards the `/mcp` and `/json-rpc` endpoints as well as HTTP routes, so one handler can authenticate API clients, MCP clients, and JSON-RPC callers against whatever it likes, a dict of keys, the KV store, an API. Registering a middleware replaces static `--bearer-token` checking on the protocol endpoints; without one, the static token guards everything as before.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Failed KV disk writes are no longer silent.** With a persistent store (`--kv-storage` or `SCRIPTLING_KV_STORAGE`, and stores opened with `kv.open()`), a snapshot write that failed, disk full, directory deleted, permissions, left no trace: the script reported success and the data was simply gone on the next run. Save failures are now logged with the store path and the cause, and `store.close()` raises the error to the script instead of returning quietly.
{{< /changelog-item >}}
