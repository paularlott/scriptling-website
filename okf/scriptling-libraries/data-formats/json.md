---
description: Parse and generate JSON data.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/data-formats/json/
sources:
    - resource: https://scriptling.dev/reference/libraries/data-formats/json/
status: stable
tags:
    - libraries
    - data-formats
title: json
type: API Reference
---
# json

The `json` library parses JSON strings into Scriptling objects and serializes Scriptling objects back to JSON strings.

## Available Functions

| Function | Description |
|----------|-------------|
| `loads(string)` | Parse a JSON string into `dict`, `list`, `str`, `int`, `float`, `bool` or `None`; objects keep the document's key order; raises on invalid JSON. |
| `dumps(object, indent=None, separators=None, sort_keys=False, ensure_ascii=True)` | Serialise to a JSON string, matching Python's `json.dumps`: keys in dict insertion order, `", "` / `": "` separators, non-ASCII escaped. |
| `parse(string)` | Alias for `loads()`. |
| `stringify(object, indent=None)` | Alias for `dumps()`. |

## Example

```python
import json

data = json.loads('{"users": [{"name": "Alice"}, {"name": "Bob"}], "ok": true}')
print(data["users"][0]["name"], data["ok"])   # Alice True

obj = {"status": "success", "count": 42}
print(json.dumps(obj))             # {"status": "success", "count": 42}
print(json.dumps(obj, separators=(",", ":")))   # {"status":"success","count":42}
print(json.dumps(obj, indent=2))   # pretty-printed, two spaces per level
# {
#   "status": "success",
#   "count": 42
# }

print(json.stringify(json.parse('[1, 2.5, null]')))  # [1, 2.5, null]

try:
    json.loads("{invalid json}")
except Exception as e:
    print("JSON parse error:", e)  # JSON parse error: JSONDecodeError: invalid character 'i' looking for beginning of object key string
```

## Differences from Python

- `loads()` builds dicts in the document's key order (a repeated key keeps its first position and its last value), so `loads()` followed by `dumps()` round-trips key order. Integers beyond 64 bits become floats, since scriptling integers are 64-bit.
- `dumps()` matches Python by default: dict keys keep the dict's insertion order, separators are `", "` and `": "`, and non-ASCII is `\u` escaped. `indent` accepts a number of spaces or a literal string; `indent=0` puts each item on its own line without indentation. `sort_keys=True`, `separators=(item, key)` and `ensure_ascii=False` are honoured.
- `dumps()` writes non-finite floats as the bare tokens `NaN`, `Infinity` and `-Infinity`, exactly like Python. `loads()` cannot read those tokens back (strict JSON only), so round-trip non-finite values as strings or `null`.
- `parse()` and `stringify()` are Scriptling aliases. There are no file-based `load()`/`dump()` functions: read the file to a string first.

## See Also

- [msgpack](https://scriptling.dev/okf/scriptling-libraries/data-formats/msgpack.md): binary serialisation — more compact, not human-readable.
- [bytes](https://scriptling.dev/okf/scriptling-libraries/data-formats/bytes.md): Scriptling's binary data type.
- [toml](https://scriptling.dev/okf/scriptling-libraries/data-formats/toml.md): parse and generate TOML configuration data.
- [yaml](https://scriptling.dev/okf/scriptling-libraries/data-formats/yaml.md): parse and generate YAML data.
- [scriptling.csv](https://scriptling.dev/okf/scriptling-libraries/utilities/csv.md): parse and generate CSV data.
- [scriptling.xml](https://scriptling.dev/okf/scriptling-libraries/utilities/xml.md): parse and generate XML data.
