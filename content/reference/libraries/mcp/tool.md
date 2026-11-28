---
title: scriptling.mcp.tool
linkTitle: mcp.tool
description: MCP tool helper for authoring MCP tools, with parameter access and result handling.
tags: [libraries, mcp]
weight: 2

aliases:
  - /reference/libraries/scriptling/mcp/tool/
---

MCP tool helper library for authoring MCP tools in scriptling. This sub-library provides functions for parameter access and result handling when implementing tool scripts.

For the MCP client library (connecting to MCP servers), see [scriptling.mcp](../client/).

## Enabling

The tool helpers are a separate, optional sub-library. Register it explicitly when needed:

```go
mcp.RegisterToolHelpers(sl)  // Registers scriptling.mcp.tool
```

## Environment Variables

MCP tool helpers read and write environment variables set by the MCP tool execution environment:

- **`__mcp_params`**: Dictionary containing tool parameters.
- **`__mcp_response`**: String containing the tool's result.

## Available Functions

| Function | Description |
|----------|-------------|
| `get_int(name, default=0)` | Get an integer parameter |
| `get_float(name, default=0.0)` | Get a float parameter |
| `get_string(name, default="")` | Get a string parameter (trims whitespace) |
| `get_bool(name, default=False)` | Get a boolean parameter |
| `get_list(name, default=None)` | Get a list parameter (splits strings by comma) |
| `get_string_list(name, default=None)` | Get a string array parameter |
| `get_int_list(name, default=None)` | Get an integer array parameter |
| `get_float_list(name, default=None)` | Get a float array parameter |
| `get_bool_list(name, default=None)` | Get a boolean array parameter |
| `get_request()` | Get the HTTP request this call arrived on, or `None` |
| `request_context()` | Get the context dict set by the middleware (empty dict if none) |
| `return_string(text)` | Return a string result and stop execution |
| `return_object(obj)` | Return an object as JSON and stop execution |
| `return_structured(obj)` | Return an object as `structuredContent` (plus the same JSON as text) and stop execution |
| `return_toon(obj)` | Return an object as TOON and stop execution |
| `return_error(message)` | Return an error message and stop execution |
| `progress(progress, total=None, message=None)` | Report progress to the client (no-op unless it asked for progress) |
| `can_ask()` | Whether the person using the client can be asked questions |
| `confirm(message)` | Ask the person to approve an action; True only if they did |
| `ask(message, schema, key="")` | Ask the person to fill in a form; their answer, or None if they can't be asked |
| `remember(name, value)` | Keep a value for the tool's re-run after a question |
| `recall(name, default=None)` | Read back what `remember()` kept |

## Parameter Access Functions

### `mcp.tool.get_int(name, default=0)`

Gets an integer parameter from the tool's input arguments. Returns the default value if the parameter doesn't exist or can't be coerced to an integer.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`int`, optional): Default value if the parameter is missing. Default: `0`.

**Returns:** `int`

```python
import scriptling.mcp.tool as tool

project_id = tool.get_int("project_id", 0)
limit = tool.get_int("limit", 100)
```

### `mcp.tool.get_float(name, default=0.0)`

Gets a float parameter from the tool's input arguments. Returns the default value if the parameter doesn't exist or can't be coerced to a float.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`float`, optional): Default value if the parameter is missing. Default: `0.0`.

**Returns:** `float`

```python
import scriptling.mcp.tool as tool

price = tool.get_float("price", 0.0)
percentage = tool.get_float("percentage", 100.0)
```

### `mcp.tool.get_string(name, default="")`

Gets a string parameter from the tool's input arguments. Automatically trims whitespace, and returns the default value if the parameter doesn't exist, is empty, or is whitespace-only.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`str`, optional): Default value if the parameter is missing or empty. Default: `""`.

**Returns:** `str`

```python
import scriptling.mcp.tool as tool

name = tool.get_string("name", "guest")
query = tool.get_string("query")
```

### `mcp.tool.get_bool(name, default=False)`

Gets a boolean parameter from the tool's input arguments. Handles `"true"`/`"false"` strings (case-insensitive) and numeric `0`/`1`.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`bool`, optional): Default value if the parameter is missing or can't be converted. Default: `False`.

**Returns:** `bool`

```python
import scriptling.mcp.tool as tool

enabled = tool.get_bool("enabled", True)
verbose = tool.get_bool("verbose")
```

### `mcp.tool.get_list(name, default=None)`

Gets a list parameter from the tool's input arguments. If the value is a string, splits it by comma.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`list`, optional): Default value if the parameter is missing. Default: empty list.

**Returns:** `list`

