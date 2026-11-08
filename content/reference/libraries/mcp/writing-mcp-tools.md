---
title: Writing MCP Tools
description: Creating custom MCP tools with metadata and script files.
tags: [libraries, mcp]
weight: 3

aliases:
  - /reference/libraries/scriptling/mcp/writing-mcp-tools/
---

Custom MCP tools allow you to expose Scriptling functionality to AI assistants.

{{< callout type="info" >}}
**Recommended:** Use the [decorator-based format](/reference/libraries/runtime/mcp/) (`@mcp.tool`) for new tools. It keeps metadata and implementation in a single file, eliminates drift between `.toml` and `.py`, and supports multiple tools per file.
{{< /callout >}}

This page documents the **legacy format** where each tool consists of a metadata file (`.toml`) and a script file (`.py`). Both formats are fully supported and can coexist in the same tools folder.

## Tool Structure

Tools are defined in a directory specified by `--mcp-tools`:

```
./tools/
  hello.toml      # Metadata for "hello" tool
  hello.py        # Implementation for "hello" tool
  add.toml        # Metadata for "add" tool
  add.py          # Implementation for "add" tool
```

Both files must have the same base name (e.g., `hello.toml` and `hello.py`).

## Metadata File (`.toml`)

The metadata file defines the tool's description, parameters, and registration mode.

### Basic Structure

```toml
description = "Greet a person by name"
keywords = ["hello", "greet", "welcome"]

[[parameters]]
name = "name"
type = "string"
description = "Name of the person to greet"
required = true

[[parameters]]
name = "times"
type = "int"
description = "Number of times to repeat the greeting"
```

### Fields

