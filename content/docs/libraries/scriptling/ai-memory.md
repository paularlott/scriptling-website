---
title: scriptling.ai.memory
linkTitle: ai.memory
weight: 3
---

Long-term memory store for AI agents. Backed by a KV store, memories persist across sessions and are automatically compacted using importance decay — older, less-accessed memories fade over time while important ones survive.

## Functions

| Function | Description |
|----------|-------------|
| `memory.new(kv_store, ai_client?, model?)` | Create a memory store |

## Memory Object Methods

| Method | Description |
|--------|-------------|
| `remember(content, type, importance)` | Store a memory; returns a dict with `id` |
| `recall(query, limit, type)` | Search memories by keyword |
| `forget(id)` | Remove a memory by ID |
| `list(type, limit)` | List all memories |
| `count()` | Total number of memories |

## Go Registration

```go
import (
    "github.com/paularlott/scriptling/extlibs"
    aimemory "github.com/paularlott/scriptling/extlibs/ai/memory"
)

extlibs.RegisterRuntimeKVLibrary(p)
aimemory.Register(p)
```

## memory.new(kv_store, ai_client=None, model="")

Creates a memory store backed by the given KV store.

**Parameters:**

- `kv_store`: A KV store object (`kv.default` or `kv.open(...)`)
- `ai_client` (AIClient, optional): AI client for Mode 2 LLM compaction — see [Compaction](#compaction)
- `model` (str, optional): Model name for LLM compaction (required if `ai_client` provided)

**Returns:** Memory store object

```python
import scriptling.runtime.kv as kv
import scriptling.ai.memory as memory

# Use the default system store
mem = memory.new(kv.default)

# Use a dedicated persistent store
db = kv.open("/data/agent-memory.db")
mem = memory.new(db)

# With LLM compaction (Mode 2)
import scriptling.ai as ai
client = ai.Client("http://127.0.0.1:1234/v1")
mem = memory.new(kv.open("./memory-db"), client, model="qwen3-8b")
```

## Store Methods

### remember(content, type="note", importance=0.5)

Store a memory.

**Parameters:**

- `content` (str): What to remember
- `type` (str, optional): `"fact"`, `"preference"`, `"event"`, or `"note"` (default: `"note"`)
- `importance` (float, optional): `0.0`–`1.0` — controls how long the memory survives compaction (default: `0.5`)

**Returns:** dict with `id`, `content`, `type`, `importance`, `created_at`, `accessed_at`

```python
result = mem.remember("User's name is Alice", type="fact", importance=0.9)
print(result["id"])  # UUIDv7 — use this to forget the memory later

mem.remember("User prefers dark mode", type="preference", importance=0.7)
mem.remember("Check API rate limits before next run")
```

### recall(query="", limit=10, type="")

Search memories by keyword. Each recall resets the memory's age clock, protecting it from compaction.

**Parameters:**

- `query` (str, optional): Keyword search against memory content. Empty returns memories ranked by recency and importance
- `limit` (int, optional): Maximum results (default: `10`)
- `type` (str, optional): Filter by type

**Returns:** list of memory dicts, ranked by relevance

```python
results = mem.recall("user name", limit=1)
if results:
    print("User is", results[0]["content"])

# Most recent/important memories
recent = mem.recall(limit=5)

# Facts only
facts = mem.recall("Alice", type="fact")

# All preferences (used by agent at startup)
prefs = mem.recall("", limit=50, type="preference")
```

### forget(id)

Remove a memory by ID.

```python
result = mem.remember("User's name is Alice", type="fact", importance=0.9)
mem.forget(result["id"])
```

### list(type="", limit=50)

List stored memories without updating their access time.

```python
all_memories = mem.list()
facts = mem.list(type="fact")
```

### count()

Returns the total number of stored memories.

```python
print(f"Stored memories: {mem.count()}")
```

## Memory Types

| Type | Decay behaviour | Use for |
|------|----------------|---------|
| `preference` | **Never decays** | User preferences — themes, formats, styles |
| `fact` | Half-life 90 days | Objective information — names, IDs, limits |
| `event` | Half-life 30 days | Things that happened — deployments, meetings |
| `note` | Half-life 7 days | Agent's own notes (default) |

`preference` memories are the only type that never decay regardless of importance. They are only removed after the 180-day hard age cap (based on last access).

## Compaction

Compaction runs automatically in the background after every 10 new memories (with a minimum 5-minute gap between runs). It never blocks normal operations.

### Mode 1 — Rule-based (always active)

Memories are pruned using exponential importance decay based on time since last access:

```
effective_importance = importance × 0.5^(age / half_life)
```

A memory is pruned when its effective importance drops below `0.1`. Accessing a memory via `recall()` resets its age clock, restoring full effective importance.

**Hard age cap:** any memory not accessed in 180 days is removed regardless of type or importance.

**Examples:**

| Memory | Importance | Age | Effective | Pruned? |
|--------|-----------|-----|-----------|---------|
| preference | 0.9 | 60 days | 0.9 (no decay) | No |
| fact | 0.9 | 90 days | 0.45 | No |
| fact | 0.9 | 270 days | 0.11 | No (but near threshold) |
| note | 0.8 | 21 days | 0.1 | Yes (at threshold) |
| event | 0.5 | 30 days | 0.25 | No |

### Mode 2 — LLM compaction (optional)

When an AI client is passed to `memory.new()`, Mode 2 runs after Mode 1. The LLM reviews remaining memories and can:

- Merge duplicates or semantically similar memories into one
- Delete outdated memories that contradict newer ones
- Re-score importance based on actual relevance

Mode 2 only runs when there are at least 20 memories remaining after Mode 1.

```python
client = ai.Client("http://127.0.0.1:1234/v1")
mem = memory.new(kv.open("./memory-db"), client, model="qwen3-8b")
```

## Agent Integration

The simplest way to give an agent memory is to pass `memory=` to `Agent()`. The agent wires up the tools and augments the system prompt automatically — see [ai.agent Memory Integration](../agent/#memory-integration).

```python
import scriptling.ai as ai
import scriptling.ai.agent as agent
import scriptling.ai.memory as memory
import scriptling.runtime.kv as kv

client = ai.Client("http://127.0.0.1:1234/v1")
mem = memory.new(kv.open("./memory-db"))

bot = agent.Agent(client, model="gpt-4", memory=mem)
bot.interact()
```

The agent automatically registers `memory_remember`, `memory_recall`, and `memory_forget` as tools, appends memory usage instructions to the system prompt, and pre-loads all stored `preference` memories into the system prompt for immediate context.

## MCP Tools

Memory can be exposed as MCP tools so any LLM client (Claude Desktop, Cursor, etc.) can use it. See the [memory MCP tools example](https://github.com/paularlott/scriptling/tree/main/examples/mcp-tools/memory-tools) for ready-to-use tool definitions.

```bash
SCRIPTLING_MEMORY_DB=~/.scriptling/memory \
  ./bin/scriptling --server :8000 --mcp-tools ./examples/mcp-tools/memory-tools
```

## See Also

- [runtime.kv](../runtime-kv/) — KV store backing the memory system
- [ai.agent](../agent/) — Agent with automatic memory integration
- [Memory MCP Tools Example](https://github.com/paularlott/scriptling/tree/main/examples/mcp-tools/memory-tools)
