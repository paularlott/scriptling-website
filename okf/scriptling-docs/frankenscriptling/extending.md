---
description: Add PHP extensions and Caddy modules to FrankenScriptling, run it without root, and use its Mercure hub.
generated:
    by: scriptling-website/okf.py
resource: https://scriptling.dev/docs/frankenscriptling/extending/
sources:
    - resource: https://scriptling.dev/docs/frankenscriptling/extending/
status: stable
tags:
    - frankenscriptling
    - docker
    - php
    - caddy
title: Extending the Image
type: Guide
---
# Extending the Image

## PHP extensions

The usual ways of adding PHP extensions work:

```dockerfile
FROM paularlott/frankenscriptling:php8.6

# Core and PECL extensions alike
RUN install-php-extensions pdo_mysql gd intl redis

# Or the official PHP image's scripts
RUN apt-get update && apt-get install -y libfreetype-dev libjpeg62-turbo-dev libpng-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd
```

The image has no compiler. `install-php-extensions` and the
`docker-php-ext-*` scripts install the build tools when they need them and
remove them afterwards, keeping only the libraries the new extensions use.
Keep `docker-php-ext-configure` and `docker-php-ext-install` in the same
`RUN`, or the build tools stay in the configure layer.

A bare `pecl install` or `phpize` fails with `Cannot find autoconf`. Use
`install-php-extensions`, or install `$PHPIZE_DEPS` and remove them in the same
`RUN`:

```dockerfile
RUN apt-get update && apt-get install -y $PHPIZE_DEPS \
    && pecl install apcu && docker-php-ext-enable apcu \
    && apt-get purge -y --auto-remove $PHPIZE_DEPS && rm -rf /var/lib/apt/lists/*
```

`session.upload_progress.enabled` is turned off in
`$PHP_INI_DIR/conf.d/zz-security.ini`, which loads after your own ini files.
Delete that file if you need upload progress.

## Caddy modules

FrankenPHP is a Caddy server, extended with Caddy modules compiled into the
binary. Each release has a builder image to rebuild the binary with extra
modules. Use the builder and runtime of the same release, so the binary
matches the image's PHP:

```dockerfile
FROM paularlott/frankenscriptling:1.2.0-builder-php8.6 AS builder
RUN build-frankenscriptling --with github.com/caddyserver/transform-encoder \
    && setcap cap_net_bind_service=+ep /usr/local/bin/frankenphp

FROM paularlott/frankenscriptling:1.2.0-php8.6
COPY --from=builder /usr/local/bin/frankenphp /usr/local/bin/frankenphp
```

`build-frankenscriptling` passes its arguments to `xcaddy build`. Replace
`1.2.0` with the release you run; `builder-php8.6` floats like `php8.6`.

## Running without root

The `frankenphp` binary can already bind ports 80 and 443, and `/config` and
`/data` belong to `www-data`, so switching user is enough:

```dockerfile
FROM paularlott/frankenscriptling:php8.6
USER www-data
```

## Mercure

The binary includes FrankenPHP's [Mercure hub](https://frankenphp.dev/docs/mercure/)
(the `mercure` Caddyfile directive and `mercure_publish()` in PHP). Scripts can
publish to it, or to any other hub, with `scriptling.mercure` once it is
enabled and the network policy allows the hub's address.

To reach the image's own hub, serve your site's hub on a loopback address of
its own as well, and allow only that address. `allow_loopback` would also
open Caddy's admin API on `localhost:2019`. Both addresses are one site, so
one hub: what a script publishes on `127.0.0.2` reaches browsers subscribed
on `example.com`.

```caddyfile
{
	frankenphp
}

example.com, http://127.0.0.2:8090 {
	root * /app/public

	mercure {
		# scriptling.mercure's tokens name https://localhost as their
		# issuer unless the script gives issuer=.
		issuer https://localhost {
			publisher {
				jwt {env.MERCURE_PUBLISHER_JWT_KEY} HS256
			}
			subscriber {
				jwt {env.MERCURE_SUBSCRIBER_JWT_KEY} HS256
			}
		}
		resource_identifier https://example.com/.well-known/mercure
	}

	# On the scripts' address, the hub only: not the app.
	@scripts {
		host 127.0.0.2
		not path /.well-known/mercure /.well-known/mercure/*
	}
	respond @scripts 404

	php_server
}
```

```toml
# SCRIPTLING_NETWORK_POLICY_FILE, with SCRIPTLING_ENABLED_LIBRARIES=scriptling.mercure
https_only = false
allow_cidrs = ["127.0.0.2/32"]
```

```php
$vm = new Scriptling();
$vm->setVar('key', getenv('MERCURE_PUBLISHER_JWT_KEY'));
$vm->eval(<<<'PY'
import scriptling.mercure as mercure

with mercure.Client("http://127.0.0.2:8090/.well-known/mercure", key=key,
                    audience="https://example.com/.well-known/mercure") as hub:
    hub.publish("https://example.com/books/1", {"title": "Dune"})
PY);
```

`audience` is the hub's public URL, which it checks tokens against. The
repository's
[`examples/mercure-local-hub`](https://github.com/paularlott/frankenscriptling/tree/main/examples/mercure-local-hub)
has a complete Caddyfile and policy.
