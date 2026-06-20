---
title: Library Registration
description: How to register built-in libraries when embedding Scriptling in Go.
weight: 14
---

When embedding Scriptling in a Go application, you control which libraries are available to scripts. Libraries are not loaded unless you explicitly register them.

## Standard Libraries

22 built-in libraries available without any configuration.

### Register All at Once

```go
import "github.com/paularlott/scriptling/stdlib"

stdlib.RegisterAll(p)
```

### Register Individually

```go
p.RegisterLibrary(stdlib.JSONLibrary)
p.RegisterLibrary(stdlib.MathLibrary)
p.RegisterLibrary(stdlib.ReLibrary)
p.RegisterLibrary(stdlib.TimeLibrary)
```

| Namespace | Constant |
|-----------|----------|
| `base64` | `Base64Library` |
| `collections` | `CollectionsLibrary` |
| `contextlib` | `ContextlibLibrary` |
| `datetime` | `DatetimeLibrary` |
| `difflib` | `DifflibLibrary` |
| `functools` | `FunctoolsLibrary` |
| `hashlib` | `HashlibLibrary` |
| `html` | `HTMLLibrary` |
| `io` | `IOLibrary` |
| `itertools` | `ItertoolsLibrary` |
| `json` | `JSONLibrary` |
| `math` | `MathLibrary` |
| `platform` | `PlatformLibrary` |
| `random` | `RandomLibrary` |
| `re` | `ReLibrary` |
| `statistics` | `StatisticsLibrary` |
| `string` | `StringLibrary` |
| `textwrap` | `TextwrapLibrary` |
| `time` | `TimeLibrary` |
| `urllib` | `URLLibLibrary` |
| `urllib.parse` | `URLParseLibrary` |
| `uuid` | `UUIDLibrary` |

## Extended Libraries

These are in the root `extlibs` package and provide Python-compatible functionality.

### Simple Registration

```go
import "github.com/paularlott/scriptling/extlibs"

extlibs.RegisterRequestsLibrary(p)
extlibs.RegisterYAMLLibrary(p)
extlibs.RegisterTOMLLibrary(p)
extlibs.RegisterSecretsLibrary(p)
extlibs.RegisterSubprocessLibrary(p)
extlibs.RegisterHTMLParserLibrary(p)
```

| Namespace | Function |
|-----------|----------|
| `requests` | `RegisterRequestsLibrary(p)` |
| `yaml` | `RegisterYAMLLibrary(p)` |
| `toml` | `RegisterTOMLLibrary(p)` |
| `secrets` | `RegisterSecretsLibrary(p)` |
| `subprocess` | `RegisterSubprocessLibrary(p)` |
| `html.parser` | `RegisterHTMLParserLibrary(p)` |

### Filesystem Libraries

These accept `allowedPaths` to restrict filesystem access. Pass `nil` for unrestricted access.

```go
extlibs.RegisterOSLibrary(p, []string{"/tmp", "/data"})
extlibs.RegisterPathlibLibrary(p, []string{"/tmp", "/data"})
extlibs.RegisterFSLibrary(p, []string{"/tmp", "/data"})
extlibs.RegisterGlobLibrary(p, []string{"/tmp", "/data"})
extlibs.RegisterGrepLibrary(p, []string{"/tmp"})
extlibs.RegisterSedLibrary(p, []string{"/tmp"})
```

| Namespace | Function |
|-----------|----------|
| `os` + `os.path` | `RegisterOSLibrary(p, allowedPaths)` |
| `pathlib` | `RegisterPathlibLibrary(p, allowedPaths)` |
| `fs` | `RegisterFSLibrary(p, allowedPaths)` |
| `glob` | `RegisterGlobLibrary(p, allowedPaths)` |
| `scriptling.grep` | `RegisterGrepLibrary(p, allowedPaths)` |
| `scriptling.sed` | `RegisterSedLibrary(p, allowedPaths)` |

### Custom Configuration

