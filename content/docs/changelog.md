---
title: Changelog
description: Scriptling release history.
tags: [docs, changelog]
layout: changelog
nav-skip: true
---

## October 2026

{{< version "v0.29.0" >}}

{{< changelog-item "breaking" >}}
- Evaluate parameter defaults once, at definition, as Python does. A mutable default is now shared between calls.
- Pass `*args` as a tuple instead of a list. Code that modifies `args` must copy it first with `list(args)`.
- Keep every `;`-separated statement of a one-line block inside that block. `def f(): return 1; f()` no longer calls `f`; put the call on its own line.
- Raise `OverflowError` when integer arithmetic passes 64 bits, instead of wrapping.
- Change `json.dumps()` output to Python's format: keys in insertion order (was sorted), `", "` and `": "` separators (was compact), non-ASCII escaped. Use `sort_keys=True`, `separators=(",", ":")` and `ensure_ascii=False` for the old shape. ([docs](/reference/libraries/data-formats/json/))
- Return `UUID` objects from the `uuid` functions instead of strings. Use `str(u)` for the text form.
- Return `bytes` from the `base64` encoders instead of a string.
- Return a `timedelta` from `datetime` and `date` subtraction (was a number), and return a struct from `time.gmtime()` and `time.localtime()` with Python's weekday numbering (Monday is 0).
- Follow `posixpath` in `os.path.dirname()`, `basename()` and `splitext()` for empty paths, trailing slashes and dotfiles.
- Uppercase `ß` as `SS` in `str.upper()`.
- Remove subclassing of `defaultdict`: it is now a function that returns a dict.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
- Iterate dicts in insertion order (was unspecified), including `json.loads()`, `requests` `.json()`, `Counter`, `popitem()` and copies. Dicts built from YAML, TOML, MessagePack and plugin results have sorted keys. ([docs](/reference/types/#dictionary))
- Make dict-building code 10-30% slower than v0.28.0 in return for ordering. Lookups, `get()` and counting are unchanged.
- Deliver `**kwargs` in alphabetical order (was random per call). Call-site order is not kept.
- Rewrite `defaultdict` as an ordinary dict with a default factory: every dict method works, lambda and function factories work, keys keep their types, and it is about twice as fast. ([docs](/reference/libraries/collections-iteration/collections/#defaultdictdefault_factory))
- Make named tuples behave like tuples: indexing, slicing, `len()`, unpacking, ordering, hashing, immutability, keyword construction and `defaults=`.
- Raise catchable Python exceptions: `TypeError` for unhashable keys, unorderable sorts and wrong argument counts, `KeyError` and `IndexError` from `pop()`, the `FileNotFoundError` and `OSError` family from file operations, and Python's types from `assert`, `str.index`, `set.remove` and `min()` of an empty sequence.
- Hash plain instances by identity, and raise `AttributeError` when assigning to a property without a setter.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
- Add generators: `yield` in a function makes a lazy generator that `for`, `list()`, `next()` and `itertools` consume. `yield from` and `send()` are not supported. ([docs](/reference/functions/))
- Add `@dataclass`, `enum.Enum` and `IntEnum`, `functools.lru_cache`, `cache` and `wraps`, user exception classes, and `from typing import ...`.
- Add `obj.__dict__`, a view of an instance's attributes whose writes go through to the object, and make `vars(obj)` the same view. ([docs](/reference/classes/#instance-attributes-as-a-dict-__dict__))
- Add `OrderedDict.move_to_end()` and `popitem(last=False)`, and accept dicts and dict views in `reversed()`.
- Add unpacking forms: `(*a, *b)`, `x = *t, 1`, starred targets in nested groups and `for` headers, `{**d}`, and `f(**d)`. ([docs](/reference/syntax/#assignment))
- Add `/` positional-only parameters, `raise X from e`, `.5` and `1.` float literals, nested and chained assignment targets, and `frozenset`.
- Add `copy.deepcopy()`, `sentinel()`, `csv.DictReader` and `DictWriter`, `math.fsum`, `time.monotonic`, `os.getpid`, number methods such as `bit_count()` and `to_bytes()`, and `int()`, `float()` and `str()` without arguments.
- Add `client.decide()` for Ollama System One decision models. ([docs](/reference/libraries/ai/client/#clientdecidemodel-state-questions-images-keep_alive))
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
- Fix a subclass's class attribute being discarded when a base class defines the same name.
- Fix arguments written after a `*` unpack being passed before it.
- Fix keyword-only parameters with defaults being unbound when not passed, and a keyword named like a positional-only parameter being rejected when the function takes `**kwargs`.
- Fix `itertools` materialising infinite generators.
- Fix `super().__init__()` failing when no base class defines `__init__`.
- Fix `int(True)`, `float(False)` and `sum()` of booleans, `%g` precision, and UUID comparison and hashing.
{{< /changelog-item >}}

---

{{< version "v0.28.0" >}}

{{< changelog-item "changed" >}}
**Python 3 behaviour.** Objects, modules, printing and formatting now behave as Python 3 does, with Python's error messages, `__getattr__` and `__format__` support, and `getattr()`/`hasattr()` working exactly like dot access. `pathlib.Path` supports `/`. See [Python Differences](/reference/python-differences/).
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Faster imports.** Library files are cached across interpreter instances, so hosts that create an instance per request import 50–77% faster. Edited files are picked up on the next import. See [Loader Chain](/docs/go-integration/loader-chain/#filesystemloader).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Methods as values.** `sorted(words, key=str.lower)`, `map(str.strip, lines)` and `add = items.append` work, and `dir([])` lists methods. See [Built-in Functions](/reference/builtins/#methods-as-values).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Extractive text shortening.** `similarity.extract(text, max_chars=, max_sentences=, ratio=)` keeps the most informative sentences of a long text, in order, using TextRank over hashed word vectors (CPU-only, parallel), and de-duplicates repetitive logs instead of ranking them; `similarity.sentences(text)` is the splitter behind it. Use it where a long text would otherwise be cut at a fixed length before going to a model. See [scriptling.similarity](/reference/libraries/utilities/similarity/#extracttext-max_charsnone-max_sentencesnone-rationone).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Gossip streams.** `cluster.open_stream()` requests a reply of any size from one node and `cluster.handle_stream()` serves it, for files and state transfers beyond the packet limit. Closing a stream, or stopping its cluster, ends a read in progress. See [scriptling.net.gossip](/reference/libraries/networking/gossip/#clusteropen_streamnode_id-message_type-data).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Import syntax.** Parenthesized lists (`from m import (a, b,)`) and PEP 810 `lazy import` are accepted; `lazy` imports run immediately. See [Imports](/reference/syntax/#imports).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**F-strings** with slices (`f"{items[1:3]}"`), `!=`, lambdas or braces inside string literals now evaluate correctly.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**`html.escape(s, quote=True)`** gains Python's `quote` argument and escapes a single quote as `&#x27;` (previously `&#39;`), matching CPython.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`similarity.sentences()` and `similarity.tokenize()`** return an empty list for blank text instead of `None`, so the result can always be iterated or measured with `len()`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Standard library matches Python.** `Counter` has the full dict API; keyword arguments such as `re` `flags=`, `int(..., base=)`, `itertools.groupby(key=)`, `random.choices(cum_weights=)` and the `textwrap` options are honoured; bounded `deque`s drop from the opposite end; `json.dumps` writes tuples as arrays; `enumerate()` and `zip()` stop on infinite iterators; `isinstance()` accepts exception types; `dict()` accepts mappings and lets keywords win; TOON integers decode as `int`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**`format()`** applies zero padding, fill, sign and grouping like f-strings: `format(42, "05d")` is `"00042"`. Unknown format codes raise `ValueError`, and `#` (`0xff`), `_` grouping, `c` and `n` are supported.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Iterators, comparisons and errors.** `map()`, `filter()`, `any()` and `all()` pull from iterators lazily, so they work with `itertools.count()`, and collecting an endless iterator raises an error instead of exhausting memory. `!=` falls back to `__eq__`; `key=` accepts bound methods and callable objects; `zip(strict=True)` works; `except` accepts a variable or tuple of types and the `LookupError`, `ArithmeticError` and `BaseException` parents; `Counter` takes float counts and compares like Python; `textwrap` splits words exactly as CPython does; `random.sample(range(10**9), k)` no longer expands the range. `itertools.islice()` accepts `None` bounds (`islice(it, 2, None)`) and stops at the right element when given a step. See [Built-in Functions](/reference/builtins/#iteration-utilities) and [Error Handling](/reference/error-handling/#exception-type-hierarchy).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Gossip HTTP transport.** `transport="http"` nodes now serve the gossip endpoint on `bind_addr`; before, they could send but never receive, so HTTP clusters could not form. `encryption_key` is rejected with this transport (use HTTPS), and a node bound to all interfaces needs `advertise_addr`.
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Apple containers** work with container CLI 1.1 and later (tested on 1.5): image pulls, image and volume listing, container status and image removal. See [scriptling.container](/reference/libraries/utilities/container/).
{{< /changelog-item >}}

{{< changelog-item "fixed" >}}
**Concurrency.** A data race when starting `runtime.background()` tasks is fixed, and a server no longer loses its setup script's error when an earlier server in the same process is still shutting down.
{{< /changelog-item >}}

---

{{< version "v0.27.3" >}}

{{< changelog-item "fixed" >}}
**Pipeline concurrency recovers after a rate limit.** `client.Pipeline`, `completion_parallel` and `ask_parallel` halve their concurrency when a request hits a 429, but never restored it, so one early rate limit left a long run at reduced parallelism to the end. Concurrency now grows back by one after each run of clean completions, up to `max_parallel`, and slot accounting stays exact while the limit changes. See [AI Client](/reference/libraries/ai/client/).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Hosts can cap script fan-out.** `ai.SetMaxParallelLimit(n)` caps the `max_parallel` a script may request from `client.Pipeline`, `completion_parallel` and `ask_parallel`, and `extlibs.SetRequestsMaxParallelLimit(n)` does the same for `requests.parallel`. A script asking for more silently gets the cap; 0 removes it. One atomic load when the pipeline or batch is created, nothing per request. See [Go Integration Basics](/docs/go-integration/basics/#script-resource-limits).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Backslash line continuation.** A backslash at the end of a line joins it to the next, as in Python, so a long condition or assignment can be split without wrapping it in parentheses. The continuation line's indentation is ignored. See [Syntax](/reference/syntax/#explicit-line-continuation).
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Process-wide memory guard for script hosts.** `scriptling.SetMemoryLimit(bytes)` sets a ceiling on heap memory held by objects. While the heap stays above it after a garbage collection, the most recently started script is cancelled and its evaluation returns a `memory limit exceeded` error; `scriptling.GetMemoryLimitStats()` reports the heap, running scripts and cancellations. The guard samples the heap on a timer, so it adds no per-instruction cost to scripts. See [Go Integration Basics](/docs/go-integration/basics/#script-resource-limits).
{{< /changelog-item >}}

---

{{< version "v0.27.2" >}}

{{< changelog-item "changed" >}}
**Performance.** Script execution is 15% to 30% faster depending on workload and calls into scripts are up to 20x faster.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Comprehensions are about twice as fast.** List, dict and set comprehensions bind their variable through a slot and iterate `range()` directly.
{{< /changelog-item >}}

{{< changelog-item "changed" >}}
**Function bodies compile on first call.** A module that defines many functions now retains compiled code only for the ones that run, reducing memory for library-heavy hosts.
{{< /changelog-item >}}

{{< changelog-item "added" >}}
**Program cache budget is configurable.** Parsed and compiled scripts are kept in a process-wide cache bounded by 64 MiB by default. The CLI gains `--program-cache-max-bytes` (`SCRIPTLING_PROGRAM_CACHE_MAX_BYTES`, `cache.program_max_bytes` in `scriptling.toml`), and Go hosts get `scriptling.SetProgramCacheMaxBytes` plus `scriptling.GetProgramCacheStats` for hit, miss and eviction counts. See [Command-Line Options](/docs/cli/command-line-options/) and [Go Integration Basics](/docs/go-integration/basics/#program-cache).
{{< /changelog-item >}}
