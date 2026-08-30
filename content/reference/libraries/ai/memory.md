---
title: scriptling.ai.memory
linkTitle: ai.memory
description: Long-term, deduplicated memory store for AI agents backed by a KV store.
tags: [libraries, ai, agents]
weight: 4

aliases:
  - /reference/libraries/scriptling/ai/memory/
---

Long-term memory store for AI agents. Backed by a KV store, memories persist across sessions and are automatically deduplicated using MinHash similarity. Pruning of old/decayed memories runs automatically in the background after every `remember()` call; full compaction (including LLM deduplication) can be triggered manually via `compact()`.

## Available Functions

| Function | Description |
|----------|-------------|
| `memory.new(kv_store, ai_client=None, model="")` | Create a memory store |

## Memory Object Methods

| Method | Description |
|--------|-------------|
| `remember(content, type, importance)` | Store a memory; returns a dict with `id` |
| `recall(query, limit, type)` | Search memories by keyword and semantic similarity; `limit=-1` for all |
| `forget(id)` | Remove a memory by ID |
| `count()` | Total number of memories |
| `compact()` | Run full compaction (prune + LLM deduplication if AI client configured); returns dict with `removed` and `remaining` counts |

## Functions

### `memory.new(kv_store, ai_client=None, model="")`

Creates a memory store backed by the given KV store.

**Parameters:**

