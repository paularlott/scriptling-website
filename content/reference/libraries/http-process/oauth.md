---
title: scriptling.oauth
linkTitle: oauth
description: OAuth 2.0 and OpenID Connect - device sign-in, client credentials, refresh tokens and access token verification.
tags: [libraries, http, security]
weight: 2
---

The `scriptling.oauth` library signs scripts in to an identity provider (IdP) with OAuth 2.0 and OpenID Connect,
and checks the tokens sent to APIs scripts serve. It works with any IdP that publishes discovery metadata (OpenID
Connect discovery or RFC 8414) and uses Go's standard library only.

- **Device sign-in** (RFC 8628): the person opens a link on any device, enters a code and approves. A CLI script
  waits for it; a script serving web pages shows the link and checks on each reload. No browser is ever opened.
- **Client credentials**: a token for the script itself, with no person.
- **Tokens** refresh themselves, give `requests` their `Authorization` header, and convert to and from a dict so
  a script can keep them between runs if it chooses to.
- **Verification**: a script serving an API checks the access tokens sent to it.

Python has no OAuth library in its standard library, so this one is Scriptling's own; tokens use the dict shape
Python's OAuth libraries use (`access_token`, `token_type`, `expires_at`, `expires_in`, `refresh_token`, `scope`).

## Available Functions

| Function | Description |
|----------|-------------|
| `Client(issuer, client_id, **kwargs)` | A client at an identity provider |

`Client()` returns an `OAuthClient`:

| Method | Description |
|--------|-------------|
| `device_start(**kwargs)` | Start a device sign-in |
| `device_resume(flow)` | Pick up a device sign-in from `DeviceFlow.to_dict()` |
| `client_credentials(**kwargs)` | A token for the client itself |
| `token_from_dict(token)` | A token saved with `Token.to_dict()` |
| `verify(token, audience, **kwargs)` | Check an access token sent to an API this script serves |
| `metadata()` | The IdP's discovery document |

`device_start()` returns a `DeviceFlow` (`user_code`, `verification_uri`, `verification_uri_complete`,
`expires_at`, `interval`; `poll()`, `wait()`, `to_dict()`). Tokens are `Token` objects (`access_token`,
`token_type`, `expires_at`, `refresh_token`, `scope`, `id_token`; `headers()`, `is_expired()`, `refresh()`,
`to_dict()`, `claims()`).

## Quick Start

### Signing in from the CLI

```python
import requests
import scriptling.oauth as oauth

idp = oauth.Client("https://id.example.com/o/acme", client_id="c_reports_cli")
flow = idp.device_start(scope="openid profile", resource="https://api.example.com/")
print("Open " + flow.verification_uri + " and enter " + flow.user_code)

token = flow.wait()
items = requests.get("https://api.example.com/items", headers=token.headers()).json()
```

The client is a **public** client at the IdP (no secret) with the device sign-in grant. Naming the API with
`resource` makes it the token's audience.

### Keeping the token between runs

The library keeps nothing on disk. A script that wants to skip signing in next time saves the token itself:

```python
import json
import os
import scriptling.oauth as oauth

idp = oauth.Client("https://id.example.com/o/acme", client_id="c_reports_cli")
path = os.path.join(os.getenv("HOME"), ".reports-token.json")

token = None
if os.path.exists(path):
    token = idp.token_from_dict(json.loads(os.read_file(path)))
    if token.is_expired() and token.refresh_token is None:
        token = None
if token is None:
    flow = idp.device_start(scope="openid profile offline_access", resource="https://api.example.com/")
    print("Open " + flow.verification_uri_complete)
    token = flow.wait()

os.write_file(path, json.dumps(token.to_dict()))
os.chmod(path, 0o600)
```

`token.headers()` refreshes an expiring token itself when it has a refresh token (ask for `offline_access` to get
one); save `to_dict()` again afterwards to keep the new one.

### Signing in from a web page

A script serving pages shows the link and code, keeps the flow server side, and checks it when the page reloads:

```python
import scriptling.oauth as oauth
import scriptling.runtime.kv as kv

idp = oauth.Client("https://id.example.com/o/acme", client_id="c_dashboard")
store = kv.open(":memory:sign-ins")

def sign_in_page(session_id):
    saved = store.get("flow:" + session_id)
    if saved is None:
        flow = idp.device_start(scope="openid profile", resource="https://api.example.com/")
        store.set("flow:" + session_id, flow.to_dict())
    else:
        flow = idp.device_resume(saved)
        token = flow.poll()              # None while waiting; asks the IdP no faster than it allows
        if token is not None:
            store.delete("flow:" + session_id)
            store.set("token:" + session_id, token.to_dict())
            return "Signed in."
    return "Open <a href='" + flow.verification_uri_complete + "'>this link</a> and approve, then reload."
```

### A service with no person

```python
import scriptling.oauth as oauth
import scriptling.secret as secret

svc = oauth.Client("https://id.example.com/o/acme", client_id="c_nightly", client_secret=secret.get("nightly"))
token = svc.client_credentials(scope="reports:read", resource="https://api.example.com/")
```

### Protecting an API the script serves

Middleware for `scriptling.runtime.http` (registered with `runtime.http.middleware("handlers.auth")`) that lets a
request through only with a valid access token for this API:

