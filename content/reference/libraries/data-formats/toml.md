---
title: toml
description: Parse and generate TOML (Tom's Obvious Minimal Language) data.
tags: [libraries, data-formats]
weight: 1

aliases:
  - /reference/libraries/extlib/toml/
  - /reference/libraries/toml/
---

The `toml` library parses TOML strings into Scriptling objects and serializes Scriptling objects back to TOML strings. Commonly used for configuration files such as `pyproject.toml` or `Cargo.toml`.

## Available Functions

| Function | Description |
|----------|-------------|
| `loads(toml_string)` | Parse a TOML string into a Scriptling object. |
| `dumps(obj)` | Convert a Scriptling object to a TOML string. |

## Functions

### `loads(toml_string)`

Parses a TOML string and returns the corresponding Scriptling object.

**Parameters:**
- `toml_string` (`str`): TOML-formatted string to parse.

**Returns:** `dict`, `list`, `str`, `int`, `float`, `bool`, or `None`: depending on the parsed TOML value. Datetimes are returned as ISO-formatted strings.

**Raises:** `Error`: if `toml_string` is not valid TOML.

```python
import toml

data = toml.loads("""
[database]
host = "localhost"
port = 5432
enabled = true

[servers]
alpha = "10.0.0.1"
beta = "10.0.0.2"
""")

print(data["database"]["host"])  # localhost
print(data["database"]["port"])  # 5432
print(data["servers"]["alpha"])  # 10.0.0.1
```

### `dumps(obj)`

Converts a Scriptling object to a TOML-formatted string.

**Parameters:**
- `obj` (`dict`, `list`, `str`, `int`, `float`, `bool`, or `None`): Value to serialize.

**Returns:** `str`: the TOML-formatted output.

```python
import toml

data = {
    "title": "My App",
    "database": {
        "host": "localhost",
        "port": 5432
    },
    "features": ["auth", "logging", "api"]
}

toml_str = toml.dumps(data)
print(toml_str)
# title = "My App"
# features = ["auth", "logging", "api"]
#
# [database]
# host = "localhost"
# port = 5432
```

## Complete Example

```python
import toml

config_toml = """
[server]
host = "0.0.0.0"
port = 8080
workers = 4

[database]
url = "postgres://localhost/mydb"
pool_size = 10
timeout = 30.5

[[servers]]
name = "web1"
ip = "10.0.0.1"

[[servers]]
name = "web2"
ip = "10.0.0.2"
"""

config = toml.loads(config_toml)

print("Server host:", config["server"]["host"])
print("Database URL:", config["database"]["url"])

for server in config["servers"]:
    print(f"Server {server['name']}: {server['ip']}")

config["server"]["workers"] = 8
updated_toml = toml.dumps(config)
print(updated_toml)
```

## Supported Types

| TOML Type | Scriptling Type |
|-----------|------------------|
| String | `str` |
| Integer | `int` |
| Float | `float` |
| Boolean | `bool` |
| Array | `list` |
| Table | `dict` |
| Inline Table | `dict` |
| Datetime | `str` (ISO format) |

## Python Compatibility

Compared to Python's `tomllib`/`tomli-w`:

- No `load()` / `dump()` for file I/O: only string input/output.
- `dumps()` is provided for writing TOML; Python's `tomllib` is read-only (the `tomli-w` package adds `dumps()` separately, which this follows the convention of).
- No `TOMLDecodeError` exception class: parse errors raise a generic Scriptling error.
- Datetime values are returned as ISO-formatted strings rather than datetime objects.

## See Also

- [json](../json/): parse and generate JSON data.
- [yaml](../yaml/): parse and generate YAML data.
- [scriptling.csv](../../utilities/csv/): parse and generate CSV data.
- [scriptling.xml](../../utilities/xml/): parse and generate XML data.
