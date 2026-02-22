---
title: Standard Libraries
description: Built-in libraries available for import in Scriptling.
weight: 1
---

Built-in libraries available for import without any registration.

## Available Libraries

| Library | Description |
|---------|-------------|
| [json](json/) | Parse and generate JSON data |
| [io](io/) | In-memory I/O streams (StringIO) |
| [base64](base64/) | Base64 encoding and decoding |
| [html](html/) | HTML escaping and unescaping |
| [math](math/) | Mathematical functions and constants |
| [random](random/) | Random number generation |
| [statistics](statistics/) | Statistical functions |
| [time](time/) | Time access and conversions |
| [datetime](datetime/) | Date and time formatting |
| [re](regex/) | Regular expression operations |
| [string](string/) | String constants |
| [textwrap](textwrap/) | Text wrapping and filling |
| [functools](functools/) | Higher-order functions |
| [itertools](itertools/) | Iterator functions |
| [collections](collections/) | Specialized container datatypes |
| [hashlib](hashlib/) | Secure hash algorithms |
| [platform](platform/) | Platform identifying data |
| [urllib](urllib/) | URL handling |
| [uuid](uuid/) | UUID generation |

## Usage

```python
import json
import math

data = json.loads('{"a": 1, "b": 2}')
result = math.sqrt(data["a"] + data["b"])
```
