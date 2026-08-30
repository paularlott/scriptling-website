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
**`--plugin` loads plugin servers; `--plugin-env` passes variables.** A `--plugin` value can be the `http://`/`https://` URL of a remote JSON-RPC plugin server instead of an executable (`--plugin-insecure <url>` marks which URLs may use self-signed certificates), and `--plugin-env KEY=VALUE` layers environment entries onto an executable plugin, binding like `--plugin-arg` (bare with one plugin, `<plugin>=` qualified with several). HTTP plugin URLs authenticate with `--plugin-header KEY=VALUE` (a bearer token, say) or `user:pass@` in the URL as Basic auth. A [plain-PHP example server](https://github.com/paularlott/scriptling/tree/main/examples/plugins/php-server) shows the whole protocol in another language (see [PHP Plugins](/docs/plugins/php-plugins/)).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Database support.** New first-party plugins bring SQLite, MySQL/MariaDB, PostgreSQL, Valkey/Redis and BadgerDB to scripts. The relational libraries `scriptling.sqlite` and `scriptling.sql` share a `connect()` → `Connection.query/execute/close` API with rows as dicts; the key/value libraries `scriptling.valkey` and `scriptling.badgerdb` share `get/set/delete/expire/ttl/incr` plus hashes, so code moves between a shared cache and local storage unchanged. The valkey client adds clusters and sentinels (`connect(url, mode=...)`), flushes (`flushdb`/`flushall`), sets, queues and database selection. All pure Go, compiled in or as external plugin binaries. See the new [Database Libraries](/reference/libraries/scriptling/databases/) reference and the runnable [examples](https://github.com/paularlott/scriptling/tree/main/examples/databases).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`get_orm()`.** Relational connections gain an ORM: query builders for `select`, `update` and `delete` that compose conditions with chained `.where(...)` calls and `.order_by(...)` (executing a mutation without a where is refused), a quick `insert(table, dict)` form, table builders, and `orm.table()` model gateways that map rows onto your objects (write columns default to the table's schema, read once and cached). One implementation serves all four relational backends.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Namespaced plugin names.** A plugin that declares a name containing a dot is imported verbatim — `myplugin.hello` imports as `myplugin.hello` — so the database plugins can declare `scriptling.sqlite` and match compiled-in builds. A name that would shadow a registered library is refused.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Plugins receive the security policy.** The handshake now carries the `--allowed-paths` filesystem roots and the network policy, and first-party plugins enforce both: file-based plugins check database paths, network plugins dial through the same guards as `requests`. Older plugins ignore the new field.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Plugin peers know who spawned them.** Every executable spawned as a plugin peer gets `SCRIPTLING_PLUGIN_PEER=1`, so a multi-role executable can divert a bare invocation into plugin mode.
{{< /changelog-item >}}


{{< changelog-item "added" >}}
**Fetcher plugins speak `fetch.glob` with typed errors.** A fetcher's second operation matches a glob pattern (`*` and `?` within a segment, `[class]`, `**` across segments) and returns every match in one round trip: existence is a wildcard-free pattern, a listing is `<dir>/*`, a subtree is `<dir>/**`, and the plugin (which knows its backend) does the matching instead of the host walking level by level. No match is an empty result; errors are typed as not found, denied, or unavailable, and the host retries unavailable backends (and transport failures) a bounded number of times on the idempotent reads. `plugin.MatchGlob` and `plugin.GlobDisk` (root containment built in) implement it for Go fetchers, `sl_glob_match` for C. A scheme source that serves its own `manifest.toml` is a whole app bundle (setup script, routes, MCP tools, webroot), and background tasks in server modes resolve handler modules from packages through the same loader request handlers use. Plugins can serve libraries and scripts over custom schemes with a single registration call (`RegisterFetcher("knot", fetcher)`). `knot://scripts/hello` runs a plugin-served script, `knot://libs` libraries attach on import, and files are fetched only when something actually imports them. Go plugins use the `Fetcher` interface; the C SDK gains `sl_register_fetcher` with the same contract. See the Plugin Fetchers page.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**`--plugin` loads a single plugin.** Point `--plugin` at one executable instead of scanning a directory, with per-plugin `--plugin-arg` values. Both flags repeat; explicit entries load before `--plugin-dir` scans and win on a clash.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Fetcher plugins for embedders.** `pluginpack.New(...)` brings the same `knot://` resolution to Go hosting applications, with context-based cancellation of in-flight fetches and reloadable schemes. Server hosts hand a fetched setup script straight to `ServerConfig.ScriptSource`. See `examples/embed-fetcher-plugin`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Unknown schemes are now named.** `scriptling knot://...` without the knot plugin loaded reported `no such file or directory`; it now names the scheme, the flag that loads a plugin for it, and the schemes that are available. Fetcher not-found errors also stopped repeating themselves.
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
