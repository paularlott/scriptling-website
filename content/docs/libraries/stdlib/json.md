---
title: json
weight: 1
---

Functions for parsing and generating JSON data.

## Available Functions

| Function                   | Description                                 |
| -------------------------- | ------------------------------------------- |
| `loads(string)`            | Parse a JSON string into Scriptling objects |
| `dumps(object, indent="")` | Convert Scriptling objects to a JSON string |
| `parse(string)`            | Alias for `loads()`                         |
| `stringify(object)`        | Alias for `dumps()`                         |

## Functions

### json.loads(string)

Parses a JSON string and returns Scriptling objects.

**Parameters:**

- `string`: JSON string to parse

**Returns:** Scriptling object (dict, list, string, number, boolean, or null)

**Example:**

```python
import json

data = json.loads('{"users":[{"name":"Alice"},{"name":"Bob"}]}')
first_user = data["users"][0]["name"]  # "Alice"
```

### json.dumps(object, indent="")

Converts Scriptling objects to a JSON string.

**Parameters:**

- `object`: Scriptling object to convert (dict, list, string, number, boolean, or null)
- `indent` (optional): String to use for indentation (enables pretty-printing)

**Returns:** String (JSON formatted)

**Example:**

```python
import json

obj = {"status": "success", "count": 42}
json_str = json.dumps(obj)  # '{"count":42,"status":"success"}'

# Pretty-printed with 2-space indentation
pretty = json.dumps(obj, indent="  ")
# {
#   "count": 42,
#   "status": "success"
# }
```

### json.parse(string)

Alias for `json.loads()`. Parses a JSON string and returns Scriptling objects.

```python
import json
data = json.parse('{"key": "value"}')  # Same as json.loads()
```

### json.stringify(object, indent="")

Alias for `json.dumps()`. Converts Scriptling objects to a JSON string.

```python
import json
json_str = json.stringify({"key": "value"})  # Same as json.dumps()
```

## Supported Types

### Parsing (json.loads)

- JSON objects → Scriptling dictionaries
- JSON arrays → Scriptling lists
- JSON strings → Scriptling strings
- JSON numbers → Scriptling integers/floats
- JSON booleans → Scriptling booleans
- JSON null → Scriptling null

### Stringifying (json.dumps)

- Scriptling dictionaries → JSON objects
- Scriptling lists → JSON arrays
- Scriptling strings → JSON strings
- Scriptling integers/floats → JSON numbers
- Scriptling booleans → JSON booleans
- Scriptling null → JSON null

## Usage Examples

```python
import json

# Parse JSON
json_str = '{"name":"Alice","age":30,"active":true,"scores":[85,92,78]}'
data = json.loads(json_str)

print(data["name"])    # "Alice"
print(data["age"])     # 30
print(data["active"])  # True
print(data["scores"][0])  # 85

# Create and stringify
person = {
    "name": "Bob",
    "age": 25,
    "hobbies": ["reading", "coding", "gaming"]
}

json_output = json.dumps(person)
print(json_output)
# {"age":25,"hobbies":["reading","coding","gaming"],"name":"Bob"}

# Pretty-print with indentation
pretty_json = json.dumps(person, indent="  ")
print(pretty_json)
# {
#   "age": 25,
#   "hobbies": [
#     "reading",
#     "coding",
#     "gaming"
#   ],
#   "name": "Bob"
# }
```

## Error Handling

```python
import json

try:
    # This will work
    data = json.loads('{"valid": "json"}')
    print("Parsed successfully")

    # This will fail with invalid JSON
    invalid = json.loads('{invalid json}')
    print(invalid)  # Won't reach here
except Exception as e:
    print("JSON parse error:", e)
```
