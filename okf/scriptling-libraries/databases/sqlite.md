---
description: SQLite embedded relational database, connect, query, execute, close.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/databases/sqlite/
sources:
    - resource: https://scriptling.dev/reference/libraries/databases/sqlite/
status: stable
tags:
    - libraries
    - databases
    - sqlite
title: scriptling.sqlite
type: API Reference
---
# scriptling.sqlite

## Overview

`scriptling.sqlite` provides the SQLite database as a pure-Go embedded engine: no server, no cgo, so it works on every platform Scriptling builds for. It shares the core connection shape and documented ORM subset with [scriptling.sql](https://scriptling.dev/okf/scriptling-libraries/databases/sql.md), but DSNs, raw SQL and DDL, types, collations, and backend-specific features still differ.

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
| `begin()` | Start a [`Transaction`](#transactions) |
| `get_orm()` | Return the [ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md) bound to this connection |
| `close()` | Close the connection and release the database handle |

The class can also be constructed directly: `sqlite.Connection(path, timeout_ms=5000)`.

## Transactions

`conn.begin()` starts a transaction and returns a `Transaction` handle. Statements run through the handle — its `query()`, `query_iter()` and `execute()` — form one atomic unit: `commit()` makes them permanent, `rollback()` discards them. The handle's statement surface matches the connection's, `?` placeholders included.

```python
tx = conn.begin()
tx.execute("update accounts set balance = balance - 25 where name = ?", "ada")
tx.execute("update accounts set balance = balance + 25 where name = ?", "grace")
tx.commit()          # or tx.rollback() to undo both
```

| Method | Description |
|--------|-------------|
| `query(sql, *params)` | Run a SELECT-style statement inside the transaction |
| `query_iter(sql, *params)` | Same statement, streamed as a `Cursor`; drain or close it before commit or rollback |
| `execute(sql, *params)` | Run a row-changing statement inside the transaction |
| `commit()` | Make the transaction's changes permanent and end it |
| `rollback()` | Discard the transaction's changes and end it |
| `get_orm()` | Return the [ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md) bound to this transaction, so its calls join it |

Every operation on a finished transaction fails with `transaction is already committed or rolled back`, whichever way it ended. A transaction abandoned without either call is rolled back automatically once the runtime collects it, so an error path that simply returns leaves no half-applied work behind — do not rely on the timing: end transactions explicitly (`try`/`except` with `rollback()` in the handler), because until collection runs the connection stays held.

Outside a transaction the API is autocommit. Two SQLite-specific notes for a private in-memory database (`":memory:"`), which runs on a single connection:

- While a transaction is open, the connection's own calls fail fast with `connection is held by an open transaction` — use the transaction's methods until it ends.
- An open `query_iter()` cursor holds the connection the same way (`connection is held by an open cursor`); drain it or call `close()`. A cursor abandoned mid-iteration releases its rows automatically once collected.

A file database serves the transaction, the cursor and the connection from separate pooled connections, so connection-level reads keep working and see the committed view.

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

See the [Relational ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md) page for `iterate()` and the rest of the
builder.

## ORM

`conn.get_orm()` returns a lightweight table helper bound to the connection: `insert`/`select`/`update`/`delete`/`count`/`tables()` over dict-shaped rows, with SQL generation following the backend. See the [Relational ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md) page for the full reference.

## See Also

- [SQL](https://scriptling.dev/okf/scriptling-libraries/databases/sql.md): the same API over MySQL, MariaDB and PostgreSQL
- [Database Libraries](https://scriptling.dev/okf/scriptling-libraries/databases/sqlite.md): all four backends, two API shapes
