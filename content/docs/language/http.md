---
title: HTTP & JSON
description: HTTP requests, response objects, and JSON handling in Scriptling.
weight: 10
---

Scriptling provides built-in support for HTTP requests and JSON processing through the `requests` and `json` libraries.

## Importing Libraries

```python
import json
import requests
```

## HTTP Response Object

All HTTP functions return a Response object with these attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `status_code` | int | HTTP status code (200, 404, etc.) |
| `body` | string | Response body as text |
| `text` | string | Response body as text (same as `body`) |
| `headers` | dict | Response headers |
| `url` | string | The URL that was requested |

```python
response = requests.get("https://api.example.com/data")
print(response.status_code)  # 200
print(response.body)         # Response content
print(response.headers)      # {"content-type": "application/json", ...}
```

## GET Request

```python
# Basic GET (default 5 second timeout)
response = requests.get("https://api.example.com/users")
status = response.status_code  # 200
body = response.body           # Response body string

# GET with options
options = {"timeout": 10}
response = requests.get("https://api.example.com/users", options)

# GET with headers
options = {
    "timeout": 10,
    "headers": {
        "Authorization": "Bearer token123",
        "Accept": "application/json"
    }
}
response = requests.get("https://api.example.com/users", options)
```

## POST Request

```python
# POST with JSON body (default 5 second timeout)
import json

payload = {"name": "Alice", "email": "alice@example.com"}
body = json.dumps(payload)
response = requests.post("https://api.example.com/users", body)

# POST with options
options = {"timeout": 15}
response = requests.post("https://api.example.com/users", body, options)

# POST with headers
options = {
    "timeout": 10,
    "headers": {
        "Authorization": "Bearer token123",
        "Content-Type": "application/json"
    }
}
response = requests.post("https://api.example.com/users", body, options)

# Check status
if response.status_code == 201:
    print("Created successfully")
```

## PUT Request

```python
# Update resource (default 5 second timeout)
payload = {"name": "Alice Updated"}
body = json.dumps(payload)
response = requests.put("https://api.example.com/users/1", body)

# With options
options = {"timeout": 10}
response = requests.put("https://api.example.com/users/1", body, options)
```

## DELETE Request

```python
# Delete resource (default 5 second timeout)
response = requests.delete("https://api.example.com/users/1")

# With options
options = {"timeout": 10}
response = requests.delete("https://api.example.com/users/1", options)
```

## PATCH Request

```python
# Partial update (default 5 second timeout)
payload = {"email": "newemail@example.com"}
body = json.dumps(payload)
response = requests.patch("https://api.example.com/users/1", body)

# With options
options = {"timeout": 10}
response = requests.patch("https://api.example.com/users/1", body, options)
```

## Request Options

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `timeout` | int | Request timeout in seconds | 5 |
| `headers` | dict | HTTP headers to send | {} |

```python
options = {
    "timeout": 30,
    "headers": {
        "Authorization": "Bearer token",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "MyApp/1.0"
    }
}
response = requests.get("https://api.example.com/data", options)
```

## Timeout Behavior

- **Default timeout**: 5 seconds
- **On timeout**: Returns an error
- **Specify timeout**: Integer (seconds) in options dictionary

```python
# Short timeout for fast APIs
options = {"timeout": 2}
response = requests.get("https://fast-api.example.com/data", options)

# Long timeout for slow APIs
options = {"timeout": 60}
response = requests.get("https://slow-api.example.com/data", options)
```

## JSON Processing

### Parsing JSON

```python
import json

# Parse JSON string to Scriptling objects
data = json.loads('{"name": "Alice", "age": 30}')
name = data["name"]  # "Alice"
age = data["age"]    # 30

# Parse array
items = json.loads('[1, 2, 3, 4, 5]')
first = items[0]  # 1

# Parse nested structure
data = json.loads('{"user": {"name": "Alice", "tags": ["admin", "user"]}}')
user_name = data["user"]["name"]      # "Alice"
first_tag = data["user"]["tags"][0]   # "admin"
```

### Generating JSON

```python
import json

# Convert Scriptling objects to JSON string
obj = {"name": "Bob", "age": 25}
json_str = json.dumps(obj)  # '{"age":25,"name":"Bob"}'

# Convert list
items = [1, 2, 3, 4, 5]
json_str = json.dumps(items)  # '[1,2,3,4,5]'

# Nested structure
data = {
    "user": {
        "name": "Alice",
        "tags": ["admin", "user"]
    }
}
json_str = json.dumps(data)
```

## Complete REST API Example

```python
import json
import requests

# Configure options
options = {"timeout": 10, "headers": {"Authorization": "Bearer token123"}}

# Fetch user
response = requests.get("https://api.example.com/users/1", options)

if response.status_code == 200:
    user = json.loads(response.body)
    print("User: " + user["name"])

    # Update user
    user["email"] = "updated@example.com"
    body = json.dumps(user)
    update_resp = requests.put("https://api.example.com/users/1", body, options)

    if update_resp.status_code == 200:
        print("Updated successfully")
    else:
        print("Update failed: " + str(update_resp.status_code))
else:
    print("Failed to fetch user")

# Create new user
new_user = {"name": "Bob", "email": "bob@example.com"}
body = json.dumps(new_user)
create_resp = requests.post("https://api.example.com/users", body, options)

if create_resp.status_code == 201:
    created = json.loads(create_resp.body)
    user_id = created["id"]
    print("Created user with ID: " + str(user_id))

    # Delete user
    delete_resp = requests.delete("https://api.example.com/users/" + str(user_id), options)
    if delete_resp.status_code == 204:
        print("Deleted successfully")
```

## Error Handling

```python
import json
import requests

try:
    options = {"timeout": 5}
    response = requests.get("https://api.example.com/data", options)

    if response.status_code != 200:
        raise "HTTP error: " + str(response.status_code)

    data = json.loads(response.body)
    print("Success: " + str(len(data)))
except:
    print("Request failed")
    data = []
finally:
    print("Request complete")
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
    print("Error: " + str(response.status_code))
```

### Always Set Timeouts

```python
# Good: Explicit timeout
options = {"timeout": 10}
response = requests.get("https://api.example.com/data", options)

# Bad: Using default (may be too short or too long)
response = requests.get("https://api.example.com/data")
```

### Always Parse JSON Responses

```python
response = requests.get("https://api.example.com/users", options)
if response.status_code == 200:
    users = json.loads(response.body)  # Don't use raw body
    for user in users:
        print(user["name"])
```

### Always Stringify Before Sending

```python
payload = {"name": "Alice"}
body = json.dumps(payload)  # Convert to JSON string first
response = requests.post("https://api.example.com/users", body, options)
```

## See Also

- [Error Handling](./error-handling/) - Try/except patterns
- [Requests Library](../libraries/extlib/requests/) - Full requests documentation
- [JSON Library](../libraries/stdlib/json/) - Full JSON documentation
