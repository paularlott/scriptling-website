---
title: Relational ORM
linkTitle: orm
description: conn.get_orm() gives queries, builders, criteria and model gateways for every relational backend.
tags: [libraries, databases, orm]
weight: 6
---

## Overview

Both relational plugins, [sqlite](../sqlite/) and [sql](../sql/), hand out the same ORM from `conn.get_orm()`. It has three layers, each useful on its own:

- **kwargs forms**: `insert(table, dict)`, `update`/`delete` (where required), `count`, `tables()`, plus `create_table`/`drop_table` builders.
- **query builder**: `orm.select(table, *columns)` returns a chainable query: `.where(...)` links AND together, criteria objects compose `OR` groups, `.fetch()` runs exactly one query.
- **model gateways**: `orm.table(factory, table, ...)` maps rows onto your objects through a factory function.

The whole ORM is scriptling script that executes host-side in both plugin modes (compiled-in and external): chained builder calls cost no round trips, not even at `get_orm()`: and one implementation serves every backend. Each plugin bakes its dialect into the kit it hands out (the sql plugin picks per connection from the DSN scheme): backtick quoting on MySQL/MariaDB, double quotes and `$n` placeholders on PostgreSQL, whatever SQLite likes. Orms from different connections never interfere, so one script can drive MySQL, SQLite and PostgreSQL at the same time.

```python
import scriptling.sqlite as sqlite

conn = sqlite.connect("app.db")
orm = conn.get_orm()

 (orm.create_table("people")
 .column("id", "integer", primary_key=True, autoincrement=True)
 .column("name", "text")
 .column("score", "real")
 .column("active", "integer", default=1)
 .execute())

orm.insert("people", {"name": "ada", "score": 9.5})
rows = (orm.select("people", "name", "score")
        .where("score", ">=", 8.0)
        .order_by("score", desc=True)
        .fetch())

conn.close()
```

