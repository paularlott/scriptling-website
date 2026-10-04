---
description: Scriptling release history.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/changelog/
sources:
    - resource: https://scriptling.dev/docs/changelog/
status: stable
tags:
    - docs
    - changelog
title: Changelog
type: Guide
---
# Changelog

## October 2026

### v0.28.1



**`sentinel()` marker values.** `MISSING = sentinel("MISSING")` creates a unique value, equal only to itself, for "not supplied" defaults that `None` cannot express (PEP 661, Python 3.15). See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md#sentinel).


---

### v0.28.0



**Python 3 behaviour.** Objects, modules, printing and formatting now behave as Python 3 does, with Python's error messages, `__getattr__` and `__format__` support, and `getattr()`/`hasattr()` working exactly like dot access. `pathlib.Path` supports `/`. See [Python Differences](https://scriptling.dev/okf/scriptling-reference/python-differences.md).



**Faster imports.** Library files are cached across interpreter instances, so hosts that create an instance per request import 50–77% faster. Edited files are picked up on the next import. See [Loader Chain](https://scriptling.dev/okf/scriptling-docs/go-integration/loader-chain.md#filesystemloader).



**Methods as values.** `sorted(words, key=str.lower)`, `map(str.strip, lines)` and `add = items.append` work, and `dir([])` lists methods. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md#methods-as-values).



**Extractive text shortening.** `similarity.extract(text, max_chars=, max_sentences=, ratio=)` keeps the most informative sentences of a long text, in order, using TextRank over hashed word vectors (CPU-only, parallel), and de-duplicates repetitive logs instead of ranking them; `similarity.sentences(text)` is the splitter behind it. Use it where a long text would otherwise be cut at a fixed length before going to a model. See [scriptling.similarity](https://scriptling.dev/okf/scriptling-libraries/utilities/similarity.md#extracttext-max_charsnone-max_sentencesnone-rationone).



**Gossip streams.** `cluster.open_stream()` requests a reply of any size from one node and `cluster.handle_stream()` serves it, for files and state transfers beyond the packet limit. Closing a stream, or stopping its cluster, ends a read in progress. See [scriptling.net.gossip](https://scriptling.dev/okf/scriptling-libraries/networking/gossip.md#clusteropen_streamnode_id-message_type-data).



**Import syntax.** Parenthesized lists (`from m import (a, b,)`) and PEP 810 `lazy import` are accepted; `lazy` imports run immediately. See [Imports](https://scriptling.dev/okf/scriptling-reference/syntax.md#imports).



**F-strings** with slices (`f"{items[1:3]}"`), `!=`, lambdas or braces inside string literals now evaluate correctly.



**`html.escape(s, quote=True)`** gains Python's `quote` argument and escapes a single quote as `&#x27;` (previously `&#39;`), matching CPython.



**`similarity.sentences()` and `similarity.tokenize()`** return an empty list for blank text instead of `None`, so the result can always be iterated or measured with `len()`.



**Standard library matches Python.** `Counter` has the full dict API; keyword arguments such as `re` `flags=`, `int(..., base=)`, `itertools.groupby(key=)`, `random.choices(cum_weights=)` and the `textwrap` options are honoured; bounded `deque`s drop from the opposite end; `json.dumps` writes tuples as arrays; `enumerate()` and `zip()` stop on infinite iterators; `isinstance()` accepts exception types; `dict()` accepts mappings and lets keywords win; TOON integers decode as `int`.



**`format()`** applies zero padding, fill, sign and grouping like f-strings: `format(42, "05d")` is `"00042"`. Unknown format codes raise `ValueError`, and `#` (`0xff`), `_` grouping, `c` and `n` are supported.



**Iterators, comparisons and errors.** `map()`, `filter()`, `any()` and `all()` pull from iterators lazily, so they work with `itertools.count()`, and collecting an endless iterator raises an error instead of exhausting memory. `!=` falls back to `__eq__`; `key=` accepts bound methods and callable objects; `zip(strict=True)` works, and `zip()` of two dict views is a `TypeError` since dict order is unspecified (use `d.items()`); `except` accepts a variable or tuple of types and the `LookupError`, `ArithmeticError` and `BaseException` parents; `Counter` takes float counts and compares like Python; `textwrap` splits words exactly as CPython does; `random.sample(range(10**9), k)` no longer expands the range. `itertools.islice()` accepts `None` bounds (`islice(it, 2, None)`) and stops at the right element when given a step. See [Built-in Functions](https://scriptling.dev/okf/scriptling-reference/builtins.md#iteration-utilities) and [Error Handling](https://scriptling.dev/okf/scriptling-reference/error-handling.md#exception-type-hierarchy).



**Gossip HTTP transport.** `transport="http"` nodes now serve the gossip endpoint on `bind_addr`; before, they could send but never receive, so HTTP clusters could not form. `encryption_key` is rejected with this transport (use HTTPS), and a node bound to all interfaces needs `advertise_addr`.



**Apple containers** work with container CLI 1.1 and later (tested on 1.5): image pulls, image and volume listing, container status and image removal. See [scriptling.container](https://scriptling.dev/okf/scriptling-libraries/utilities/container.md).



**Concurrency.** A data race when starting `runtime.background()` tasks is fixed, and a server no longer loses its setup script's error when an earlier server in the same process is still shutting down.


---

### v0.27.3



**Pipeline concurrency recovers after a rate limit.** `client.Pipeline`, `completion_parallel` and `ask_parallel` halve their concurrency when a request hits a 429, but never restored it, so one early rate limit left a long run at reduced parallelism to the end. Concurrency now grows back by one after each run of clean completions, up to `max_parallel`, and slot accounting stays exact while the limit changes. See [AI Client](https://scriptling.dev/okf/scriptling-libraries/ai/client.md).



**Hosts can cap script fan-out.** `ai.SetMaxParallelLimit(n)` caps the `max_parallel` a script may request from `client.Pipeline`, `completion_parallel` and `ask_parallel`, and `extlibs.SetRequestsMaxParallelLimit(n)` does the same for `requests.parallel`. A script asking for more silently gets the cap; 0 removes it. One atomic load when the pipeline or batch is created, nothing per request. See [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#script-resource-limits).



**Backslash line continuation.** A backslash at the end of a line joins it to the next, as in Python, so a long condition or assignment can be split without wrapping it in parentheses. The continuation line's indentation is ignored. See [Syntax](https://scriptling.dev/okf/scriptling-reference/syntax.md#explicit-line-continuation).



**Process-wide memory guard for script hosts.** `scriptling.SetMemoryLimit(bytes)` sets a ceiling on heap memory held by objects. While the heap stays above it after a garbage collection, the most recently started script is cancelled and its evaluation returns a `memory limit exceeded` error; `scriptling.GetMemoryLimitStats()` reports the heap, running scripts and cancellations. The guard samples the heap on a timer, so it adds no per-instruction cost to scripts. See [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#script-resource-limits).


---

### v0.27.2



**Performance.** Script execution is 15% to 30% faster depending on workload and calls into scripts are up to 20x faster.



**Comprehensions are about twice as fast.** List, dict and set comprehensions bind their variable through a slot and iterate `range()` directly.



**Function bodies compile on first call.** A module that defines many functions now retains compiled code only for the ones that run, reducing memory for library-heavy hosts.



**Program cache budget is configurable.** Parsed and compiled scripts are kept in a process-wide cache bounded by 64 MiB by default. The CLI gains `--program-cache-max-bytes` (`SCRIPTLING_PROGRAM_CACHE_MAX_BYTES`, `cache.program_max_bytes` in `scriptling.toml`), and Go hosts get `scriptling.SetProgramCacheMaxBytes` plus `scriptling.GetProgramCacheStats` for hit, miss and eviction counts. See [Command-Line Options](https://scriptling.dev/okf/scriptling-docs/cli/command-line-options.md) and [Go Integration Basics](https://scriptling.dev/okf/scriptling-docs/go-integration/basics.md#program-cache).