```python
import scriptling.mcp.tool as tool

ids = tool.get_list("ids")              # "1,2,3" → ["1", "2", "3"]
tags = tool.get_list("tags", ["all"])   # "tag1, tag2" → ["tag1", "tag2"]
```

### `mcp.tool.get_string_list(name, default=None)`

Gets a string array parameter (`array:string` type) from the tool's input arguments.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`list`, optional): Default value if the parameter is missing. Default: empty list.

**Returns:** `list` of `str`

```python
import scriptling.mcp.tool as tool

args = tool.get_string_list("arguments")  # ["--verbose", "-o", "file.txt"]
tags = tool.get_string_list("tags", ["default"])
```

### `mcp.tool.get_int_list(name, default=None)`

Gets an integer array parameter (`array:int` type) from the tool's input arguments.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`list`, optional): Default value if the parameter is missing. Default: empty list.

**Returns:** `list` of `int`

```python
import scriptling.mcp.tool as tool

ids = tool.get_int_list("ids")  # [1, 2, 3, 4]
ports = tool.get_int_list("ports", [8080])
```

### `mcp.tool.get_float_list(name, default=None)`

Gets a float array parameter (`array:float` type) from the tool's input arguments.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`list`, optional): Default value if the parameter is missing. Default: empty list.

**Returns:** `list` of `float`

```python
import scriptling.mcp.tool as tool

prices = tool.get_float_list("prices")  # [19.99, 29.99, 39.99]
weights = tool.get_float_list("weights", [1.0])
```

### `mcp.tool.get_bool_list(name, default=None)`

Gets a boolean array parameter (`array:bool` type) from the tool's input arguments.

**Parameters:**

- `name` (`str`): Parameter name.
- `default` (`list`, optional): Default value if the parameter is missing. Default: empty list.

**Returns:** `list` of `bool`

```python
import scriptling.mcp.tool as tool

flags = tool.get_bool_list("flags")  # [True, False, True]
options = tool.get_bool_list("options", [False])
```

## Request Access Functions

When the MCP server is served over HTTP, these give tool scripts a look at the HTTP request the call arrived on — the same one the server's [middleware](/reference/libraries/runtime/http/#middlewarehandler) saw. Over the stdio transport there is no HTTP request.

### `mcp.tool.get_request()`

