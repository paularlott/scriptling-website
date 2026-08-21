---
description: Register MCP tools via decorators — metadata and implementation in a single file.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/runtime/mcp/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/runtime/mcp/
status: stable
tags:
    - libraries
    - runtime
    - mcp
title: scriptling.runtime.mcp
type: API Reference
---
# scriptling.runtime.mcp

The `scriptling.runtime.mcp` sub-library provides decorator-based registration for MCP (Model Context Protocol) tools. It is the recommended way to define tools when using Scriptling as an MCP server.

Instead of maintaining separate `.toml` metadata and `.py` script files, you define the tool's description, parameters, and implementation in one place.

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
@mcp.tool(description, params=None, keywords=None, discoverable=False)
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
- `.py` without a sibling `.toml` → decorator format (scanned for `@mcp.tool`)

Both formats work in the same folder and can coexist indefinitely.

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

Decorated tools work in [app bundles](../../../scriptling-docs/cli/packages.md) exactly the same way — place them in the bundle's `tools/` directory:

```
myapp/
├── manifest.toml        # serve = ["mcp"]
├── setup.py
├── tools/
│   └── calc.py          # @mcp.tool decorated
└── lib/
    └── ...
```

## See Also

- [Writing MCP Tools (legacy format)](../mcp/writing-mcp-tools.md) — The `.toml` + `.py` format reference
- [Decorators](../../../scriptling-reference/decorators.md) — General decorator syntax and patterns
- [MCP Server Mode](../../../scriptling-docs/cli/mcp-server.md) — Running Scriptling as an MCP server
- [App Bundles](../../../scriptling-docs/cli/packages.md) — Packaging tools, HTTP routes, and assets together