| Field         | Required | Description                                               |
| ------------- | -------- | --------------------------------------------------------- |
| `description` | Yes      | Tool description shown to the AI                          |
| `keywords`    | No       | Keywords for search (array of strings)                    |
| `discoverable`| No       | Registration mode (default: `false`)                      |
| `title`       | No       | Human-readable display name ([Title and behaviour hints](#title-and-behaviour-hints)) |
| `read_only`   | No       | Behaviour hint: doesn't modify its environment (bool)     |
| `destructive` | No       | Behaviour hint: may delete or overwrite data (bool)       |
| `idempotent`  | No       | Behaviour hint: repeating a call has no further effect (bool) |
| `open_world`  | No       | Behaviour hint: talks to external systems (bool)          |
| `[ui]`        | No       | Links a companion UI resource ([MCP Apps](#linking-a-ui-resource-ui)) |
| `[[icons]]`   | No       | Visual identifiers shown on the tool's `tools/list` descriptor ([Icons](/reference/libraries/mcp/mcp-apps/#icons); generate the block from an image file with `scriptling tools/make_icon/make_icon.py`) |

### Parameter Types

Each type emits a valid JSON Schema type in the tool definition sent to the LLM.

| Type           | Aliases           | JSON Schema emitted                      | Description            |
| -------------- | ----------------- | ---------------------------------------- | ---------------------- |
| `string`       |                   | `string`                                 | Text values            |
| `integer`      | `int`             | `integer`                                | Whole numbers          |
| `number`       | `float`           | `number`                                 | Integer or float       |
| `boolean`      | `bool`            | `boolean`                                | True/false values      |
| `array:string` |                   | `array` of `string`                      | Array of strings       |
| `array:integer`| `array:int`       | `array` of `integer`                     | Array of whole numbers |
| `array:number` | `array:float`     | `array` of `number`                      | Array of numbers       |
| `array:boolean`| `array:bool`      | `array` of `boolean`                     | Array of booleans      |

Unknown type strings cause the tool to fail to register at server startup with
a clear error message.

Arguments are checked against the declared types before the script runs: an
argument whose JSON type doesn't match (a string for an `int` parameter, a
number for a `string` one), or a missing required argument, comes back as a
tool result with `isError` set and a message such as `parameter n must be of
type integer`, so the model can read it and retry; the script is never
started. Unambiguous quoted numbers and booleans (`"10"`, `"true"`) are
accepted for `int`, `float` and `bool` parameters and converted to the
declared type first. An `int` parameter then reaches the script as an int
and a `float` one as a float, whatever JSON the client sent.

### Parameter Fields

| Field         | Required | Description                                               |
| ------------- | -------- | --------------------------------------------------------- |
| `name`        | Yes      | Parameter name                                            |
| `type`        | Yes      | Data type (see table above)                               |
| `description` | Yes      | Description shown to the AI                               |
| `required`    | No       | Whether the parameter must be provided (default: `false`) |

### Registration Modes

- **Native mode** (default, `discoverable = false`): Tool appears in `tools/list` and can be called directly
- **Discovery mode** (`discoverable = true`): Tool is hidden from `tools/list`, searchable via `tool_search`, and callable via `execute_tool`

`tool_search` and `execute_tool` are only listed, and only callable, when the
server has discoverable tools to find; otherwise calling them is an unknown-tool
error.

### Title and Behaviour Hints

`title` gives the tool a display name. `read_only`, `destructive`,
`idempotent` and `open_world` become the tool's `annotations` in `tools/list`
(`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`),
telling clients how careful to be with it: a client may run a read-only tool
without asking, and ask the user before a destructive one.

```toml
description = "Delete a note by ID"
title = "Delete Note"
destructive = true    # may delete or overwrite data (false: only adds)
idempotent = true     # deleting the same note twice has no further effect
open_world = false    # works on the local notes store, not external systems
```

Leave a hint out and it isn't sent, so clients assume the spec default: not
read-only, possibly destructive, not idempotent, open world. `destructive` and
`idempotent` only mean something when `read_only` isn't `true`. A value of the
wrong type (`read_only = "yes"`) fails the tool's registration.

Hints are not access control: a client may ignore them, and nothing stops a
tool marked `read_only` from writing. Enforce what a tool may do in the script
itself. Decorated and request-scoped tools take the same options as keyword
arguments — see [`scriptling.runtime.mcp`](/reference/libraries/runtime/mcp/#title-and-behaviour-hints).

### Linking a UI Resource (`[ui]`)

A tool can link to a companion interactive HTML UI, which a compliant
[MCP Apps](https://github.com/modelcontextprotocol/ext-apps) host renders in
a sandboxed iframe instead of (or alongside) the tool's text result. Add a
`[ui]` table with a `resourceUri`:

```toml
description = "Get the sales report"

[ui]
resourceUri = "ui://sales-dashboard/dashboard.html"
visibility = ["model", "app"]
```

Decorated and dynamically-registered tools link the same way, with a `ui=`
keyword argument instead of a TOML table — see the dedicated
**[MCP Apps](../mcp-apps/)** page for the full field reference, the paired
`ui://` resource's own `[ui]` metadata (CSP, permissions), and
`tool.return_structured()` for returning the data such a UI expects.

## Script File (`.py`)

The script file implements the tool logic using the `scriptling.mcp.tool` library.

### Basic Structure

```python
import scriptling.mcp.tool as tool

# Get parameters with defaults
name = tool.get_string("name", "World")
times = tool.get_int("times", 1)

# Implement tool logic
greetings = []
for i in range(times):
    greetings.append(f"Hello, {name}!")

result = "\n".join(greetings)

# Return result
tool.return_string(result)
```

### Getting Parameters

```python
import scriptling.mcp.tool as tool

# Get parameters by name (with optional defaults)
name = tool.get_string("name", "World")     # String parameter
count = tool.get_int("count", 1)            # Integer parameter
ratio = tool.get_float("ratio", 0.5)        # Float parameter
enabled = tool.get_bool("enabled", False)   # Boolean parameter
items = tool.get_list("items", [])          # List parameter
```

### Returning Results

```python
import scriptling.mcp.tool as tool

# Return text
tool.return_string("Operation completed")

# Return JSON object as text content
data = {"users": ["Alice", "Bob"], "count": 2}
tool.return_object(data)

# Return a dict as the MCP result's structuredContent field (plus the same
# JSON as a text fallback, for clients that don't read structuredContent)
tool.return_structured(data)

# Return object as TOON format
tool.return_toon(data)

# Return error
tool.return_error("Something went wrong")
```

### Reporting Progress

A tool that takes a while can tell the client how far it has got with
`tool.progress(progress, total=None, message=None)`. The client gets a
`notifications/progress` message for each call when it asked for progress
(sent a `progressToken`); otherwise the call does nothing.

```python
import scriptling.mcp.tool as tool

items = tool.get_string_list("items")
for i, item in enumerate(items):
    process(item)
    tool.progress(i + 1, total=len(items), message="Processed " + item)
tool.return_string("done")
```

See [`mcp.tool.progress()`](/reference/libraries/mcp/tool/#mcptoolprogressprogress-totalnone-messagenone).

`return_object` and `return_structured` both accept a dict, but only
`return_structured` sets the MCP result's `structuredContent` field — the
field a client can read without having to parse JSON out of the text
content, and what a [`[ui]`-linked](#linking-a-ui-resource-ui) MCP Apps view
typically expects. `return_structured` requires its argument to be a dict
(structuredContent must be a JSON object per the MCP spec); use
`return_object` for a list, string, or other non-object value.

## Complete Examples

### Hello Tool

**hello.toml:**

```toml
description = "Greet a person by name"
keywords = ["hello", "greet", "welcome"]

[[parameters]]
name = "name"
type = "string"
description = "Name of the person to greet"
required = true

[[parameters]]
name = "times"
type = "int"
description = "Number of times to repeat the greeting"
```

**hello.py:**

```python
import scriptling.mcp.tool as tool

name = tool.get_string("name", "World")
times = tool.get_int("times", 1)

greetings = []
for i in range(times):
    greetings.append(f"Hello, {name}!")

tool.return_string("\n".join(greetings))
```

### Add Tool (Discovery Mode)

**add.toml:**

```toml
description = "Calculate the sum of two numbers"
keywords = ["math", "add", "sum", "calculate"]
discoverable = true  # Hidden from tools/list, searchable

[[parameters]]
name = "a"
type = "int"
description = "First number"
required = true

[[parameters]]
name = "b"
type = "int"
description = "Second number"
required = true
```

**add.py:**

```python
import scriptling.mcp.tool as tool

a = tool.get_int("a")
b = tool.get_int("b")

result = a + b
tool.return_string(f"{a} + {b} = {result}")
```

### List Processing Tool

**process_list.toml:**

```toml
description = "Process a list of numbers and return statistics"
keywords = ["list", "numbers", "statistics", "sum", "average"]

[[parameters]]
name = "numbers"
type = "array:number"
description = "List of numbers to process"
required = true

[[parameters]]
name = "operation"
type = "string"
description = "Operation to perform: sum, average, min, max"
required = true
```

**process_list.py:**

```python
import scriptling.mcp.tool as tool

numbers = tool.get_list("numbers", [])
operation = tool.get_string("operation", "sum")

if not numbers:
    tool.return_error("Numbers list is empty")
else:
    if operation == "sum":
        result = sum(numbers)
    elif operation == "average":
        result = sum(numbers) / len(numbers)
    elif operation == "min":
        result = min(numbers)
    elif operation == "max":
        result = max(numbers)
    else:
        tool.return_error(f"Unknown operation: {operation}")
        result = None

    if result is not None:
        tool.return_object({
            "operation": operation,
            "result": result,
            "count": len(numbers)
        })
```

## Testing Tools

### Start the Server

```bash
scriptling --server :8000 --mcp-tools ./tools setup.py
```

### List Available Tools

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### Call a Native Tool

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"hello",
      "arguments":{"name":"Alice","times":2}
    }
  }'
```

### Search for Discoverable Tools

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":3,
    "method":"tools/call",
    "params":{
      "name":"tool_search",
      "arguments":{"query":"math"}
    }
  }'
```

### Execute a Discoverable Tool

Pass the tool's arguments in `parameters`, as an object or a string holding a
JSON object. Any other key is refused with an `isError` result saying what to
send.

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":4,
    "method":"tools/call",
    "params":{
      "name":"execute_tool",
      "arguments":{"name":"add","parameters":{"a":5,"b":3}}
    }
  }'
```

## Tool Function Reference

### Getting Parameters

| Function                        | Description                    |
| ------------------------------- | ------------------------------ |
| `tool.get_string(name, default)`| Get string parameter           |
| `tool.get_int(name, default)`   | Get integer parameter          |
| `tool.get_float(name, default)` | Get float parameter            |
| `tool.get_bool(name, default)`  | Get boolean parameter          |
| `tool.get_list(name, default)`  | Get list parameter             |

### Returning Results

| Function                     | Description                                          |
| ---------------------------- | ----------------------------------------------------- |
| `tool.return_string(text)`   | Return text result                                    |
| `tool.return_object(obj)`    | Return object as JSON text content                    |
| `tool.return_structured(obj)`| Return a dict as `structuredContent` (+ text fallback) |
| `tool.return_toon(obj)`      | Return object as TOON format                          |
| `tool.return_error(msg)`     | Return error message as an `isError` tool result      |

## See Also

- [MCP Tool Library](../tool/) - Full API reference for the tool library
- [MCP Library](../) - MCP server library reference
- [MCP Server Mode](/docs/cli/mcp-server/) - Running Scriptling as an MCP server
