---
title: Relational ORM
linkTitle: orm
description: conn.get_orm() gives queries, builders, criteria and model gateways for every relational backend.
tags: [libraries, databases, orm]
weight: 6

aliases:
  - /reference/libraries/scriptling/databases/orm/
---

## Overview

Both relational plugins, [sqlite](../sqlite/) and [sql](../sql/), hand out the same ORM from `conn.get_orm()`. It has three layers, each useful on its own:

- **query builders**: `orm.select(table, *columns)`, `orm.update(table, values)` and `orm.delete(table)` return chainable queries: `.where(...)` links AND together, criteria objects compose `OR` groups, and a terminal (`fetch()`, `execute()`, `count()`) runs exactly one statement.
- **quick forms**: `insert(table, dict)` for the write with nothing to filter, and `tables()`.
- **model gateways**: `orm.table(factory, table, ...)` maps rows onto your objects through a factory function.

The ORM is Scriptling code that runs host-side in both plugin modes, so chained builder calls do not cross the plugin boundary. Each connection supplies its dialect: backtick quoting on MySQL/MariaDB, double quotes and `$n` placeholders on PostgreSQL, and SQLite syntax for SQLite. ORMs from different connections do not interfere.

The example is backend-neutral: pass it a connection created by either `scriptling.sqlite.connect(...)` or `scriptling.sql.connect(...)`.

```python
def high_scores(conn):
    orm = conn.get_orm()

    (orm.create_table("people")
     .column("id", "integer", primary_key=True, autoincrement=True)
     .column("name", "text")
     .column("score", "real")
     .column("active", "integer", default=1)
     .if_not_exists()
     .execute())

    orm.insert("people", {"name": "ada", "score": 9.5})
    return (orm.select("people", "name", "score")
            .where("score", ">=", 8.0)
            .order_by("score", desc=True)
            .fetch())
```

The table builder renders the auto-increment primary key per backend, so the function works with SQLite, MySQL/MariaDB, or PostgreSQL connections; the caller is still responsible for importing the selected plugin and supplying its file path or DSN.

## Transactions

Through a connection's ORM the terminal operations are autocommit: each `fetch()`, `count()`, `insert()`, `execute()`, `save()`, or `delete()` call runs as its own statement. To group several calls into one atomic unit, start a transaction with `conn.begin()` and take the ORM from the handle: `tx.get_orm()` returns a kit whose every call — queries, builders, model gateways — runs inside the transaction until `tx.commit()` or `tx.rollback()`.

```python
tx = conn.begin()
torm = tx.get_orm()
torm.insert("people", {"name": "ada", "score": 9.5})
torm.update("people", {"score": 9.9}).where("name", "=", "ada").execute()
tx.rollback()        # both changes disappear
```

## Query Builders

`orm.select(table, *columns)`, `orm.update(table, values)` and `orm.delete(table)` each return a chainable query; every method returns the same query so calls chain; the terminal (`fetch()`, `execute()`, `count()`) assembles the SQL, binds the parameters and runs exactly one statement.

