---
title: scriptling.sql
linkTitle: sql
description: MySQL, MariaDB and PostgreSQL client with one connect() per DSN scheme and one shared API.
tags: [libraries, databases, sql, mysql, mariadb, postgresql]
weight: 3

aliases:
  - /reference/libraries/scriptling/databases/sql/
---

## Overview

`scriptling.sql` connects Scriptling to MySQL, MariaDB and PostgreSQL. The DSN scheme picks the driver: `postgres://` (or `postgresql://`), `mysql://`, or `mariadb://`. MySQL and MariaDB share the MySQL wire protocol, so those schemes are interchangeable. Its core connection API is shared with [scriptling.sqlite](../sqlite/); backend-specific DDL is the main portability qualification.

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
| `begin()` | Start a [`Transaction`](#transactions) |
| `get_orm()` | Return the [ORM](../orm/) bound to this connection |
| `close()` | Close the connection |

PostgreSQL has no last-insert-id: `last_insert_id` is 0 there. Use `insert ... returning id` with `query()` instead:

```python
rows = conn.query("insert into people (name) values (?) returning id", "ada")
print(rows[0]["id"])
```

## Transactions

`conn.begin()` starts a transaction and returns a `Transaction` handle. Statements run through the handle — its `query()`, `query_iter()` and `execute()` — form one atomic unit: `commit()` makes them permanent, `rollback()` discards them. The handle's statement surface matches the connection's, `?` placeholders included.

```python
tx = conn.begin()
tx.execute("update accounts set balance = balance - 25 where name = ?", "ada")
tx.execute("update accounts set balance = balance + 25 where name = ?", "grace")
tx.commit()          # or tx.rollback() to undo both

tx = conn.begin()
tx.execute("insert into people (name) values (?)", "temporary")
tx.rollback()        # the row is gone
```

| Method | Description |
|--------|-------------|
| `query(sql, *params)` | Run a SELECT-style statement inside the transaction |
| `query_iter(sql, *params)` | Same statement, streamed as a `Cursor`; drain or close it before commit or rollback |
| `execute(sql, *params)` | Run a row-changing statement inside the transaction |
| `commit()` | Make the transaction's changes permanent and end it |
| `rollback()` | Discard the transaction's changes and end it |
| `get_orm()` | Return the [ORM](../orm/) bound to this transaction, so its calls join it |

Every operation on a finished transaction fails with `transaction is already committed or rolled back`, whichever way it ended. A transaction abandoned without either call is rolled back automatically once the runtime collects it, so an error path that simply returns leaves no half-applied work behind — end transactions explicitly (`try`/`except` with `rollback()` in the handler) rather than relying on collection timing. On pooled server backends an abandoned transaction holds one pooled connection until then; the connection's other calls are unaffected.

Outside a transaction the API is autocommit: each connection-level `query()`, `execute()` or ORM terminal call runs independently. Connection-level calls while a transaction is open run on separate pooled connections and do not see its uncommitted changes until commit.

```python
tx = conn.begin()
tx.execute("insert into people (name) values (?)", "pending")
len(conn.query("select 1 from people where name = 'pending'"))   # 0 — not committed
tx.commit()
len(conn.query("select 1 from people where name = 'pending'"))   # 1
```

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

The same [ORM](../orm/) is used across relational backends. `conn.get_orm()` returns a table helper with dialect-aware SQL generation: backticks on MySQL/MariaDB, `"` and `$n` on PostgreSQL, and placeholder renumbering where required. `iterate()` works in both compiled-in and external SQL deployments.

## See Also

- [scriptling.sqlite](../sqlite/): the same core API, embedded
- [Relational ORM](../orm/): portable query and model helpers
- [Database Libraries](./): deployment and backend selection
