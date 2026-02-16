---
title: Libraries
description: Available libraries and APIs in Scriptling.
weight: 3
---

Scriptling provides a rich set of libraries organized into three categories.

## Core Functions

Always available without importing:

### I/O
- `print(value)` - Output to console

### Type Conversions
- `str(value)` - Convert to string
- `int(value)` - Convert to integer
- `float(value)` - Convert to float
- `bool(value)` - Convert to boolean
- `list(value)` - Convert to list
- `dict(value)` - Convert to dictionary

### System
- `import library_name` - Load library dynamically
- `help([object])` - Display help information
- `type(object)` - Get type of object
- `isinstance(object, type)` - Check if object is instance of type

## Library Categories

### [Standard Libraries](stdlib/)

Built-in libraries available for import without any registration. These include common utilities like JSON, math, regex, and time handling.

### [Scriptling Libraries](scriptling/)

Scriptling-specific libraries for AI/LLM integration, MCP protocol support, HTTP server functionality, and concurrency.

### [Extended Libraries](extlib/)

Python-compatible libraries requiring explicit registration by the host application. These include HTTP requests, filesystem access, and subprocess management.

## Quick Reference

```python
# Import and use libraries
import json
import math
import requests

# JSON
data = json.loads('{"key": "value"}')
text = json.dumps(data)

# Math
result = math.sqrt(16)  # 4.0

# HTTP (requires registration)
response = requests.get("https://api.example.com")
```

## Getting Help

Use the `help()` function within scripts:

```python
import json
help(json)
```