```python
# select: filter, order, page, then fetch() (or one(), iterate(), count())
rows = (orm.select("people", "name")
        .where("active", "=", 1)                                    # flat AND
        .where("score", ">=", 8.0)
        .where(orm.any_of(orm.eq("name", "ada"),                    # OR group
                          orm.eq("name", "grace")))
        .order_by("score", desc=True)
        .limit(10)
        .fetch())

# count: the same filters, SELECT count(*) underneath
high = orm.select("people").where("score", ">=", 8.0).count()

# update: the same filters, execute() returns rows_affected
result = (orm.update("people", {"score": 0.0})
          .where("score", "<", 5.0)
          .execute())                       # -> {"rows_affected": 2}

# delete: the same filters
orm.delete("people").where("active", "=", 0).execute()
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

`where` and `where_sql` work the same on all three builders; the rest belong to the select query.

| Method | Description |
|--------|-------------|
| `where(column, op, value)` / `where(criterion)` | add a condition (AND); select, update and delete |
| `where_sql(fragment, *params)` | escape hatch: raw SQL fragment, `?` placeholders bind to params (renumbered on postgres); select, update and delete |

On postgres the renumbering leaves quoted literals, quoted identifiers, comments, and the jsonb `?|`/`?&` operators alone. A bare jsonb `?` is indistinguishable from a placeholder on this path; `jsonb_exists(data, 'k')` is the function form that works.
| `order_by(column, desc=False)` | order; repeatable; select |
| `limit(n)` / `offset(n)` | paging; select |
| `fetch()` | run and return all rows as a list of dicts; select |
| `iterate()` | stream rows from the query; compiled-in relational builds read lazily, while external plugins fetch one row per call across the plugin boundary |
| `one()` | first row or `None`; select |
| `count()` | run as `SELECT count(*)` and return an `int`; select |
| `execute()` | run the `UPDATE`/`DELETE` and return `{"rows_affected": int}`; update and delete |

## Quick Forms

| Method | Description |
|--------|-------------|
| `insert(table, values, pk="id")` | Insert one row from a dict; returns `{"last_insert_id": int, "rows_affected": int}`: the id is recovered via `RETURNING` on postgres, through the primary key named by `pk` |
| `tables()` | User table names in the current database, sorted |

Blanket updates and deletes are refused: `.execute()` without any `where` raises, so if you genuinely want every row, say so explicitly with `conn.execute("delete from t")`.

## Table Builder

`orm.create_table(table)` returns a builder with the same shape as the query builder; `.execute()` runs the DDL. Identifiers are quoted and validated like everywhere else, and the documented integer auto-incrementing primary-key shape renders per backend: `AUTOINCREMENT` on SQLite, `AUTO_INCREMENT` on MySQL/MariaDB, and `SERIAL` on PostgreSQL. Portability is limited to this documented generated subset; raw DDL, type names, constraints, indexes, collations, and backend-specific features still differ.

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

Column types pass through as-is: `integer`, `text` and `real` work on all three backends; anything backend-specific (for example, `serial` or `jsonb`) is yours to spell. `default` accepts integers, finite floats, strings, and booleans. `None` means no `DEFAULT` clause; non-finite floats (`NaN`, positive infinity, or negative infinity) are rejected with `ValueError`. Indexes and foreign keys stay with raw `conn.execute`: DDL beyond tables is where the backends genuinely disagree.

## Model Gateways

`orm.table(factory, table, pk="id")` returns a gateway bound to the connection. The factory is a plain function that turns a row dict into your object (a dict, an instance of your class: anything with the columns as attributes or keys):

```python
def make_person(id=None, name=None, score=None, active=None):
    return Person(id, name, score, active)     # or just return a dict

# no columns: the gateway writes every column the table has
people = orm.table(make_person, "people", pk="id")

p = people.get(1)          # factory(row) or None
people.save(p)             # update by pk
people.insert(make_person(name="kurt", score=6.0))
people.delete(p)           # by instance or raw pk
people.count()
people.select("name").where("active", "=", 0).fetch()   # full builder

# columns=[...]: the same table through a narrower gateway
names = orm.table(make_person, "people", pk="id", columns=["id", "name"])
n = names.get(1)
n.name = "ada lovelace"
names.save(n)              # writes name only; score and active stay untouched

# per-call columns: narrow one save or insert without a second gateway
people.save(p, columns=["score"])
people.insert(make_person(name="kurt", score=6.0), columns=["name", "score"])
```

`columns` is optional. Without it the gateway writes every column the table has: the column list is read from the schema once per `get_orm()` and cached, so adding or removing a column in the table needs no script change. Pass `columns=["id", "name"]` to manage a subset (a wide table, or columns you deliberately do not want writes to touch); the list then applies to `insert` and `save` only, and costs no schema lookup. That list is the gateway's default write shape — `save(p, columns=[...])` and `insert(p, columns=[...])` narrow it for a single call.

Two write semantics worth knowing: `insert` skips `None` values, so unset fields take their schema defaults and the primary key auto-assigns (an object with everything unset inserts a pure-defaults row); `save` writes every managed column, including `None` (that is how you clear one). An explicit `columns=` list on either call is explicit: `None` in a listed column is written as `NULL`, which is the way to override a schema default on insert through the gateway (the kit form `orm.insert(table, {"cleared_at": None})` does the same).

## See Also

- [sqlite](../sqlite/) and [sql](../sql/): the connections that hand out ORMs
- [Database Libraries](./): all four backends, two API shapes