```go
// sys — requires argv and stdin
extlibs.RegisterSysLibrary(p, []string{"script.py"}, os.Stdin)

// logging — requires a logger instance (or use default)
extlibs.RegisterLoggingLibraryDefault(p)
// or with custom logger:
// extlibs.RegisterLoggingLibrary(p, myLogger)

// secrets provider — requires a secret registry
extlibs.RegisterSecretLibrary(p, registry)

// wait_for, websocket, templates
extlibs.RegisterWaitForLibrary(p)
extlibs.RegisterWebSocketLibrary(p)
extlibs.RegisterTemplateHTMLLibrary(p)
extlibs.RegisterTemplateTextLibrary(p)
```

| Namespace | Function |
|-----------|----------|
| `sys` | `RegisterSysLibrary(p, argv []string, stdin io.Reader)` |
| `logging` | `RegisterLoggingLibrary(p, logger)` or `RegisterLoggingLibraryDefault(p)` |
| `scriptling.secret` | `RegisterSecretLibrary(p, registry *secretprovider.Registry)` |
| `scriptling.wait_for` | `RegisterWaitForLibrary(p)` |
| `scriptling.net.websocket` | `RegisterWebSocketLibrary(p)` |
| `scriptling.template.html` | `RegisterTemplateHTMLLibrary(p)` |
| `scriptling.template.text` | `RegisterTemplateTextLibrary(p)` |

## Runtime Libraries

Background tasks, HTTP routing, key-value store, concurrency, and sandboxing.

```go
// Register all runtime libraries at once
extlibs.RegisterRuntimeLibraryAll(p, []string{"/tmp"})

// Or register individually
extlibs.RegisterRuntimeLibrary(p)          // scriptling.runtime (background tasks)
extlibs.RegisterRuntimeHTTPLibrary(p)      // scriptling.runtime.http
extlibs.RegisterRuntimeKVLibrary(p)        // scriptling.runtime.kv
extlibs.RegisterRuntimeSyncLibrary(p)      // scriptling.runtime.sync
extlibs.RegisterRuntimeSandboxLibrary(p, []string{"/tmp"})  // scriptling.runtime.sandbox
```

| Namespace | Function |
|-----------|----------|
| `scriptling.runtime` | `RegisterRuntimeLibrary(p)` |
| All runtime libs | `RegisterRuntimeLibraryAll(p, allowedPaths)` |
| `scriptling.runtime.http` | `RegisterRuntimeHTTPLibrary(p)` |
| `scriptling.runtime.kv` | `RegisterRuntimeKVLibrary(p)` or `RegisterRuntimeKVLibraryWithSecurity(p, allowedPaths)` |
| `scriptling.runtime.sync` | `RegisterRuntimeSyncLibrary(p)` |
| `scriptling.runtime.sandbox` | `RegisterRuntimeSandboxLibrary(p, allowedPaths)` |

## Scriptling-Specific Libraries

These live in subpackages under `extlibs/` and each expose a `Register` function.

### AI & Agent

```go
import (
    "github.com/paularlott/scriptling/extlibs/ai"
    "github.com/paularlott/scriptling/extlibs/agent"
    aimemory "github.com/paularlott/scriptling/extlibs/ai/memory"
    aitools "github.com/paularlott/scriptling/extlibs/ai/tools"
)

ai.Register(p)                  // scriptling.ai
agent.Register(p)               // scriptling.ai.agent (returns error)
agent.RegisterInteract(p)       // scriptling.ai.agent.interact (returns error)
aimemory.Register(p)            // scriptling.ai.memory
aitools.Register(p)             // scriptling.ai.tools
```

| Namespace | Import Path | Call |
|-----------|-------------|------|
| `scriptling.ai` | `extlibs/ai` | `ai.Register(p)` |
| `scriptling.ai.agent` | `extlibs/agent` | `agent.Register(p)` |
| `scriptling.ai.agent.interact` | `extlibs/agent` | `agent.RegisterInteract(p)` |
| `scriptling.ai.memory` | `extlibs/ai/memory` | `memory.Register(p)` |
| `scriptling.ai.tools` | `extlibs/ai/tools` | `tools.Register(p)` |

### MCP Protocol & TOON

```go
import "github.com/paularlott/scriptling/extlibs/mcp"

mcp.Register(p)             // scriptling.mcp
mcp.RegisterToolHelpers(p)  // scriptling.mcp.tool
mcp.RegisterToon(p)         // scriptling.toon
```

