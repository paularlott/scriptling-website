---
title: yaml
description: Parse and generate YAML (YAML Ain't Markup Language) data.
weight: 1

aliases:
  - /reference/libraries/extlib/yaml/
  - /reference/libraries/yaml/
---

The `yaml` library parses YAML strings into Scriptling objects and serializes Scriptling objects back to YAML strings. Commonly used for configuration files, infrastructure-as-code manifests, and CI/CD pipelines.

## Available Functions

| Function | Description |
|----------|-------------|
| `safe_load(yaml_string)` | Parse a YAML string into a Scriptling object. |
| `load(yaml_string)` | Alias for `safe_load()`. |
| `safe_dump(obj)` | Convert a Scriptling object to a YAML string. |
| `dump(obj)` | Alias for `safe_dump()`. |

## Functions

### `safe_load(yaml_string)`

Parses a YAML string and returns the corresponding Scriptling object.

**Parameters:**
- `yaml_string` (`str`): YAML-formatted string to parse.

**Returns:** `dict`, `list`, `str`, `int`, `float`, `bool`, or `None`: depending on the parsed YAML value.

**Raises:** `Error`: if `yaml_string` is not valid YAML.

```python
import yaml

data = yaml.safe_load("""
name: John Doe
age: 30
active: true
tags:
  - python
  - yaml
""")

print(data["name"])  # John Doe
print(data["age"])   # 30
print(data["tags"])  # ["python", "yaml"]
```

### `load(yaml_string)`

Alias for `safe_load()`. In PyYAML, `load()` is deprecated in favor of `safe_load()` because it can execute arbitrary Python objects; in Scriptling both functions are identical and safe, since there is no equivalent unsafe loader.

**Parameters:**
- `yaml_string` (`str`): YAML-formatted string to parse.

**Returns:** `dict`, `list`, `str`, `int`, `float`, `bool`, or `None`

```python
import yaml

data = yaml.load("name: John\nage: 30")
print(data["name"])
```

### `safe_dump(obj)`

Converts a Scriptling object to a YAML-formatted string.

**Parameters:**
- `obj` (`dict`, `list`, `str`, `int`, `float`, `bool`, or `None`): Value to serialize.

**Returns:** `str`: the YAML-formatted output.

```python
import yaml

data = {
    "name": "Jane Smith",
    "age": 25,
    "skills": ["Go", "Python", "JavaScript"],
    "active": True
}

yaml_str = yaml.safe_dump(data)
print(yaml_str)
# active: true
# age: 25
# name: Jane Smith
# skills:
# - Go
# - Python
# - JavaScript
```

### `dump(obj)`

Alias for `safe_dump()`. Both functions are identical in Scriptling.

**Parameters:**
- `obj` (`dict`, `list`, `str`, `int`, `float`, `bool`, or `None`): Value to serialize.

**Returns:** `str`: the YAML-formatted output.

```python
import yaml

yaml_str = yaml.dump({"name": "John", "age": 30})
```

## Complete Example

```python
import yaml

config_yaml = """
database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secret

features:
  - authentication
  - logging
  - caching

debug: false
"""

config = yaml.safe_load(config_yaml)

print("Database host:", config["database"]["host"])
print("Features:", config["features"])

config["debug"] = True
config["features"].append("monitoring")

updated_yaml = yaml.safe_dump(config)
print(updated_yaml)
```

## Supported Types

| YAML Type | Scriptling Type |
|-----------|------------------|
| String | `str` |
| Integer | `int` |
| Float | `float` |
| Boolean | `bool` |
| Null | `None` |
| Sequence | `list` |
| Mapping | `dict` |

## Python Compatibility

- No `load_all()` / `dump_all()` for multiple documents.
- No file I/O: only string input/output.
- No custom constructors or representers.
- No `Loader` / `Dumper` class parameters.
- No YAML tags or anchors support.
- `load()` and `safe_load()` are identical (both safe), unlike PyYAML where `load()` without a `Loader` is deprecated and unsafe by default.

## See Also

- [json](../json/): parse and generate JSON data.
- [toml](../toml/): parse and generate TOML configuration data.
- [scriptling.csv](../../scriptling/utilities/csv/): parse and generate CSV data.
- [scriptling.xml](../../scriptling/utilities/xml/): parse and generate XML data.
