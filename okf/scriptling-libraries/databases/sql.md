---
description: MySQL, MariaDB and PostgreSQL client with one connect() per DSN scheme and one shared API.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/databases/sql/
sources:
    - resource: https://scriptling.dev/reference/libraries/databases/sql/
status: stable
tags:
    - libraries
    - databases
    - sql
    - mysql
    - mariadb
    - postgresql
title: scriptling.sql
type: API Reference
---
# scriptling.sql

## Overview

`scriptling.sql` connects Scriptling to MySQL, MariaDB and PostgreSQL. The DSN scheme picks the driver: `postgres://` (or `postgresql://`), `mysql://`, or `mariadb://`. MySQL and MariaDB share the MySQL wire protocol, so those schemes are interchangeable. Its core connection API is shared with [scriptling.sqlite](https://scriptling.dev/okf/scriptling-libraries/databases/sqlite.md); backend-specific DDL is the main portability qualification.

```python
import scriptling.sql as sql

conn = sql.connect("postgres://user:pass@localhost:5432/app")
conn.execute("create table people (id serial primary key, name text)")
conn.execute("insert into people (name) values (?)", "ada")      # ? works everywhere
rows = conn.query("select name from people where name = ?", "ada")
conn.close()
```

## Available Functions

| Function | Description |
|----------|-------------|
| `connect(dsn)` | Connect to a server and return a `Connection` |

## Functions

### `connect(dsn)`

Connects to a database server and returns a [`Connection`](#connection).

- `postgres://user:pass@host:5432/db`: PostgreSQL (`?` placeholders are translated to `$n`; explicit `$n` also works)
- `mysql://user:pass@host:3306/db`: MySQL
- `mariadb://user:pass@host:3306/db`: MariaDB

Query parameters in the URL pass through as driver options (for example, `?charset=utf8mb4`). The server address must pass the database plugin's host network policy.

## Connection

Rows are dicts keyed by column name; values are ints, floats, bools, strings or `None`. `?` placeholders work on every backend and are translated to `$n` on PostgreSQL.

| Method | Description |
|--------|-------------|
| `query(sql, *params)` | Run a SELECT-style statement, returning a list of row dicts |
| `query_iter(sql, *params)` | Stream a statement as a `Cursor` in compiled-in and external SQL deployments |
| `execute(sql, *params)` | Run a row-changing statement, returning `{"last_insert_id": int, "rows_affected": int}` |
| `get_orm()` | Return the [ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md) bound to this connection |
| `close()` | Close the connection |

PostgreSQL has no last-insert-id: `last_insert_id` is 0 there. Use `insert ... returning id` with `query()` instead:

```python
rows = conn.query("insert into people (name) values (?) returning id", "ada")
print(rows[0]["id"])
```

## Transactions

The script-facing API is autocommit: each `query()`, `execute()`, or ORM terminal call runs independently. It exposes no transaction handle and no `begin()`, `commit()`, or `rollback()` methods, so multiple calls cannot be grouped into one atomic transaction through this API.

## Streaming Large Results

`query()` materialises the entire result set in memory. `query_iter()` streams rows one at a time in compiled-in and external SQL deployments:

```python
cur = conn.query_iter("select * from events where ts > ?", since)
row = cur.next()          # a dict, or None at the end
cur.close()               # release early; safe once exhausted too

for row in orm.select("events").where("ts", ">=", since).iterate():
    handle(row)
```

Compiled-in SQL reads lazily from the driver. External SQL keeps the result cursor in its plugin process and fetches each row through the plugin boundary, so host-side result memory remains constant.

## ORM

The same [ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md) is used across relational backends. `conn.get_orm()` returns a table helper with dialect-aware SQL generation: backticks on MySQL/MariaDB, `"` and `$n` on PostgreSQL, and placeholder renumbering where required. `iterate()` works in both compiled-in and external SQL deployments.

## See Also

- [scriptling.sqlite](https://scriptling.dev/okf/scriptling-libraries/databases/sqlite.md): the same core API, embedded
- [Relational ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md): portable query and model helpers
- [Database Libraries](https://scriptling.dev/okf/scriptling-libraries/databases/sql.md): deployment and backend selection
