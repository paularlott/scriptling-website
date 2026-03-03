---
title: scriptling.mcp.tool
linkTitle: mcp.tool
weight: 3
---

MCP tool helper library for authoring MCP tools in scriptling. This sub-library provides functions for parameter access and result handling when implementing tool scripts.

For the MCP client library (connecting to MCP servers), see the [MCP Library](mcp.md) documentation.

## Registration

The tool helpers are a separate, optional sub-library. Register it explicitly when needed:

```python
mcp.RegisterToolHelpers(sl)  # Registers scriptling.mcp.tool
```

## Environment Variables

MCP tool helpers read and write to environment variables set by the MCP tool execution environment:

- **`__mcp_params`**: Dictionary containing tool parameters
- **`__mcp_response`**: String containing the tool's result

## Available Functions

| Function                            | Description                                      |
| ----------------------------------- | ------------------------------------------------ |
| `get_int(name, default=0)`          | Get an integer parameter                         |
| `get_float(name, default=0.0)`      | Get a float parameter                            |
| `get_string(name, default="")`      | Get a string parameter (trims whitespace)        |
| `get_bool(name, default=false)`     | Get a boolean parameter                          |
| `get_list(name, default=None)`      | Get a list parameter (splits strings by comma)   |
| `get_string_list(name, default=None)` | Get a string array parameter                    |
| `get_int_list(name, default=None)`  | Get an integer array parameter                   |
| `get_float_list(name, default=None)` | Get a float array parameter                     |
| `get_bool_list(name, default=None)` | Get a boolean array parameter                    |
| `return_string(text)`               | Return a string result and stop execution        |
| `return_object(obj)`                | Return an object as JSON and stop execution      |
| `return_toon(obj)`                  | Return an object as TOON and stop execution      |
| `return_error(message)`             | Return an error message and stop execution       |

## Parameter Access Functions

### mcp.tool.get_int(name, default=0)

Get an integer parameter from the tool's input arguments.

**Parameters:**

- `name` (str): Parameter name
- `default` (int): Default value if parameter is missing (default: 0)

**Returns:** int

**Example:**

```python
import scriptling.mcp.tool as tool

project_id = tool.get_int("project_id", 0)
limit = tool.get_int("limit", 100)
```

### mcp.tool.get_float(name, default=0.0)

Get a float parameter from the tool's input arguments.

**Parameters:**

- `name` (str): Parameter name
- `default` (float): Default value if parameter is missing (default: 0.0)

**Returns:** float

**Example:**

```python
import scriptling.mcp.tool as tool

price = tool.get_float("price", 0.0)
percentage = tool.get_float("percentage", 100.0)
```

### mcp.tool.get_string(name, default="")

Get a string parameter from the tool's input arguments. Automatically trims whitespace.

**Parameters:**

- `name` (str): Parameter name
- `default` (str): Default value if parameter is missing or empty (default: "")

**Returns:** str

**Example:**

```python
import scriptling.mcp.tool as tool

name = tool.get_string("name", "guest")
query = tool.get_string("query")
```

### mcp.tool.get_bool(name, default=false)

Get a boolean parameter from the tool's input arguments. Handles "true"/"false" strings and numeric 0/1.

**Parameters:**

- `name` (str): Parameter name
- `default` (bool): Default value if parameter is missing (default: false)

**Returns:** bool

**Example:**

```python
import scriptling.mcp.tool as tool

enabled = tool.get_bool("enabled", True)
verbose = tool.get_bool("verbose")
```

### mcp.tool.get_list(name, default=None)

Get a list parameter from the tool's input arguments. If the parameter is a string, splits by comma.

**Parameters:**

- `name` (str): Parameter name
- `default` (list): Default value if parameter is missing (default: empty list)

**Returns:** list

**Example:**

```python
import scriptling.mcp.tool as tool

ids = tool.get_list("ids")              # "1,2,3" → ["1", "2", "3"]
tags = tool.get_list("tags", ["all"])   # "tag1, tag2" → ["tag1", "tag2"]
```

### mcp.tool.get_string_list(name, default=None)

Get a string array parameter (array:string type) from the tool's input arguments.

**Parameters:**

- `name` (str): Parameter name
- `default` (list): Default value if parameter is missing (default: empty list)

**Returns:** list of strings

**Example:**

```python
import scriptling.mcp.tool as tool

args = tool.get_string_list("arguments")  # ["--verbose", "-o", "file.txt"]
tags = tool.get_string_list("tags", ["default"])
```

### mcp.tool.get_int_list(name, default=None)

Get an integer array parameter (array:int type) from the tool's input arguments.

**Parameters:**

- `name` (str): Parameter name
- `default` (list): Default value if parameter is missing (default: empty list)

**Returns:** list of integers

**Example:**

```python
import scriptling.mcp.tool as tool

ids = tool.get_int_list("ids")  # [1, 2, 3, 4]
ports = tool.get_int_list("ports", [8080])
```

### mcp.tool.get_float_list(name, default=None)

Get a float array parameter (array:float type) from the tool's input arguments.

**Parameters:**

- `name` (str): Parameter name
- `default` (list): Default value if parameter is missing (default: empty list)

**Returns:** list of floats

**Example:**

