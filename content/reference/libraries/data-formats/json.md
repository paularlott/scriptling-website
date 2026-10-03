---
title: json
description: Parse and generate JSON data.
tags: [libraries, data-formats]
weight: 2

aliases:
  - /reference/libraries/stdlib/json/
  - /reference/libraries/json/
---

The `json` library parses JSON strings into Scriptling objects and serializes Scriptling objects back to JSON strings.

## Available Functions

| Function | Description |
|----------|-------------|
| `loads(string)` | Parse a JSON string into `dict`, `list`, `str`, `int`, `float`, `bool` or `None`; raises on invalid JSON. |
| `dumps(object, indent=None)` | Serialise to a JSON string: compact with sorted keys by default; `indent` (spaces or a string) pretty-prints. |
| `parse(string)` | Alias for `loads()`. |
| `stringify(object, indent=None)` | Alias for `dumps()`. |

## Example

```python
import json

data = json.loads('{"users": [{"name": "Alice"}, {"name": "Bob"}], "ok": true}')
print(data["users"][0]["name"], data["ok"])   # Alice True

obj = {"status": "success", "count": 42}
print(json.dumps(obj))             # {"count":42,"status":"success"}
print(json.dumps(obj, indent=2))   # pretty-printed, two spaces per level
# {
#   "count": 42,
#   "status": "success"
# }

print(json.stringify(json.parse('[1, 2.5, null]')))  # [1,2.5,null]

try:
    json.loads("{invalid json}")
except Exception as e:
    print("JSON parse error:", e)  # JSON parse error: JSONDecodeError: invalid character 'i' looking for beginning of object key string
```

## Differences from Python

- `dumps()` output is compact by default (`{"a":1}`, no spaces after `,` and `:`) and object keys are always sorted. `indent` accepts a number of spaces or a literal string; `indent=0` puts each item on its own line without indentation.
- Non-ASCII characters are written as-is rather than `\u` escaped; there is no `ensure_ascii`, `sort_keys`, `separators` or `default` parameter.
- `nan` and `inf` raise an error instead of producing `NaN`/`Infinity`.
- `parse()` and `stringify()` are Scriptling aliases. There are no file-based `load()`/`dump()` functions: read the file to a string first.

## See Also

- [msgpack](../msgpack/): binary serialisation — more compact, not human-readable.
- [bytes](../bytes/): Scriptling's binary data type.
- [toml](../toml/): parse and generate TOML configuration data.
- [yaml](../yaml/): parse and generate YAML data.
- [scriptling.csv](../../utilities/csv/): parse and generate CSV data.
- [scriptling.xml](../../utilities/xml/): parse and generate XML data.
