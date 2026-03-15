---
title: scriptling.ai.memory
linkTitle: ai.memory
weight: 3
---

Long-term memory store for AI agents. Backed by a KV store, memories persist across sessions and are automatically compacted when they go unaccessed for too long.

## Functions

| Function | Description |
|----------|-------------|
| `memory.new(kv_store, idle_timeout=24)` | Create a memory store |

## Memory Object Methods

| Method | Description |
|--------|-------------|
| `remember(content, type, key, importance)` | Store a memory |
| `recall(query, limit, type)` | Search memories by keyword against content and key |
| `forget(id_or_key, by_key)` | Remove a memory |
| `list(type, limit)` | List all memories |
| `count()` | Total number of memories |
| `compact(idle_timeout, exempt_threshold)` | Manually trigger compaction |
| `close()` | Stop background compaction goroutine |

## Setup

```go
import (
    "github.com/paularlott/scriptling/extlibs"
    aimemory "github.com/paularlott/scriptling/extlibs/ai/memory"
)

// Register the KV and memory libraries
extlibs.RegisterRuntimeKVLibrary(p)
aimemory.Register(p)
```

## memory.new(kv_store, idle_timeout=24)

Creates a memory store backed by the given KV store. The KV store manages persistence — use `kv.default` for the system store or `kv.open()` for a dedicated store.

**Parameters:**

- `kv_store`: A KV store object (`kv.default` or `kv.open(...)`)
- `idle_timeout` (float, optional): Hours before unaccessed memories are automatically removed. Memories with `importance >= 0.8` are exempt. Pass `0` to disable automatic compaction. Default: `24`

**Returns:** Memory store object

```python
import scriptling.runtime.kv as kv
import scriptling.ai.memory as memory

# Use the default system store
mem = memory.new(kv.default)

# Use a dedicated persistent store
db = kv.open("/data/agent-memory.db")
mem = memory.new(db, idle_timeout=48)
```

## Store Methods

### remember(content, type="note", key="", importance=0.5)

Store a memory.

**Parameters:**

- `content` (str): What to remember
- `type` (str, optional): `"fact"`, `"preference"`, `"event"`, or `"note"` (default: `"note"`)
- `key` (str, optional): Semantic key used to tag the memory (e.g. `"user_name"`, `"api_limit"`). Used as a searchable field by `recall`
- `importance` (float, optional): `0.0`–`1.0`; memories with importance `>= 0.8` are exempt from compaction (default: `0.5`)

**Returns:** dict with `id`, `content`, `type`, `key`, `importance`, `created_at`, `accessed_at`

```python
# Store a fact with a key for fast retrieval
mem.remember("User's name is Alice", type="fact", key="user_name", importance=0.9)

# Store a preference
mem.remember("User prefers dark mode", type="preference", key="ui_theme", importance=0.7)

# Store a note
mem.remember("Check API rate limits before next run")
```

### recall(query="", limit=10, type="")

Search memories by keyword. Scores results against both the `content` and `key` fields — key matches are weighted higher. Pass a semantic key like `"user_name"` or a natural language phrase like `"dark mode"`.

**Parameters:**

- `query` (str, optional): Search query matched against both memory content and keys. Empty returns memories ranked by recency and importance
- `limit` (int, optional): Maximum results (default: `10`)
- `type` (str, optional): Filter by type

**Returns:** list of memory dicts, ranked by relevance

```python
# Search by semantic key (fuzzy — "wife_name" matches stored key "user_wife_name")
results = mem.recall("user_name", limit=1)
if results:
    print("User is", results[0]["content"])

# Natural language search against content
results = mem.recall("dark mode")
for r in results:
    print(r["content"])

# Most recent/important memories
recent = mem.recall(limit=5)

# Facts only
facts = mem.recall("Alice", type="fact")
```

### forget(id_or_key, by_key=False)

Remove a memory.

**Parameters:**

- `id_or_key` (str): Memory ID or semantic key
- `by_key` (bool, optional): If `True`, treat argument as a key. Default `False` tries ID first, then key

