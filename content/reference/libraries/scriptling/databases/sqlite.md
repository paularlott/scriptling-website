---
title: scriptling.sqlite
linkTitle: sqlite
description: SQLite embedded relational database, connect, query, execute, close.
tags: [libraries, databases, sqlite]
weight: 2
---

## Overview

`scriptling.sqlite` provides the SQLite database as a pure-Go embedded engine: no server, no cgo, so it works on every platform Scriptling builds for. It shares its API with [plugin.sql](../sql/), so scripts port between SQLite and the network databases unchanged.

```python
import scriptling.sqlite as sqlite

conn = sqlite.connect("app.db")
conn.execute("create table people (id integer primary key autoincrement, name text)")
result = conn.execute("insert into people (name) values (?)", "ada")
print(result.last_insert_id)                 # 1
rows = conn.query("select * from people where name = ?", "ada")
print(rows[0]["name"])                       # ada
conn.close()
```

## Available Functions

| Function | Description |
|----------|-------------|
| `connect(path=":memory:", timeout_ms=5000)` | Open a database file (or a private in-memory database) and return a `Connection` |

## Functions

### `connect(path=":memory:", timeout_ms=5000)`

Opens a SQLite database and returns a [`Connection`](#connection).

- `path`: the database file. `":memory:"` (the default) opens a private in-memory database, which needs no file and is always allowed by the security policy.
- `timeout_ms`: how long a writer waits for a lock held by another connection before failing (`busy_timeout`).

The path must fall inside the host's `--allowed-paths` when one is configured.

## Connection

Rows are dicts keyed by column name; values are ints, floats, bools, strings or `None`. Both `?` placeholders and `?NNN`/`$name` forms are passed to SQLite as-is.

| Method | Description |
|--------|-------------|
| `query(sql, *params)` | Run a SELECT-style statement, returning a list of row dicts |
| `query_iter(sql, *params)` | Same statement, streamed: a `Cursor` whose `next()` yields one row dict at a time (`None` at the end) instead of materialising the whole result |
| `execute(sql, *params)` | Run a row-changing statement (INSERT/UPDATE/DELETE/DDL), returning `{"last_insert_id": int, "rows_affected": int}` |
| `close()` | Close the connection and release the database handle |

The class can also be constructed directly: `sqlite.Connection(path, timeout_ms=5000)`.

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

See the [Relational ORM](../orm/) page for `iterate()` and the rest of the
builder.

## ORM

`conn.get_orm()` returns a lightweight table helper bound to the connection: `insert`/`select`/`update`/`delete`/`count`/`tables()` over dict-shaped rows, with SQL generation following the backend. See the [Relational ORM](../orm/) page for the full reference.

## See Also

- [SQL](../sql/): the same API over MySQL, MariaDB and PostgreSQL
- [Database Libraries](./): all four backends, two API shapes
