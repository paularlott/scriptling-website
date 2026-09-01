---
description: Scriptling release history.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/changelog/
sources:
    - resource: https://scriptling.dev/docs/changelog/
status: stable
tags:
    - docs
    - changelog
title: Changelog
type: Guide
---
# Changelog

## September 2026

### v0.24.0



**Database drivers are built in by default.** `scriptling` now ships with the SQLite, SQL, Valkey and BadgerDB plugins compiled in, so database support needs no extra setup. `scriptling-full` is replaced by `scriptling-slim`, the lean build without the compiled-in drivers, which can still load them at runtime via `scriptling-plugins` or `--plugin-dir`. Homebrew users of the old full formula should run `brew uninstall scriptling-full && brew install scriptling`.


## August 2026

### v0.23.0



**Database libraries and ORM.** New first-party plugins add SQLite, a multi-driver SQL client for MySQL/MariaDB and PostgreSQL, Valkey/Redis, and BadgerDB. Relational connections share one API and provide `get_orm()` for queries, model gateways, and schema builders; Valkey and BadgerDB share a key/value API. Database support is available in `scriptling-full`, through the platform-specific `plugins-<os>-<arch>.zip` archive, or with Homebrew's `scriptling-plugins` package configured via `--plugin-dir`. See [Database Libraries](https://scriptling.dev/okf/scriptling-libraries/databases.md) and the runnable [database examples](https://github.com/paularlott/scriptling/tree/main/examples/databases).



**More ways to load and deploy plugins.** The repeatable `--plugin` option loads individual executables or remote HTTP(S) plugin servers, with support for plugin arguments, environment variables, and HTTP authentication. Plugin configuration now reads the documented `plugins.dirs` and `plugins.paths` keys. Dotted names such as `scriptling.sqlite` are supported; conflicting discovered libraries are skipped with a warning and compiled-in plugins take precedence. Executable peers receive the host version, and the handshake carries host filesystem and network policies for compatible plugins to enforce. See [Using Plugins](https://scriptling.dev/okf/scriptling-docs/plugins/using.md) and [PHP Plugins](https://scriptling.dev/okf/scriptling-docs/plugins/php-plugins.md).



**Plugin-provided scripts, libraries, and packages.** Fetcher plugins can expose content through custom schemes such as `knot://`, supplying packages for Scriptling's existing app-bundle and server machinery. Fetchers support recursive glob matching and lazy loading, and Go applications can use the same scheme resolution through `pluginpack`. See [Plugin Fetchers](https://scriptling.dev/okf/scriptling-docs/plugins/fetchers.md).



**Request-aware HTTP transports.** For HTTP-served MCP and JSON-RPC, middleware can authenticate a request, add Scriptling request-context data, and register MCP tools, resources, and prompts for that request. HTTP route handlers receive the normalized Scriptling request directly; MCP and JSON-RPC handlers can read it with `get_request()` and an isolated copy of its context with `request_context()`. `transport()` reports `http`, `stdio`, or `None`; request-scoped registration is HTTP-only.



**HTTP authentication covers the full surface.** `--bearer-token` now wraps the entire HTTP mux even when script middleware is registered, protecting health, protocol, route, WebSocket-upgrade, static, webroot, and not-found paths. Script middleware also runs before a WebSocket is promoted, so it can reject the upgrade or pass request-context data to the socket handler.



**Generated Scriptling and MCP error payloads are JSON-escaped.** Errors synthesized from middleware, request-scoped MCP registration, and MCP helper failures now encode quotes, backslashes, and newlines correctly instead of producing malformed JSON.



**HTTP request limits and timeouts.** HTTP servers use 10-second header, 5-minute read/write, and 2-minute idle timeouts. Request bodies default to a 32 MiB cap (`ServerConfig.MaxRequestBodyBytes` or `--max-request-body`; zero uses the default and a negative value disables it). Protocol and script handlers now reject an over-limit body with `413 Request Entity Too Large` rather than processing a truncated payload.



**MCP SSE is exempt from the HTTP write deadline.** For the long-lived `GET /mcp` event stream, Scriptling clears the server write deadline after protocol middleware, so the normal HTTP write timeout no longer ends an otherwise healthy subscription.



**Background task startup is race-free.** `runtime.background()` now completes task setup on the caller's goroutine before queuing or starting the task, avoiding concurrent reads of partially prepared state.



**`finally` control flow is complete.** `return`, `break`, and `continue` in a `finally` block now propagate correctly; a normal exception raised there replaces an ordinary pending result. `finally` still runs for `SystemExit` and `PermissionError`, but cannot replace those protected exceptions.



**Circular imports fail fast.** Two modules importing each other used to re-evaluate forever; the import chain is now tracked and a cycle reports `circular import: a -> b -> a`.



**Self-referential values convert safely.** A list or dict containing itself crashed host conversion with an unrecoverable stack overflow; it now converts cyclic references to a `<cyclic reference>` marker.



**Repetition results are bounded.** `"ab" * n`, `bytes * n`, and `list`/`tuple * n` refuse oversized results with a clear error (1 GiB for strings and bytes, roughly 134 million elements for sequences) instead of allocating unbounded results; a constant-folded repetition no longer panics at parse time.



**Release artifacts are built safely for their target platforms.** Cross-platform `scriptling-full` builds now export `GOOS` and `GOARCH`, preventing host binaries from being labeled as another platform. Homebrew formulas are generated to temporary files and atomically moved into place before release tagging, so a failed generator cannot truncate a formula or leave a green release.



**Releasing remote objects reports the actual outcome.** Concurrent explicit and GC-finalizer releases now wait for the winning destroy request and return its result instead of reporting success while it may still fail.



**Instance destructors get a boundary.** A user-defined `__del__` running on the Go GC finalizer goroutine now has panic recovery and a bounded context, preventing a destructor panic from terminating the host process.



**Selected shared options work after subcommands.** Package, cache, library/plugin, logging, filesystem/network-security, and Docker/Podman-host options marked global are accepted before or after nested commands such as `cache clear` and `help`; server-only options remain specific to server invocations.


---

### v0.22.0



**Per-user keys for MCP and JSON-RPC.** The middleware registered with `runtime.http.middleware(...)` now guards the `/mcp` and `/json-rpc` endpoints as well as HTTP routes, so one handler can authenticate API clients, MCP clients, and JSON-RPC callers against whatever it likes, a dict of keys, the KV store, an API. Registering a middleware replaces static `--bearer-token` checking on the protocol endpoints; without one, the static token guards everything as before.



**Failed KV disk writes are no longer silent.** With a persistent store (`--kv-storage` or `SCRIPTLING_KV_STORAGE`, and stores opened with `kv.open()`), a snapshot write that failed, disk full, directory deleted, permissions, left no trace: the script reported success and the data was simply gone on the next run. Save failures are now logged with the store path and the cause, and `store.close()` raises the error to the script instead of returning quietly.
