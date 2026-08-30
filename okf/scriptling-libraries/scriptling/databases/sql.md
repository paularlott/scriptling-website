---
description: MySQL, MariaDB and PostgreSQL client with one connect() per DSN scheme and one shared API.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/scriptling/databases/sql/
sources:
    - resource: https://scriptling.dev/reference/libraries/scriptling/databases/sql/
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

`scriptling.sql` connects Scriptling to MySQL, MariaDB and PostgreSQL. The DSN scheme picks the driver: `postgres://` (or `postgresql://`), `mysql://`, `mariadb://` (MySQL and MariaDB share the MySQL wire protocol, so the schemes are interchangeable). The API is shared with [scriptling.sqlite](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/sqlite.md), so a script can move from a local file to a network server unchanged.

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

Query parameters in the URL pass through as driver options (e.g. `?charset=utf8mb4`).

The server address must pass the host's network policy: connections dial through the same guard as the `requests` library.

## Connection

Rows are dicts keyed by column name; values are ints, floats, bools, strings or `None`. `?` placeholders work on every backend (translated to `$n` on PostgreSQL).

| Method | Description |
|--------|-------------|
| `query(sql, *params)` | Run a SELECT-style statement, returning a list of row dicts |
| `query_iter(sql, *params)` | Same statement, streamed: a `Cursor` whose `next()` yields one row dict at a time (`None` at the end) instead of materialising the whole result |
| `execute(sql, *params)` | Run a row-changing statement, returning `{"last_insert_id": int, "rows_affected": int}` |
| `get_orm()` | Return the [ORM](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/orm.md) bound to this connection |
| `close()` | Close the connection |

PostgreSQL has no last-insert-id: `last_insert_id` is 0 there; use `insert ... returning id` with `query()` instead:

```python
rows = conn.query("insert into people (name) values (?) returning id", "ada")
print(rows[0]["id"])
```

## Streaming Large Results

`query()` materialises the entire result set in memory. For big exports or
scans, `query_iter()` streams row by row from the driver, and the ORM's
`iterate()` is the same streaming under the query builder:

```python
cur = conn.query_iter("select * from events where ts > ?", since)
row = cur.next()          # a dict, or None at the end
cur.close()               # release early; safe once exhausted too

for row in orm.select("events").where("ts", ">=", since).iterate():
    handle(row)           # one row in memory at a time
```

See the [Relational ORM](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/orm.md) page for `iterate()` and the rest of the
builder.

## ORM

The same [ORM](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/orm.md) as sqlite: `conn.get_orm()` returns a table helper with dialect-aware SQL generation: backticks on MySQL/MariaDB, `"` and `$n` on PostgreSQL, and `?` placeholders in where clauses renumbered automatically, so one script targets all three servers.

## See Also

- [scriptling.sqlite](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/sqlite.md): the same API, embedded
- [Database Libraries](https://scriptling.dev/okf/scriptling-libraries/scriptling/databases/sql.md): all four backends, two API shapes