```python
import scriptling.oauth as oauth
import scriptling.runtime as runtime

idp = oauth.Client("https://id.example.com/o/acme", client_id="c_items_api")

def auth(request):
    bearer = (request.header("Authorization") or "").removeprefix("Bearer ")
    try:
        claims = idp.verify(bearer, "https://items.example.com/", typ="at+jwt")
    except Exception:
        return runtime.http.json(401, {"error": "invalid_token"})
    request.context["user"] = claims["sub"]
    return None
```

## Functions

### `Client(issuer, client_id, client_secret=None, verify=True, timeout=10)`

A client at an identity provider. The IdP's endpoints are read from its discovery document on first use (and
again after an hour), which must name `issuer`.

**Parameters:**
- `issuer` (`str`): The IdP's issuer URL, e.g. `"https://id.example.com/o/acme"`. https only; plain http only on
  `localhost` or a loopback address. No query or fragment.
- `client_id` (`str`): This script's client ID at the IdP.
- `client_secret` (`str`, optional): The secret of a confidential client, needed for `client_credentials()`. Read
  it with `scriptling.secret` or `os.getenv`; never write it in the script.
- `verify` (`bool` or `str`, optional): Verify the IdP's TLS certificate. Default: `True`. `False` accepts any
  certificate (a development IdP only); a path names a PEM bundle of CA certificates to trust instead of the
  system's.
- `timeout` (`float`, optional): Per-request timeout in seconds. Default: `10`.

**Returns:** `OAuthClient`.

### `OAuthClient.device_start(scope=None, resource=None)`

Starts a device sign-in.

**Parameters:**
- `scope` (`str` or `list`, optional): Scopes to ask for, e.g. `"openid profile"`.
- `resource` (`str` or `list`, optional): The API(s) the token is for (RFC 8707); they become its audience.

**Returns:** `DeviceFlow`.

### `OAuthClient.device_resume(flow)`

A `DeviceFlow` from the dict `DeviceFlow.to_dict()` gave, e.g. on a later web request.

### `OAuthClient.client_credentials(scope=None, resource=None)`

A token for the client itself, with no person. Needs `client_secret`.

**Returns:** `Token`.

### `OAuthClient.token_from_dict(token)`

A `Token` from a dict `Token.to_dict()` gave, able to refresh itself with this client.

### `OAuthClient.verify(token, audience, typ=None, leeway=60)`

Checks an access token sent to an API this script serves, and returns its claims. It checks the signature
against the issuer's published keys (fetched again, at most once a minute, when a token names a new key), that
`iss` is this client's issuer, that `aud` contains `audience`, `exp` and `nbf` within `leeway` seconds, that the
token is not bound to a key (`cnf`, which this cannot check), and its JWT type when `typ` is given (RFC 9068 access
tokens are `"at+jwt"`). ES256/384/512, RS256/384/512, PS256/384/512 and EdDSA signatures are accepted; `none` and
HMAC never are.

**Returns:** `dict`: the claims (`sub`, `scope`, `client_id`, ...). Raises on any failure; the error never contains
the token.

### `OAuthClient.metadata()`

The IdP's discovery document.

### `DeviceFlow.poll()`

Checks once whether the person approved: the `Token` once they have, `None` while waiting. It asks the IdP no
sooner than its interval allows, so an earlier call (a page reloading) returns `None` without a request, and it
slows down when the IdP says so. Raises if the sign-in was denied or the code expired.

### `DeviceFlow.wait(timeout=None)`

Waits, polling at the IdP's interval, until the person approves. Raises if the sign-in is denied, the code expires
or `timeout` seconds pass.

### `DeviceFlow.to_dict()`

The flow as a dict, for `device_resume()`. It holds the device code: keep it server side, never in a page, URL or
cookie.

### `Token.headers()`

`{"Authorization": "Bearer <access token>"}`, for `requests`. A token that expires within 30 seconds and has a
refresh token is refreshed first.

### `Token.is_expired(margin=30)`

Whether the access token expires within `margin` seconds. `False` when the IdP did not say when it expires.

### `Token.refresh(scope=None)`

Gets a new access token with the refresh token, in place. Raises when there is no refresh token.

### `Token.to_dict()`

The token as a dict: `access_token`, `token_type`, `expires_at`, `expires_in`, and `refresh_token`, `scope` and
`id_token` when present. It holds the tokens: store it where only the script can read it.

### `Token.claims()`

What a JWT access token says, **not verified**: for showing or debugging. An API checks a token with
`OAuthClient.verify()`.

## Security Considerations

This is an extended library, requiring registration in Go, see [Library Registration](/docs/go-integration/library-registration/#utilities).
The CLI registers it, under `--network-policy` and `--allowed-paths`.

- Every request to the IdP goes through the network policy when one is set; `verify=False` only stops the
  certificate being checked.
- A CA bundle named with `verify="path"` must lie within `--allowed-paths`, else an uncatchable `PermissionError`.
- Requests that carry codes, secrets or tokens never follow redirects, so a redirect cannot send them elsewhere.
  Responses from the IdP are capped at 1 MB.
- Errors carry the IdP's error code and description, never a code, secret or token.
- Device sign-in can be abused by someone who sends a victim a code to approve. Show the code only to the person
  who started the sign-in, and keep `DeviceFlow.to_dict()` server side.

## See Also

- [requests](../requests/): HTTP client, used with `token.headers()`
- [scriptling.secret](../../utilities/secret/): Reading client secrets