Returns the HTTP request this tool call is being served for: a [Request object](/reference/libraries/runtime/http/#request-object) with `method`, `path`, `headers`, `query`, `remote_addr`, `context` and `auth` (the authenticated caller, or `None`). Returns `None` over stdio or anywhere else outside a served request.

**Returns:** `Request` or `None`

```python
import scriptling.mcp.tool as tool

req = tool.get_request()
if req != None:
    log(req.remote_addr + " called this tool")
```

### `mcp.tool.request_context()`

Returns the context dict the middleware populated for this request — e.g. `request.context["user"] = name` after authenticating. Always a dict: empty when no middleware ran or it set nothing, so `.get(name, default)` is always safe. Each call gets its own copy, so writes from the handler are local and never visible to other handlers.

**Returns:** `dict`

```python
import scriptling.mcp.tool as tool

user = tool.request_context().get("user", "anonymous")
tool.return_string("hello " + user)
```

## Result Functions

Result functions set the tool's response and immediately stop script execution using `SystemExit`. No code after these calls will execute.

### `mcp.tool.return_string(text)`

Returns a string result and stops execution.

**Parameters:**

- `text` (`str`): The result text.

**Returns:** `None`: execution stops before returning to caller.

```python
import scriptling.mcp.tool as tool

tool.return_string("Search completed successfully")
# Code here will not execute
```

### `mcp.tool.return_object(obj)`

Returns an object as JSON and stops execution.

**Parameters:**

- `obj` (`dict` or `list`): The result object.

**Returns:** `None`: execution stops before returning to caller.

```python
import scriptling.mcp.tool as tool

tool.return_object({"status": "success", "count": 42})
# Code here will not execute
```

### `mcp.tool.return_structured(obj)`

Returns an object as the tool result's `structuredContent` field and stops execution. The same JSON is also attached as a text content block, so clients that don't read `structuredContent` still see the data — this is the return to use for [MCP Apps](/reference/libraries/mcp/mcp-apps/) views, which read `structuredContent` to render themselves. The argument must be a `dict`; anything else is an error.

**Parameters:**

- `obj` (`dict`): The structured result object.

**Returns:** `None`: execution stops before returning to caller.

```python
import scriptling.mcp.tool as tool

tool.return_structured({"records": records, "total": len(records)})
# Code here will not execute
```

### `mcp.tool.return_toon(obj)`

Returns an object encoded as TOON (compact text format optimized for LLMs) and stops execution.

**Parameters:**

- `obj` (`dict` or `list`): The result object.

**Returns:** `None`: execution stops before returning to caller.

```python
import scriptling.mcp.tool as tool

tool.return_toon({"result": data})
# Code here will not execute
```

### `mcp.tool.return_error(message)`

Returns an error message and stops execution with error code 1. The client receives a tool result with `isError` set and the message as its text (a tool execution error, not a JSON-RPC error), so the model can see what went wrong and retry.

**Parameters:**

- `message` (`str`): Error message.

**Returns:** `None`: execution stops before returning to caller.

```python
import scriptling.mcp.tool as tool

if not customer_id:
    tool.return_error("Customer ID is required")
    # Code here will not execute

tool.return_error("Customer not found")
```

## Progress

### `mcp.tool.progress(progress, total=None, message=None)`

Sends a `notifications/progress` message for the MCP request the tool, prompt or resource handler is serving, so the client can show how far a long-running call has got. It does nothing when the client didn't ask for progress (it sent no `progressToken`), and nothing after the request has been answered, so it is always safe to call. Unlike the `return_*` functions it doesn't stop execution.

**Parameters:**

- `progress` (`int` | `float`): Work done so far. It must increase with every call; a value that doesn't raises `ValueError`.
- `total` (`int` | `float`, optional): Total amount of work, when known.
- `message` (`str`, optional): Human-readable status.

Calls closer together than 10ms are dropped, except the one that reaches `total`.

```python
import scriptling.mcp.tool as tool

files = tool.get_string_list("files")
for i, name in enumerate(files):
    convert(name)
    tool.progress(i + 1, total=len(files), message="Converted " + name)
tool.return_string("Converted " + str(len(files)) + " files")
```

## Asking the Person (Elicitation)

A tool can stop to ask the person using the MCP client something: approve an action, pick an option, fill in a few fields. The client shows the question as a form, which MCP calls elicitation. Only clients that support elicitation can be asked; `can_ask()` tells you, and the other functions degrade safely when it is `False`.

**The tool may run twice.** Clients on MCP 2025-06-18 and 2025-11-25 are asked mid-call, and `ask()` waits for the answer. Clients on 2026-07-28 (and hosts that call tools in-process, such as a chat UI) answer by calling the tool again: the script stops at the question, then runs again from the top, and this time the question returns the answer at once. So:

- Read and check everything before asking, and write only after the answer.
- Ask the same questions in the same order on every run.
- Keep slow or AI work done before the question with `remember()`, and read it back with `recall()`, so it isn't done twice.

### `mcp.tool.can_ask()`

Returns `True` when the client supports elicitation for this call, so `ask()` and `confirm()` reach the person. When it is `False`, `ask()` returns `None` and `confirm()` returns `False`.

```python
import scriptling.mcp.tool as tool

if not tool.can_ask() and not tool.get_bool("confirmed"):
    tool.return_error("Ask the user to confirm, then call again with confirmed=true")
```

### `mcp.tool.confirm(message)`

Shows `message` with an Approve box. Returns `True` only when the person submitted it with the box ticked; `False` when they declined, dismissed it or left the box unticked, and when the client cannot be asked.

**Parameters:**

- `message` (`str`): The action to approve. It is shown as plain text.

```python
import scriptling.mcp.tool as tool

ids = find_archived_invoices()
if not tool.confirm("Delete the " + str(len(ids)) + " archived invoices?"):
    tool.return_error("Not confirmed, nothing was deleted")
delete_invoices(ids)
tool.return_string("Deleted " + str(len(ids)) + " invoices")
```

The question is named after its text, so when a re-run asks something different (it read different data), the person is asked again rather than reusing the earlier yes. Name what is being approved in the message ("Delete invoice 1042?", not "Are you sure?"). The same message may be asked more than once in one call, and a question nobody answers in time counts as no.

### `mcp.tool.ask(message, schema, key="")`

Shows `message` with a form built from `schema`, and returns the person's answer.

**Parameters:**

- `message` (`str`): What is being asked, and why.
- `schema` (`dict`): The form, as a JSON Schema object whose properties are flat: `string` (optionally with `format` `email`, `uri`, `date` or `date-time`, and `minLength`/`maxLength`), `number` and `integer` (with `minimum`/`maximum`), `boolean`, a string `enum` (or `oneOf` with `const` and `title`) for a single choice, and an `array` of enum items for a multiple choice. Properties may have a `title`, `description` and `default`; list the ones that must be filled in under `required`.
- `key` (`str`, optional): The question's name. Left empty, the question is named after its message and schema, so an answer is never taken for a different question when a re-run asks about something else. Set it yourself only to name the question explicitly, changing it whenever what is being asked changes.

**Returns:** `dict`: `{"action": "accept", "content": {...}}` when the person submitted the form (integer properties as `int`), `{"action": "decline"}` when they declined, `{"action": "cancel"}` when they dismissed it or didn't answer in time. `None` when the client cannot be asked.

```python
import scriptling.mcp.tool as tool

answer = tool.ask("Where should the report go?", {
    "type": "object",
    "properties": {
        "env": {"type": "string", "title": "Environment", "enum": ["staging", "prod"]},
        "notify": {"type": "boolean", "title": "Email the team", "default": False},
    },
    "required": ["env"],
})
if answer is None or answer["action"] != "accept":
    tool.return_error("No environment chosen, nothing was published")
publish(answer["content"]["env"], answer["content"]["notify"])
```

### `mcp.tool.remember(name, value)`

Keeps `value` for the tool's re-run after a question, so work done before the question is not done again. The value travels to the client with the question and back with the answer, signed so it cannot be changed, and only the same call from the same user can bring it back. Keep it small, and keep only what the person may see: plain values, lists and dicts. It lasts until the call finishes. It is a cache, not a record: until the question state expires, a client can send an earlier round's state back with earlier kept values, so never let a recalled value authorize anything on its own.

**Parameters:**

- `name` (`str`): The value's name.
- `value`: The value to keep.

**Returns:** `bool`: `True` when kept; `False` when there will be no re-run to keep it for (the client is asked mid-call, or cannot be asked). `recall()` then returns its default, so the work is simply done each time.

### `mcp.tool.recall(name, default=None)`

Returns the value an earlier run of this same tool call kept with `remember(name, value)`, or `default` when there is none. A kept value travels as JSON, so it comes back with JSON's types: a whole number is an `int` (also inside lists and dicts), any other number a `float`, a tuple a `list`.

```python
import scriptling.mcp.tool as tool

plan = tool.recall("plan")
if plan is None:
    plan = make_plan(tool.get_string("goal"))   # slow, or an AI call
    tool.remember("plan", plan)
if not tool.confirm("Apply this plan? " + plan["summary"]):
    tool.return_error("Not confirmed, nothing was changed")
apply_plan(plan)
```

## Complete Tool Example

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
# Tool script: greet_user.py
import scriptling.mcp.tool as tool

name = tool.get_string("name", "guest")
age = tool.get_int("age", 0)

tool.return_object({
    "message": f"Hello, {name}! You are {age} years old."
})
```

The tool execution environment will:

1. Set the `__mcp_params` dict with tool parameters.
2. Run the script.
3. Catch the `SystemExit` exception from `return_*` functions.
4. Extract the result from `__mcp_response`.
5. Return it to the MCP client.

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

**Function signature:**

```go
func RunToolScript(
    ctx context.Context,
    sl *scriptling.Scriptling,
    script string,
    params map[string]interface{}
) (response string, exitCode int, err error)
```

**Parameters:**

- `ctx`: Context for cancellation and timeouts.
- `sl`: Scriptling instance (must have tool helpers registered).
- `script`: The tool script code.
- `params`: Map of parameter name to value.

**Returns:**

- `response`: The tool response from `__mcp_response` (usually JSON).
- `exitCode`: `0` for success, `1` for error.
- `err`: Go error if execution failed (`nil` for `exitCode` `0`).

## Best Practices

1. **Always use defaults**: Provide sensible default values for optional parameters.
2. **Validate early**: Check required parameters and return errors immediately.
3. **Return quickly**: Use `return_*` functions as soon as you have a result.
4. **Handle errors**: Use `return_error()` for user-facing error messages.
5. **Choose the right format**: Use `return_string` for text, `return_object` for structured data, `return_toon` for LLM-optimized output.
6. **Ask before writing**: When a tool asks the person with `confirm()` or `ask()`, do every check before the question and every write after it, since the tool may run again from the top to get the answer.

## Security Considerations

This is an extension library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extension-libraries).

`scriptling.mcp.tool` itself has no implicit network, filesystem, or process access: it only reads `__mcp_params` and writes `__mcp_response`. Risk depends entirely on what the tool script you write does with those parameters.

Answers from `ask()` and `confirm()` come from the person through their client, so validate them like any other input. Values kept with `remember()` are signed, not encrypted: the client can read them, so never keep secrets there.

## See Also

- [scriptling.mcp](../client/): MCP client for connecting to MCP servers
- [scriptling.ai](../../ai/): AI client and completion functions
- [scriptling.ai.agent](../../ai/agent/): Building AI agents with automatic tool execution
