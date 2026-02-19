---
title: LLM Code Generation Guide
description: Quick reference for LLMs generating Scriptling code.
weight: 7
---

A quick reference for Large Language Models generating Scriptling code.

## Quick Summary

When generating Scriptling code:

1. **Indentation**: Use 4-space indentation for blocks
2. **Booleans and Null**: Use `True`/`False` for booleans, `None` for null (all capitalized)
3. **Loops**: Use `range(n)`, `range(start, stop)`, or `range(start, stop, step)` for numeric loops
4. **Slicing**: Use slice notation: `list[1:3]`, `list[:3]`, `list[3:]`, `list[::2]`, `list[::-1]`
5. **Dict Iteration**: Use `keys(dict)`, `values(dict)`, `items(dict)` for dictionary iteration
6. **HTTP Response**: HTTP functions return a Response object with `status_code`, `body`, `text`, `headers`, `url` fields
7. **HTTP Options**: HTTP functions accept optional options dictionary with `timeout` and `headers` keys
8. **Import Libraries**: Use `import json`, `import requests`, `import re` to load libraries
9. **JSON Functions**: Always use `json.loads()` and `json.dumps()` for JSON (dot notation)
10. **HTTP Functions**: Always use `requests.get()`, `requests.post()`, etc. for HTTP (dot notation)
11. **Regex**: Use `re.match()`, `re.search()`, `re.findall()`, `re.sub()`, `re.split()` for regex
12. **Timeouts**: Default HTTP timeout is 5 seconds if not specified
13. **Conditions**: Use `elif` for multiple conditions
14. **Augmented Assignment**: Use augmented assignment: `x += 1`, `x *= 2`, etc.
15. **Loop Control**: Use `break` to exit loops, `continue` to skip iterations
16. **Placeholder**: Use `pass` as a placeholder in empty blocks
17. **List Append**: `append(list, item)` modifies list in-place
18. **String Concat**: Strings use `+` for concatenation
19. **File Extension**: Use `.py` file extension
20. **Status Checks**: Check `response.status_code` before processing
21. **Error Handling**: Use `try`/`except`/`finally` for error handling
22. **Raise Errors**: Use `raise "message"` or `raise ValueError("msg")` to raise errors
23. **Unpacking**: Multiple assignment: `a, b = [1, 2]` for unpacking lists
24. **Variadic Args**: Use `*args` to collect extra positional arguments into a list
25. **Keyword Args**: Use `**kwargs` to collect extra keyword arguments into a dictionary

## Key Differences from Python

- **No Nested Classes**: Classes must be defined at the top level of a module
- **Single Inheritance Only**: Multiple inheritance is not supported
- **HTTP Response Format**: Response object with `status_code`, `body`, `text`, `headers`, `url` fields
- **Default Timeout**: HTTP requests have a 5-second default timeout
- **No Generators**: `yield` is not supported
- **No Dict Comprehensions**: Only list comprehensions are supported

## Code Template

```python
import json
import requests

# HTTP with headers and status check
options = {
    "timeout": 10,
    "headers": {"Authorization": "Bearer token"}
}
resp = requests.get("https://api.example.com/data", options)

if resp.status_code == 200:
    data = json.loads(resp.body)
    # Process data
    result = {"success": True, "count": len(data)}
else:
    result = {"success": False, "error": resp.status_code}

# Return structured data
scriptling.mcp.tool.return_object(result)
```

## Common Patterns

### Error Handling

```python
try:
    result = risky_operation()
except Exception as e:
    result = None
finally:
    cleanup()
```

### Loop with Index

```python
for item in items(data):
    key = item[0]
    value = item[1]
    print(key, value)
```

### String Building in Loops

```python
# Use join() for efficiency
parts = []
for item in items:
    parts.append(str(item))
result = "".join(parts)
```

### HTTP POST with JSON

```python
import json
import requests

payload = {"name": "Alice", "email": "alice@example.com"}
body = json.dumps(payload)
options = {"timeout": 10, "headers": {"Content-Type": "application/json"}}

response = requests.post("https://api.example.com/users", body, options)

if response.status_code == 201:
    created = json.loads(response.body)
    print("Created user:", created["id"])
```

## See Also

- [Language Guide](../language/) - Complete language reference
- [Library Cheat Sheet](../libraries/cheat-sheet/) - Quick library reference
- [Python Differences](../language/python-differences/) - What's NOT supported