The table builder renders the auto-increment primary key per backend, so this intro runs unchanged on SQLite, MySQL/MariaDB and PostgreSQL; see [Table Builder](#table-builder) for the full column options.

## Query Builder

`orm.select(table, *columns)` returns a query; every method returns the same query so calls chain; `.fetch()` (or `.one()`, `.count()`) assembles the SQL, binds the parameters and runs it.

```python
rows = (orm.select("people", "name")
        .where("active", "=", 1)                                    # flat AND
        .where("score", ">=", 8.0)
        .where(orm.any_of(orm.eq("name", "ada"),                    # OR group
                          orm.eq("name", "grace")))
        .order_by("score", desc=True)
        .limit(10)
        .fetch())
```

### Conditions

`.where(...)` accepts either shape:

- `.where(column, op, value)`: flat condition; `op` is whitelisted (`= != <> < <= > >= like`).
- `.where(criterion)`: a criterion from the constructors below, including groups.

Criteria are plain values: build them anywhere, pass them around, combine them:

| Constructor | SQL |
|-------------|-----|
| `orm.eq / ne / lt / le / gt / ge(column, value)` | the obvious comparison |
| `orm.like(column, pattern)` | Case-sensitive on postgres (`LIKE`); follows the backend's default elsewhere |
| `orm.ilike(column, pattern)` | Case-insensitive: `ILIKE` on postgres; on MySQL/MariaDB and SQLite, which have no `ILIKE`, it renders `LIKE`, which is case-insensitive under their default collations |
| `orm.one_of(column, values)` / `orm.not_one_of(column, values)` | `IN (...)` / `NOT IN (...)`: the column equals one of the values, or none of them |
| `orm.is_null / not_null(column)` | `IS NULL` / `IS NOT NULL` |
| `orm.any_of(*criteria)` | criteria joined with `OR`, parenthesised |
| `orm.all_of(*criteria)` | criteria joined with `AND`, parenthesised |

Groups nest arbitrarily. `(a OR b) AND (a OR c)`:

```python
rows = (orm.select("people", "name")
        .where(orm.any_of(orm.eq("a", 1), orm.eq("b", 2)))
        .where(orm.any_of(orm.eq("a", 1), orm.eq("c", 3)))
        .fetch())
```

Every value binds as a parameter and every identifier is quoted and validated against a safe character set: conditions are generated, never interpolated.

### Methods

| Method | Description |
|--------|-------------|
| `where(column, op, value)` / `where(criterion)` | add a condition (AND) |
| `iterate()` | stream rows instead of materialising: `for row in q.iterate():`; close early with the iterator's `close()` |
| `where_sql(fragment, *params)` | escape hatch: raw SQL fragment, `?` placeholders bind to params (renumbered on postgres) |
| `order_by(column, desc=False)` | order; repeatable |
| `limit(n)` / `offset(n)` | paging |
| `fetch()` | run and return all rows as a list of dicts |
| `iterate()` | run and return an iterator: `for row in q.iterate():` streams row by row; compiled-in builds read lazily from the driver, external-plugin builds make one call per row (constant memory either way) |
| `one()` | first row or `None` |
| `count()` | run as `SELECT count(*)` and return the number |

## Kwargs Forms

| Method | Description |
|--------|-------------|
| `insert(table, values, pk="id")` | Insert one row from a dict; returns `{"last_insert_id": int, "rows_affected": int}`: the id is recovered via `RETURNING` on postgres, through the primary key named by `pk` |
| `update(table, values, where, *params)` | Set columns from a dict on matching rows; **where required** |
| `delete(table, where, *params)` | Delete matching rows; **where required** |
| `count(table, where="", *params)` | Row count |
| `tables()` | User table names in the current database, sorted |

Blanket updates and deletes are refused: if you genuinely want every row, say so explicitly with `conn.execute("delete from t")`.

## Table Builder

`orm.create_table(table)` returns a builder with the same shape as the query builder; `.execute()` runs the DDL. Identifiers are quoted and validated like everywhere else, and the auto-incrementing primary key renders per backend: `AUTOINCREMENT` on SQLite, `AUTO_INCREMENT` on MySQL/MariaDB, `SERIAL` on PostgreSQL: so one script builds the same table everywhere.

```python
(orm.create_table("people")
 .column("id", "integer", primary_key=True, autoincrement=True)
 .column("name", "text", nullable=False, unique=True)
 .column("score", "real", default=0.0)
 .if_not_exists()
 .execute())

orm.drop_table("people")     # DROP TABLE IF EXISTS, same everywhere
```

| Method | Description |
|--------|-------------|
| `column(name, type, primary_key=False, autoincrement=False, nullable=True, unique=False, default=None)` | add a column; `type` is raw SQL (`"text"`, `"varchar(100)"`, …) |
| `if_not_exists()` | `CREATE TABLE IF NOT EXISTS` |
| `execute()` | run and return the execute result |

Column types pass through as-is: `integer`, `text` and `real` work on all three backends; anything backend-specific (e.g. `serial`, `jsonb`) is yours to spell. `default` accepts numbers, strings, booleans and `None`. Indexes and foreign keys stay with raw `conn.execute`: DDL beyond tables is where the backends genuinely disagree.

## Model Gateways

`orm.table(factory, table, pk="id", columns=[...])` returns a gateway bound to the connection. The factory is a plain function that turns a row dict into your object (a dict, an instance of your class: anything with the columns as attributes or keys):

```python
def make_person(id=None, name=None, score=None, active=None):
    return Person(id, name, score, active)     # or just return a dict

people = orm.table(make_person, "people", pk="id",
                   columns=["id", "name", "score", "active"])

p = people.get(1)          # factory(rows) or None
people.save(p)             # update by pk
people.insert(make_person(name="kurt", score=6.0))
people.delete(p)           # by instance or raw pk
people.count()
people.select("name").where("active", "=", 0).fetch()   # full builder
```

`columns` is required for `insert`/`save` (the gateway needs to know what to write); `get`, `select`, `count` and `delete` work without it.

## See Also

- [sqlite](../sqlite/) and [sql](../sql/): the connections that hand out ORMs
- [Database Libraries](./): all four backends, two API shapes
