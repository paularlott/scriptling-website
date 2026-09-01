---
description: SQLite, MySQL/MariaDB/PostgreSQL, Valkey/Redis and BadgerDB plugins, two API shapes, four backends.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/databases/
sources:
    - resource: https://scriptling.dev/reference/libraries/databases/
status: stable
tags:
    - libraries
    - databases
title: Database Libraries
type: API Reference
---
# Database Libraries

## Start Here

Database libraries are plugins, not an unconditional part of every Scriptling binary. First choose how they are deployed, then choose a backend and API:

1. Use the default `scriptling` build with all four compiled in, add only the matching build tags to a custom binary, or load external plugin executables.
2. Before connecting, ensure the host policy permits the storage or endpoint: SQLite file paths and BadgerDB directories must be allowed, while SQLite `":memory:"` needs no path permission; SQL and Valkey endpoints must pass the host network policy.
3. Choose [SQLite](https://scriptling.dev/okf/scriptling-libraries/databases/sqlite.md) for an embedded relational file or private in-memory database; choose [SQL](https://scriptling.dev/okf/scriptling-libraries/databases/sql.md) for MySQL, MariaDB, or PostgreSQL over the network.
4. Use direct SQL for exact backend statements, or call `conn.get_orm()` for the dialect-aware common subset documented by the [Relational ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md).
5. Choose [Valkey](https://scriptling.dev/okf/scriptling-libraries/databases/valkey.md) for a network key/value server or [BadgerDB](https://scriptling.dev/okf/scriptling-libraries/databases/badgerdb.md) for embedded key/value storage.

| Library | Import | API | Deployment shape |
|---------|--------|-----|------------------|
| [SQLite](https://scriptling.dev/okf/scriptling-libraries/databases/sqlite.md) | `scriptling.sqlite` | relational | embedded, pure Go |
| [SQL](https://scriptling.dev/okf/scriptling-libraries/databases/sql.md) | `scriptling.sql` | relational | MySQL, MariaDB, PostgreSQL servers |
| [Valkey](https://scriptling.dev/okf/scriptling-libraries/databases/valkey.md) | `scriptling.valkey` | key/value | Valkey or Redis server |
| [BadgerDB](https://scriptling.dev/okf/scriptling-libraries/databases/badgerdb.md) | `scriptling.badgerdb` | key/value | embedded BadgerDB |

## Minimal Relational Query

```python
import scriptling.sqlite as sqlite

conn = sqlite.connect(":memory:")
conn.execute("create table people (name text)")
conn.execute("insert into people (name) values (?)", "ada")
rows = conn.query("select name from people where name = ?", "ada")
print(rows[0]["name"])
conn.close()
```

Expected output:

```text
ada
```

The same `query()` and `execute()` shape applies to `scriptling.sql`; change the import, connection string, and backend-specific DDL as needed. Parameters are bound rather than interpolated, and `?` placeholders are translated for PostgreSQL.

## SQL or ORM?

Use connection methods when you need backend-specific SQL, joins, DDL, or exact query plans. Use the [Relational ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md) for generated selects, criteria, inserts, guarded updates/deletes, dialect-aware table creation for its documented common subset, and model gateways. Both operate through the same connection.

The script-level relational API is autocommit: each connection or ORM terminal call executes independently. It exposes no transaction handle, `begin()`, `commit()`, or `rollback()`, so it cannot group multiple script calls into one atomic transaction.

## Availability

- **Compiled in:** the default `scriptling` build includes SQLite, SQL, Valkey, and BadgerDB; `scriptling-slim` omits them. Custom builds select them with `plugin_sqlite`, `plugin_sql`, `plugin_valkey`, and `plugin_badgerdb` build tags.
- **External plugins:** matching `sqlite`, `sql`, `valkey`, and `badgerdb` executables can be discovered or loaded through the host's plugin manager. This keeps the core binary lean but adds a separate plugin process and protocol boundary.

The script APIs are aligned across compiled and external forms, including streaming `query_iter()` and ORM `iterate()`.

## Deployment and Security

Embedded databases keep storage local but require writable paths permitted by the host; `":memory:"` SQLite needs no file. Server databases require network reachability and credentials, often embedded in the DSN. Keep credentials out of source and logs.

Database plugins receive host policy through their plugin handshake. SQLite and BadgerDB enforce configured allowed paths. SQL and Valkey use the guarded network dialer with host allow/deny rules, address-category controls, and DNS-rebinding-resistant validated-IP dialing. External plugins also expand the deployment surface: distribute trusted binaries, constrain their process permissions, and account for their lifecycle and logs. See the [Security Guide](https://scriptling.dev/okf/scriptling-docs/security.md).

## See Also

- [Relational ORM](https://scriptling.dev/okf/scriptling-libraries/databases/orm.md): dialect-aware builders for the documented common subset, criteria, and model gateways
- [Database examples](https://github.com/paularlott/scriptling/tree/main/examples/databases): runnable scripts against real servers
- [Plugin Control Library](https://scriptling.dev/okf/scriptling-libraries/plugin.md): loading and calling plugins at runtime
