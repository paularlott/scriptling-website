---
title: Bash Plugins
description: Implement the plugin JSON-RPC protocol directly from a shell script.
weight: 7
---

A plugin can be any executable that speaks Scriptling's line-delimited JSON-RPC protocol on stdio. This Bash example requires `jq`.

```bash
#!/usr/bin/env bash
set -euo pipefail

while IFS= read -r line; do
  method=$(printf '%s\n' "$line" | jq -r '.method')
  id=$(printf '%s\n' "$line" | jq -r '.id')

  case "$method" in
    scriptling.handshake)
      printf '{"jsonrpc":"2.0","id":%s,"result":{"protocol":"1.0","transport":"json","library":{"name":"hello","version":"1.0.0","description":"Bash hello plugin"},"capabilities":[],"schema":{"functions":[{"name":"greet"}],"classes":[],"constants":[]}}}\n' "$id"
      ;;
    function.call)
      name=$(printf '%s\n' "$line" | jq -r '.params.name')
      if [ "$name" = "greet" ]; then
        who=$(printf '%s\n' "$line" | jq -r '.params.args[0].value')
        jq -nc --argjson id "$id" --arg text "Hello, $who" \
          '{"jsonrpc":"2.0","id":$id,"result":{"type":"string","value":$text}}'
      else
        jq -nc --argjson id "$id" \
          '{"jsonrpc":"2.0","id":$id,"error":{"code":-32601,"message":"unknown function"}}'
      fi
      ;;
    plugin.shutdown)
      printf '{"jsonrpc":"2.0","id":%s,"result":null}\n' "$id"
      exit 0
      ;;
  esac
done
```

Make it executable and run it:

```bash
chmod +x plugins/hello-bash
scriptling --plugin-dir ./plugins -c 'import plugin.hello; print(plugin.hello.greet("Ada"))'
```

The handshake declares the short name `hello`; Scriptling imports it as `plugin.hello`.

## Protocol Methods

The host sends these JSON-RPC methods:

| Method | Direction | Description |
| --- | --- | --- |
| `scriptling.handshake` | host → plugin | Exchange protocol version and schema |
| `environment.open` | host → plugin | Notify plugin of new environment |
| `environment.close` | host → plugin | Notify plugin of environment closing |
| `function.call` | host → plugin | Call a registered function |
| `object.new` | host → plugin | Construct a class instance |
| `object.call_method` | host → plugin | Call a method on an instance |
| `object.destroy` | host → plugin | Destroy an instance |
| `plugin.shutdown` | host → plugin | Graceful shutdown |

Bash is useful for small integrations and protocol tests. For richer plugins with classes and resource cleanup, prefer the Go server package.

See [JSON-RPC Protocol](../protocol/) for the complete method and value encoding reference.