| Namespace | Call |
|-----------|------|
| `scriptling.mcp` | `mcp.Register(p)` |
| `scriptling.mcp.tool` | `mcp.RegisterToolHelpers(p)` |
| `scriptling.toon` | `mcp.RegisterToon(p)` |

### Networking

```go
import (
    "github.com/paularlott/scriptling/extlibs/net/resolve"
    "github.com/paularlott/scriptling/extlibs/net/multicast"
    "github.com/paularlott/scriptling/extlibs/net/unicast"
    "github.com/paularlott/scriptling/extlibs/net/gossip"
)

resolve.Register(p, myResolver) // scriptling.net.resolve (requires a Resolver implementation)
multicast.Register(p)       // scriptling.net.multicast
unicast.Register(p)         // scriptling.net.unicast
gossip.Register(p, nil)     // scriptling.net.gossip (nil = null logger)
```

| Namespace | Import Path | Call |
|-----------|-------------|------|
| `scriptling.net.resolve` | `extlibs/net/resolve` | `resolve.Register(p, resolver)` |
| `scriptling.net.multicast` | `extlibs/net/multicast` | `multicast.Register(p)` |
| `scriptling.net.unicast` | `extlibs/net/unicast` | `unicast.Register(p)` |
| `scriptling.net.gossip` | `extlibs/net/gossip` | `gossip.Register(p, logger)` |

### Messaging

```go
import (
    "github.com/paularlott/scriptling/extlibs/messaging/console"
    "github.com/paularlott/scriptling/extlibs/messaging/telegram"
    "github.com/paularlott/scriptling/extlibs/messaging/discord"
    "github.com/paularlott/scriptling/extlibs/messaging/slack"
)

console.Register(p, nil)    // scriptling.messaging.console
telegram.Register(p, nil)   // scriptling.messaging.telegram
discord.Register(p, nil)    // scriptling.messaging.discord
slack.Register(p, nil)      // scriptling.messaging.slack
```

| Namespace | Import Path | Call |
|-----------|-------------|------|
| `scriptling.messaging.console` | `extlibs/messaging/console` | `console.Register(p)` |
| `scriptling.messaging.telegram` | `extlibs/messaging/telegram` | `telegram.Register(p, logger)` |
| `scriptling.messaging.discord` | `extlibs/messaging/discord` | `discord.Register(p, logger)` |
| `scriptling.messaging.slack` | `extlibs/messaging/slack` | `slack.Register(p, logger)` |

### Utilities

```go
import (
    "github.com/paularlott/scriptling/extlibs/console"
    "github.com/paularlott/scriptling/extlibs/container"
    "github.com/paularlott/scriptling/extlibs/similarity"
    "github.com/paularlott/scriptling/extlibs/provision/fetch"
    "github.com/paularlott/scriptling/extlibs/provision/file"
)

console.Register(p)                        // scriptling.console
container.Register(p, "", "")              // scriptling.container (empty = default sockets)
similarity.Register(p)                     // scriptling.similarity
file.Register(p)                           // scriptling.provision.file
fetch.Register(p)                          // scriptling.provision.fetch
```

| Namespace | Import Path | Call |
|-----------|-------------|------|
| `scriptling.console` | `extlibs/console` | `console.Register(p)` |
| `scriptling.container` | `extlibs/container` | `container.Register(p, dockerSock, podmanSock)` |
| `scriptling.similarity` | `extlibs/similarity` | `similarity.Register(p)` |
| `scriptling.provision.file` | `extlibs/provision/file` | `file.Register(p)` |
| `scriptling.provision.fetch` | `extlibs/provision/fetch` | `fetch.Register(p)` |

## Security Considerations

When embedding Scriptling, you have full control over what scripts can access. See the [Security Guide](../security/) for best practices.

**Never register these libraries when running untrusted code:**

- `subprocess` — allows arbitrary command execution
- `sys` — provides access to environment variables and system internals
- `scriptling.runtime.sandbox` — can execute arbitrary code
- `scriptling.ai.agent` — can execute AI-generated code with tools

## See Also

- [Basics](basics/) — creating interpreters and exchanging variables
- [Security Guide](../security/) — security best practices for embedding
- [Libraries](../../reference/libraries/) — usage reference for all libraries
