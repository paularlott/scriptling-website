---
title: Changelog
description: Scriptling release history.
tags: [docs, changelog]
layout: changelog
nav-skip: true
---

## November 2026

{{< version "v0.40.1" >}}

{{< changelog-item "changed" >}}
- Dependencies updated
{{< /changelog-item >}}

---

{{< version "v0.40.0" >}}

{{< changelog-item "changed" >}}
- **Breaking:** Split the Go package `extlibs` into one package per library or family, so an application links only what it registers: registering only YAML used to give a 13.7 MB binary and now gives 6.83 MB. There is no compatibility layer; the old and new names are listed in the [migration table](/docs/go-integration/library-registration/#migrating-from-v039)
- **Breaking:** Make `csv`, `xml`, `html.parser`, `shlex` and `secrets` standard libraries, and move `platform` out to an extension because it reveals the host name ([docs](/docs/security/#standard-libraries))
- **Breaking:** Split `scriptling.runtime.kv` and `scriptling.runtime.http` into their own packages; register each runtime library you want. Both take `allowedPaths`, and `kv.open()` outside them raises the same uncatchable `PermissionError` as the filesystem libraries ([docs](/docs/go-integration/library-registration/#runtime-libraries))
- **Breaking:** Register the Vault and 1Password Connect secret providers explicitly with `vault.Register()` and `onepassword.Register()`, and load policy files with `policyfile.LoadConfig` ([docs](/docs/go-integration/library-registration/#secret-providers))
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Let the CLI disable each runtime sub-library on its own, for example `--disable-lib scriptling.runtime.kv` ([docs](/docs/cli/libraries/#disable-specific-libraries))
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Keep a Mercure client alive while one of its subscriptions is open; an unnamed client's subscription could end when the client was garbage-collected
{{< /changelog-item >}}

---

{{< version "v0.39.0" >}}

{{< changelog-item "added" >}}
- Add `mercure.WithoutSubscribe()` for `mercure.RegisterConfigured()`, to let scripts publish but not receive: `subscribe()` raises `RuntimeError`, which a script can catch to carry on without it ([docs](/reference/libraries/networking/mercure/#security-considerations))
{{< /changelog-item >}}

---

{{< version "v0.38.0" >}}

{{< changelog-item "changed" >}}
- **Breaking:** Close what a script leaves open, Mercure clients and subscriptions, WebSocket connections, stdio MCP servers and zip and tar archives, when its interpreter is done with it: `Reset()` and `ResetEnv()` close them, a background task closes its own when it returns, and anything a script no longer holds closes once collected. They used to stay open until the process exited ([docs](/docs/go-integration/basics/#what-a-script-leaves-open))
- Keep a Mercure subscription open until it or its client is closed; it used to end with the call that made it
- Close what each call left open in MCP tool, resource and prompt handlers and in the server's request handlers, and what the setup script left open when the server stops
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add `Close()` to close what scripts left open in an interpreter you are done with, and `evaluator.TrackResource()` for libraries that open things for scripts ([docs](/docs/go-integration/gc-release-hooks/#resources-a-script-opens))
{{< /changelog-item >}}

{{< changelog-item "removed" >}}
- **Breaking:** Remove `OnReset()` and `mercure.WithLifetime()`, which the interpreter now does for you; `mercure.RegisterConfigured()` takes no options
{{< /changelog-item >}}

---

{{< version "v0.37.0" >}}

{{< changelog-item "changed" >}}
- **Breaking:** Refuse code Python refuses: two statements on one line without `;` (`a = 1b = 2`), and a line indented where no block starts. A script embedded in Go source must start at column 0 ([docs](/reference/syntax/))
- Apply an explicit `mode` in `scriptling.provision.file` to a file whose content is already right, and give the parent directories `ensure_directory()` creates the default mode instead of the one asked for ([docs](/reference/libraries/provisioning/provision-file/))
- Upgrade `scriptling.net.gossip` to gossip v0.31.0: a node takes a reply only from the node it asked and only as the answer to its own request, so a captured reply can't answer a later one. Nodes on v0.36 and earlier send replies it refuses, so upgrade a cluster's nodes together ([docs](/reference/libraries/networking/gossip/))
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add `scriptling.mercure` to publish to and subscribe at Mercure hubs; given the hub's key, clients renew their own tokens so long-running subscriptions never expire ([docs](/reference/libraries/networking/mercure/))
- Add `become=True` to the provisioning libraries to run a step as root through sudo, asked once per script and not at all where sudo needs no password; the CLI refuses it with `--deny-become` or a disabled `subprocess` library ([docs](/reference/libraries/provisioning/#running-as-root))
- Add `scriptling.provision.command` to run commands and `scriptling.provision.package` to install packages with apt, dnf, yum, apk or Homebrew ([docs](/reference/libraries/provisioning/))
- Add `owner` and `group` to `scriptling.provision.file` and `scriptling.provision.fetch`
- Add `OnReset()` and `mercure.WithLifetime()` for embedders, so a pooled interpreter can close what a script left open ([docs](/docs/go-integration/basics/#interpreter-lifecycle))
{{< /changelog-item >}}

---

{{< version "v0.36.1" >}}

{{< changelog-item "added" >}}
- macOS binaries are now signed and notarized.
{{< /changelog-item >}}

---

{{< version "v0.36.0" >}}

{{< changelog-item "changed" >}}
- **Breaking:** Raise `JSONDecodeError` from `json.loads()` and `response.json()` when text follows the JSON value, as Python does; `json.loads("1 2")` used to return `1` ([docs](/reference/libraries/data-formats/json/))
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add each tool's `title` and behaviour hints (`read_only`, `destructive`, `idempotent`, `open_world`) to the MCP client's `tools()`, so scripts can tell which calls to confirm first ([docs](/reference/libraries/mcp/client/#clienttools))
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Return an MCP tool's plain-text reply in full when it only starts like JSON; `2 notes mention milk` came back as the number `2`
{{< /changelog-item >}}

---

{{< version "v0.35.0" >}}

{{< changelog-item "changed" >}}
- **Breaking:** Offer `tool_search` and `execute_tool` only when there are discoverable tools to find
- Report invalid MCP tool arguments to the model as a tool error it can correct, and accept quoted numbers and booleans ([docs](/reference/libraries/runtime/mcp/#parameter-resolution-rules))
- Validate `register_request_tool` arguments before the handler runs, like `@mcp.tool`
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add tool titles and behaviour hints (`read_only`, `destructive`, `idempotent`, `open_world`) so clients know when to ask before calling a tool ([docs](/reference/libraries/runtime/mcp/#title-and-behaviour-hints))
- Add argument completion for prompts and resource templates ([docs](/reference/libraries/runtime/mcp/#argument-completion))
- Add `mcp.tool.progress()` to report progress from long-running handlers ([docs](/reference/libraries/mcp/tool/#progress))
- Add `mcp.notify_resource_updated()` to notify clients subscribed to a resource ([docs](/reference/libraries/runtime/mcp/#resource-update-notifications))
- Add `complete()` to the MCP client ([docs](/reference/libraries/mcp/client/#clientcompleteref-argument-value-contextnone))
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Pass `int` and `float` tool arguments to handlers with the declared type
{{< /changelog-item >}}

---

{{< version "v0.34.0" >}}

{{< changelog-item "changed" >}}
- **Breaking:** Return MCP tool failures as results with `isError` instead of JSON-RPC errors
- **Breaking:** Raise `MCP tool error: <text>` from `call_tool()`, `execute_discovered()` and `mcp.decode_response()` for an `isError` result; the parallel variants put it in `error` ([docs](/reference/libraries/mcp/client/))
- **Breaking:** Refuse MCP tool arguments of the wrong JSON type with `-32602` before the script runs; the `params={"n": "Description"}` shorthand declares a string ([docs](/reference/libraries/runtime/mcp/#parameter-metadata-params))
- **Breaking:** Drop MCP protocol 2024-11-05 from the `scriptling.mcp` client
- Answer refused requests with a `WWW-Authenticate: Bearer` challenge (`401`, or `403` `insufficient_scope`)
- Report the build version in the MCP server's `serverInfo`
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add identity-provider (OAuth / OIDC) authentication to the HTTP server with `--oidc-issuer`, `--oidc-audience`, `--oidc-jwks-url`, `--oidc-required-scopes` and `--oidc-require-at-jwt`; with `--bearer-token`, either credential is accepted ([docs](/docs/cli/http-server/#identity-provider-oauth--oidc))
- Add `--oidc-ca-file` and `--oidc-tls-insecure` for an identity provider with a private or self-signed certificate
- Publish protected resource metadata at `/.well-known/oauth-protected-resource/mcp` when an identity provider is configured
- Add `request.auth` with the caller's `subject`, `audience`, `scopes`, `expiry` and `claims` ([docs](/reference/libraries/runtime/http/#request-object))
{{< /changelog-item >}}

## October 2026

{{< version "v0.33.1" >}}

{{< changelog-item "added" >}}
- Add `verify` to `requests`: `False` accepts any certificate, a path trusts a CA bundle
- Add `scriptling.oauth` for OAuth 2.0 sign-in, tokens and token verification ([docs](/reference/libraries/http-process/oauth/))
{{< /changelog-item >}}

---

{{< version "v0.33.0" >}}

_This release hardens scriptling against hostile scripts and input; read the breaking changes before upgrading._

{{< changelog-item "changed" >}}
- **Breaking:** Stop scripts catching timeouts, cancellations and the memory-limit stop, and stop `with` blocks (including `contextlib.suppress`) suppressing them, `SystemExit` or jail `PermissionError`s
- **Breaking:** Refuse script-driven plugin loads and stdio MCP servers where the `subprocess` library is disabled; `--plugin`, `--plugin-dir` and HTTP(S) plugins are unaffected
- **Breaking:** Enforce the network policy on `net.unicast`, `net.gossip` (TCP only), `nomad`, `wait_for.port`, script-supplied `container` endpoints and every request the Slack, Discord and Telegram libraries make, their platforms' own hosts included; under a strict `allow_hosts`, list the platform hosts you use
- **Breaking:** Apply `deny_cidrs` and the link-local block to `allow_hosts` entries, and require `allow_cidrs` for `multicast` groups under a policy
- **Breaking:** Confine `runtime.http.static` and `runtime.kv.open` to `--allowed-paths`, hiding dotfiles and directory listings when restricted
- **Breaking:** Confine `wait_for` `file`, `dir` and `file_content` checks, messaging `send_file` local files, `provision.fetch` paths and `container.run()` bind mounts to `--allowed-paths`; jail denials raise uncatchable `PermissionError`s, `provision.file`'s included (they were catchable errors), and `network="host"` is refused under a network policy
- **Breaking:** Check the `Host` header on every endpoint of a server bound to loopback (`127.0.0.1`, `[::1]`, `localhost`), blocking DNS rebinding against local servers, and answer any name but a loopback one with `421`. A server bound to any other address (`:8000`, `0.0.0.0`) still answers every `Host` until the new `--allowed-hosts` is set; once set, it answers loopback names, IP addresses, the machine's own host name and the listed names, refusing the rest with `421` ([docs](/docs/cli/http-server/#authentication))
- **Breaking:** Require `--bearer-token` for `--mcp-exec-script` over HTTP, and answer browser requests to `/json-rpc` from other origins with `403`; allowlist browser apps with `--json-rpc-cors-origin`
- **Breaking:** Limit JSON-RPC servers, and plugin servers over HTTP, to batches of 1,000 elements and 4 × CPUs handlers at once; change with `--json-rpc-max-batch` and `--json-rpc-concurrency`
- **Breaking:** Refuse `image_url` values other than `data:` URIs for the Ollama provider instead of fetching them from the host outside the network policy
- **Breaking:** Match Python 3.14 in `html.parser`: valueless attributes are `None`, CDATA goes to `unknown_decl`, and handler exceptions, `sys.exit` and timeouts propagate out of `feed()`; parsing is about 40% faster
- **Breaking:** Return Go panics from `Eval` and every other entry point (`CallFunction`, `CallMethod`, `CreateInstance`, `Import` and `LoadLibraryIntoEnv`) as a `*scriptling.PanicError` reported as `script panic: <value>`, with the Go stack trace in its `Stack` field; `Eval`'s message used to include the stack, and the other entry points did not recover panics
- **Breaking:** Raise `RecursionError` from `msgpack.packb`, `yaml.dump`, `toml.dumps` and `toon.encode` for values nested more than 10,000 levels instead of truncating them, and reject TOML nested more than 100 levels, in `toml.loads` and in network policy and secret config files, script metadata, package manifests and MCP tool metadata
- **Breaking:** Raise `RecursionError` past the call-depth limit instead of a plain `Exception` (`except Exception` still catches it), `TypeError` from `min()` and `max()` for unorderable values, and `ValueError` for a negative `collections.deque` `maxlen`, as Python does
- **Breaking:** Run the Apple `container` CLI from `/usr/local/bin/container` instead of `PATH`, refuse option values that start with `-`, pass script-supplied names, IDs and images after `--`, and list `runtimes()` without starting any process
- Treat container elements that are the same object as equal, as Python does, so a NaN held twice is found by `count()` and `index()`
- Enforce memory limits mid-run and count Go-built lists, tuples, itertools and random results and `lru_cache` growth towards them
- Resolve `--allowed-paths` the way the kernel opens paths so dangling and parent-escaping symlinks cannot leave them, and confine library-loader symlinks to library dirs and allowed paths
- Send messaging bot tokens only to their platform's hosts
- Answer a panic in an HTTP handler with a 500 and log panic stack traces at debug level
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add `--max-background-tasks` to cap an interpreter's queued or running background tasks at once (env `SCRIPTLING_MAX_BACKGROUND_TASKS`, config `limits.max_background_tasks`); off by default. Go hosts use `scriptling.SetMaxBackgroundTasks`, `WithMaxBackgroundTasks` or `p.SetMaxBackgroundTasks`, and `ResourceUsage.BackgroundTasks` counts the live tasks
- Add `--container-deny-privileged` to refuse privileged containers (env and config forms too); off by default
- Complete `collections.deque` as in Python: a real class (`isinstance()` and subclassing work) with `insert()`, `remove()`, `index()`, `reverse()`, item assignment and deletion, comparisons, `+` and `*`, `reversed()` and a read-only `maxlen`
- Add reflected and in-place operator methods (`__radd__`, `__iadd__` and the rest), and `__reversed__` for `reversed()`; as in Python, `str % obj` formats `obj` and never calls `obj.__rmod__`
- Add `object.Equal`, `object.Compare` and `object.SetCompareHooks` so Go-backed classes compare their elements as scripts do
- Add `netsecurity` policy guards (`Guard.CheckHost`, `Guard.Dial`, `Guard.ResolveIPs`, `ErrPolicy`) and `fssecurity` path checks (`Config.CheckPath`, `DeniedError`, `ErrPathNotAllowed`)
- Add Go-integration counterparts to the new restrictions: `extlibs.RegisterWaitForLibraryConfigured`, messaging `RegisterConfigured`/`NewLibraryConfigured`, a network policy argument to `unicast.Register`, `multicast.Register`, `gossip.Register`, `nomad.Register`, `telegram.Register`, `discord.Register` and `slack.Register`, `scriptlingmcp.RegisterConfigured`, `plugin.RegisterLibrariesConfigured` and `plugin.ProcessesAllowed`, `container.RegisterWithOptions`, `container.Options` (with `DenyPrivileged` and `AppleCLI`) and `container.RegisterConfigured`, `libloader.WithAllowedPaths` and `MultiFilesystemLoader.RestrictTo`, `Scriptling.SetPanicHandler`, `conversion.ToGoChecked`, the `ServerConfig` fields for the new server options, and `plugin.Server.SetHTTPLimits` ([docs](/docs/go-integration/library-registration/))
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Fix whole-process crashes from deeply nested or self-referential values: comparing or `repr()` of over-deep values, cyclic containers, and generators that resume generators now raise `RecursionError`; `xml.loads()` and `xml.dumps()` past 1,000 levels raise an error; and over-deep source is a parse error
- Fix `html.parser` panics on `<!-->`, `<!--->`, `<?>` and `&;`
- Fix zip web roots serving members with absolute or `..` names
- Fix `ZipFile`/`TarFile` `extract()` and `extractall()` writing members of any size under a value limit; an oversized member now raises `MemoryError` and leaves nothing on disk
- Fix network-policy host matching for trailing-dot hosts, bare domains under suffix rules and non-canonical numeric hosts
- Fix the Gemini provider exposing its API key in `models()` and `embedding()` error messages
- Fix `scriptling.ai` responses and `ai.collect_stream()` bypassing the interpreter's value and memory limits, and error messages repeating the provider's prefix
- Fix `runtime.background` tasks escaping the memory limit; each live task is now charged `object.TaskBytes` (48 KiB) against it
- Fix `collections.deque` ignoring the memory and value limits, `appendleft()` and `extendleft()` copying the whole deque on every element, and `str()` showing string elements unquoted
- Fix `setattr()` on an instance bypassing property setters, read-only properties and frozen dataclasses
- Fix an exception raised inside a `+` chain that starts with a variable reaching the caller as `TypeError` instead (since 0.20.0)
- Fix `scriptling help` ignoring `--no-subprocess`, so a module it imported to document could run processes
- Fix `scriptling.plugin.load()` registering a plugin over a library already registered under the same name, or over a module the library loader supplies from disk, letting a script replace a host library; it now raises `load(): library <name> is already registered`, and a `--plugin` or `--plugin-dir` plugin under such a name is skipped with a warning
- Fix `os.symlink()` under `--allowed-paths` creating a link whose target lies outside them; the target is resolved from the link's directory and refused with a `PermissionError`
{{< /changelog-item >}}

---

{{< version "v0.32.0" >}}

{{< changelog-item "breaking" >}}
- Return Python's type names from `type(x)` and `x.type()`: `"int"`, `"str"`, `"bool"`, `"NoneType"`, `"list"`, `"dict"`, `"bytes"`, `"function"`, `"method"`, `"builtin_function_or_method"`, `"module"`, `"type"`, `"FloatArray"`, and for iterators `"range"`, `"map"`, `"filter"`, `"zip"`, `"enumerate"`, `"list_iterator"`, `"count"` and so on. The old names (`"INTEGER"`, `"STRING"`, `"NULL"`, `"ITERATOR"`, ...) no longer match, so `type(x) == "INTEGER"` is now `False`; compare with `int`, `"int"` or `isinstance()` instead ([docs](/reference/builtins/#type))
- Match `isinstance()` type-name strings exactly as `type()` reports them: `isinstance(x, "int")` and `isinstance(None, "NoneType")` work, but `"INTEGER"`, `"Int"`, `"None"` and a class name in the wrong case no longer match
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Fix `type(x).__name__` returning scriptling's upper-case name (`"INTEGER"`) instead of Python's (`"int"`)
- Fix `type()` reporting a module as `"DICT"`, a class and `type(int)` as `"CLASS"`/`"BUILTIN"` instead of `"type"`, and a bound method as `"FUNCTION"` instead of `"method"`
- Fix `"INTEGER" == int` and `"STR" == str` comparing equal
{{< /changelog-item >}}

---

{{< version "v0.31.0" >}}

{{< changelog-item "changed" >}}
- **Breaking:** apply `scriptling.SetMemoryLimit` to each interpreter separately instead of the whole process ([docs](/docs/go-integration/basics/#memory-limit))
- Apply the call-depth limit to `CallFunction`, `CallMethod` and `CreateInstance`
- Run `requests.parallel` on a fixed pool of `max_parallel` workers
- Stream files into zip and tar archives instead of reading each into memory
- Build `scriptling.grep`, `scriptling.sed`, `scriptling.find`, `os.listdir` and `csv.loads` results under the interpreter's limits
- Refuse `json.dumps` of a value nested more than 10,000 levels deep
- Force at most one garbage collection per 100 ms for an interpreter over its memory limit
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add per-interpreter memory and value limits, off unless set, and the `MemoryError` exception ([docs](/docs/go-integration/basics/#script-resource-limits))
- Add `WithMemoryLimit` and `WithMaxValueBytes` options to `scriptling.New`, and `p.SetMemoryLimit` and `p.SetMaxValueBytes`
- Add `p.ResourceUsage()` and `p.ShareResourceGuard()`
- Add `--memory-limit` and `--max-value-bytes` CLI options and `limits.*` in `scriptling.toml` ([docs](/docs/cli/command-line-options/))
- Add `object` helpers for libraries that create values from script input: `CheckAlloc`, `CheckElements`, `CheckRoom`, `CheckValue`, `TrackSlice`, `TrackMap`, `ReadAllLimited`, `ReadFileLimited`, `BindGuard`, `CurrentGuard` and `RunFromContext` ([docs](/docs/go-integration/basics/#value-limit))
{{< /changelog-item >}}

{{< changelog-item "removed" >}}
- **Breaking:** remove `scriptling.GetMemoryLimitStats`, `MemoryLimitStats` and `DefaultMemoryLimitCheckInterval`; use `p.ResourceUsage()`
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Fix comprehensions over a huge `range` and `f(*iterator)` ignoring timeouts and allocating their whole result up front
- Fix `secrets.randbits(k)` for k over 63 returning a truncated value; it now raises `OverflowError`
- Fix `str.expandtabs(0)` dividing by zero
- Fix a huge padding or format width, such as `"x".ljust(10**12)`, attempting the allocation; it now raises `MemoryError`
- Fix `requests.parallel` returning an error object instead of a status 0 `Response` for a request that failed before it was sent
- Fix the call-depth counter staying incremented after a call refused for exceeding the limit
- Fix the CLI server starting with its error lost when the setup script fails as the server is signalled to start
- Fix the CLI server resetting its runtime while a previous server's WebSocket handler was still running
{{< /changelog-item >}}

---

{{< version "v0.30.4" >}}

{{< changelog-item "changed" >}}
- Read 1Password Connect secrets in one request instead of three after an item's first lookup, by remembering vault and item ids for 10 minutes
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add 1Password service accounts to the `onepassword` secret provider through the separate [scriptling-onepassword](https://github.com/paularlott/scriptling-onepassword) extension: give `service_account_token` instead of a Connect `address` and `token`; the released CLI supports Connect only ([docs](/reference/libraries/utilities/secret/#1password-service-accounts))
- Add the `scriptlingcmd` package, so a custom CLI with extensions compiled in is a `main.go` calling `scriptlingcmd.Main()` ([docs](/reference/libraries/utilities/secret/#service-accounts-in-embedded-applications-and-custom-builds))
- Add the `scriptling-onepassword` and `scriptling-slim-onepassword` builds, with 1Password service accounts compiled in, to the release and Homebrew ([docs](/docs/quick-start/cli/#1password-builds))
{{< /changelog-item >}}

---

{{< version "v0.30.3" >}}

{{< changelog-item "breaking" >}}
- Pass everything after the script file to the script in `sys.argv`, flags included, so `scriptling tool.py input.json --verbose` works without `--`; give scriptling's own options before the script file. A `--` straight after the file is still accepted and dropped ([docs](/docs/cli/basic-usage/#pass-arguments-to-a-script))
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Fix a script argument that matches a subcommand name, such as `scriptling tool.py cache` or `scriptling tool.py help`, running that subcommand instead of the script
{{< /changelog-item >}}

---

{{< version "v0.30.2" >}}

{{< changelog-item "changed" >}}
- Block reserved address ranges (CGNAT, documentation, benchmarking, NAT64, 6to4 and similar) under a network policy unless `allow_reserved_ips = true` ([docs](/docs/cli/network-policy/))
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add `allow_reserved_ips` network policy option (`AllowReservedIPs` in Go) ([docs](/docs/go-integration/library-registration/#network-policy))
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Accept TLS 1.2 on connections made under a network policy
{{< /changelog-item >}}

---

{{< version "v0.30.0" >}}

{{< changelog-item "breaking" >}}
- Change `client.response_compact(id)` to `client.response_compact(model, previous_response_id=, input=, instructions=)`. It now compacts a conversation into an `output` to continue from, using OpenAI's and xAI's compaction endpoints or, for other providers, a model summary; the old call only stripped reasoning items from a stored response. ([docs](/reference/libraries/ai/client/responses/#clientresponse_compactmodel-previous_response_idnone-inputnone-instructionsnone))
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add Grok (xAI) as a provider: `ai.Client("", provider=ai.GROK, api_key="xai-...")`, using xAI's native Responses API. ([docs](/reference/libraries/ai/client/))
- Add `previous_response_id`, `instructions`, `tools` and `store` to `client.response_create()` and `client.response_stream()`, for multi-turn conversations and tool calling with the Responses API. ([docs](/reference/libraries/ai/client/responses/))
- Add `ai.tool_outputs()` to send tool results back to the Responses API, and read Responses API output in `ai.text()` and `ai.tool_calls()`. ([docs](/reference/libraries/ai/ai/#aitool_outputstool_results))
- Add `client.supports(capability)`, reporting whether a client uses a native (`"responses"`) or emulated (`"responses_emulated"`) Responses API, and supports `"embeddings"` and `"decision"`. ([docs](/reference/libraries/ai/client/#clientsupportscapability))
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
- Continue emulated Responses API conversations (Claude, Gemini, Ollama, Z AI, Mistral) with `previous_response_id`, which was previously ignored, keeping each response's turn in the process for 15 minutes after last use. Responses are only visible to clients with the same provider, base URL and API key.
- Stream tool calls as `function_call` items from emulated `client.response_stream()`, and stream a single response when the client runs `remote_servers` tools on the native Responses API.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Fix native Responses API streaming returning no events, tool calls through the native Responses API failing, and emulated responses ignoring input messages without a `type` field and the `instructions` of a request.
- Fix Ollama tool calls: parallel calls to the same tool sharing an ID, and all but the last of several streamed calls being dropped.
- Fix tool calls without arguments being sent as `"null"` instead of `{}`.
{{< /changelog-item >}}

---

{{< version "v0.29.0" >}}

{{< changelog-item "breaking" >}}
- Evaluate parameter defaults once, at definition, as Python does. A mutable default is now shared between calls.
- Pass `*args` as a tuple instead of a list. Code that modifies `args` must copy it first with `list(args)`.
- Keep every `;`-separated statement of a one-line block inside that block. `def f(): return 1; f()` no longer calls `f`; put the call on its own line.
- Raise `OverflowError` when integer arithmetic passes 64 bits, instead of wrapping.
- Change `json.dumps()` output to Python's format: keys in insertion order (was sorted), `", "` and `": "` separators (was compact), non-ASCII escaped. Use `sort_keys=True`, `separators=(",", ":")` and `ensure_ascii=False` for the old shape. ([docs](/reference/libraries/data-formats/json/))
- Return `UUID` objects from the `uuid` functions instead of strings. Use `str(u)` for the text form.
- Return `bytes` from the `base64` encoders instead of a string.
- Return a `timedelta` from `datetime` and `date` subtraction (was a number), and return a struct from `time.gmtime()` and `time.localtime()` with Python's weekday numbering (Monday is 0).
- Follow `posixpath` in `os.path.dirname()`, `basename()` and `splitext()` for empty paths, trailing slashes and dotfiles.
- Uppercase `ß` as `SS` in `str.upper()`.
- Remove subclassing of `defaultdict`: it is now a function that returns a dict.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
- Iterate dicts in insertion order (was unspecified), including `json.loads()`, `requests` `.json()`, `Counter`, `popitem()` and copies. Dicts built from YAML, TOML, MessagePack and plugin results have sorted keys. ([docs](/reference/types/#dictionary))
- Make dict-building code 10-30% slower than v0.28.0 in return for ordering. Lookups, `get()` and counting are unchanged.
- Deliver `**kwargs` in alphabetical order (was random per call). Call-site order is not kept.
- Rewrite `defaultdict` as an ordinary dict with a default factory: every dict method works, lambda and function factories work, keys keep their types, and it is about twice as fast. ([docs](/reference/libraries/collections-iteration/collections/#defaultdictdefault_factory))
- Make named tuples behave like tuples: indexing, slicing, `len()`, unpacking, ordering, hashing, immutability, keyword construction and `defaults=`.
- Raise catchable Python exceptions: `TypeError` for unhashable keys, unorderable sorts and wrong argument counts, `KeyError` and `IndexError` from `pop()`, the `FileNotFoundError` and `OSError` family from file operations, and Python's types from `assert`, `str.index`, `set.remove` and `min()` of an empty sequence.
- Hash plain instances by identity, and raise `AttributeError` when assigning to a property without a setter.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add generators: `yield` in a function makes a lazy generator that `for`, `list()`, `next()` and `itertools` consume. `yield from` and `send()` are not supported. ([docs](/reference/functions/))
- Add `@dataclass`, `enum.Enum` and `IntEnum`, `functools.lru_cache`, `cache` and `wraps`, user exception classes, and `from typing import ...`.
- Add `obj.__dict__`, a view of an instance's attributes whose writes go through to the object, and make `vars(obj)` the same view. ([docs](/reference/classes/#instance-attributes-as-a-dict-__dict__))
- Add `OrderedDict.move_to_end()` and `popitem(last=False)`, and accept dicts and dict views in `reversed()`.
- Add unpacking forms: `(*a, *b)`, `x = *t, 1`, starred targets in nested groups and `for` headers, `{**d}`, and `f(**d)`. ([docs](/reference/syntax/#assignment))
- Add `/` positional-only parameters, `raise X from e`, `.5` and `1.` float literals, nested and chained assignment targets, and `frozenset`.
- Add `copy.deepcopy()`, `sentinel()`, `csv.DictReader` and `DictWriter`, `math.fsum`, `time.monotonic`, `os.getpid`, number methods such as `bit_count()` and `to_bytes()`, and `int()`, `float()` and `str()` without arguments.
- Add `client.decide()` for Ollama System One decision models. ([docs](/reference/libraries/ai/client/#clientdecidemodel-state-questions-images-keep_alive))
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Fix a subclass's class attribute being discarded when a base class defines the same name.
- Fix arguments written after a `*` unpack being passed before it.
- Fix keyword-only parameters with defaults being unbound when not passed, and a keyword named like a positional-only parameter being rejected when the function takes `**kwargs`.
- Fix `itertools` materialising infinite generators.
- Fix `super().__init__()` failing when no base class defines `__init__`.
- Fix `int(True)`, `float(False)` and `sum()` of booleans, `%g` precision, and UUID comparison and hashing.
{{< /changelog-item >}}

---

{{< version "v0.28.0" >}}

{{< changelog-item "changed" >}}
**Python 3 behaviour.** Objects, modules, printing and formatting now behave as Python 3 does, with Python's error messages, `__getattr__` and `__format__` support, and `getattr()`/`hasattr()` working exactly like dot access. `pathlib.Path` supports `/`. See [Python Differences](/reference/python-differences/).
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Faster imports.** Library files are cached across interpreter instances, so hosts that create an instance per request import 50–77% faster. Edited files are picked up on the next import. See [Loader Chain](/docs/go-integration/loader-chain/#filesystemloader).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Methods as values.** `sorted(words, key=str.lower)`, `map(str.strip, lines)` and `add = items.append` work, and `dir([])` lists methods. See [Built-in Functions](/reference/builtins/#methods-as-values).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Extractive text shortening.** `similarity.extract(text, max_chars=, max_sentences=, ratio=)` keeps the most informative sentences of a long text, in order, using TextRank over hashed word vectors (CPU-only, parallel), and de-duplicates repetitive logs instead of ranking them; `similarity.sentences(text)` is the splitter behind it. Use it where a long text would otherwise be cut at a fixed length before going to a model. See [scriptling.similarity](/reference/libraries/utilities/similarity/#extracttext-max_charsnone-max_sentencesnone-rationone).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Gossip streams.** `cluster.open_stream()` requests a reply of any size from one node and `cluster.handle_stream()` serves it, for files and state transfers beyond the packet limit. Closing a stream, or stopping its cluster, ends a read in progress. See [scriptling.net.gossip](/reference/libraries/networking/gossip/#clusteropen_streamnode_id-message_type-data).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Import syntax.** Parenthesized lists (`from m import (a, b,)`) and PEP 810 `lazy import` are accepted; `lazy` imports run immediately. See [Imports](/reference/syntax/#imports).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**F-strings** with slices (`f"{items[1:3]}"`), `!=`, lambdas or braces inside string literals now evaluate correctly.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`html.escape(s, quote=True)`** gains Python's `quote` argument and escapes a single quote as `&#x27;` (previously `&#39;`), matching CPython.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`similarity.sentences()` and `similarity.tokenize()`** return an empty list for blank text instead of `None`, so the result can always be iterated or measured with `len()`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Standard library matches Python.** `Counter` has the full dict API; keyword arguments such as `re` `flags=`, `int(..., base=)`, `itertools.groupby(key=)`, `random.choices(cum_weights=)` and the `textwrap` options are honoured; bounded `deque`s drop from the opposite end; `json.dumps` writes tuples as arrays; `enumerate()` and `zip()` stop on infinite iterators; `isinstance()` accepts exception types; `dict()` accepts mappings and lets keywords win; TOON integers decode as `int`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`format()`** applies zero padding, fill, sign and grouping like f-strings: `format(42, "05d")` is `"00042"`. Unknown format codes raise `ValueError`, and `#` (`0xff`), `_` grouping, `c` and `n` are supported.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Iterators, comparisons and errors.** `map()`, `filter()`, `any()` and `all()` pull from iterators lazily, so they work with `itertools.count()`, and collecting an endless iterator raises an error instead of exhausting memory. `!=` falls back to `__eq__`; `key=` accepts bound methods and callable objects; `zip(strict=True)` works; `except` accepts a variable or tuple of types and the `LookupError`, `ArithmeticError` and `BaseException` parents; `Counter` takes float counts and compares like Python; `textwrap` splits words exactly as CPython does; `random.sample(range(10**9), k)` no longer expands the range. `itertools.islice()` accepts `None` bounds (`islice(it, 2, None)`) and stops at the right element when given a step. See [Built-in Functions](/reference/builtins/#iteration-utilities) and [Error Handling](/reference/error-handling/#exception-type-hierarchy).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Gossip HTTP transport.** `transport="http"` nodes now serve the gossip endpoint on `bind_addr`; before, they could send but never receive, so HTTP clusters could not form. `encryption_key` is rejected with this transport (use HTTPS), and a node bound to all interfaces needs `advertise_addr`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Apple containers** work with container CLI 1.1 and later (tested on 1.5): image pulls, image and volume listing, container status and image removal. See [scriptling.container](/reference/libraries/utilities/container/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Concurrency.** A data race when starting `runtime.background()` tasks is fixed, and a server no longer loses its setup script's error when an earlier server in the same process is still shutting down.
{{< /changelog-item >}}

---

{{< version "v0.27.3" >}}

{{< changelog-item "fixed" >}}
**Pipeline concurrency recovers after a rate limit.** `client.Pipeline`, `completion_parallel` and `ask_parallel` halve their concurrency when a request hits a 429, but never restored it, so one early rate limit left a long run at reduced parallelism to the end. Concurrency now grows back by one after each run of clean completions, up to `max_parallel`, and slot accounting stays exact while the limit changes. See [AI Client](/reference/libraries/ai/client/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Hosts can cap script fan-out.** `ai.SetMaxParallelLimit(n)` caps the `max_parallel` a script may request from `client.Pipeline`, `completion_parallel` and `ask_parallel`, and `extlibs.SetRequestsMaxParallelLimit(n)` does the same for `requests.parallel`. A script asking for more silently gets the cap; 0 removes it. One atomic load when the pipeline or batch is created, nothing per request. See [Go Integration Basics](/docs/go-integration/basics/#script-resource-limits).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Backslash line continuation.** A backslash at the end of a line joins it to the next, as in Python, so a long condition or assignment can be split without wrapping it in parentheses. The continuation line's indentation is ignored. See [Syntax](/reference/syntax/#explicit-line-continuation).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Process-wide memory guard for script hosts.** `scriptling.SetMemoryLimit(bytes)` sets a ceiling on heap memory held by objects. While the heap stays above it after a garbage collection, the most recently started script is cancelled and its evaluation returns a `memory limit exceeded` error; `scriptling.GetMemoryLimitStats()` reports the heap, running scripts and cancellations. The guard samples the heap on a timer, so it adds no per-instruction cost to scripts. See [Go Integration Basics](/docs/go-integration/basics/#script-resource-limits).
{{< /changelog-item >}}

---

{{< version "v0.27.2" >}}

{{< changelog-item "changed" >}}
**Performance.** Script execution is 15% to 30% faster depending on workload and calls into scripts are up to 20x faster.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Comprehensions are about twice as fast.** List, dict and set comprehensions bind their variable through a slot and iterate `range()` directly.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Function bodies compile on first call.** A module that defines many functions now retains compiled code only for the ones that run, reducing memory for library-heavy hosts.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Program cache budget is configurable.** Parsed and compiled scripts are kept in a process-wide cache bounded by 64 MiB by default. The CLI gains `--program-cache-max-bytes` (`SCRIPTLING_PROGRAM_CACHE_MAX_BYTES`, `cache.program_max_bytes` in `scriptling.toml`), and Go hosts get `scriptling.SetProgramCacheMaxBytes` plus `scriptling.GetProgramCacheStats` for hit, miss and eviction counts. See [Command-Line Options](/docs/cli/command-line-options/) and [Go Integration Basics](/docs/go-integration/basics/#program-cache).
{{< /changelog-item >}}
