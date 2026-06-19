---
title: JSON-RPC Protocol
description: The wire protocol between Scriptling and plugin executables.
weight: 8
---

Plugins communicate with the Scriptling host over line-delimited JSON-RPC 2.0 on stdio. Each frame is a JSON object or JSON-RPC batch array terminated by a newline. The host writes requests to the plugin's stdin and reads responses from the plugin's stdout.

## Wire Envelope

All messages are one of three shapes:

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "function.call",
  "params": { }
}
```

**Response (success):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { }
}
```

**Response (error):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": { "code": -32000, "message": "unknown function greet" }
}
```

The `id` field is a unique integer set by the sender. Every response echoes back the `id` of the request it corresponds to, so both sides can correlate requests and responses on the shared stdio transport. Responses may arrive out of order when a plugin handles overlapping requests. The host assigns incrementing IDs for its requests.

Error codes:

| Code | Meaning |
| --- | --- |
| `-32000` | Application error (function not found, bad arguments, unknown method, etc.) |

## Transport Values

Arguments and return values are encoded as `Value` objects. Exactly one payload
field is set depending on `type`:

```json
{"type": "null"}
```

```json
{"type": "bool", "value": true}
```

```json
{"type": "int", "value": 42}
```

```json
{"type": "float", "value": 3.14}
```

```json
{"type": "string", "value": "hello"}
```

```json
{
  "type": "list",
  "items": [
    {"type": "int", "value": 1},
    {"type": "int", "value": 2}
  ]
}
```

```json
{
  "type": "dict",
  "entries": {
    "name": {"type": "string", "value": "Ada"},
    "age": {"type": "int", "value": 30}
  }
}
```

Callbacks are passed by reference. A callback id is valid only while the outer plugin call that received it is still running:

```json
{
  "type": "callback",
  "callback": {
    "id": "cb-1"
  }
}
```

Remote objects are passed by reference:

```json
{
  "type": "remote",
  "remote": {
    "library": "hello",
    "class": "Config",
    "id": "1"
  }
}
```

## Methods

### `scriptling.handshake`

**Direction:** Host → Plugin
**When:** First message after the plugin process starts.

**Request params:**

| Field | Type | Description |
| --- | --- | --- |
| `protocol` | string | Protocol version, always `"1.0"` |
| `host` | string | Always `"scriptling"` |
| `host_version` | string | Host version string |
| `transports` | [string] | Always `["json"]` |
| `capabilities` | [string] | Host capabilities |

**Response result:**

| Field | Type | Description |
| --- | --- | --- |
| `protocol` | string | Must exactly match the host protocol version, currently `"1.0"` |
| `transport` | string | Must be `"json"` |
| `library` | object | `name`, `version`, `description` |
| `capabilities` | [string] | Plugin capabilities |
| `schema` | object | Functions, classes, and constants |

The `schema` object:

```json
{
  "functions": [
    {
      "name": "greet",
      "source": ""
    }
  ],
  "classes": [
    {
      "name": "Config",
      "constructor": { "name": "Config" },
      "methods": [
        { "name": "get" }
      ],
      "properties": [
        { "name": "name", "settable": true },
        { "name": "label" }
      ]
    }
  ],
  "constants": [
    { "name": "max_retries", "value": { "type": "int", "value": 3 } }
  ]
}
```

If the plugin returns any other protocol version, the host refuses to load it and records a manager warning. Breaking protocol changes require a new protocol version and older hosts will reject the plugin during handshake.

When `source` is empty or absent the host auto-generates an RPC proxy. When `source` is provided the host uses it directly — either as a wrapper around RPC calls or as pure host-side Scriptling code.

Class `properties` are auto-generated as Scriptling @property descriptors. `settable: true` means the host also generates a setter. Getter-only properties are read-only from Scriptling.

### `environment.open`

**Direction:** Host → Plugin
**When:** Reserved for future use. Currently a no-op.

**Request params:** None
**Response result:** `null`

### `environment.close`

**Direction:** Host → Plugin
**When:** Reserved for future use. Currently a no-op.

**Request params:** None
**Response result:** `null`

### `plugin.shutdown`

**Direction:** Host → Plugin
**When:** Host is shutting down the plugin process. Sent with a 1-second timeout.

**Request params:** None
**Response result:** `null`

The plugin should release resources and exit after responding.

### `function.call`

**Direction:** Host → Plugin
**When:** Calling a registered function.

**Request params:**

| Field | Type | Optional | Description |
| --- | --- | --- | --- |
| `name` | string | No | Registered function name |
| `args` | [Value] | Yes | Positional arguments |
| `kwargs` | {string: Value} | Yes | Keyword arguments |

**Response result:** A single `Value` — the function's return value.

Example:

```json
→ {"jsonrpc":"2.0","id":2,"method":"function.call","params":{"name":"greet","args":[{"type":"string","value":"Ada"}]}}
← {"jsonrpc":"2.0","id":2,"result":{"type":"string","value":"Hello, Ada"}}
```

### `callback.call`

**Direction:** Plugin -> Host  
**When:** A plugin invokes a callback argument before the outer function, constructor, or method call has returned.

Callback calls are ordinary JSON-RPC requests sent over the same stdio stream while another host -> plugin request is still pending. The host executes the Scriptling callback synchronously on the same environment call stack and responds before the plugin continues.

**Request params:**

| Field | Type | Optional | Description |
| --- | --- | --- | --- |
| `id` | string | No | Callback id from a `callback` transport value |
| `args` | [Value] | Yes | Positional callback arguments |
| `kwargs` | {string: Value} | Yes | Keyword callback arguments |

**Response result:** A single `Value` — the callback return value.

Example:

```json
-> {"jsonrpc":"2.0","id":7,"method":"callback.call","params":{"id":"cb-1","args":[{"type":"dict","entries":{"token":{"type":"string","value":"Hello"}}}]}}
<- {"jsonrpc":"2.0","id":7,"result":{"type":"string","value":"ack"}}
```

If the callback raises an error, the host returns a JSON-RPC error and the plugin function should fail the outer call. Once the outer call returns, all callback ids created for that call expire; later use returns `unknown callback`.




### `host.log`

**Direction:** Plugin -> Host  
**When:** A Go plugin writes through `plugin.Logger(ctx)` during an active function, constructor, or method call.

**Request params:**

| Field | Type | Optional | Description |
| --- | --- | --- | --- |
| `level` | string | No | `trace`, `debug`, `info`, `warn`, `error`, or `fatal` |
| `message` | string | No | Log message |
| `args` | [Value] | Yes | Logger key/value arguments encoded as transport values |

**Response result:** `null`

Example:

```json
-> {"jsonrpc":"2.0","id":8,"method":"host.log","params":{"level":"info","message":"plugin work started","args":[{"type":"string","value":"name"},{"type":"string","value":"Ada"}]}}
<- {"jsonrpc":"2.0","id":8,"result":{"type":"null"}}
```

The host forwards the record to the plugin manager logger if one is configured. If no host logger is configured, the host acknowledges the request and drops the record.

### `object.new`

**Direction:** Host → Plugin
**When:** Constructing a class instance.

**Request params:**

| Field | Type | Optional | Description |
| --- | --- | --- | --- |
| `class` | string | No | Registered class name |
| `args` | [Value] | Yes | Constructor arguments |
| `kwargs` | {string: Value} | Yes | Constructor keyword arguments |

**Response result:** A `RemoteRef` identifying the new instance:

```json
{
  "library": "hello",
  "class": "Config",
  "id": "1"
}
```

### `object.call_method`

**Direction:** Host → Plugin
**When:** Calling a method on a remote instance.

**Request params:**

| Field | Type | Optional | Description |
| --- | --- | --- | --- |
| `object_id` | string | No | Instance ID from `object.new` |
| `method` | string | No | Method name |
| `args` | [Value] | Yes | Positional arguments |
| `kwargs` | {string: Value} | Yes | Keyword arguments |

**Response result:** A single `Value` — the method return value.

Class properties also use `object.call_method`. A getter call sends the property name with no `args`; a setter call sends the property name with one positional argument containing the new value. Read-only properties return a JSON-RPC error when called as a setter.

### `object.destroy`

**Direction:** Host → Plugin
**When:** Releasing a remote instance (explicit release or GC finalizer).

**Request params:**

| Field | Type | Optional | Description |
| --- | --- | --- | --- |
| `object_id` | string | No | Instance ID to destroy |

**Response result:** `null`

The plugin removes the instance and calls `__del__` if defined. Destroy is idempotent — destroying an already-destroyed ID succeeds silently.

## Lifecycle

1. Host starts the plugin executable.
2. Host sends `scriptling.handshake`. Plugin responds with schema.
3. Host sends `environment.open` (reserved, currently no-op).
4. Host sends `function.call`, `object.new`, `object.call_method`, `object.destroy` as needed.
5. Host sends `environment.close` (reserved, currently no-op).
6. Host sends `plugin.shutdown`. Plugin responds and exits.

## Skipping the handshake

Executables loaded via `scriptling.plugin.load(name, path)` (without
`scriptling=True`) skip the plugin handshake — no `scriptling.handshake`
exchange and no schema/version metadata collected. The host still reports
`transport` as `"json"` because raw peers use the same JSON-RPC-over-stdio
codec. In this raw JSON-RPC mode,
`scriptling.plugin.call_function(library, name, ...)` sends `name` directly as
the JSON-RPC method instead of wrapping it in `function.call`. This is useful
for peers such as `scriptling --json-rpc setup.py`, where methods are
registered with `scriptling.runtime.jsonrpc.method()`.

`plugin.shutdown` is sent on `unload()` as a best-effort hint and any
method-not-found response is ignored, so implementing it is optional. The
host closes stdin immediately afterwards; the executable should exit promptly
when stdin reaches EOF.
