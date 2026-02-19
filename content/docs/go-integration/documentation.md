---
title: Documenting Extensions
description: Add help text to functions, libraries, and classes for discoverability.
weight: 5
---

Scriptling includes a built-in `help()` function that provides Python-like help for functions and libraries. This guide shows how to document your Go extensions.

## Using the Help System

The `help()` function works like Python's help system:

```python
# Show general help
help()

# List all available libraries
help("modules")

# List all builtin functions
help("builtins")

# Get help for a specific builtin function
help("print")
help("len")

# Get help for a library
import math
help("math")

# Get help for a library function
help("math.sqrt")

# Get help for user-defined functions
def my_function(a, b=10):
    return a + b

help("my_function")
help(my_function)  # Can also pass the function object
```

## Documenting Native Functions

When registering Go functions, provide documentation via the `HelpText` field:

```go
p.RegisterFunc("my_func", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    // Implementation
    return object.None
}, `my_func(arg1, arg2) - Brief description

  Detailed description of what the function does.

  Parameters:
    arg1 - Description of first parameter
    arg2 - Description of second parameter

  Returns:
    Description of return value

  Examples:
    my_func("value1", "value2")
`)
```

If you omit the help text, basic help will be auto-generated:

```go
p.RegisterFunc("my_func", func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
    return object.None
})  // Auto-generates: "my_func(...) - User-defined function"
```

## Documenting Native Libraries

Go libraries include a description parameter:

```go
var MyLibrary = object.NewLibrary("mylib",
    map[string]*object.Builtin{
        "process": {
            Fn: func(ctx context.Context, kwargs object.Kwargs, args ...object.Object) object.Object {
                return &object.String{Value: "processed"}
            },
            HelpText: `process(data) - Process the input data

  Parameters:
    data - The data to process (string or list)

  Returns:
    Processed data as a string

  Examples:
    mylib.process("hello")
`,
        },
    },
    nil,
    "My custom data processing library",  // Library description
)
```

## Documenting with Builder API

### Function Builder

```go
fb := object.NewFunctionBuilder()
fn := fb.FunctionWithHelp(func(a, b int) int {
    return a + b
}, `add(a, b) - Add two integers

  Parameters:
    a - First integer
    b - Second integer

  Returns:
    The sum of a and b

  Examples:
    add(1, 2)  # Returns 3
`).Build()

p.RegisterFunc("add", fn)
```

### Library Builder

```go
library := object.NewLibraryBuilder("mylib", "My custom data processing library").
    FunctionWithHelp("process", func(data string) string {
        return "processed: " + data
    }, `process(data) - Process the input data

  Parameters:
    data - The data to process

  Returns:
    Processed data as string
`).
    Constant("MAX_SIZE", 1000).
    Build()

p.RegisterLibrary(library)
```

### Class Builder

```go
classBuilder := object.NewClassBuilder("MyClass")
classBuilder.MethodWithHelp("__init__", func(self *object.Instance, name string) {
    self.Fields["name"] = &object.String{Value: name}
}, `__init__(name) - Initialize MyClass

  Parameters:
    name - The name for this instance
`)
classBuilder.MethodWithHelp("get_data", func(self *object.Instance) string {
    name, _ := self.Fields["name"].AsString()
    return "data for " + name
}, `get_data() - Get data for this instance

  Returns:
    Data string with the instance name
`)
```

## Documenting Script Functions

When registering Scriptling functions, docstrings in the script become help text:

```go
script := `
def process_data(data):
    """Process input data and return result.

    Args:
        data: The data to process

    Returns:
        Processed data
    """
    return data.upper()

process_data
`

err := p.RegisterScriptFunc("process_data", script)
```

## Documenting Script Libraries

Register a complete library with module docstring and function docstrings:

```go
err := p.RegisterScriptLibrary("mylib", `
"""My Library - Custom data processing utilities.

This library provides functions for data processing and formatting.
"""

def process(data):
    """Process input data.

    Args:
        data: Input string or list

    Returns:
        Processed data
    """
    if isinstance(data, str):
        return data.upper()
    return data

def format(value, fmt_type="default"):
    """Format a value for display.

    Args:
        value: Value to format
        fmt_type: Format type (default: "default")

    Returns:
        Formatted string
    """
    return str(value)
`)

// Users can now access help
// help("mylib")          # Shows module docstring
// help("mylib.process")  # Shows function docstring
```

## User Functions with Docstrings

Scriptling supports Python-style docstrings. If the first statement in your function body is a string literal, it becomes documentation:

```python
def calculate_area(radius):
    """Calculate the area of a circle.

    Parameters:
      radius - The radius of the circle

    Returns:
      The area as a float
    """
    return 3.14159 * radius * radius

help(calculate_area)
```

## Help Text Best Practices

### Format

1. **First Line**: Function signature and brief one-line description
2. **Blank Line**: Add a blank line after the first line
3. **Detailed Description**: Provide more detailed explanation if needed
4. **Parameters Section**: List each parameter with description
5. **Returns Section**: Describe what the function returns
6. **Examples Section**: Provide practical usage examples

### Example

```go
HelpText: `fetch(url, timeout=30) - Fetch data from a URL

  Makes an HTTP GET request to the specified URL and returns
  the response data.

  Parameters:
    url - The URL to fetch (required)
    timeout - Request timeout in seconds (default: 30)

  Returns:
    Response object with status_code, body, and headers

  Raises:
    Error if the request times out or fails

  Examples:
    response = fetch("https://api.example.com/data")
    if response.status_code == 200:
        print(response.body)
`,
```

## Registration Summary

| Method | Help Source |
|--------|-------------|
| `RegisterFunc(name, func, help)` | Help text parameter |
| `RegisterScriptFunc(name, script)` | Docstring in script |
| `RegisterLibrary(library)` | Library's HelpText fields |
| `RegisterScriptLibrary(name, script)` | Module/function docstrings |
| `FunctionBuilder.FunctionWithHelp(fn, help)` | Help text parameter |
| `LibraryBuilder(name, description)` | Description + FunctionWithHelp |

## Notes

- **Optional**: Help text is optional. If not provided, `help()` shows "No documentation available"
- **User Functions**: User-defined functions automatically show parameter information including defaults
- **Libraries**: `help("library_name")` lists all functions in the library
- **Discoverability**: Use `help("modules")` to see all imported and available libraries

## See Also

- [Native Functions](native/functions/) - Registering Go functions
- [Native Libraries](native/libraries/) - Creating Go libraries
- [Builder Functions](builder/functions/) - Type-safe function builder
- [Builder Libraries](builder/libraries/) - Type-safe library builder
- [Script Extensions](scripts/) - Script-based extensions
