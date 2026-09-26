---
title: scriptling.runtime.mcp
linkTitle: runtime.mcp
description: Register MCP tools, resources, prompts and skills via decorators — metadata and implementation in a single file.
tags: [libraries, runtime, mcp]
weight: 8

aliases:
  - /reference/libraries/scriptling/runtime/mcp/
---

The `scriptling.runtime.mcp` sub-library provides decorator-based registration for MCP (Model Context Protocol) entries: tools with `@mcp.tool`, resources with `@mcp.resource`, prompts with `@mcp.prompt` and skills with `@mcp.skill`. It is the recommended way to define tools when using Scriptling as an MCP server.

Instead of maintaining separate `.toml` metadata and `.py` script files, you define the description, parameters, and implementation in one place — and the same decorated file can mix tools, resources, prompts and skills.

## Importing

```python
import scriptling.runtime.mcp as mcp
```

Or via the parent library:

```python
import scriptling.runtime as runtime
# use as runtime.mcp.tool(...)
```

## `@mcp.tool()` Decorator

Registers a function as an MCP tool. The function's parameters become the tool's input schema; the return value becomes the tool response.

### Signature

```python
@mcp.tool(description, params=None, keywords=None, discoverable=False, ui=None, icons=None)
def tool_name(param1, param2=default):
    ...
```

### Arguments

| Argument       | Type   | Required | Description |
|----------------|--------|----------|-------------|
| `description`  | str    | Yes      | Tool description shown to the AI |
| `params`       | dict   | No       | Parameter metadata keyed by name (see below) |
| `keywords`     | list   | No       | Keywords for tool search/discovery |
| `discoverable` | bool   | No       | If `True`, hidden from `tools/list`, searchable via `tool_search` (default: `False`) |
| `ui`           | dict   | No       | Links this tool to a companion UI resource — see [MCP Apps](/reference/libraries/mcp/mcp-apps/) |
| `icons`        | list   | No       | Visual identifiers shown on the tool's `tools/list` descriptor — see [Icons](/reference/libraries/mcp/mcp-apps/#icons) |

### Parameter Metadata (`params`)

Each key in the `params` dict must match a function parameter name. The value can be:

- **A string** — treated as the description; type is inferred from the default value or defaults to `"string"`.
- **A dict** — full control over `type`, `description`, and optionally `required`.

```python
@mcp.tool("Example", params={
    "name": "Person's name",                          # shorthand: description only
    "count": {"type": "int", "description": "How many times"},  # explicit type
    "force": {"type": "boolean", "description": "Force mode", "required": True},
})
def example(name, count=1, force=False):
    ...
```

### Parameter Resolution Rules

| Source                    | Determines                                    |
|---------------------------|-----------------------------------------------|
| Function signature        | Parameter names, required (no default → required) |
| `params` dict value (str) | Description; type inferred or defaults to `"string"` |
| `params` dict value (dict)| `type`, `description`, optional `required` override |
| Default value type        | Inferred type when not explicit: `int` → `"integer"`, `float` → `"number"`, `bool` → `"boolean"` |

A `params` key that doesn't match any function parameter produces a registration error at startup.

### Parameter Types

| Type           | Aliases         | Description            |
|----------------|-----------------|------------------------|
| `string`       | `str`           | Text values            |
| `integer`      | `int`           | Whole numbers          |
| `number`       | `float`         | Integer or float       |
| `boolean`      | `bool`          | True/false values      |
| `array:string` |                 | Array of strings       |
| `array:integer`| `array:int`     | Array of whole numbers |
| `array:number` | `array:float`   | Array of numbers       |
| `array:boolean`| `array:bool`    | Array of booleans      |

### Return Value Semantics

The function's return value is mapped to the MCP tool response:

| Return Type      | MCP Response           |
|------------------|------------------------|
| `str`            | Text content           |
| `dict` or `list` | JSON content           |
| `None` (or no return) | Empty text content |
| Exception raised | Error response         |

### Complete Example

