---
title: json
description: Parse and generate JSON data.
weight: 1

aliases:
  - /reference/libraries/stdlib/json/
  - /reference/libraries/json/
---

The `json` library parses JSON strings into Scriptling objects and serializes Scriptling objects back to JSON strings.

## Available Functions

| Function | Description |
|----------|-------------|
| `loads(string)` | Parse a JSON string into Scriptling objects. |
| `dumps(object, indent="")` | Convert Scriptling objects to a JSON string. |
| `parse(string)` | Alias for `loads()`. |
| `stringify(object, indent="")` | Alias for `dumps()`. |

## Functions

### `loads(string)`

Parses a JSON string and returns the corresponding Scriptling object.

**Parameters:**
- `string` (`str`): JSON-formatted string to parse.

**Returns:** `dict`, `list`, `str`, `int`, `float`, `bool`, or `None`: depending on the parsed JSON value.

**Raises:** `Error`: if `string` is not valid JSON.

```python
import json

data = json.loads('{"users":[{"name":"Alice"},{"name":"Bob"}]}')
first_user = data["users"][0]["name"]  # "Alice"
```

### `dumps(object, indent="")`

Converts a Scriptling object to its JSON string representation. Object keys are emitted in sorted order.

**Parameters:**
- `object` (`dict`, `list`, `str`, `int`, `float`, `bool`, or `None`): Value to serialize.
- `indent` (`str`, optional): Indentation string used for pretty-printing. Default: `""` (compact, no whitespace).

**Returns:** `str`: the JSON-formatted output.

```python
import json

obj = {"status": "success", "count": 42}
json_str = json.dumps(obj)  # '{"count":42,"status":"success"}'

pretty = json.dumps(obj, indent="  ")
# {
#   "count": 42,
#   "status": "success"
# }
```

### `parse(string)`

Alias for `loads()`.

**Parameters:**
- `string` (`str`): JSON-formatted string to parse.

**Returns:** `dict`, `list`, `str`, `int`, `float`, `bool`, or `None`

```python
import json

data = json.parse('{"key": "value"}')  # Same as json.loads()
```

### `stringify(object, indent="")`

Alias for `dumps()`.

**Parameters:**
- `object` (`dict`, `list`, `str`, `int`, `float`, `bool`, or `None`): Value to serialize.
- `indent` (`str`, optional): Indentation string used for pretty-printing. Default: `""`.

**Returns:** `str`: the JSON-formatted output.

```python
import json

json_str = json.stringify({"key": "value"})  # Same as json.dumps()
```

## Error Handling

```python
import json

try:
    data = json.loads('{"valid": "json"}')
    print("Parsed successfully")

    invalid = json.loads('{invalid json}')
    print(invalid)  # Won't reach here
except Exception as e:
    print("JSON parse error:", e)
```

## See Also

- [toml](../toml/): parse and generate TOML configuration data.
- [yaml](../yaml/): parse and generate YAML data.
- [scriptling.csv](../../scriptling/utilities/csv/): parse and generate CSV data.
- [scriptling.xml](../../scriptling/utilities/xml/): parse and generate XML data.
