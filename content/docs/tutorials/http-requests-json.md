---
title: HTTP Requests & JSON
description: Learn how to make HTTP requests and process JSON responses with Scriptling.
weight: 2
---

This tutorial covers using Scriptling's `requests` and `json` libraries for common HTTP patterns — GET, POST, PUT, DELETE, error handling, and best practices.

## Prerequisites

- Scriptling CLI installed ([Installation](../../quick-start/cli/))

## Making a GET Request

```python
import requests

response = requests.get("https://api.example.com/data")
print(response.status_code)  # 200
print(response.body)         # Response content as string
```

### With Options

```python
options = {
    "timeout": 10,
    "headers": {
        "Authorization": "Bearer token123",
        "Accept": "application/json"
    }
}
response = requests.get("https://api.example.com/data", options)
```

## Making a POST Request

```python
import json
import requests

payload = {"name": "Alice", "email": "alice@example.com"}
body = json.dumps(payload)

options = {
    "timeout": 10,
    "headers": {"Content-Type": "application/json"}
}
response = requests.post("https://api.example.com/users", body, options)
```

## PUT, PATCH & DELETE

```python
import json
import requests

# Update (PUT)
payload = {"name": "Alice Updated"}
body = json.dumps(payload)
response = requests.put("https://api.example.com/users/1", body)

# Partial update (PATCH)
payload = {"email": "newemail@example.com"}
body = json.dumps(payload)
response = requests.patch("https://api.example.com/users/1", body)

# Delete
response = requests.delete("https://api.example.com/users/1")
```

## Parsing JSON

```python
import json

# Parse a string to Scriptling objects
data = json.loads('{"name": "Alice", "age": 30}')
print(data["name"])  # Alice

# Nested structures
user = json.loads('{"user": {"name": "Alice", "tags": ["admin"]}}')
print(user["user"]["tags"][0])  # admin
```

## Generating JSON

```python
import json

obj = {"name": "Bob", "age": 25}
json_str = json.dumps(obj)  # '{"age":25,"name":"Bob"}'

# Pretty-printed output
items = [1, 2, 3]
print(json.dumps(items, indent="  "))
```

## Error Handling

```python
import requests
import json

try:
    response = requests.get("https://api.example.com/data", timeout=5)

    if response.status_code != 200:
        raise "HTTP error: " + str(response.status_code)

    data = json.loads(response.body)
    print("Success:", len(data))
except:
    print("Request failed")
    data = []
finally:
    print("Request complete")
```

## Complete REST CRUD Example

```python
import json
import requests

API_URL = "https://api.example.com/users"
options = {"timeout": 10, "headers": {"Authorization": "Bearer token"}}

# Create
new_user = {"name": "Bob", "email": "bob@example.com"}
body = json.dumps(new_user)
create_resp = requests.post(API_URL, body, options)
if create_resp.status_code == 201:
    user_id = json.loads(create_resp.body)["id"]

# Read
response = requests.get(API_URL + "/" + str(user_id), options)
user = json.loads(response.body) if response.status_code == 200 else None

# Update
user["email"] = "updated@example.com"
body = json.dumps(user)
update_resp = requests.put(API_URL + "/" + str(user_id), body, options)

# Delete
delete_resp = requests.delete(API_URL + "/" + str(user_id), options)
if delete_resp.status_code == 204:
    print("Deleted successfully")
```

## Best Practices

### Always Check Status Codes

```python
response = requests.get("https://api.example.com/data", options)
if response.status_code == 200:
    data = json.loads(response.body)
elif response.status_code == 404:
    print("Not found")
else:
    print("Error:", response.status_code)
```

### Always Set Timeouts

```python
# Good: Explicit timeout
options = {"timeout": 10}
response = requests.get("https://api.example.com/data", options)
```

### Always Parse JSON Responses

```python
response = requests.get("https://api.example.com/users", options)
if response.status_code == 200:
    users = json.loads(response.body)
    for user in users:
        print(user["name"])
```

## See Also

- [Requests Library](../../../reference/libraries/http-process/requests/) - Full HTTP client documentation
- [JSON Library](../../../reference/libraries/data-formats/json/) - JSON parsing reference
- [Error Handling](../../error-handling/) - Try/except patterns
