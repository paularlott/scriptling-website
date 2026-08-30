---
title: Database Libraries
linkTitle: Databases
description: SQLite, MySQL/MariaDB/PostgreSQL, Valkey/Redis and BadgerDB plugins, two API shapes, four backends.
tags: [libraries, databases]
weight: 11

aliases:
  - /reference/libraries/scriptling/databases/
---

## Overview

The database plugins cover the common backends with just two API shapes: a **relational** surface shared by SQLite and the SQL client (MySQL, MariaDB, PostgreSQL), and a **key/value** surface shared by Valkey/Redis and BadgerDB. Learn one, use all four.

| Library | Import | API | Backend |
|---------|--------|-----|---------|
| [SQLite](sqlite/) | `scriptling.sqlite` | relational | embedded, pure Go |
| [SQL](sql/) | `scriptling.sql` | relational | MySQL, MariaDB, PostgreSQL |
| [Valkey](valkey/) | `scriptling.valkey` | key/value | Valkey and Redis servers |
| [BadgerDB](badgerdb/) | `scriptling.badgerdb` | key/value | embedded BadgerDB |

```python
import scriptling.sqlite as sqlite
import scriptling.valkey as valkey

conn = sqlite.connect("app.db")
conn.execute("insert into people (name) values (?)", "ada")
rows = conn.query("select * from people where name = ?", "ada")
conn.close()

cache = valkey.connect("valkey://localhost:6379")
cache.set("greeting", "hello", ttl_seconds=60)
print(cache.get("greeting"))
cache.close()
```

## Availability

The plugins are available two ways, and scripts are identical in both:

- **Compiled in**: `scriptling-full` ships with all four; custom builds select any subset with build tags (`plugin_sqlite`, `plugin_sql`, `plugin_valkey`, `plugin_badgerdb`).
- **External plugins**: `sqlite`, `sql`, `valkey` and `badgerdb` binaries load from `--plugin` / `--plugin-dir` like any other plugin, keeping the core binary lean.

## Security

Each database operation honours the host's security policy, delivered in the plugin handshake: file-based plugins (`sqlite`, `badgerdb`) require paths inside `--allowed-paths`, and network plugins (`sql`, `valkey`) dial through the same guard as the `requests` library: host allow/deny lists, address-category blocks, and DNS-rebinding-safe validated-IP dialing. See the [Security Guide](/docs/security/).

## See Also

- [Database examples](https://github.com/paularlott/scriptling/tree/main/examples/databases): runnable scripts against real servers
- [Plugin Control Library](../plugin/): loading and calling plugins at runtime
