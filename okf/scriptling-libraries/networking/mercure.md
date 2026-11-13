---
description: Mercure hub client - publish updates to topics and subscribe to them over Server-Sent Events.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/reference/libraries/networking/mercure/
sources:
    - resource: https://scriptling.dev/reference/libraries/networking/mercure/
status: stable
tags:
    - libraries
    - networking
title: scriptling.mercure
type: API Reference
---
# scriptling.mercure

The `scriptling.mercure` library is a client for [Mercure](https://mercure.rocks) hubs: a script publishes updates
to topics and subscribes to them over Server-Sent Events. It works with any Mercure hub, the official one,
FrankenPHP's built-in hub, or a [gossiper](https://github.com/paularlott/gossiper) cluster.

It speaks Mercure 1.0 by default: access tokens bound to the hub, and subscriptions by exact topic or URL pattern,
which current hubs take. Draft-07, for hubs that take only that, is one argument away (see
[Draft-07 hubs](#draft-07-hubs)).

- **Publishing** is a POST per update by default, as Mercure's HTTP protocol has it, which every hub takes. With
  `stream=True` a client publishes to a gossiper hub over one long streaming request instead, many times faster
  for a script that publishes a lot.
- **Subscriptions** reconnect by themselves after a lost connection or a hub restart, and resume from their last
  event ID, so nothing the hub kept is missed.
- **Tokens** never run out under a client given the hub's key (`key=`): it makes its own and renews each before
  it expires, so subscriptions and publish streams last as long as the script does. See [Tokens](#tokens).

## Available Functions

| Function | Description |
|----------|-------------|
| `Client(url, **kwargs)` | A client of a Mercure hub |
| `create_token(key, audience, **kwargs)` | A Mercure JWT signed with a hub's HMAC key |

`Client()` returns a `Client`:

| Method/Property | Description |
|-----------------|-------------|
| `publish(topic, data=None, **kwargs)` | Publish an update and return its event ID |
| `publish_many(updates)` | Publish several updates and return their event IDs, in order |
| `subscribe(*topics, **kwargs)` | Subscribe to topics |
| `set_token(token)` | Replace the token of a client made with `token=` |
| `close()` | Close the client and its subscriptions |
| `url` | `str` property: the hub's URL |
| `transport` | `str` property: how the client publishes now, `"http"` or `"stream"` |
| `closed` | `bool` property: whether the client has been closed |

`subscribe()` returns a `Subscription` (`receive(timeout=30)`, iteration with `for`, `close()`, `last_event_id`),
which yields `Event` objects (`id`, `type`, `data`, `retry`, `json()`, `to_dict()`). Clients and subscriptions are
context managers: a `with` block closes them at its end.

## Quick Start

```python
import os
import scriptling.mercure as mercure

URL = "https://hub.example.com/.well-known/mercure"

with mercure.Client(URL, key=os.getenv("MERCURE_JWT_KEY")) as hub:
    sub = hub.subscribe(match_urlpattern="https://example.com/books/:id")

    hub.publish("https://example.com/books/1", {"title": "Dune"}, type="book")

    event = sub.receive(timeout=10)
    print(event.id, event.type, event.json()["title"])
```

### A long-running subscriber

Iterating over a subscription waits for each event in turn, until the subscription is closed or the script is
stopped. It reconnects by itself, with a fresh token when the hub ends it as a token expires, and resumes from
its last event ID:

```python
hub = mercure.Client(URL, key=KEY, subscribe=["https://example.com/notifications"])
for event in hub.subscribe("https://example.com/notifications"):
    print(f"[{event.id}] {event.data}")
```

### Tokens

There are two ways to give a client its token.

**`key=`, the hub's key.** The client makes its own tokens and renews each once half its life (`token_ttl`, one
hour by default) is gone. A hub ends a stream as the token it was opened with expires; the client reopens it with
a fresh one. Subscriptions resume from their last event ID, and a publish stream sends again, first and in order,
what the hub had not taken, so nothing is lost or duplicated. `publish=` and `subscribe=` narrow what its tokens
allow; without them, every topic.

```python
hub = mercure.Client(URL, key=KEY)                                         # every topic
reader = mercure.Client(URL, key=KEY, subscribe=["https://example.com/inbox/alice"])
```

**`token=`, a token made elsewhere** (an OAuth server, your application). The client presents it as it is and
cannot renew it: once it expires, the hub refuses it, and a subscription ends with an error saying so. Replace it
with `set_token()` before then; every request and stream from then on uses the new one.

```python
hub = mercure.Client(URL, token=issued.access_token)   # issued: a scriptling.oauth Token
...
issued.refresh()
hub.set_token(issued.access_token)
```

`create_token()` makes a single token, to hand to another program or a browser.

### Delivery and errors

- **Subscriptions** reconnect by themselves (a dropped connection, a hub restart, a token reaching its end) and
  resume from their last event ID, so they miss nothing the hub still holds in its history. `receive()` raises
  only when the hub refuses the subscription for good.
- **A script that falls behind** fills the subscription's `buffer` (1024 events by default); the hub then drops the
  stream and the subscription resumes from its last event, again within the hub's history. Raise `buffer` for
  bursts.
- **A publish that raises** was not confirmed. A refusal (400, 401, 403) was not published. After a lost connection
  it may or may not have been, so publishing it again can deliver it twice: give it an `id`, and with gossiper
  `replicas`, which makes a publish with that ID idempotent.
- **Over a stream**, updates the hub had not taken when it ended the stream (a token expiring, the hub shutting
  down) are sent again on a new one, first and in order; nothing is lost or doubled.

### Draft-07 hubs

Hubs older than Mercure 1.0, or FrankenPHP in compatibility mode, take only draft-07: tokens with the `mercure`
claim, and topic selectors (topics, URI templates or `*`) to subscribe to. `draft07=True` makes such a token, and
`topics=` subscribes with selectors. Gossiper, Mercure 1.0 only by default like the official hub, takes both revisions in any mix with `--protocol both`.

```python
hub = mercure.Client(URL, key=KEY, draft07=True)
books = hub.subscribe(topics="https://example.com/books/{id}")
```

### Publishing many updates

`publish_many()` publishes a list of updates and returns their event IDs in order. Over a stream (gossiper,
`stream=True`) they are pipelined: sent without waiting for each answer. `stream="auto"` streams to a gossiper hub
and falls back to a POST per update with any other.

```python
with mercure.Client(URL, key=KEY, stream="auto") as hub:
    ids = hub.publish_many([
        {"topic": "https://example.com/ticks", "data": {"n": i}}
        for i in range(10000)
    ])
```

How fast a script goes, against a gossiper hub on the same machine (Apple M5 Max):

| From a script | Rate |
| --- | --- |
| `publish()`, a POST each, one at a time | about 19k/s |
| `publish()` over a stream, one at a time | about 31k/s |
| `publish_many()` over a stream | about 570k/s |
| `receive()` | about 1.3M events/s |

`publish()` waits for the hub's answer each time; `publish_many()` over a stream does not, which is where most of
the difference comes from. The scriptling layer adds 5 to 17% to what gossiper's Go client does alone.

## Functions

### `Client(url, key=None, publish=None, subscribe=None, token_ttl=3600, token=None, stream=False, verify=True, timeout=30, headers=None, host=None, h2c=False, max_event_size=8388608)`

Creates a client of a Mercure hub. It connects when first used.

**Parameters:**
- `url` (`str`): The hub's URL, e.g. `"https://example.com/.well-known/mercure"`.
- `key` (`str`, optional): The hub's JWT key. The client makes its own tokens with it and renews them (see
  [Tokens](#tokens)). Not with `token`. Default: `None`.
- `publish` (`str` or `list`, optional): With `key`, the topics its tokens may publish to. Default: every topic,
  when `subscribe` is not given either.
- `subscribe` (`str` or `list`, optional): With `key`, the topics its tokens may receive private updates of.
  Default: every topic, when `publish` is not given either.
- `token_ttl` (`float`, optional): With `key`, each token's lifetime in seconds, at least `10`; tokens are renewed
  at half their life. `0`, no expiry, only with `draft07=True`. Default: `3600`.
- `payload`, `issuer`, `audience`, `match_type`, `subject`, `client_id`, `algorithm`, `draft07`: With `key`, the
  token's other claims, as `create_token()` (below) takes them; `audience` defaults to `url`.
- `token` (`str`, optional): A token made elsewhere, presented as it is; replace it with `set_token()` before it
  expires. Not with `key`. Default: `None` (anonymous).
- `stream` (`bool` or `str`, optional): How to publish. `False`: a POST per update, which every hub takes.
  `True`: one long streaming publish to a gossiper hub. `"auto"`: a stream to a gossiper hub, a POST per update
  to any other. Default: `False`.
- `verify` (`bool` or `str`, optional): Verify the hub's TLS certificate. `False` accepts any certificate
  (development only); a path names a PEM bundle of CA certificates to trust, such as a gossiper node's
  `self-signed.crt`. Default: `True`.
- `timeout` (`float`, optional): Seconds to wait for the hub to answer a publish or accept a subscription.
  Default: `30`.
- `headers` (`dict`, optional): Headers added to every request. Default: `None`.
- `host` (`str`, optional): The host name to ask for when it is not the URL's, for a hub node reached by its
  address. Default: `None`.
- `h2c` (`bool`, optional): Speak HTTP/2 without TLS to an `http://` gossiper hub, so the publish stream and every
  subscription share one connection. Default: `False`.
- `max_event_size` (`int`, optional): The largest event a subscription takes, in bytes. A larger one ends the
  stream, which then reconnects. Default: `8388608` (8 MiB).

**Returns:** `Client`. A client of the hub.

**Raises:** `ValueError`. When both `key` and `token` are given, a token argument is given without `key`, or the
token arguments are invalid (as `create_token()` says).

```python
hub = mercure.Client("https://localhost:8080/.well-known/mercure", key=KEY,
                     verify="/etc/gossiper/tls/self-signed.crt", stream=True)
```

### `create_token(key, audience, publish=None, subscribe=None, payload=None, expires=3600, issuer="https://localhost", match_type="exact", subject=None, client_id="scriptling", algorithm="HS256", draft07=False)`

Makes one Mercure JWT signed with a hub's HMAC key, to hand to another program or a browser; a client given
`key=` makes and renews its own. By default it is a Mercure 1.0 access token (RFC 9068, `typ`
`at+jwt`, with RFC 9396 `authorization_details`) for the hub at `audience`, which current hubs take.
`draft07=True` makes a draft-07 token (the `mercure` claim) instead, for hubs that take only that.

**Parameters:**
- `key` (`str`): The hub's publisher or subscriber JWT key. Keep it out of the script: read it with
  [scriptling.secret](https://scriptling.dev/okf/scriptling-libraries/utilities/secret.md) or `os.getenv`.
- `audience` (`str`): The hub's URL, its resource identifier (the `aud` claim), by position or by name. Not given
  with `draft07=True`.
- `publish` (`str` or `list`, optional): Topics the token may publish to, e.g. `["*"]`. Default: `None`.
- `subscribe` (`str` or `list`, optional): Topics the token may receive private updates of. Default: `None`.
- `payload` (`dict`, optional): Shared with other subscribers in subscription events. Default: `None`.
- `expires` (`float`, optional): Seconds until the token expires; `0` for none, only with `draft07=True`.
  Default: `3600`.
- `issuer` (`str`, optional): The `iss` claim, an issuer the hub trusts. The official hub's image and gossiper
  trust `"https://localhost"` unless configured otherwise; set the hub's own in production.
  Default: `"https://localhost"`.
- `match_type` (`str`, optional): How `publish` and `subscribe` match topics: `"exact"` or `"urlpattern"`.
  Default: `"exact"`.
- `subject` (`str`, optional): The `sub` claim. Default: `None` (the client ID; none with `draft07=True`).
- `client_id` (`str`, optional): The `client_id` claim. Default: `"scriptling"`.
- `algorithm` (`str`, optional): `"HS256"`, `"HS384"` or `"HS512"`. Default: `"HS256"`.
- `draft07` (`bool`, optional): Make a draft-07 token: `publish` and `subscribe` are draft-07 selectors, and there
  is no audience or issuer. Default: `False`.

**Returns:** `str`. The signed token.

**Raises:** `ValueError`. When neither `publish` nor `subscribe` is given, a Mercure 1.0 token has no `audience` or
would not expire, or a draft-07 token is given Mercure 1.0 claims.

```python
subscriber = mercure.create_token(KEY, URL, subscribe=["https://example.com/inbox/alice"], expires=600)
```

### `Client.publish(topic, data=None, id=None, type=None, private=False, retry=None, replicas=0)`

Publishes an update and returns its event ID once the hub has it.

**Parameters:**
- `topic` (`str` or `list`): The update's topic, or its canonical topic followed by alternates.
- `data` (`str` or any, optional): The update's content. A `str` is sent as it is; any other value (a `dict`, a
  `list`, a number) is sent as JSON. Default: `None` (empty).
- `id` (`str`, optional): The event ID. Default: `None` (the hub makes one).
- `type` (`str`, optional): The SSE event type. Default: `None`.
- `private` (`bool`, optional): Deliver only to subscribers whose token allows the topic. Default: `False`.
- `retry` (`float`, optional): The reconnection time subscribers are given, in seconds. Default: `None`.
- `replicas` (`int`, optional): Copies a gossiper hub keeps, on as many nodes, before it answers. Other hubs ignore
  it. Default: `0`.

**Returns:** `str`. The event ID.

**Raises:** `ValueError`. When the update has no topic, or the hub refuses it as invalid (400). Any other refusal
(401 without a valid token, 403 beyond the token's grants) is an error naming the hub's status.

```python
event_id = hub.publish("https://example.com/orders/42", {"status": "shipped"}, type="order", private=True)
```

### `Client.publish_many(updates)`

Publishes several updates and returns their event IDs, in the same order. Over a stream the updates are pipelined,
in order; with a POST per update they are published one after another.

**Parameters:**
- `updates` (`list`): Dicts with the arguments of `publish()`: `topic`, `data`, `id`, `type`, `private`, `retry`,
  `replicas`.

**Returns:** `list`. The event IDs.

**Raises:** An error naming the update that failed (`publish_many: update 3: ...`); the updates before it were
published.

```python
ids = hub.publish_many([{"topic": "https://example.com/n", "data": str(i)} for i in range(100)])
```

### `Client.subscribe(*topics, match=None, match_urlpattern=None, topics=None, last_event_id=None, buffer=1024)`

Subscribes to topics and returns once the hub has accepted the subscription. From then on it reconnects by itself,
resuming from its last event ID, until it is closed.

**Parameters:**
- `*topics` (`str` or `list`): Topics to subscribe to, exactly (Mercure 1.0 `match`); `"*"` for every topic.
- `match` (`str` or `list`, optional): More exact topics, as by position. Default: `None`.
- `match_urlpattern` (`str` or `list`, optional): URL patterns (Mercure 1.0), e.g.
  `"https://example.com/books/:id"`. Default: `None`.
- `topics` (`str` or `list`, optional): Draft-07 topic selectors, for hubs that take only draft-07: topics, URI
  templates (e.g. `"https://example.com/books/{id}"`) or `"*"`. Default: `None`.
- `last_event_id` (`str`, optional): Resume after that event, or `"earliest"` for the hub's whole history.
  Default: `None`.
- `buffer` (`int`, optional): Events held for the script before the stream waits for it. Default: `1024`.

**Returns:** `Subscription`. The open subscription.

**Raises:** An error naming the hub's status when it refuses the subscription (400 for parameters of a revision it
does not take, 401, 403). `RuntimeError` when the host lets scripts publish only
([Security Considerations](#security-considerations)).

```python
sub = hub.subscribe(match_urlpattern="https://example.com/books/:id", last_event_id=saved_id)
```

A script meant for hosts of both kinds can carry on without the subscription:

```python
try:
    sub = hub.subscribe("https://example.com/news")
except RuntimeError:
    sub = None  # publish-only host: send updates, don't listen
```

### `Client.set_token(token)`

Replaces the token of a client made with `token=`. The next request, and every stream the client opens or
reopens from then on, presents it: a subscription the hub ends as its old token expires reconnects with the new
one.

**Parameters:**
- `token` (`str`): The new token.

**Returns:** `None`

**Raises:** `ValueError`. When the client was made with `key=`: it renews its own tokens.

```python
issued.refresh()
hub.set_token(issued.access_token)
```

### `Client.close()`

Closes the client, its subscriptions and its publish stream. Publishing on a closed client is an error. A client
the script does not close is closed for it when the script's interpreter is reset or done with (a pooled or
per-request interpreter, a finished background task), or once the script no longer holds it.

**Returns:** `None`

```python
hub.close()
```

### `Subscription.receive(timeout=30)`

Returns the next event, waiting up to `timeout` seconds for one.

**Parameters:**
- `timeout` (`float`, optional): Seconds to wait. `None` waits until an event comes or the subscription is closed;
  `0` takes only an event already received. Default: `30`.

**Returns:** `Event` or `None`. `None` on a timeout, or once the subscription is closed.

**Raises:** An error when the hub refused the subscription for good while reconnecting: with `token=`, its token
expired (the error says so). With `key=` that does not happen.

```python
event = sub.receive(timeout=5)
if event is not None:
    print(event.data)
```

### `Subscription.close()`

Ends the subscription. Iteration over it stops, and `receive()` returns `None`.

**Returns:** `None`

```python
sub.close()
```

### `Subscription.last_event_id`

The ID of the last event received, which the subscription resumes from should it reconnect. Save it to resume a
later subscription with `last_event_id=`.

```python
saved_id = sub.last_event_id
```

### `Event`

An event a subscription received.

- `id` (`str`): The event ID.
- `type` (`str` or `None`): The SSE event type.
- `data` (`str`): The event's data.
- `retry` (`float` or `None`): The reconnection time the hub gave, in seconds.
- `json()`: The data parsed as JSON. Raises `ValueError` when it is not JSON.
- `to_dict()`: The event as a dict: `id`, `type`, `data` and `retry`.

```python
for event in sub:
    if event.type == "book":
        print(event.json()["title"])
```

## Security Considerations

This is an extension library, requiring registration in Go, see
[Library Registration](https://scriptling.dev/okf/scriptling-docs/go-integration/library-registration.md#networking). The CLI registers it, under
`--network-policy` and `--allowed-paths`.

- Every connection to the hub goes through the network policy when one is set; `verify=False` only stops the
  certificate being checked.
- A CA bundle named with `verify="path"` must lie within `--allowed-paths`, else an uncatchable `PermissionError`.
- Requests never follow redirects: the token goes to the hub's URL and nowhere else.
- A host can let scripts publish but not receive (`mercure.WithoutSubscribe()` in Go): `subscribe()` then raises
  `RuntimeError`, which a script can catch to carry on without it, and everything else works as before.
- `key=` and `create_token()` need the hub's signing key, which can mint tokens for any topic: `publish=` and
  `subscribe=` limit what the client's own tokens allow, not what the key can do. A script that should never hold
  the key is given a token made elsewhere (`token=`), with just the topics it needs, and `set_token()` before it
  expires.
- Mercure 1.0 tokens are bound to one hub by their audience; draft-07 tokens are not, and work at any hub that
  shares the key.

## See Also

- [scriptling.net.websocket](https://scriptling.dev/okf/scriptling-libraries/networking/websocket.md): WebSocket client
- [scriptling.secret](https://scriptling.dev/okf/scriptling-libraries/utilities/secret.md): Reading keys and tokens
- [Mercure](https://mercure.rocks): The protocol and the official hub