```python
import scriptling.runtime.mcp as mcp

@mcp.tool(
    "Calculate a mathematical expression",
    params={"expr": "Expression to evaluate (e.g. 2+3*4)"},
)
def calc(expr):
    allowed = "0123456789+-*/.() "
    if not all(c in allowed for c in expr):
        raise ValueError("invalid characters in expression")
    result = eval(expr)
    return f"{expr} = {result}"
```

## `@mcp.resource()` Decorator

Registers a function as an MCP resource. The first argument is the URI; with `template=True` it is a URI template and the function's parameters are the URI's `{var}` variables.

```python
import scriptling.runtime.mcp as mcp

@mcp.resource("config://shop", name="Shop configuration", mime_type="application/json")
def shop_config():
    return {"currency": "USD", "items": 3}

@mcp.resource("shop://catalog/{category}", template=True, mime_type="text/markdown")
def catalog(category):
    return "# Catalog: " + category
```

**Arguments:**

- `uri` (`str`): Resource URI, or the URI template when `template=True`.
- `name` (`str`, optional): Human-readable name (defaults to the URI).
- `description` (`str`, optional): Resource description.
- `mime_type` (`str`, optional): Content type. Default `text/plain`, or `application/json` for dict/list results. Ignored for a `ui://` URI: the [MCP Apps](/reference/libraries/mcp/mcp-apps/) extension MUSTs that exact mimeType, so it is always set for you.
- `template` (`bool`, optional): Treat `uri` as a `{var}` URI template. Default: `False`.

The function runs on every `resources/read`, in a fresh interpreter, so its content can change between reads. A string return is the text content; a dict or list return is JSON encoded. Only the template variables are passed as parameters — the function's signature is the contract (there is no `__uri` parameter unless the template itself declares one). `mcp.tool.return_string()` / `return_object()` work too: they set the content the same way a return value does.

The signature is cross-checked against the URI at startup, the same way `@mcp.tool` params are: every template `{var}` must be a function parameter, every required parameter must be a template variable, and a static resource function must not require any parameters. A violation fails the scan instead of every read. A decorated resource colliding with a resource from `--mcp-resources` is last-wins (the resources folder registers after the tools folder, both at startup and on reload).

## `@mcp.prompt()` Decorator

Registers a function as an MCP prompt under the function's own name. The function's parameters become the prompt's arguments and are passed on every `prompts/get`.

```python
import scriptling.runtime.mcp as mcp

@mcp.prompt(description="Summarise a document")
def summarise(text, style="brief"):
    return "Summarise (style=" + style + "): " + text

@mcp.prompt(description="Review code", arguments=[
    {"name": "language", "description": "Language of the code", "required": True},
    {"name": "code", "description": "The code"},
])
def review(language, code):
    return {"messages": [
        {"role": "user", "content": "Review this " + language + " code:"},
        {"role": "assistant", "content": code},
    ]}
```

**Arguments:**

- `description` (`str`, optional): Prompt description.
- `arguments` (`list`, optional): Argument metadata dicts with `name`, `description` and `required`. When omitted, the arguments are inferred from the function signature (a parameter without a default is required).

A string return is a single user message; a dict with a `"messages"` list of `{"role": "user"|"assistant", "content": "..."}` (or a plain list of them) builds a multi-message prompt. `mcp.tool.return_*()` is honoured like a return value, and explicit `arguments` names are cross-checked against the function signature at startup.

## `@mcp.skill()` Decorator

Registers a function as an MCP skill (the Agent Skills format, served per the Skills extension) under the function's own name. The function takes no parameters and returns the `SKILL.md` content, YAML frontmatter included; the `files` argument supplies supporting files.

```python
import scriptling.runtime.mcp as mcp

@mcp.skill(files={"regions.md": "eu: Europe\nus: United States\n"})
def shipping_regions():
    return """---
name: shipping_regions
description: How to pick the right shipping region for an order
---

# Shipping regions

Read regions.md for the region codes.
"""
```

**Arguments:**

