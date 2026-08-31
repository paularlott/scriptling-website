---
description: Create isolated Scriptling execution environments for running script code with its own variable scope.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/runtime/sandbox/
sources:
    - resource: https://scriptling.dev/reference/libraries/runtime/sandbox/
status: stable
tags:
    - libraries
    - runtime
    - security
title: scriptling.runtime.sandbox
type: API Reference
---
# scriptling.runtime.sandbox

## Overview

The `scriptling.runtime.sandbox` library lets a running script create a fresh, independent Scriptling instance, set variables in it, execute code, and read variables back. Use it to run untrusted-shaped or dynamically generated code in its own variable scope without polluting the parent script's state.

A factory function must be configured via `SetSandboxFactory()` before `sandbox.create()` can be used.

## Available Functions

| Function | Description |
|----------|-------------|
| `create(capture_output=False)` | Create a new isolated sandbox execution environment |

## Sandbox Object Methods

| Method | Description |
|--------|-------------|
| `set(name, value)` | Set a variable in the sandbox |
| `get(name)` | Get a variable from the sandbox |
| `exec(code)` | Execute script code in the sandbox |
| `exec_file(path)` | Load and execute a script file in the sandbox |
| `exit_code()` | Get the exit code from the last execution |

## Functions

### `create(capture_output=False)`

Creates a new isolated sandbox execution environment. The sandbox inherits the same library registrations and import paths as the parent but has its own completely independent variable scope. By default, `print()` output from the sandbox is discarded; set `capture_output=True` to send output to the parent's stdout instead.

**Parameters:**
- `capture_output` (`bool`, optional): If `True`, print output goes to stdout. Default: `False` (output discarded).

**Returns:** Sandbox object: with `set()`, `get()`, `exec()`, `exec_file()`, and `exit_code()` methods.

**Raises:** `Error`: if no sandbox factory has been configured via `SetSandboxFactory()`.

```python
import scriptling.runtime as runtime

# Output from print() inside the sandbox is discarded
env = runtime.sandbox.create()

# Output from print() inside the sandbox goes to stdout
env = runtime.sandbox.create(capture_output=True)
```

### `env.set(name, value)`

Sets a variable in the sandbox's scope.

**Parameters:**
- `name` (`str`): Variable name.
- `value` (any): Value to assign.

**Returns:** `None`

```python
import scriptling.runtime as runtime

env = runtime.sandbox.create()
env.set("config", {"debug": True, "timeout": 30})
env.set("items", [1, 2, 3])
env.set("name", "test")
```

### `env.get(name)`

Retrieves a variable's value from the sandbox.

**Parameters:**
- `name` (`str`): Variable name.

**Returns:** any: the variable's value, or `None` if not found.

```python
import scriptling.runtime as runtime

env = runtime.sandbox.create()
env.set("x", 42)
env.exec("y = x * 2")
print(env.get("y"))  # 84
print(env.get("z"))  # None
```

### `env.exec(code)`

Executes script code within the sandbox. The code runs in the sandbox's isolated scope and can access variables set via `set()` and any imported libraries.

Errors during execution are captured internally: the script does not propagate errors to the caller. Check `exit_code()` after execution to determine success or failure. If the script calls `sys.exit()` or a function that triggers a `SystemExit` (such as `scriptling.mcp.tool.return_string()`), the exit code is captured and available via `exit_code()`.

**Parameters:**
- `code` (`str`): Scriptling source code to execute.

**Returns:** `None`

```python
import scriptling.runtime as runtime

env = runtime.sandbox.create()
env.set("data", [3, 1, 4, 1, 5])
env.exec("""
import json
data.sort()
result = json.dumps(data)
""")
print(env.get("result"))  # "[1, 1, 3, 4, 5]"
```

### `env.exec_file(path)`

Loads a script from the filesystem and executes it within the sandbox. Equivalent to reading the file and calling `exec()` with its contents. Import resolution uses the same library paths as the parent.

