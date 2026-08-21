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

| Flag                  | Env Variable               | Config Path                  | Description                                          | Default          |
| --------------------- | -------------------------- | ---------------------------- | ---------------------------------------------------- | ---------------- |
| `-C`, `--config`      | `SCRIPTLING_CONFIG`        | -                            | Path to configuration file                           | see below        |
| `-i`, `--interactive` | -                          | -                            | Start interactive mode                               | -            |
| `-c`, `--code`        | -                          | -                            | Execute inline code string                           | -                |
| `-l`, `--lint`        | -                          | -                            | Lint script files without executing                  | -            |
| `--lint-format`       | `SCRIPTLING_LINT_FORMAT`   | `lint.format`                | Output format for lint (text/json)                   | text             |
| `-p`, `--package`     | -                          | `packages`                   | Package (.zip) path or URL to load (repeatable)      | (none)           |
| `-k`, `--insecure`    | -                          | `insecure`                   | Allow self-signed HTTPS certificates                 | false            |
| `--cache-dir`         | `SCRIPTLING_CACHE_DIR`     | `cache.dir`                  | Cache directory for remote packages                  | OS default       |
| `-L`, `--libpath`     | `SCRIPTLING_LIBPATH`       | `libpath`                    | Extra library search directory (repeatable)          | (none)           |
| `--plugin-dir`       | `SCRIPTLING_PLUGIN_DIR`    | `plugins.dirs`               | Plugin executable directory (repeatable)             | (none)           |
| `--log-level`         | `SCRIPTLING_LOG_LEVEL`     | `log.level`                  | Log level (trace/debug/info/warn/error)              | info             |
| `--log-format`        | `SCRIPTLING_LOG_FORMAT`    | `log.format`                 | Log format (console/json)                            | console          |
| `-S`, `--server`      | `SCRIPTLING_SERVER`        | `server.address`             | HTTP server address (host:port)                      | (disabled)       |
| `--web-root`          | `SCRIPTLING_WEB_ROOT`      | `server.web_root`            | Directory to serve static files from                 | (disabled)       |
| `--json-rpc`          | `SCRIPTLING_JSONRPC`       | -                            | JSON-RPC server mode: stdio by default, HTTP `/json-rpc` with `--server` | false            |
| `--mcp-tools`         | `SCRIPTLING_MCP_TOOLS`     | `mcp.tools`                  | Directory containing MCP tools                       | (disabled)       |
| `--mcp-exec-script`   | `SCRIPTLING_MCP_EXEC_SCRIPT` | `mcp.exec_script`          | Enable MCP script execution tool                     | false            |
| `--bearer-token`      | `SCRIPTLING_BEARER_TOKEN`  | `server.bearer_token`        | Bearer token for authentication                      | none             |
| `--allowed-paths`     | `SCRIPTLING_ALLOWED_PATHS` | `security.allowed_paths`     | Comma-separated allowed filesystem paths             | (no restriction) |
| `--network-policy`    | `SCRIPTLING_NETWORK_POLICY`| `security.network_policy`    | TOML network policy file for script outbound access  | (no restriction) |
| `--no-subprocess`     | `SCRIPTLING_NO_SUBPROCESS` | `security.no_subprocess`     | Do not register the subprocess library               | false            |
| `--disable-lib`       | `SCRIPTLING_DISABLE_LIB`   | `security.disable_libs`      | Disable a built-in library by name (repeatable)      | (none)           |
| `--list-libs`         | -                          | -                            | List available built-in libraries and exit           | -            |
| `--kv-storage`        | `SCRIPTLING_KV_STORAGE`    | `kv.storage`                 | Directory for persistent KV store                    | (in-memory)      |
| `--docker-host`       | `DOCKER_HOST`              | `container.docker_host`      | Docker endpoint (socket path, tcp://, https://)      | `/var/run/docker.sock` |
| `--podman-host`       | `CONTAINER_HOST`           | `container.podman_host`      | Podman endpoint (socket path or unix:// URI)         | `/var/run/podman.sock` |
| `--secret-config`     | `SCRIPTLING_SECRET_CONFIG` | `secret.config`              | TOML file for secret provider aliases                | none             |
| `--tls-cert`          | `SCRIPTLING_TLS_CERT`      | `tls.cert`                   | TLS certificate file                                 | none             |
| `--tls-key`           | `SCRIPTLING_TLS_KEY`       | `tls.key`                    | TLS key file                                         | none             |
| `--tls-generate`      | -                          | `tls.generate`               | Generate self-signed certificate                     | -            |

The [network policy](network-policy.md) flag has its own page with the policy file reference.

## Configuration File

Scriptling looks for `scriptling.toml` in the following locations (in order):

1. Current directory (`.`)
2. `$HOME/`
3. `$HOME/.config/scriptling/`

Use `--config` (or `-C`) to specify a different path explicitly.

All flags that have a config path can be set in the file. The TOML structure mirrors the config paths shown in the flags table above:

```toml
# scriptling.toml

[log]
level = "debug"
format = "console"

libpath = ["/shared/libs", "/company/libs"]

packages = ["./mypackage.zip", "https://example.com/lib.zip"]
insecure = false

[server]
address = ":8000"
bearer_token = "secret"

[mcp]
tools = "./tools"
exec_script = false

[security]
allowed_paths = "/tmp/data,./uploads"
disable_libs = ["subprocess", "os"]

[kv]
storage = "/var/lib/scriptling/kv"

[container]
docker_host = "unix:///Users/paul/.lima/docker/sock/docker.sock"
podman_host = "unix:///run/user/1000/podman/podman.sock"

[secret]
config = "/etc/scriptling/secrets.toml"

[tls]
cert = "/etc/scriptling/tls.crt"
key = "/etc/scriptling/tls.key"
generate = false

[cache]
dir = "/var/cache/scriptling"

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