- `files` (`dict`, optional): Supporting files mapping file name to content string, served as `skill://<name>/<file>` alongside `SKILL.md`. `SKILL.md` itself must not appear here — it is the function's return value.

The frontmatter's `name` must match the function name and its `description` seeds the skill's listing, exactly as for a `SKILL.md` file in the skills folder. The function runs once when the server starts: skill content is static thereafter, matching the skills folder (which also only registers at startup). A skill that fails validation is skipped with a warning; the rest of the file's registrations are unaffected.

## Request-Scoped Registration

The `register_request_*` functions expose MCP entries **for the life of a single request**. Call them from [middleware](/reference/libraries/runtime/http/#middlewarehandler): every MCP message over HTTP is its own request and runs the middleware, so the entries each caller sees — and can call — are exactly the ones that caller's middleware registered. That makes per-user tool sets possible, with authorization re-evaluated on every message rather than only at listing time. Static entries always win on a name collision; a malformed registration fails the request with a 500.

Over the stdio transport middleware never runs — gate on `mcp.transport()` and register statically there instead.

### `mcp.register_request_tool(name, handler, ...)`

```python
import scriptling.runtime.mcp as mcp

def auth(request):
    user = identify(request)
    if user == "admin":
        mcp.register_request_tool("restart_service",
            handler="admintools.restart",
            description="Restart a service",
            params={"service": {"type": "string", "description": "Service to restart", "required": True}},
        )
    return None
```

`handler` is a `"module.function"` reference invoked per call with the tool arguments as keyword parameters — the same conventions as any other handler reference. Inside the handler, `mcp.tool.get_string()` reads the arguments and `mcp.tool.request_context()` reads the middleware's context (who is calling). `params` uses the same metadata vocabulary as `@mcp.tool`: a string per parameter (its description) or a dict with `type`, `description` and `required`. `keywords` and `discoverable` feed tool search, and `ui` links the tool to a companion UI resource, exactly as on `@mcp.tool` — see [MCP Apps](/reference/libraries/mcp/mcp-apps/).

### `mcp.register_request_resource(uri, handler, name, ...)`

Exposes a resource (or, with `template=True`, a URI template like `"user://docs/{path}"`). `resources/list` and `resources/templates/list` show it; `resources/read` runs the handler with the template variables as keyword parameters (and `__uri` holding the full URI). A string return is the content; a dict or list is JSON encoded. `mime_type` defaults to `text/plain`, or `application/json` for structured results — except for a `"ui://"` uri, where it's always `text/html;profile=mcp-app` (the [MCP Apps](/reference/libraries/mcp/mcp-apps/) extension MUSTs that exact mimeType), overriding whatever `mime_type` was passed.

### `mcp.register_request_prompt(name, handler, ...)`

Exposes a prompt. `prompts/get` runs the handler with the prompt arguments as keyword parameters: a string return is a single user message, a dict with a `"messages"` list of `{"role": "user"|"assistant", "content": "..."}` builds a multi-message prompt. `arguments` is a list of metadata dicts with `name`, `description` and `required`.

### `mcp.transport()`

Returns `"http"` when serving over HTTP (also from middleware and handlers mid-request), `"stdio"` for the MCP stdio server, and `None` when the script is not being served at all — so one setup script can work in every mode:

```python
if mcp.transport() == "stdio":
    # No middleware over stdio: expose the extra tools to everyone.
    ...
```

## Multiple Tools per File

A single `.py` file can define multiple tools:

```python
import scriptling.runtime.mcp as mcp

@mcp.tool("Encode text to base64", params={"text": "Text to encode"})
def encode_base64(text):
    import base64
    return base64.b64encode(text.encode()).decode()

@mcp.tool("Decode base64 to text", params={"data": "Base64 string to decode"})
def decode_base64(data):
    import base64
    return base64.b64decode(data).decode()
```

Both tools are discovered and registered when the file is scanned.

## File Layout

Place decorated tool files in the `tools/` directory without a `.toml` sibling:

```
tools/
├── calc.py           # Decorated tool (no .toml needed)
├── multi.py          # Multiple tools in one file
├── greet.toml        # Legacy format (still supported)
└── greet.py          # Legacy format script
```

The server auto-detects the format:
- `.py` with a sibling `.toml` → legacy format (uses `tool.get_*` / `tool.return_*`)
- `.py` without a sibling `.toml` → decorator format (scanned for `@mcp.tool`, `@mcp.resource`, `@mcp.prompt` and `@mcp.skill`; one file may use any mix of them)

Both formats work in the same folder and can coexist indefinitely. Registrations from decorated files reload with the tools folder; skills refresh silently (the Skills extension has no listChanged notification).

## Comparison with Legacy Format

| Aspect                 | Decorator (`@mcp.tool`)         | Legacy (`.toml` + `.py`)         |
|------------------------|----------------------------------|-----------------------------------|
| Files per tool         | 1                                | 2                                 |
| Parameter source       | Function signature + decorator   | `.toml` `[[parameters]]` section  |
| Implementation style   | `def fn(params) -> result`       | Top-level script with `tool.get_*`/`tool.return_*` |
| Type safety            | Params cross-checked at startup  | Drift possible between `.toml` and `.py` |
| Multiple tools/file    | Yes                              | No (one pair per tool)            |
| Discovery              | Requires evaluating the file     | Static TOML parse                 |

## Migration from Legacy Format

Converting a `.toml` + `.py` tool:

**Before** (`greet.toml` + `greet.py`):

```toml
# greet.toml
description = "Greet a person"
[[parameters]]
name = "name"
type = "string"
description = "Person name"
required = true
[[parameters]]
name = "times"
type = "int"
description = "Repeat count"
```

```python
# greet.py
import scriptling.mcp.tool as tool
name = tool.get_string("name", "World")
times = tool.get_int("times", 1)
greetings = "\n".join(f"Hello, {name}!" for _ in range(times))
tool.return_string(greetings)
```

**After** (single `greet.py`, delete `greet.toml`):

```python
import scriptling.runtime.mcp as mcp

@mcp.tool("Greet a person", params={
    "name": "Person name",
    "times": {"type": "int", "description": "Repeat count"},
})
def greet(name, times=1):
    return "\n".join(f"Hello, {name}!" for _ in range(times))
```

## Usage in App Bundles

Decorated tools work in [app bundles](/docs/cli/packages/) exactly the same way — place them in the bundle's `tools/` directory:

```
myapp/
├── manifest.toml        # serve = ["mcp"]
├── setup.py
├── tools/
│   └── calc.py          # @mcp.tool decorated
└── lib/
    └── ...
```

## Go Registration

`scriptling.runtime.mcp` is part of the runtime aggregate:

```go
extlibs.RegisterRuntimeLibraryAll(p, allowedPaths)
```

That call registers the sub-library independently and also exposes it as `scriptling.runtime.mcp` through the parent `scriptling.runtime` object. An embedder that needs only this namespace can call:

```go
extlibs.RegisterRuntimeMCPLibrary(p)
```

This server/decorator namespace is distinct from `scriptling.mcp`, which is an MCP client library.

## Security Considerations

Static decorators expose the registered functions to every client that can reach the MCP server. Request-scoped registrations let HTTP middleware choose entries per request, but the middleware must authenticate and authorize the caller before registering privileged handlers. Stdio has no middleware, so static entries there are available to the process connected to stdin/stdout. Treat each tool, resource, and prompt handler as a remotely callable entry point and grant it only the host capabilities it needs.

## See Also

- [Writing MCP Tools (legacy format)](/reference/libraries/mcp/writing-mcp-tools/) — The `.toml` + `.py` format reference
- [MCP Apps](/reference/libraries/mcp/mcp-apps/) — Linking a tool to an interactive UI resource
- [Decorators](/reference/decorators/) — General decorator syntax and patterns
- [MCP Server Mode](/docs/cli/mcp-server/) — Running Scriptling as an MCP server
- [App Bundles](/docs/cli/packages/) — Packaging tools, HTTP routes, and assets together
