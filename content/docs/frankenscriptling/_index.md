---
title: FrankenScriptling
description: Run Scriptling from PHP with a FrankenPHP Docker image that adds a Scriptling class.
tags: [frankenscriptling, php, docker, frankenphp]
weight: 8
---

FrankenScriptling is a Docker image of [FrankenPHP](https://frankenphp.dev/)
(PHP served by the Caddy web server) with Scriptling built in as a PHP class.
PHP code creates a `Scriptling` object, hands it data and runs scripts in it:
user-supplied rules, formulas, report templates, or code an LLM wrote. Each
script runs in Scriptling's sandbox, not in PHP, so it can only reach the
files, hosts and libraries the operator allows.

```php
<?php
$vm = new Scriptling();
$vm->setVarJSON('order', json_encode(['items' => [20.00, 5.50], 'country' => 'AU']));

echo $vm->eval(<<<'PY'
subtotal = sum(order["items"])
tax = subtotal * 0.1 if order["country"] == "AU" else 0
f"{subtotal + tax:.2f}"
PY);   // 28.05
```

## The image

Images are on Docker Hub as
[`paularlott/frankenscriptling`](https://hub.docker.com/r/paularlott/frankenscriptling),
built for `linux/amd64` and `linux/arm64`:

```bash
docker pull paularlott/frankenscriptling:php8.6
```

`php8.6` always points at the newest release on PHP 8.6. Other PHP lines
have their own tag (`php8.5`, `php8.4`), and `latest` is the newest release on
the newest PHP line. In production, pin a fixed release:
`<version>-php8.6` (for example `1.2.0-php8.6`) never changes. The image
version is its own, separate from the Scriptling version inside it; the
`dev.scriptling.scriptling-version` label and `getBuildInfo()` say which
Scriptling, FrankenPHP and PHP versions an image contains.

The image is the official FrankenPHP image rebuilt on `debian:trixie-slim`
without the compiler toolchain, at less than half the size. It keeps the same
layout: the Caddyfile at `/etc/frankenphp/Caddyfile`, the site in
`/app/public`, ports 80, 443 and 2019, and the usual `install-php-extensions`
and `docker-php-ext-*` scripts.

## Quick start

Create `public/index.php`:

```php
<?php
$vm = new Scriptling();
$vm->setVar('name', $_GET['name'] ?? 'world');
echo $vm->eval('f"Hello, {name.title()}!"');
```

Run it:

```bash
docker run --rm -p 8080:80 -v "$PWD/public:/app/public" paularlott/frankenscriptling:php8.6
```

Open `http://localhost:8080/?name=ada` to see `Hello, Ada!`.

The image serves `/app/public` on port 80 with its default Caddyfile. Mount
or copy your own Caddyfile to `/etc/frankenphp/Caddyfile`, or add site files
to `/app/Caddyfile.d/*.caddyfile`; see the
[FrankenPHP configuration docs](https://frankenphp.dev/docs/config/).

## What scripts can use

Every VM has the standard library (`json`, `re`, `datetime`, `decimal`,
`collections` and the rest) and the extension libraries that only compute:
`toml`, `yaml`, `logging`, `scriptling.csv`, `scriptling.xml`,
`scriptling.markdown` and the templates. See the
[Library Reference](/reference/libraries/).

Libraries that reach files, the network or other processes (`pathlib`, `os`,
`requests`, `subprocess`, `scriptling.ai`, `scriptling.mcp` and others) are
not registered until the operator enables them, and then only within the
directories and hosts the operator allows. PHP code cannot change this. See
[Configuration](configuration/).

## Guides

{{< cards >}}
{{< card link="configuration/" title="Configuration" description="Enable libraries, allow paths and hosts, set memory limits, secrets and plugins" >}}
{{< card link="php-api/" title="PHP API" description="The Scriptling class: running scripts, variables, libraries and calling PHP functions" >}}
{{< card link="extending/" title="Extending the Image" description="Add PHP extensions and Caddy modules, run without root, use the Mercure hub" >}}
{{< /cards >}}
