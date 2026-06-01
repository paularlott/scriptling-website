---
title: requests
weight: 1
---

Functions for making HTTP requests. Matches Python's `requests` library API.

## Available Functions

| Function                          | Description                                |
| --------------------------------- | ------------------------------------------ |
| `get(url, **kwargs)`              | Make a GET request to the specified URL    |
| `post(url, data=None, **kwargs)`  | Make a POST request to the specified URL   |
| `put(url, data=None, **kwargs)`   | Make a PUT request to the specified URL    |
| `delete(url, **kwargs)`           | Make a DELETE request to the specified URL |
| `patch(url, data=None, **kwargs)` | Make a PATCH request to the specified URL  |
| `parallel(requests, max_parallel=4)` | Execute multiple HTTP requests in parallel |

## Setup

```go
import "github.com/paularlott/scriptling/extlibs"

// Register the Requests library
p.RegisterLibrary("requests", extlibs.RequestsLibrary)
```

## Functions

### requests.get(url, \*\*kwargs)

Makes a GET request to the specified URL.

**Parameters:**

- `url`: URL to request
- `**kwargs`: Optional arguments
  - `timeout` (int): Request timeout in seconds (default: 5)
  - `headers` (dict): HTTP headers to send
  - `params` (dict): Query parameters to append to the URL
  - `auth` (tuple/list): Basic authentication as (username, password)

**Returns:** Response object

### requests.post(url, data=None, \*\*kwargs)

Makes a POST request to the specified URL.

**Parameters:**

- `url`: URL to request
- `data` (string, optional): Request body
- `**kwargs`: Optional arguments
  - `timeout` (int): Request timeout in seconds (default: 5)
  - `headers` (dict): HTTP headers to send
  - `params` (dict): Query parameters to append to the URL
  - `json` (dict/list): JSON-encode as request body and set Content-Type
  - `auth` (tuple/list): Basic authentication as (username, password)

**Returns:** Response object

### requests.put(url, data=None, \*\*kwargs)

Makes a PUT request to the specified URL.

**Parameters:**

- `url`: URL to request
- `data` (string, optional): Request body
- `**kwargs`: Optional arguments
  - `timeout` (int): Request timeout in seconds (default: 5)
  - `headers` (dict): HTTP headers to send
  - `params` (dict): Query parameters to append to the URL
  - `auth` (tuple/list): Basic authentication as (username, password)

**Returns:** Response object

### requests.delete(url, \*\*kwargs)

Makes a DELETE request to the specified URL.

**Parameters:**

- `url`: URL to request
- `**kwargs`: Optional arguments
  - `timeout` (int): Request timeout in seconds (default: 5)
  - `headers` (dict): HTTP headers to send
  - `params` (dict): Query parameters to append to the URL
  - `auth` (tuple/list): Basic authentication as (username, password)

**Returns:** Response object

### requests.patch(url, data=None, \*\*kwargs)

Makes a PATCH request to the specified URL.

**Parameters:**

- `url`: URL to request
- `data` (string, optional): Request body
- `**kwargs`: Optional arguments
  - `timeout` (int): Request timeout in seconds (default: 5)
  - `headers` (dict): HTTP headers to send
  - `params` (dict): Query parameters to append to the URL
  - `auth` (tuple/list): Basic authentication as (username, password)

**Returns:** Response object

### requests.parallel(requests, max_parallel=4)

Executes multiple HTTP requests concurrently with a configurable concurrency limit. Results are returned in the same order as the input requests regardless of completion order.

**Parameters:**

- `requests` (list): List of request specification dicts, each containing:
  - `method` (string): HTTP method — `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`, `"PATCH"` (default: `"GET"`)
  - `url` (string, required): The URL to request
  - `data` (string, optional): Request body as a string
  - `json` (dict/list, optional): Data to JSON-encode as request body (sets Content-Type)
  - `headers` (dict, optional): HTTP headers
  - `params` (dict, optional): Query parameters to append to the URL
  - `auth` (list/tuple, optional): Basic authentication as `[username, password]`
  - `timeout` (int, optional): Request timeout in seconds (default: 30)
- `max_parallel` (int): Maximum number of concurrent requests (default: 4)

**Returns:** List of Response objects in the same order as the input list. Failed requests return a Response with `status_code=0` and the error message in `body`.

**Example:**

```python
import requests

results = requests.parallel([
    {"method": "GET", "url": "https://api.example.com/items/1"},
    {"method": "GET", "url": "https://api.example.com/items/2"},
    {"method": "POST", "url": "https://api.example.com/items", "json": {"name": "new"}},
], max_parallel=4)

for resp in results:
    if resp.status_code == 200:
        data = resp.json()
        print(data)
```

## Response Object

All HTTP functions return a response object with these attributes:

- `status_code` or `["status_code"]`: HTTP status code (integer)
- `text` or `["text"]`: Response body (string)
- `body` or `["body"]`: Response body (string, alias for text)
- `headers` or `["headers"]`: Response headers (dictionary)
- `url` or `["url"]`: The URL of the response

## Response Methods

- `json()`: Parse response body as JSON
- `raise_for_status()`: Raise exception if status code >= 400

## Exceptions

The requests library provides the following exception types for error handling:

- `RequestException`: Base exception for all request errors
- `HTTPError`: Exception for HTTP error responses (4xx, 5xx)

**Example:**

```python
import requests

try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()
except requests.HTTPError as e:
    print("HTTP error:", e)
except requests.RequestException as e:
    print("Request failed:", e)
```

## Examples

### Basic GET Request

```python
import requests

response = requests.get("https://api.example.com/users/1")
if response.status_code == 200:
    print("User data:", response.text)
```

### GET with Options

```python
import requests

# Using kwargs
response = requests.get("https://api.example.com/users/1", timeout=10, headers={"Authorization": "Bearer token123"})

# Using legacy options dict
options = {
    "timeout": 10,
    "headers": {"Authorization": "Bearer token123"}
}
response = requests.get("https://api.example.com/users/1", options)
```

### POST Request

```python
import requests
import json

new_user = {"name": "Alice", "email": "alice@example.com"}
body = json.dumps(new_user)

# Using kwargs
response = requests.post("https://api.example.com/users", data=body, headers={"Content-Type": "application/json"})

if response.status_code == 201:
    created = response.json()
    print("Created user:", created["id"])
```

### Error Handling

```python
import requests

try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()  # Raises error if 4xx or 5xx
    data = response.json()
    print("Success:", data)
except Exception as e:
    print("Request failed:", e)
```

### Using Response Attributes

```python
import requests

response = requests.get("https://api.example.com/data")

# Both syntaxes work
status = response.status_code
# or
status = response["status_code"]

content = response.text
headers = response.headers
```

## Complete Example

```python
import requests
import json

# GET request with error handling
try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    response.raise_for_status()

    post = response.json()
    print("Post title:", post["title"])
    print("Status code:", response.status_code)

except Exception as e:
    print("Error:", e)

# POST request
try:
    new_post = {
        "title": "My Post",
        "body": "This is my post content",
        "userId": 1
    }

    body = json.dumps(new_post)

    response = requests.post(
        url="https://jsonplaceholder.typicode.com/posts",
        data=body,
        timeout=15,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()

    created = response.json()
    print("Created post ID:", created["id"])

except Exception as e:
    print("Error:", e)
```

## Notes

- HTTP/2 support with automatic fallback to HTTP/1.1
- Connection pooling (100 connections per host)
- Accepts self-signed certificates
- Default timeout: 5 seconds
- Python requests-compatible API