Path restrictions configured via `SetSandboxAllowedPaths()` are enforced for this method: files outside allowed directories are rejected (`exit_code()` is set to `1`). Read failures are likewise captured internally rather than propagated.

**Parameters:**
- `path` (`str`): Path to the script file.

**Returns:** `None`

```python
import scriptling.runtime as runtime

env = runtime.sandbox.create()
env.set("input_data", {"key": "value"})
env.exec_file("scripts/process.py")
output = env.get("result")
```

### `env.exit_code()`

Gets the exit code from the last `exec()` or `exec_file()` call.

**Returns:** `int`: `0` for successful execution, non-zero for errors or explicit `sys.exit(N)` calls.

```python
import scriptling.runtime as runtime

env = runtime.sandbox.create()
env.exec("x = 1 + 1")
print(env.exit_code())  # 0

env.exec("x = undefined_var")
print(env.exit_code())  # 1
```

## Examples

### Running an isolated computation

```python
import scriptling.runtime as runtime

env = runtime.sandbox.create()
env.set("numbers", [10, 20, 30, 40, 50])
env.exec("""
total = 0
for n in numbers:
    total = total + n
average = total / len(numbers)
""")
print(env.get("average"))  # 30.0
```

### Executing a script file with parameters

```python
import scriptling.runtime as runtime

env = runtime.sandbox.create()
env.set("__mcp_params", {"customer_id": 123, "format": "json"})
env.exec_file("scripts/customer_report.py")

response = env.get("__mcp_response")
code = env.exit_code()
if code != 0:
    print("Script failed with exit code:", code)
else:
    print(response)
```

### Multiple independent sandboxes

```python
import scriptling.runtime as runtime

# Each sandbox has its own isolated scope
env1 = runtime.sandbox.create()
env2 = runtime.sandbox.create()

env1.set("x", 100)
env2.set("x", 200)

env1.exec("result = x * 2")
env2.exec("result = x * 3")

print(env1.get("result"))  # 200
print(env2.get("result"))  # 600
```

## Notes

- Each `sandbox.create()` call creates a **new Scriptling instance** via the configured factory. Sandboxes do not share state with each other or with the parent.
- By default, `print()` output from sandbox scripts is **discarded**. Use `capture_output=True` to see output.
- Errors in `exec()` and `exec_file()` are **captured internally**, not propagated to the caller. Always check `exit_code()` to detect failures.
- Libraries imported inside a sandbox are resolved through the same import paths configured by the factory (e.g. the `--libpath` flag in CLI mode).
- `SystemExit` exceptions (e.g. from `scriptling.mcp.tool.return_string()`) are captured and reported via `exit_code()`: they do not terminate the parent script.
- The same factory is used by both `scriptling.runtime.sandbox` and `scriptling.runtime.background()`. Call `extlibs.SetSandboxFactory()` to configure both at once.
- Path restrictions for `exec_file()` are configured via `SetSandboxAllowedPaths()`. By default, no restrictions are applied.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#runtime-libraries).

`scriptling.runtime.sandbox` executes arbitrary Scriptling code strings: a significant risk, even though execution stays inside an isolated sub-environment within the **same OS process** (it is not a separate process or VM boundary). Filesystem access via `exec_file()` is restricted to the `allowedPaths` passed to `RegisterRuntimeSandboxLibrary(p, allowedPaths)`; by default no restrictions are applied, so an unconfigured embedder gets unrestricted file reads. Never pass untrusted or unvalidated input directly to `exec()` or `exec_file()`. See [Library Registration: Runtime Libraries](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#runtime-libraries) and [Code Injection Prevention](https://scriptling.dev/okf/scriptling-docs/security.md#code-injection-prevention).

## See Also

- [scriptling.runtime](https://scriptling.dev/okf/scriptling-libraries/runtime.md): background tasks, which share the same sandbox factory
- [scriptling.runtime.plugin](https://scriptling.dev/okf/scriptling-libraries/plugin.md): expose registered functions instead of executing arbitrary code
- [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md#code-injection-prevention)
