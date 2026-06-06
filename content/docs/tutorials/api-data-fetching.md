---
title: Fetching and Processing API Data
description: Write a CLI script that fetches data from a public API and processes the results.
weight: 1
---

This tutorial walks through building a CLI script that fetches user data from a public API, processes it with JSON, and outputs a formatted report.

## Prerequisites

- Scriptling CLI installed ([Installation](../../quick-start/cli/))

## Step 1: Fetch Data from an API

Create a file called `fetch_users.py`:

```python
import requests
import json

# Fetch users from a public API
response = requests.get("https://jsonplaceholder.typicode.com/users")

if response.status_code != 200:
    print("Failed to fetch data:", response.status_code)
else:
    users = json.loads(response.body)
    print(f"Found {len(users)} users")
```

Run it:

```bash
scriptling fetch_users.py
```

Output:

```
Found 10 users
```

## Step 2: Extract and Format Data

Extract relevant fields from each user and format the output:

```python
import requests
import json

response = requests.get("https://jsonplaceholder.typicode.com/users")
users = json.loads(response.body)

for user in users:
    name = user["name"]
    email = user["email"]
    city = user["address"]["city"]
    company = user["company"]["name"]

    print(f"{name}")
    print(f"  Email:   {email}")
    print(f"  City:    {city}")
    print(f"  Company: {company}")
    print()
```

## Step 3: Add Filtering

Filter users by company name:

```python
import requests
import json

def fetch_users():
    """Fetch users from the API."""
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    if response.status_code != 200:
        print("Error:", response.status_code)
        return []
    return json.loads(response.body)

def filter_by_domain(users, domain):
    """Filter users by email domain."""
    result = []
    for user in users:
        if domain in user["email"]:
            result.append(user)
    return result

def print_report(users, title):
    """Print a formatted user report."""
    print(f"\n{'=' * 40}")
    print(f"  {title}")
    print(f"  {len(users)} user(s)")
    print(f"{'=' * 40}\n")

    for user in users:
        print(f"  {user['name']} <{user['email']}>")
        print(f"    {user['company']['name']} — {user['address']['city']}")
        print()

# Main
users = fetch_users()

# Filter and report
matched = filter_by_domain(users, ".biz")
if matched:
    print_report(matched, "Users with .biz domain")
else:
    print("No users found with .biz domain")

# Full report
print_report(users, "All Users")
```

## Step 4: Add Error Handling

Wrap the API call in error handling to manage network issues:

```python
import requests
import json

def fetch_users():
    """Fetch users from the API with error handling."""
    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/users",
            timeout=10
        )
        response.raise_for_status()
        return json.loads(response.body)
    except Exception as e:
        print(f"API request failed: {e}")
        return []

def summarize(users):
    """Generate a summary of user locations."""
    cities = {}
    for user in users:
        city = user["address"]["city"]
        if city in cities:
            cities[city] += 1
        else:
            cities[city] = 1
    return cities

# Main
users = fetch_users()
if users:
    cities = summarize(users)
    print(f"Total users: {len(users)}")
    print(f"Cities represented: {len(cities)}")
    print()
    for city, count in cities.items():
        print(f"  {city}: {count}")
```

## Step 5: Save Results to a File

Export the processed data as JSON:

```python
import requests
import json

def fetch_users():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        response.raise_for_status()
        return json.loads(response.body)
    except Exception as e:
        print(f"Error: {e}")
        return []

# Fetch and process
users = fetch_users()

# Transform data
summary = []
for user in users:
    summary.append({
        "name": user["name"],
        "email": user["email"],
        "city": user["address"]["city"],
        "company": user["company"]["name"]
    })

# Save to file
output = json.dumps(summary, indent="  ")
print(output)

# Write to file (requires os library registration when embedding)
with open("users_export.json", "w") as f:
    f.write(output)

print(f"\nExported {len(summary)} users to users_export.json")
```

> **Note:** File system access (`open()`) works in the CLI. When embedding in Go, the `os` library requires explicit registration. See [Library Registration](../../go-integration/library-registration/).

## Complete Script

Here's the complete script with all steps combined:

```python
import requests
import json

API_URL = "https://jsonplaceholder.typicode.com/users"

def fetch_users():
    """Fetch users from the API."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return json.loads(response.body)
    except Exception as e:
        print(f"API request failed: {e}")
        return []

def build_report(users):
    """Build a summary report from user data."""
    report = {
        "total": len(users),
        "by_city": {},
        "by_company": [],
    }

    for user in users:
        city = user["address"]["city"]
        company = user["company"]["name"]

        if city in report["by_city"]:
            report["by_city"][city] += 1
        else:
            report["by_city"][city] = 1

        report["by_company"].append({
            "name": user["name"],
            "company": company,
            "city": city,
        })

    return report

def display_report(report):
    """Display the formatted report."""
    print(f"\nTotal Users: {report['total']}")
    print(f"Cities: {len(report['by_city'])}")
    print("\nUsers by City:")
    for city, count in report["by_city"].items():
        print(f"  {city}: {count}")

# Main
users = fetch_users()
if users:
    report = build_report(users)
    display_report(report)
```

## What You Learned

- Using `requests` to fetch data from HTTP APIs
- Parsing JSON with `json.loads()` and formatting with `json.dumps()`
- Working with lists, dictionaries, and loops
- Defining and calling functions
- Error handling with try/except
- File I/O with `open()` and `with` statements

## See Also

- [Requests Library](../../libraries/http-process/requests/) - Full HTTP client documentation
- [JSON Library](../../libraries/data-formats/json/) - JSON parsing reference
- [Language Guide](../../language/) - Complete syntax reference
- [CLI Reference](../../cli/) - Command-line options