- `kv_store`: A KV store object (`kv.default` or `kv.open(...)`).
- `ai_client` (`AIClient`, optional): AI client for resolving ambiguous duplicates during `remember()`: see [Deduplication](#deduplication). Default: `None`.
- `model` (`str`, optional): Model name for LLM resolution (required if `ai_client` is provided). Default: `""`.

**Returns:** Memory store object with `remember()`, `recall()`, `forget()`, `count()`, and `compact()` methods.

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

### `remember(content, type="note", importance=0.5)`

Stores a memory. Before saving, performs a pre-flight similarity check against existing memories of the same type:

- **Similarity ≥ 0.85**: Updates the existing memory in place (no new entry).
- **Similarity 0.50 to 0.85** (with AI client): Asks the LLM whether to merge or keep separate.
- **Similarity < 0.50**: Creates a new memory.

**Parameters:**

- `content` (`str`): What to remember.
- `type` (`str`, optional): `"fact"`, `"preference"`, `"event"`, or `"note"`. Default: `"note"`.
- `importance` (`float`, optional): `0.0` to `1.0`: controls how long the memory survives compaction. Default: `0.5`.

**Returns:** `dict`: with `id`, `content`, `type`, `importance`, `created_at`, `accessed_at`.

```python
result = mem.remember("User's name is Alice", type="fact", importance=0.9)
print(result["id"])  # UUIDv7: use this to forget the memory later

mem.remember("User prefers dark mode", type="preference", importance=0.7)
mem.remember("Check API rate limits before next run")
```

### `recall(query="", limit=10, type="")`

Searches memories using **hybrid scoring**: keyword matching + semantic similarity (MinHash). Each recall updates the memory's `accessed_at`, protecting it from compaction.

When called with no `query` and no `type` filter, `recall()` enters **context load mode**: it returns all `preference` memories (unlimited) plus the top `limit` non-preference memories, deduplicated by ID. This is the recommended way to prime an agent's context at the start of a session.

**Parameters:**

- `query` (`str`, optional): Keyword search against memory content. An empty string with no `type` triggers context load mode. Default: `""`.
- `limit` (`int`, optional): Maximum results. `-1` for unlimited. In context load mode, applies only to non-preference memories. Default: `10`.
- `type` (`str`, optional): Filter by type. Use `!xxx` to exclude a type (e.g. `!preference`). Setting this disables context load mode. Default: `""`.

**Returns:** `list`: memory dicts, ranked by relevance.

**Scoring formula (when querying):**

```
score = keyword_hits×0.3 + semantic_similarity×0.3 + importance×0.2 + recency×0.2
```

```python
# Context load: all preferences + top 10 non-preferences (recommended for session start)
memories = mem.recall()

# Keyword search
results = mem.recall("user name", limit=1)
if results:
    print("User is", results[0]["content"])

# All preferences
prefs = mem.recall(type="preference", limit=-1)

# Facts only
facts = mem.recall("Alice", type="fact")
```

### `forget(id)`

Removes a memory by ID.

**Parameters:**

- `id` (`str`): Memory ID returned by `remember()`.

**Returns:** `bool`: `True` if a memory was removed.

```python
result = mem.remember("User's name is Alice", type="fact", importance=0.9)
mem.forget(result["id"])
```

### `count()`

Returns the total number of stored memories.

**Returns:** `int`

```python
print(f"Stored memories: {mem.count()}")
```

### `compact()`

Manually triggers full compaction (prune + LLM deduplication). Pruning alone runs automatically in the background after every `remember()`: call `compact()` when you also want LLM-based deduplication.

**Returns:** `dict`: with `removed` and `remaining` counts.

```python
result = mem.compact()
print(f"Removed {result['removed']}, {result['remaining']} remaining")
```

## Memory Types

| Type | Decay behaviour | Use for |
|------|----------------|---------|
| `preference` | **Never decays** | User preferences: themes, formats, styles |
| `fact` | Half-life 90 days | Objective information: names, IDs, limits |
| `event` | Half-life 30 days | Things that happened: deployments, meetings |
| `note` | Half-life 7 days | Agent's own notes (default) |

`preference` memories are the only type that never decay regardless of importance. They are only removed after the 180-day hard age cap (based on last access).

## Deduplication

### Pre-flight Check

When `remember()` is called, the store checks for similar existing memories of the same type using **MinHash similarity** (estimated Jaccard similarity):

1. **Similarity ≥ 0.85**: Auto-merge: updates existing memory content.
2. **Similarity 0.50 to 0.85** (with AI client): LLM decides whether to merge or keep separate.
3. **Similarity < 0.50**: Creates new memory.

This prevents duplicate memories from accumulating while allowing the LLM to make nuanced decisions about borderline cases.

### During Compaction

If an AI client is configured, `compact()` also runs pairwise similarity deduplication across all memories. Similar pairs with scores in the ambiguous range (0.50 to 0.85) are sent to the LLM for merge/keep decisions.

## Compaction

Pruning runs **automatically in the background** after every `remember()` call. A single background goroutine (started when the store is created) waits for a signal, runs `prune()`, then goes back to sleep. The signal channel is buffered at size 1, so if a prune is already queued or running, subsequent `remember()` calls simply skip the signal: no blocking, no overlapping runs.

Automatic pruning only runs **Phase 1** (age cap + decay). It never calls the LLM.

Call `compact()` manually when you also want **Phase 2** (LLM deduplication), for example after a bulk import or on a maintenance schedule.

**Phase 1: Prune** (automatic after every `remember()`):

- Hard age cap: 180 days since last access.
- Importance decay: `effective_importance = importance × 0.5^(age / half_life)`.
  - Pruned when effective importance drops below 0.1.

**Phase 2: Deduplicate** (manual `compact()` only, requires AI client):

- Finds similar memory pairs using MinHash.
- Sends ambiguous pairs to the LLM for merge/keep decisions.

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

- **Pre-flight deduplication**: ~15ns per comparison.
- **Hybrid search**: combines keyword hits with semantic similarity.
- **Automatic recomputation**: Memories loaded from legacy databases without MinHash have it computed on first access.

## Agent Integration

The simplest way to give an agent memory is to pass `memory=` to `Agent()`. The agent wires up the tools and augments the system prompt automatically: see [scriptling.ai.agent Memory Integration](../agent/#memory-integration).

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
| `recall` | Keyword + semantic search; no args triggers context load (all preferences + top N others) |
| `forget` | Remove a memory by ID |
| `compact` | Manually trigger compaction |

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#extended-libraries).

`scriptling.ai.memory` has no network access by itself: it stores conversation history and other memories in the KV store the embedder provides (in-memory or persistent), and only talks to an AI provider if you explicitly pass an `ai_client` for LLM-based deduplication. Risk is low; see the [Security Guide](/docs/security/#library-security) for the general model.

## See Also

- [scriptling.runtime.kv](../../runtime/kv/): KV store backing the memory system
- [scriptling.ai.agent](../agent/): Agent with automatic memory integration
- [Memory MCP Tools Example](https://github.com/paularlott/scriptling/tree/main/examples/mcp-tools/memory-tools)