```python
import scriptling.mcp.tool as tool

prices = tool.get_float_list("prices")  # [19.99, 29.99, 39.99]
weights = tool.get_float_list("weights", [1.0])
```

### mcp.tool.get_bool_list(name, default=None)

Get a boolean array parameter (array:bool type) from the tool's input arguments.

**Parameters:**

- `name` (str): Parameter name
- `default` (list): Default value if parameter is missing (default: empty list)

**Returns:** list of booleans

**Example:**

```python
import scriptling.mcp.tool as tool

flags = tool.get_bool_list("flags")  # [true, false, true]
options = tool.get_bool_list("options", [false])
```

## Result Functions

Result functions set the tool's response and immediately stop script execution using `SystemExit`. No code after these calls will execute.

### mcp.tool.return_string(text)

Return a string result and stop execution.

**Parameters:**

- `text` (str): The result text

**Example:**

```python
import scriptling.mcp.tool as tool

tool.return_string("Search completed successfully")
# Code here will not execute
```

### mcp.tool.return_object(obj)

Return an object as JSON and stop execution.

**Parameters:**

- `obj` (dict|list): The result object

**Example:**

```python
import scriptling.mcp.tool as tool

tool.return_object({"status": "success", "count": 42})
# Code here will not execute
```

### mcp.tool.return_toon(obj)

Return an object encoded as TOON (compact text format optimized for LLMs) and stop execution.

**Parameters:**

- `obj` (dict|list): The result object

**Example:**

```python
import scriptling.mcp.tool as tool

tool.return_toon({"result": data})
# Code here will not execute
```

### mcp.tool.return_error(message)

Return an error message and stop execution with error code 1.

**Parameters:**

- `message` (str): Error message

**Example:**

```python
import scriptling.mcp.tool as tool

if not customer_id:
    tool.return_error("Customer ID is required")
    # Code here will not execute

tool.return_error("Customer not found")
```

## Complete Tool Example

Here's a complete example of an MCP tool using the helpers:

```python
# Recommended: import as alias (cleanest)
import scriptling.mcp.tool as tool

# Get parameters with defaults
name = tool.get_string("name", "guest")
age = tool.get_int("age", 0)
verbose = tool.get_bool("verbose", False)

# Validate inputs
if age < 0:
    tool.return_error("Age must be positive")

# Process and return result
result = {
    "greeting": f"Hello, {name}!",
    "age": age,
    "category": "adult" if age >= 18 else "minor"
}

if verbose:
    import time
    result["timestamp"] = time.time()

tool.return_object(result)
```

## Usage in Tool Scripts

When implementing MCP tools, the execution environment sets `__mcp_params` before running your script:

```python
# Tool script: greet_user.sl
import scriptling.mcp.tool as tool

name = tool.get_string("name", "guest")
age = tool.get_int("age", 0)

tool.return_object({
    "message": f"Hello, {name}! You are {age} years old."
})
```

The tool execution environment will:

1. Set `__mcp_params` dict with tool parameters
2. Run the script
3. Catch the `SystemExit` exception from `return_*` functions
4. Extract the result from `__mcp_response`
5. Return it to the MCP client

## Go Helper Function

For Go applications that need to run MCP tool scripts, the `RunToolScript` helper function simplifies the process:

```go
import (
    "context"
    "github.com/paularlott/scriptling"
    "github.com/paularlott/scriptling/extlibs/mcp"
)

// Create scriptling instance and register tool helpers
sl := scriptling.New()
mcp.RegisterToolHelpers(sl)

// Define tool script
script := `
import scriptling.mcp.tool as tool

name = tool.get_string("name", "guest")
age = tool.get_int("age", 0)

tool.return_object({
    "message": f"Hello, {name}! You are {age} years old."
})
`

// Run the tool with parameters
params := map[string]interface{}{
    "name": "Alice",
    "age":  30,
}

response, exitCode, err := mcp.RunToolScript(context.Background(), sl, script, params)
// response: JSON string with the result
// exitCode: 0 for success, 1 for error
// err: Go error if execution failed
```

**Function Signature:**

```go
func RunToolScript(
    ctx context.Context,
    sl *scriptling.Scriptling,
    script string,
    params map[string]interface{}
) (response string, exitCode int, err error)
```

**Parameters:**

- `ctx`: Context for cancellation and timeouts
- `sl`: Scriptling instance (must have tool helpers registered)
- `script`: The tool script code
- `params`: Map of parameter name to value

**Returns:**

- `response`: The tool response from `__mcp_response` (usually JSON)
- `exitCode`: 0 for success, 1 for error
- `err`: Go error if execution failed (nil for exitCode 0)

## Best Practices

1. **Always use defaults**: Provide sensible default values for optional parameters
2. **Validate early**: Check required parameters and return errors immediately
3. **Return quickly**: Use `return_*` functions as soon as you have a result
4. **Handle errors**: Use `return_error()` for user-facing error messages
5. **Choose the right format**: Use `return_string` for text, `return_object` for structured data, `return_toon` for LLM-optimized output

## See Also

- [MCP Library](mcp.md) - MCP client for connecting to MCP servers
- [AI Library](ai.md) - AI client and completion functions
- [Agent Library](agent.md) - Building AI agents with automatic tool execution
