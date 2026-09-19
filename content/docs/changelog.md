---
title: Changelog
description: Scriptling release history.
tags: [docs, changelog]
layout: changelog
nav-skip: true
---

## September 2026

{{< version "v0.25.3" >}}

{{< changelog-item "security" >}}
**Scripts could load or unload plugins you never intended them to touch.** If your host registered `scriptling.plugin`, scripts got the same `load()`/`unload()` power as the host itself, with no way to say "just use what I already loaded." You can now hand scripts a plugin scope that's read-only (they use your pre-loaded plugins but can't load or unload anything), or one that can load new plugins only over an HTTP endpoint you control. See [Plugin Manager](/docs/plugins/host-integration/#restricting-transport-type) for how to set it up. Nothing changes unless you already register `scriptling.plugin`.
{{< /changelog-item >}}

{{< changelog-item "security" >}}
**A nested plugin scope could quietly lose its parent's restrictions.** If you locked a scope down and then created a scope from it without repeating the same options, the new scope came back fully open. Restrictions now carry through by default, and you can still loosen or tighten them on the child if you want to.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**You can now limit which folders scripts are allowed to load new plugins from.** This is the same idea as restricting plugin loading to an approved network policy, but for local executables — scripts can use a plugin folder you approve, not any executable on the machine. See [Restricting Which Paths Scripts May Load Executables From](/docs/plugins/host-integration/#restricting-which-paths-scripts-may-load-executables-from).
{{< /changelog-item >}}

---

{{< version "v0.25.2" >}}

{{< changelog-item "security" >}}
**The network policy now also covers `scriptling.ai` and `scriptling.mcp`.** Previously a `--network-policy` (or embedded `*netsecurity.Config`) only governed `requests`, `scriptling.wait_for`, and `scriptling.net.websocket` — a script could reach an arbitrary IP or bypass the configured DNS servers simply by using `ai.Client(...)` or `mcp.Client(...)` instead. Both HTTP-transport clients are now built through the same guard: `ai.Register(p, policy)` and `mcp.Register(p, policy)` restrict the main client and, for `scriptling.ai`, every `remote_servers` entry too. Stdio-transport `mcp.Client()` instances (a local subprocess) are unaffected, since the policy only governs network access. Omitting the policy argument (or calling `Register(p)` with none) keeps the previous, unrestricted behaviour — no action needed for existing scripts or hosts that don't use a network policy.
{{< /changelog-item >}}

---

{{< version "v0.25.1" >}}

{{< changelog-item "changed" >}}
**The guarded HTTP client no longer enforces a fixed 30-second cap.** `requests` and `scriptling.wait_for` under a network policy now run as long as their own per-request timeout allows, so long-running calls such as LLM APIs are no longer cut off. Hosts that want a cap can set `ClientTimeout` on `netsecurity.Config`, or `client_timeout = "30s"` in a `--network-policy` file.
{{< /changelog-item >}}

---

{{< version "v0.25.0" >}}

{{< changelog-item "changed" >}}
**Reading a missing dict key or an out-of-range index now raises `KeyError` / `IndexError`, matching Python.** Scripts that relied on getting `None` back should use `key in d`, `d.get(key, default)`, or a bounds check instead.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Exceptions behave like Python everywhere.** A `raise` inside a call argument, comprehension, condition, f-string, `with`, `match`, user iterator, or dunder method now reaches the nearest `except` instead of being swallowed, silently converted to a value, or reported as a confusing type error. Constructing an exception (`e = ValueError("x")`) remains a harmless value, exactly as in Python.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Classes now work where they used to be quietly ignored.** Class bodies run every statement, so attribute assignments like `x = 5` become class attributes. `sorted()`, `min()`/`max()`, membership tests, `.index()`, and dict keys all honor `__lt__`, `__eq__` and `__hash__`, comparisons try the reflected operator (`b.__gt__(a)` when `a` defines no `__lt__`), and `str()`, `%s`, f-strings and `join()` convert instances through `__str__` (falling back to `__repr__`).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Anything iterable works anywhere a list does.** `list()`, `sorted()`, `map()`, `filter()`, `sum()`, `zip()`, `enumerate()`, `join()` and tuple unpacking now accept classes with `__iter__`/`__next__` (previously rejected with a type error), a raising iterator surfaces its error instead of hanging, and infinite iterators stay cancellable by timeout.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Formatting is up to Python spec.** `str.format` supports named fields, indexes, escapes and format specs (`"{name:>10}".format(name=…)`), f-strings gained `!r`/`!s` conversions and nested spec fields (`f"{x:>{w}}"`), and bare `raise ValueError` (no parentheses) instantiates the class — so `raise StopIteration` works inside iterators.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Smaller fixes:** using the default `scriptling.runtime.kv` store before it's open raises a catchable error instead of crashing the host; importing a module whose top level raises re-raises the original exception instead of flattening to `ImportError`; a `re.sub()` callback's raise surfaces instead of being spliced into the result; `itertools` accepts script-defined functions; out-of-range subscript *writes* raise `IndexError`; `functools.reduce` accepts lambdas.
{{< /changelog-item >}}

---

{{< version "v0.24.6" >}}

{{< changelog-item "fixed" >}}
**Reduce log noise during plugin load.** Plugin initialization messages are now less verbose, focusing only on essential information.
{{< /changelog-item >}}

---

{{< version "v0.24.5" >}}

{{< changelog-item "added" >}}
**Script peers can serve sources from the script itself.** `runtime.plugin.register_fetcher(scheme, read_handler, glob_handler=None)` registers a fetcher backed by script handlers: the host asks for files on demand and the read handler answers from strings or bytes inside the script (`None` is a miss). This is how a script peer carries a host's declared assets — an icon, a logo — without any files on disk, the scriptling equivalent of a Go peer's embedded assets. knot reads declared plugin assets peer-first, disk second, so a scriptling peer can now be a single-file plugin. See [Plugin server](/docs/cli/plugin-server/#runtime-plugin-register-fetcher-scheme-read-handler-glob-handler-none).
{{< /changelog-item >}}
---

{{< version "v0.24.4" >}}

{{< changelog-item "added" >}}
**Plugins can declare opaque manifest data in the handshake.** A plugin may attach a host-defined data map that travels verbatim in the plugin handshake — Go peers via `Server.SetMetadata(map[string]any)`, Scriptling-authored peers via `runtime.plugin.serve(name, ..., metadata={...})` — and the host reads it back with `Client.Metadata().Custom`. Scriptling never interprets the data; it is the channel for a host to learn plugin-specific declarations from the manifest without running any plugin code. Backward compatible: plugins that declare none send nothing, and older hosts ignore the field. See [Plugin protocol](/docs/plugins/protocol/#custom-manifest-data).
{{< /changelog-item >}}

---

{{< version "v0.24.3" >}}

{{< changelog-item "fixed" >}}
**Multiline conditional expressions and parser robustness.** `x if cond else y` written across lines inside brackets now parses (newlines are whitespace there, as in Python), and a malformed `if` no longer crashes the parser with a nil dereference — it reports ordinary parser errors.
{{< /changelog-item >}}

---

{{< version "v0.24.2" >}}

{{< changelog-item "added" >}}
**Relational transactions with commit and rollback.** `conn.begin()` on `scriptling.sqlite` and `scriptling.sql` returns a Transaction whose `query()`, `query_iter()` and `execute()` run inside one atomic unit, ended by `commit()` (keep) or `rollback()` (discard). `tx.get_orm()` binds the ORM to the open transaction so builder chains and model gateways join it, `?` placeholders keep working on PostgreSQL, and an abandoned transaction rolls back automatically once collected (compiled-in builds previously never ran the cleanup for objects created inside plugin methods — abandoned cursors leaked their connection too, and both now release at the next collection cycle). See the [SQLite](/reference/libraries/databases/sqlite/#transactions) and [SQL](/reference/libraries/databases/sql/#transactions) transaction sections.
{{< /changelog-item >}}

---

{{< version "v0.24.1" >}}

{{< changelog-item "added" >}}
**`[tool.*]` metadata tables are surfaced to embedding hosts.** `metadata.Parse` now returns the `[tool.<name>]` tables via `Metadata.Tools` and `Tool(name)`, so hosts can carry their own declarations in the block; scriptling still ignores their contents. See [Tool tables](/docs/script-metadata/#tool-tables).
{{< /changelog-item >}}

---

{{< version "v0.24.0" >}}

{{< changelog-item "added" >}}
**Scripts can declare their requirements.** A PEP 723-style inline metadata block (`# /// script`) lets a script state a minimum scriptling version, the libraries it imports, and the plugins it expects to be connected, with optional version constraints. The CLI verifies the block before the code runs — one-shot scripts and `--code`, server setup scripts once at startup before anything binds, and package main entries — reporting every unmet requirement in one error with the remedy: load a plugin, use a build with it compiled in, or upgrade the host. `--lint` validates the block itself, and embedding hosts can run the same check through the `metadata` package. See [Script Metadata](/docs/script-metadata/).
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Database drivers are built in by default.** `scriptling` now ships with the SQLite, SQL, Valkey and BadgerDB plugins compiled in, so database support needs no extra setup. `scriptling-full` is replaced by `scriptling-slim`, the lean build without the compiled-in drivers, which can still load them at runtime via `scriptling-plugins` or `--plugin-dir`. Homebrew users of the old full formula should run `brew uninstall scriptling-full && brew install scriptling`.
{{< /changelog-item >}}

---

## August 2026

{{< version "v0.23.0" >}}

{{< changelog-item "added" >}}
**Database libraries and ORM.** New first-party plugins add SQLite, a multi-driver SQL client for MySQL/MariaDB and PostgreSQL, Valkey/Redis, and BadgerDB. Relational connections share one API and provide `get_orm()` for queries, model gateways, and schema builders; Valkey and BadgerDB share a key/value API. Database support is available in `scriptling-full`, through the platform-specific `plugins-<os>-<arch>.zip` archive, or with Homebrew's `scriptling-plugins` package configured via `--plugin-dir`. See [Database Libraries](/reference/libraries/databases/) and the runnable [database examples](https://github.com/paularlott/scriptling/tree/main/examples/databases).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**More ways to load and deploy plugins.** The repeatable `--plugin` option loads individual executables or remote HTTP(S) plugin servers, with support for plugin arguments, environment variables, and HTTP authentication. Plugin configuration now reads the documented `plugins.dirs` and `plugins.paths` keys. Dotted names such as `scriptling.sqlite` are supported; conflicting discovered libraries are skipped with a warning and compiled-in plugins take precedence. Executable peers receive the host version, and the handshake carries host filesystem and network policies for compatible plugins to enforce. See [Using Plugins](/docs/plugins/using/) and [PHP Plugins](/docs/plugins/php-plugins/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Plugin-provided scripts, libraries, and packages.** Fetcher plugins can expose content through custom schemes such as `knot://`, supplying packages for Scriptling's existing app-bundle and server machinery. Fetchers support recursive glob matching and lazy loading, and Go applications can use the same scheme resolution through `pluginpack`. See [Plugin Fetchers](/docs/plugins/fetchers/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Request-aware HTTP transports.** For HTTP-served MCP and JSON-RPC, middleware can authenticate a request, add Scriptling request-context data, and register MCP tools, resources, and prompts for that request. HTTP route handlers receive the normalized Scriptling request directly; MCP and JSON-RPC handlers can read it with `get_request()` and an isolated copy of its context with `request_context()`. `transport()` reports `http`, `stdio`, or `None`; request-scoped registration is HTTP-only.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**HTTP authentication covers the full surface.** `--bearer-token` now wraps the entire HTTP mux even when script middleware is registered, protecting health, protocol, route, WebSocket-upgrade, static, webroot, and not-found paths. Script middleware also runs before a WebSocket is promoted, so it can reject the upgrade or pass request-context data to the socket handler.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Generated Scriptling and MCP error payloads are JSON-escaped.** Errors synthesized from middleware, request-scoped MCP registration, and MCP helper failures now encode quotes, backslashes, and newlines correctly instead of producing malformed JSON.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**HTTP request limits and timeouts.** HTTP servers use 10-second header, 5-minute read/write, and 2-minute idle timeouts. Request bodies default to a 32 MiB cap (`ServerConfig.MaxRequestBodyBytes` or `--max-request-body`; zero uses the default and a negative value disables it). Protocol and script handlers now reject an over-limit body with `413 Request Entity Too Large` rather than processing a truncated payload.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**MCP SSE is exempt from the HTTP write deadline.** For the long-lived `GET /mcp` event stream, Scriptling clears the server write deadline after protocol middleware, so the normal HTTP write timeout no longer ends an otherwise healthy subscription.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Background task startup is race-free.** `runtime.background()` now completes task setup on the caller's goroutine before queuing or starting the task, avoiding concurrent reads of partially prepared state.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`finally` control flow is complete.** `return`, `break`, and `continue` in a `finally` block now propagate correctly; a normal exception raised there replaces an ordinary pending result. `finally` still runs for `SystemExit` and `PermissionError`, but cannot replace those protected exceptions.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Circular imports fail fast.** Two modules importing each other used to re-evaluate forever; the import chain is now tracked and a cycle reports `circular import: a -> b -> a`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Self-referential values convert safely.** A list or dict containing itself crashed host conversion with an unrecoverable stack overflow; it now converts cyclic references to a `<cyclic reference>` marker.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Repetition results are bounded.** `"ab" * n`, `bytes * n`, and `list`/`tuple * n` refuse oversized results with a clear error (1 GiB for strings and bytes, roughly 134 million elements for sequences) instead of allocating unbounded results; a constant-folded repetition no longer panics at parse time.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Release artifacts are built safely for their target platforms.** Cross-platform `scriptling-full` builds now export `GOOS` and `GOARCH`, preventing host binaries from being labeled as another platform. Homebrew formulas are generated to temporary files and atomically moved into place before release tagging, so a failed generator cannot truncate a formula or leave a green release.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Releasing remote objects reports the actual outcome.** Concurrent explicit and GC-finalizer releases now wait for the winning destroy request and return its result instead of reporting success while it may still fail.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Instance destructors get a boundary.** A user-defined `__del__` running on the Go GC finalizer goroutine now has panic recovery and a bounded context, preventing a destructor panic from terminating the host process.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Selected shared options work after subcommands.** Package, cache, library/plugin, logging, filesystem/network-security, and Docker/Podman-host options marked global are accepted before or after nested commands such as `cache clear` and `help`; server-only options remain specific to server invocations.
{{< /changelog-item >}}

---

{{< version "v0.22.0" >}}

{{< changelog-item "added" >}}
**Per-user keys for MCP and JSON-RPC.** The middleware registered with `runtime.http.middleware(...)` now guards the `/mcp` and `/json-rpc` endpoints as well as HTTP routes, so one handler can authenticate API clients, MCP clients, and JSON-RPC callers against whatever it likes, a dict of keys, the KV store, an API. Registering a middleware replaces static `--bearer-token` checking on the protocol endpoints; without one, the static token guards everything as before.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Failed KV disk writes are no longer silent.** With a persistent store (`--kv-storage` or `SCRIPTLING_KV_STORAGE`, and stores opened with `kv.open()`), a snapshot write that failed, disk full, directory deleted, permissions, left no trace: the script reported success and the data was simply gone on the next run. Save failures are now logged with the store path and the cause, and `store.close()` raises the error to the script instead of returning quietly.
{{< /changelog-item >}}
