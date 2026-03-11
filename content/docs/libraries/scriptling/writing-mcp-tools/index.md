---
title: Writing MCP Tools
description: Creating custom MCP tools with metadata and script files.
weight: 4
---

Custom MCP tools allow you to expose Scriptling functionality to AI assistants. Each tool consists of a metadata file (`.toml`) and a script file (`.py`).

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

### Parameter Types

| Type           | Aliases                                     | Description            |
| -------------- | ------------------------------------------- | ---------------------- |
| `string`       |                                             | Text values            |
| `int`          | `integer`                                   | Integer numbers        |
| `float`        | `number`                                    | Floating point numbers |
| `bool`         | `boolean`                                   | True/false values      |
| `array:string` |                                             | Array of strings       |
| `array:number` | `array:int`, `array:integer`, `array:float` | Array of numbers       |
| `array:bool`   | `array:boolean`                             | Array of booleans      |

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

# Return JSON object
data = {"users": ["Alice", "Bob"], "count": 2}
tool.return_object(data)

# Return object as TOON format
tool.return_toon(data)

# Return error
tool.return_error("Something went wrong")
```

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

```bash
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":4,
    "method":"tools/call",
    "params":{
      "name":"execute_tool",
      "arguments":{"name":"add","arguments":{"a":5,"b":3}}
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

| Function                  | Description                      |
| ------------------------- | -------------------------------- |
| `tool.return_string(text)`| Return text result               |
| `tool.return_object(obj)` | Return object as JSON            |
| `tool.return_toon(obj)`   | Return object as TOON format     |
| `tool.return_error(msg)`  | Return error message             |

## See Also

- [MCP Tool Library](../mcp-tool/) - Full API reference for the tool library
- [MCP Library](../mcp/) - MCP server library reference
- [MCP Server Mode](../../../cli/mcp-server/) - Running Scriptling as an MCP server
