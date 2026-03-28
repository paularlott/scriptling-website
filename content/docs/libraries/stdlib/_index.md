---
title: Standard Libraries
description: Built-in libraries available for import in Scriptling.
weight: 1
---

Built-in libraries available for import without any registration.

| Library | Description |
|---------|-------------|
| [base64](base64/) | Base64 encoding and decoding |
| [collections](collections/) | Specialized container datatypes |
| [contextlib](contextlib/) | Utilities for the `with` statement (`suppress`) |
| [datetime](datetime/) | Date and time formatting |
| [difflib](difflib/) | Sequence comparison and diff generation |
| [functools](functools/) | Higher-order functions and decorators |
| [hashlib](hashlib/) | Secure hash algorithms |
| [html](html/) | HTML escaping and unescaping |
| [io](io/) | In-memory I/O streams (StringIO) |
| [itertools](itertools/) | Iterator functions |
| [json](json/) | Parse and generate JSON data |
| [math](math/) | Mathematical functions and constants |
| [platform](platform/) | Platform identifying data |
| [random](random/) | Random number generation |
| [re](regex/) | Regular expression operations |
| [statistics](statistics/) | Statistical functions |
| [string](string/) | String constants |
| [textwrap](textwrap/) | Text wrapping and filling |
| [time](time/) | Time access and conversions |
| [urllib](urllib/) | URL handling |
| [uuid](uuid/) | UUID generation |

## Usage

```python
import json
import math

data = json.loads('{"a": 1, "b": 2}')
result = math.sqrt(data["a"] + data["b"])
```
