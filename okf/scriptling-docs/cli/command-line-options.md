---
description: Every CLI flag, environment variable, and configuration file setting.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/cli/command-line-options/
sources:
    - resource: https://scriptling.dev/docs/cli/command-line-options/
status: stable
tags:
    - cli
title: Command Line Options
type: Guide
---
# Command Line Options

## Command Line Options

Give these options before the script file: everything after it is passed to the script in `sys.argv` (see [Pass Arguments to a Script](https://scriptling.dev/okf/scriptling-docs/cli/basic-usage.md#pass-arguments-to-a-script)).

| Flag                  | Env Variable               | Config Path                  | Description                                          | Default          |
| --------------------- | -------------------------- | ---------------------------- | ---------------------------------------------------- | ---------------- |
| `-C`, `--config`      | `SCRIPTLING_CONFIG`        | -                            | Path to configuration file                           | see below        |
| `-i`, `--interactive` | -                          | -                            | Start interactive mode                               | -            |
| `-c`, `--code`        | -                          | -                            | Execute inline code string                           | -                |
| `-l`, `--lint`        | -                          | -                            | Lint script files without executing                  | -            |
| `--lint-format`       | `SCRIPTLING_LINT_FORMAT`   | `lint.format`                | Output format for lint (text/json)                   | text             |
| `-p`, `--package`     | -                          | `packages`                   | Package directory, zip, or HTTP(S) URL (repeatable) | (none)           |
| `-k`, `--insecure`    | -                          | `insecure`                   | Allow self-signed HTTPS certificates                 | false            |
| `--cache-dir`         | `SCRIPTLING_CACHE_DIR`     | `cache.dir`                  | Cache directory for remote packages                  | OS default       |
| `--program-cache-max-bytes` | `SCRIPTLING_PROGRAM_CACHE_MAX_BYTES` | `cache.program_max_bytes` | Memory budget for parsed scripts kept in memory (bytes; 0 = default, negative = unlimited) | 64 MiB |
| `--memory-limit` | `SCRIPTLING_MEMORY_LIMIT` | `limits.memory_bytes` | Estimated memory each interpreter may hold (bytes; 0 = no limit) | 0 |
| `--max-value-bytes` | `SCRIPTLING_MAX_VALUE_BYTES` | `limits.max_value_bytes` | Largest single string, bytes value or container (list, tuple, dict, set) one operation may create (bytes; 0 = no limit). Separate from the fixed 1 GiB cap on a single repetition or padding width, which always applies | 0 |
| `--max-background-tasks` | `SCRIPTLING_MAX_BACKGROUND_TASKS` | `limits.max_background_tasks` | Most `runtime.background` tasks each interpreter may have queued or running at once; one more raises `RuntimeError` (0 = no limit) | 0 |
| `-L`, `--libpath`     | `SCRIPTLING_LIBPATH`       | `libpath`                    | Extra library search directory (repeatable)          | (none)           |
| `--plugin-dir`       | `SCRIPTLING_PLUGIN_DIR`    | `plugins.dirs`               | Plugin executable directory (repeatable)             | (none)           |
| `--plugin`           | `SCRIPTLING_PLUGIN`        | `plugins.paths`              | Plugin executable to load, path taken literally (repeatable) | (none) |
| `--plugin-arg`       | `SCRIPTLING_PLUGIN_ARG`    | `plugins.args`               | Argument to pass to a `--plugin` executable (repeatable)   | (none)           |
| `--plugin-env`       | `SCRIPTLING_PLUGIN_ENV`    | `plugins.env`                | KEY=VALUE environment entry for a `--plugin` executable (repeatable) | (none) |
| `--plugin-header`    | `SCRIPTLING_PLUGIN_HEADER` | `plugins.headers`            | HTTP header KEY=VALUE for an http(s) `--plugin` (repeatable) | (none) |
| `--plugin-insecure`  | `SCRIPTLING_PLUGIN_INSECURE` | `plugins.insecure`         | Mark this https:// `--plugin` URL as insecure, skipping TLS verification (repeatable) | (none) |
| `--log-level`         | `SCRIPTLING_LOG_LEVEL`     | `log.level`                  | Log level (trace/debug/info/warn/error)              | info             |
| `--log-format`        | `SCRIPTLING_LOG_FORMAT`    | `log.format`                 | Log format (console/json/null)                       | console          |
| `-S`, `--server`      | `SCRIPTLING_SERVER`        | `server.address`             | HTTP server address (host:port)                      | (disabled)       |
| `--web-root`          | `SCRIPTLING_WEB_ROOT`      | `server.web_root`            | Directory to serve static files from                 | (disabled)       |
| `--json-rpc`          | `SCRIPTLING_JSONRPC`       | -                            | JSON-RPC server mode: stdio by default, HTTP `/json-rpc` with `--server` | false            |
| `--mcp-tools`         | `SCRIPTLING_MCP_TOOLS`     | `mcp.tools`                  | Directory containing MCP tools                       | (disabled)       |
| `--mcp-exec-script`   | `SCRIPTLING_MCP_EXEC_SCRIPT` | `mcp.exec_script`          | Enable MCP script execution tool; over HTTP requires `--bearer-token` or `--oidc-issuer` | false            |
| `--mcp-resources`     | `SCRIPTLING_MCP_RESOURCES` | `mcp.resources`              | Directory containing MCP resources                   | (disabled)       |
| `--mcp-prompts`       | `SCRIPTLING_MCP_PROMPTS`   | `mcp.prompts`                | Directory containing MCP prompts                     | (disabled)       |
| `--bearer-token`      | `SCRIPTLING_BEARER_TOKEN`  | `server.bearer_token`        | Bearer token for authentication                      | none             |
| `--oidc-issuer`       | `SCRIPTLING_OIDC_ISSUER`   | `server.oidc_issuer`         | Accept OAuth JWT access tokens from this identity provider (issuer URL); with `--bearer-token`, either is accepted | none |
| `--oidc-jwks-url`     | `SCRIPTLING_OIDC_JWKS_URL` | `server.oidc_jwks_url`       | Identity provider JWKS URL                           | discovered from the issuer |
| `--oidc-audience`     | `SCRIPTLING_OIDC_AUDIENCE` | `server.oidc_audience`       | This server's resource identifier: the public URL of its `/mcp` endpoint, which tokens' `aud` must name (required with `--oidc-issuer`) | none |
| `--oidc-required-scopes` | `SCRIPTLING_OIDC_REQUIRED_SCOPES` | `server.oidc_required_scopes` | Scopes every identity-provider token must grant (comma or space separated) | none |
| `--oidc-require-at-jwt` | `SCRIPTLING_OIDC_REQUIRE_AT_JWT` | `server.oidc_require_at_jwt` | Require RFC 9068 access tokens (JWT `typ` `at+jwt`), refusing ID tokens | false |
| `--oidc-ca-file` | `SCRIPTLING_OIDC_CA_FILE` | `server.oidc_ca_file` | PEM file of CA certificates trusted (with the system roots) for the identity provider's discovery and JWKS fetches | none |
| `--oidc-tls-insecure` | `SCRIPTLING_OIDC_TLS_INSECURE` | `server.oidc_tls_insecure` | Skip TLS certificate verification for the identity provider's discovery and JWKS fetches (development only) | false |
| `--max-request-body`  | `SCRIPTLING_MAX_REQUEST_BODY` | `server.max_request_body` | Maximum HTTP request body in bytes (0 = 32MiB, negative = unlimited) | 0 (32MiB)        |
| `--json-rpc-max-batch` | `SCRIPTLING_JSONRPC_MAX_BATCH` | `server.json_rpc_max_batch` | Maximum elements in one JSON-RPC batch; a larger batch gets one Invalid Request error (0 = 1000, negative = unlimited, e.g. `--json-rpc-max-batch=-1`) | 0 (1000) |
| `--json-rpc-concurrency` | `SCRIPTLING_JSONRPC_CONCURRENCY` | `server.json_rpc_concurrency` | Maximum JSON-RPC handlers running at once across all batches, requests and streams (0 = 4 × CPUs, negative = unlimited) | 0 (4 × CPUs) |
| `--websocket-origin`  | `SCRIPTLING_WEBSOCKET_ORIGIN` | `server.websocket_origins` | Allowed browser origin for WebSocket upgrades (repeatable, `*` for any) | same-origin      |
| `--mcp-cors-origin`   | `SCRIPTLING_MCP_CORS_ORIGIN` | `server.mcp_cors_origins`  | Allowed browser origin for cross-origin MCP requests on `/mcp` (repeatable, `*` for any) | same-origin      |
| `--json-rpc-cors-origin` | `SCRIPTLING_JSONRPC_CORS_ORIGIN` | `server.json_rpc_cors_origins` | Allowed browser origin for cross-origin requests to `/json-rpc` (repeatable, `*` for any); other origins get `403` | same-origin |
| `--allowed-hosts`     | `SCRIPTLING_ALLOWED_HOSTS` | `server.allowed_hosts`     | Host name the HTTP server answers (repeatable; `.example.com` or `*.example.com` for a domain and its subdomains; a port is ignored). A loopback-bound server answers only loopback names plus these. Any other bind answers every `Host` until this is set; then it answers loopback names, IP addresses, its own host name and these, and refuses the rest with `421`, blocking DNS rebinding | loopback binds: loopback names only; other binds: every `Host` |
| `--allowed-paths`     | `SCRIPTLING_ALLOWED_PATHS` | `security.allowed_paths`     | Restrict participating library filesystem I/O; `-` denies it entirely | (no restriction) |
| `--network-policy`    | `SCRIPTLING_NETWORK_POLICY`| `security.network_policy`    | TOML network policy file for script outbound access  | (no restriction) |
| `--disable-lib`       | `SCRIPTLING_DISABLE_LIB`   | `security.disable_libs`      | Disable a built-in library by name (repeatable), including a single runtime sub-library such as `scriptling.runtime.kv` ([details](https://scriptling.dev/okf/scriptling-docs/cli/libraries.md#disable-specific-libraries)) | (none)           |
| `--no-subprocess`   | `SCRIPTLING_NO_SUBPROCESS` | `security.no_subprocess`     | Same as `--disable-lib subprocess`: removes the `subprocess` library and refuses stdio MCP servers in `scriptling.mcp` and script-driven executable `scriptling.plugin.load()`; applies to every command, `help` included | false |
| `--list-libs`         | -                          | -                            | Print the CLI's current built-in inventory and exit  | -            |
| `--kv-storage`        | `SCRIPTLING_KV_STORAGE`    | `kv.storage`                 | Directory for persistent KV store                    | (in-memory)      |
| `--deny-become` | `SCRIPTLING_DENY_BECOME` | `security.deny_become` | Refuse provisioning steps run as root with `become=True`. They are allowed by default, through `sudo` (no prompt where sudo needs no password; otherwise asked once on the terminal), and refused whenever the subprocess library is disabled. See [Running as Root](https://scriptling.dev/okf/scriptling-libraries/provisioning.md#running-as-root) | false (allowed) |
| `--container-deny-privileged` | `SCRIPTLING_CONTAINER_DENY_PRIVILEGED` | `container.deny_privileged` | Refuse `scriptling.container` `run(privileged=True)` | false (allowed) |
| `--docker-host`       | `DOCKER_HOST`              | `container.docker_host`      | Docker endpoint (socket path, tcp://, https://)      | `/var/run/docker.sock` |
| `--podman-host`       | `CONTAINER_HOST`           | `container.podman_host`      | Podman endpoint (socket path or unix:// URI)         | `/var/run/podman.sock` |
| `--secret-config`     | `SCRIPTLING_SECRET_CONFIG` | `secret.config`              | TOML file for secret provider aliases                | none             |
| `--tls-cert`          | `SCRIPTLING_TLS_CERT`      | `tls.cert`                   | TLS certificate file                                 | none             |
| `--tls-key`           | `SCRIPTLING_TLS_KEY`       | `tls.key`                    | TLS key file                                         | none             |
| `--tls-generate`      | -                          | `tls.generate`               | Generate self-signed certificate                     | false            |

The [network policy](https://scriptling.dev/okf/scriptling-docs/cli/network-policy.md) flag has its own page with the policy file reference.

## Loading Plugins {#loading-plugins}

Plugins come from two places, and both can be repeated:

- `--plugin-dir` scans a directory and loads every executable in it.
- `--plugin` loads one plugin: an executable path, or the `http://`/`https://`
  URL of a plugin server, where the plugin protocol speaks JSON-RPC over POST
  instead of stdio (the same plugin either way; a
  [PHP example](https://github.com/paularlott/scriptling/tree/main/examples/plugins/php-server)
  shows how little it takes to serve one).

A `--plugin` value is used literally, so a path containing spaces needs nothing
beyond ordinary shell quoting:

```bash
scriptling --plugin "/Applications/Knot.app/Contents/MacOS/knot" script.py
```

Arguments for a plugin come from `--plugin-arg`, applied in the order given:

```bash
scriptling --plugin /usr/local/bin/knot \
           --plugin-arg scriptling-server \
           --plugin-arg=--alias=testing \
           script.py
```

Values that begin with `-` need the `--plugin-arg=value` form, otherwise the
parser reads them as another flag.

With one `--plugin`, every `--plugin-arg` belongs to it. With several, qualify
each argument as `<plugin>=<arg>`, where `<plugin>` is the executable's base
name or its full path:

```bash
scriptling --plugin /usr/local/bin/knot --plugin /usr/local/bin/vault-helper \
           --plugin-arg knot=scriptling-server \
           --plugin-arg vault-helper=--role=reader \
           script.py
```

An unqualified argument with more than one plugin is an error rather than a
guess. A value whose text before `=` matches no `--plugin` is treated as a
plain argument, so ordinary flags like `--alias=testing` pass through
unqualified.

Environment variables reach an executable plugin with `--plugin-env`, binding
exactly like `--plugin-arg` with `KEY=VALUE` payloads:

```bash
scriptling --plugin /usr/local/bin/knot            --plugin-env KNOT_DB=/var/lib/knot            --plugin-env LOG=debug            script.py
```

The entries layer on top of the inherited environment, so a variable already
set is overridden and everything else passes through. They apply to executable
plugins, which the host spawns; a plugin server owns its own environment,
since the host connects to it.

An HTTP plugin that needs authentication takes headers with
`--plugin-header`, binding like the other plugin flags (bare with one plugin,
`<plugin>=` qualified with several); the value keeps its own equals sign, so
bearer tokens pass through whole. The token does not belong on the command
line, where it is visible in process listings: prefer the environment
variable or the config file, both of which accept the same values:

```bash
export SCRIPTLING_PLUGIN_HEADER="Authorization=Bearer $PLUGIN_TOKEN"
scriptling --plugin https://plugins.internal:8443 script.py
```

```toml
# scriptling.toml
[plugins]
paths = ["https://plugins.internal:8443"]
headers = ["Authorization=Bearer eyJ..."]
```

The flag form exists for quick tests:

```bash
scriptling --plugin https://plugins.internal:8443 \
           --plugin-header "Authorization=Bearer $PLUGIN_TOKEN" \
           script.py
```

Username and password can also ride the URL itself, as HTTP Basic auth:

```bash
scriptling --plugin https://user:pass@plugins.internal:8443 script.py
```

The credentials travel as the Authorization header and never appear in the
request line or Host header; an explicit `--plugin-header Authorization=...`
wins over URL credentials.

For https plugin URLs whose certificate is self-signed (development, internal
networks), `--plugin-insecure` names the URLs to load without certificate
verification, so one self-signed endpoint never weakens the others:

```bash
scriptling --plugin https://plugins.internal:8443 \
           --plugin-insecure https://plugins.internal:8443 \
           script.py
```

Explicit `--plugin` entries load before `--plugin-dir` scans. Plugin identity
is the resolved executable path, so the same binary found in a scanned
directory is skipped — the explicit entry and its arguments win. Plugins
register under the library name they declare in their handshake, however they
were loaded.

Plugins only start when the invocation can use them. `--lint`, `--list-libs`,
and the `pack`, `unpack` and `cache` subcommands never spawn plugin
processes.

## Configuration File

Scriptling looks for `scriptling.toml` in the following locations (in order):

1. Current directory (`.`)
2. `$HOME/`
3. `$HOME/.config/scriptling/`

Use `--config` (or `-C`) to specify a different path explicitly.

All flags that have a config path can be set in the file. The TOML structure mirrors the config paths shown in the flags table above:

```toml
# scriptling.toml

# Root-level options must appear before the first [table].
libpath = ["/shared/libs", "/company/libs"]
packages = ["./mypackage.zip", "https://example.com/lib.zip"]
insecure = false

[log]
level = "debug"
format = "console" # console, json, or null

[limits]
memory_bytes = 268435456     # 0 = no limit
max_value_bytes = 67108864   # 0 = no limit
max_background_tasks = 100   # 0 = no limit

[plugins]
dirs = ["/usr/local/lib/scriptling/plugins"]
paths = ["/usr/local/bin/knot"]
args = ["scriptling-server", "--alias=testing"]
env = ["KNOT_DB=/var/lib/knot"]
headers = ["Authorization=Bearer token"]
insecure = ["https://plugins.internal:8443"]

[server]
address = ":8000"
web_root = "./public"
bearer_token = "secret"
# oidc_issuer = "https://idp.example.com/realms/acme"
# oidc_audience = "https://mcp.example.com/mcp"
# oidc_required_scopes = "mcp:use"
allowed_hosts = ["app.example.com", ".internal.example.com"]
json_rpc_cors_origins = ["https://app.example.com"]
json_rpc_max_batch = 0       # 0 = 1000, negative = unlimited
json_rpc_concurrency = 0     # 0 = 4 x CPUs, negative = unlimited

[mcp]
tools = "./tools"
exec_script = false
resources = "./resources"
prompts = "./prompts"

[security]
allowed_paths = "/tmp/data,./uploads"
network_policy = "./network-policy.toml"
disable_libs = ["subprocess", "os"]
no_subprocess = false        # true is the same as listing "subprocess" in disable_libs

[kv]
storage = "/var/lib/scriptling/kv"

[container]
docker_host = "unix:///Users/paul/.lima/docker/sock/docker.sock"
podman_host = "unix:///run/user/1000/podman/podman.sock"
deny_privileged = false   # true refuses run(privileged=True)

[secret]
config = "/etc/scriptling/secrets.toml"

[tls]
cert = "/etc/scriptling/tls.crt"
key = "/etc/scriptling/tls.key"
generate = false

[cache]
dir = "/var/cache/scriptling"
# Parsed and compiled scripts are kept in memory so repeated runs skip
# parsing. 0 keeps the 64 MiB default; a negative value removes the limit.
program_max_bytes = 134217728

[lint]
format = "text"
```

Priority order (highest to lowest): **command-line flag** > **environment variable** > **config file** > **default**.

## Container Endpoints {#container-endpoints}

When using the `scriptling.container` library, Docker and Podman endpoints can be configured via flags or environment variables. Both accept any of the following forms:

| Form | Example |
|---|---|
| Unix socket path | `/var/run/docker.sock` |
| Unix socket URI | `unix:///var/run/docker.sock` |
| TCP (Docker only) | `tcp://192.168.1.10:2375` or `192.168.1.10:2375` |
| TLS TCP (Docker only) | `https://192.168.1.10:2376` |

Podman does not expose a plain TCP endpoint: use a Unix socket path or URI. For remote Podman, use `podman system service` with SSH tunnelling and point the socket at the local tunnel endpoint.

```bash
scriptling --docker-host unix:///Users/paul/.lima/docker/sock/docker.sock script.py
scriptling --docker-host tcp://192.168.1.10:2375 script.py
scriptling --podman-host unix:///run/user/1000/podman/podman.sock script.py
```
