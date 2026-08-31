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

## August 2026

### v0.23.0


**Database libraries and ORM.** New first-party plugins add SQLite, MySQL/MariaDB, PostgreSQL, Valkey/Redis and BadgerDB support. Relational connections share one API and provide `get_orm()` for queries, model gateways and schema builders; Valkey and BadgerDB share a key/value API. The drivers are available compiled into `scriptling-full` or as external plugin binaries. See [Database Libraries](https://scriptling.dev/okf/scriptling-libraries/./databases.md) and the runnable [database examples](https://github.com/paularlott/scriptling/tree/main/examples/databases).



**More ways to load and deploy plugins.** The repeatable `--plugin` option loads individual executables or remote HTTP(S) plugin servers, with support for plugin arguments, environment variables and HTTP authentication. Plugins can declare dotted names such as `scriptling.sqlite`, while collisions with registered libraries are rejected. Executable peers receive the host version, and the plugin handshake now carries the host filesystem and network policies for plugins to enforce. See [Using Plugins](https://scriptling.dev/okf/scriptling-docs/plugins/using.md) and [PHP Plugins](https://scriptling.dev/okf/scriptling-docs/plugins/php-plugins.md).



**Plugin-provided scripts, libraries and packages.** Fetcher plugins can expose content through custom schemes such as `knot://`, including complete app bundles with setup scripts, routes, MCP tools and web assets. Fetchers support recursive glob matching and lazy loading, and Go applications can use the same scheme resolution through `pluginpack`. See [Plugin Fetchers](https://scriptling.dev/okf/scriptling-docs/plugins/fetchers.md).



**Request-aware MCP, HTTP and JSON-RPC servers.** Middleware can register request-scoped MCP tools, resources and prompts, and pass authenticated user data to handlers through a fresh request context. Scripts can inspect whether MCP or JSON-RPC is running over HTTP or stdio, while HTTP handlers can access the complete incoming request when needed.



**WebSocket routes now respect authentication.** WebSocket upgrades run through middleware—or the configured bearer token—like other HTTP endpoints.



**Error responses are always valid JSON.** Middleware and MCP error messages containing quotes or newlines are now encoded correctly.



**Recursive package globs work correctly.** Patterns such as `**/*.md` now match files at any depth, including the package root.



**Background task startup is race-free.** `runtime.background()` now completes task setup on the caller's goroutine before starting the task.



**Subcommands consistently accept global flags.** Commands such as `cache clear` and `help` now honor package, cache, security and container-host options regardless of their position.



**Plugin configuration uses the documented keys.** `--plugin-dir` reads `plugins.dirs`, and `--plugin` reads `plugins.paths`.


---

### v0.22.0



**Per-user keys for MCP and JSON-RPC.** The middleware registered with `runtime.http.middleware(...)` now guards the `/mcp` and `/json-rpc` endpoints as well as HTTP routes, so one handler can authenticate API clients, MCP clients, and JSON-RPC callers against whatever it likes, a dict of keys, the KV store, an API. Registering a middleware replaces static `--bearer-token` checking on the protocol endpoints; without one, the static token guards everything as before.



**Failed KV disk writes are no longer silent.** With a persistent store (`--kv-storage` or `SCRIPTLING_KV_STORAGE`, and stores opened with `kv.open()`), a snapshot write that failed, disk full, directory deleted, permissions, left no trace: the script reported success and the data was simply gone on the next run. Save failures are now logged with the store path and the cause, and `store.close()` raises the error to the script instead of returning quietly.