**Returns:** `True` if a memory was removed

```python
mem.forget("user_name", by_key=True)   # by key
mem.forget("abc-123-def")              # by ID (falls back to key if not found)
```

### list(type="", limit=50)

List stored memories.

**Parameters:**

- `type` (str, optional): Filter by type
- `limit` (int, optional): Maximum results (default: `50`)

**Returns:** list of memory dicts

```python
all_memories = mem.list()
facts = mem.list(type="fact")
```

### count()

Returns the total number of stored memories.

```python
print(f"Stored memories: {mem.count()}")
```

### compact(idle_timeout=24, exempt_threshold=0.8)

Manually trigger compaction. Removes memories not accessed within `idle_timeout` hours, except those with `importance >= exempt_threshold`.

**Returns:** int — number of memories removed

```python
removed = mem.compact(idle_timeout=12, exempt_threshold=0.7)
print(f"Compacted {removed} memories")
```

### close()

Stops the background compaction goroutine. Does not close the underlying KV store.

```python
mem.close()
db.close()  # close the kv store separately if needed
```

## Memory Types

| Type | Use for |
|------|---------|
| `fact` | Objective information — names, IDs, limits |
| `preference` | User preferences — themes, formats, styles |
| `event` | Things that happened — deployments, meetings |
| `note` | Agent's own notes (default) |

## Compaction

Memories are automatically removed when they have not been accessed for longer than `idle_timeout` hours. This keeps the store from growing indefinitely without any manual intervention.

**Exempt from compaction:** memories with `importance >= 0.8` (configurable via `compact()`).

**Accessing a memory** (via `recall`) resets its idle timer.

```python
# 24h idle timeout, memories with importance >= 0.8 are kept forever
mem = memory.new(kv.default, idle_timeout=24)

# Disable automatic compaction, manage manually
mem = memory.new(kv.default, idle_timeout=0)
mem.compact(idle_timeout=48)  # run manually when needed
```

## Agent Integration

```python
import scriptling.runtime.kv as kv
import scriptling.ai.memory as memory
import scriptling.ai as ai
import scriptling.ai.agent as agent

client = ai.Client("http://127.0.0.1:1234/v1")
tools = ai.ToolRegistry()
mem = memory.new(kv.default, idle_timeout=24)

tools.add("remember", "Store information in long-term memory", {
    "content": "string",
    "type": "string?",
    "key": "string?",
    "importance": "float?"
}, lambda args: mem.remember(
    args["content"],
    type=args.get("type", "note"),
    key=args.get("key", ""),
    importance=float(args.get("importance", 0.5))
))

tools.add("recall", "Search long-term memory", {
    "query": "string?",
    "key": "string?"
}, lambda args: mem.recall((args.get("key") or "") + " " + (args.get("query") or ""), limit=5))

tools.add("forget", "Remove a memory", {
    "key": "string?",
    "id": "string?"
}, lambda args: mem.forget(args["key"], by_key=True) if args.get("key") else mem.forget(args.get("id", "")))

bot = agent.Agent(client, tools=tools,
    system_prompt="You are a helpful assistant with long-term memory.",
    model="gpt-4")

bot.interact()
```

## MCP Tools

Memory can be exposed as MCP tools so any LLM client (Claude Desktop, Cursor, etc.) can use it. See the [memory MCP tools example](https://github.com/paularlott/scriptling/tree/main/examples/mcp-tools/memory-tools) for ready-to-use `.toml`/`.py` tool definitions.

```bash
# Start the MCP server with memory tools
./bin/scriptling --server :8000 --mcp-tools ./examples/mcp-tools/memory-tools
```

## See Also

- [runtime.kv](../runtime-kv/) — KV store backing the memory system
- [ai.agent](../agent/) — Agentic loop that memory integrates with
- [Memory MCP Tools Example](https://github.com/paularlott/scriptling/tree/main/examples/mcp-tools/memory-tools)
