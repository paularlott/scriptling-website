---
title: scriptling.ai.memory
linkTitle: ai.memory
weight: 3
---

Long-term memory store for AI agents. Backed by a KV store, memories persist across sessions and are automatically deduplicated using MinHash similarity. Compaction (pruning old/decayed memories) runs on-demand via `compact()`.

## Functions

| Function | Description |
|----------|-------------|
| `memory.new(kv_store, ai_client?, model?)` | Create a memory store |

## Memory Object Methods

| Method | Description |
|--------|-------------|
| `remember(content, type, importance)` | Store a memory; returns a dict with `id` |
| `recall(query, limit, type)` | Search memories by keyword and semantic similarity; `limit=-1` for all |
| `forget(id)` | Remove a memory by ID |
| `count()` | Total number of memories |
| `compact()` | Run compaction (prune old/decayed memories); returns dict with `removed` and `remaining` counts |

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
- `ai_client` (AIClient, optional): AI client for resolving ambiguous duplicates during `remember()` — see [Deduplication](#deduplication)
- `model` (str, optional): Model name for LLM resolution (required if `ai_client` provided)

**Returns:** Memory store object

```python
import scriptling.runtime.kv as kv
import scriptling.ai.memory as memory

# Use the default system store
mem = memory.new(kv.default)

# Use a dedicated persistent store
db = kv.open("/data/agent-memory.db")
mem = memory.new(db)

# With LLM-based deduplication resolution
import scriptling.ai as ai
client = ai.Client("http://127.0.0.1:1234/v1")
mem = memory.new(kv.open("./memory-db"), ai_client=client, model="qwen3-8b")
```

## Store Methods

### remember(content, type="note", importance=0.5)

Store a memory. Before saving, performs a pre-flight similarity check against existing memories of the same type:

- **Similarity ≥ 0.85**: Updates the existing memory in place (no new entry)
- **Similarity 0.50–0.85** (with AI client): Asks LLM whether to merge or keep separate
- **Similarity < 0.50**: Creates a new memory

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

Search memories using **hybrid scoring**: keyword matching + semantic similarity (MinHash). Each recall updates the memory's `accessed_at`, protecting it from compaction.

**Parameters:**

- `query` (str, optional): Keyword search against memory content. Empty returns memories ranked by recency and importance
- `limit` (int, optional): Maximum results (default: `10`, `-1` for unlimited)
- `type` (str, optional): Filter by type

**Returns:** list of memory dicts, ranked by relevance

**Scoring formula:**
```
score = keyword_hits×0.3 + semantic_similarity×0.3 + importance×0.2 + recency×0.2
```

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

### count()

Returns the total number of stored memories.

```python
print(f"Stored memories: {mem.count()}")
```

### compact()

Manually trigger compaction. Returns a dict with `removed` and `remaining` counts.

```python
result = mem.compact()
print(f"Removed {result['removed']}, {result['remaining']} remaining")
```

## Memory Types

| Type | Decay behaviour | Use for |
|------|----------------|---------|
| `preference` | **Never decays** | User preferences — themes, formats, styles |
| `fact` | Half-life 90 days | Objective information — names, IDs, limits |
| `event` | Half-life 30 days | Things that happened — deployments, meetings |
| `note` | Half-life 7 days | Agent's own notes (default) |

`preference` memories are the only type that never decay regardless of importance. They are only removed after the 180-day hard age cap (based on last access).

## Deduplication

### Pre-flight Check

When `remember()` is called, the store checks for similar existing memories of the same type using **MinHash similarity** (estimated Jaccard similarity):

1. **Similarity ≥ 0.85**: Auto-merge — updates existing memory content
2. **Similarity 0.50–0.85** (with AI client): LLM decides whether to merge or keep separate
3. **Similarity < 0.50**: Creates new memory

This prevents duplicate memories from accumulating while allowing the LLM to make nuanced decisions about borderline cases.

### During Compaction

If an AI client is configured, `compact()` also runs pairwise similarity deduplication across all memories. Similar pairs with scores in the ambiguous range (0.50–0.85) are sent to the LLM for merge/keep decisions.

## Compaction

Compaction is **manual only** — call `compact()` when appropriate (e.g., on a schedule, during idle time, or after bulk imports). It performs two phases:

**Phase 1 — Prune:** Removes memories based on:
- Hard age cap: 180 days since last access
- Importance decay: `effective_importance = importance × 0.5^(age / half_life)`
  - Pruned when effective importance drops below 0.1

**Phase 2 — Deduplicate** (if AI client configured):
- Finds similar memory pairs using MinHash
- Sends ambiguous pairs to LLM for merge/keep decisions

### Decay Examples

| Memory | Importance | Age | Effective | Pruned? |
|--------|-----------|-----|-----------|---------|
| preference | 0.9 | 60 days | 0.9 (no decay) | No |
| fact | 0.9 | 90 days | 0.45 | No |
| fact | 0.9 | 270 days | 0.11 | No (but near threshold) |
| note | 0.8 | 21 days | 0.1 | Yes (at threshold) |
| event | 0.5 | 30 days | 0.25 | No |

## MinHash Similarity

The store uses **MinHash signatures** (64 hash values, 256 bytes per memory) for fast similarity estimation:

- **Pre-flight deduplication**: ~15ns per comparison
- **Hybrid search**: combines keyword hits with semantic similarity
- **Automatic recomputation**: Memories loaded from legacy databases without MinHash have it computed on first access

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

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SCRIPTLING_MEMORY_DB` | Path to the memory KV store directory | `./memory-db` |
| `SCRIPTLING_AI_BASE_URL` | Base URL of the AI provider for LLM deduplication | (disabled) |
| `SCRIPTLING_AI_PROVIDER` | Provider type: `openai`, `claude`, `gemini`, `ollama`, `zai`, `mistral` | `openai` |
| `SCRIPTLING_AI_MODEL` | Model name for LLM deduplication | (disabled) |
| `SCRIPTLING_AI_TOKEN` | API key / bearer token for the AI provider | (empty) |

LLM-based deduplication is enabled when both `SCRIPTLING_AI_BASE_URL` and `SCRIPTLING_AI_MODEL` are set.

```bash
# Basic (rule-based deduplication only)
SCRIPTLING_MEMORY_DB=~/.scriptling/memory \
  ./bin/scriptling --server :8000 --mcp-tools ./examples/mcp-tools/memory-tools

# With LLM deduplication
SCRIPTLING_MEMORY_DB=~/.scriptling/memory \
SCRIPTLING_AI_BASE_URL=http://127.0.0.1:1234/v1 \
SCRIPTLING_AI_MODEL=qwen3-8b \
  ./bin/scriptling --server :8000 --mcp-tools ./examples/mcp-tools/memory-tools
```

### Available Tools

| Tool | Description |
|------|-------------|
| `remember` | Store information with optional type and importance |
| `recall` | Hybrid keyword + semantic search, or no args for full context load |
| `forget` | Remove a memory by ID |
| `compact` | Manually trigger compaction |

## See Also

- [runtime.kv](../runtime-kv/) — KV store backing the memory system
- [ai.agent](../agent/) — Agent with automatic memory integration
- [Memory MCP Tools Example](https://github.com/paularlott/scriptling/tree/main/examples/mcp-tools/memory-tools)
