default: help

## Generate architecture diagram
architecture: asset-src/distributed-architecture.d2 asset-src/architecture-single-location.d2 asset-src/architecture-local-docker.d2 asset-src/multi-server-cluster.d2 asset-src/multi-server-load-balancer.d2
	d2 --sketch --bundle --layout elk asset-src/architecture-single-location.d2 content/docs/getting-started/architecture-single-location.svg
	d2 --sketch --bundle --layout elk asset-src/architecture-local-docker.d2 content/docs/getting-started/architecture-local-docker.svg
	d2 --sketch --bundle --layout elk asset-src/distributed-architecture.d2 content/docs/getting-started/distributed-architecture.svg
	d2 --sketch --bundle --layout elk asset-src/restricted-leaf-server.d2 content/docs/getting-started/restricted-leaf-server.svg
	d2 --sketch --bundle --layout elk asset-src/multi-server-cluster.d2 content/docs/quick-start/local-containers/multi-server-cluster.svg
	d2 --sketch --bundle --layout elk asset-src/multi-server-load-balancer.d2 content/docs/quick-start/local-containers/multi-server-load-balancer.svg

## Generate OKF 0.2 knowledge bundles into okf/ (committed: Cloudflare runs Hugo, not scripts;
## mounted into the site at /okf/ via hugo.toml)
okf:
	scriptling scripts/okf.py

## Pack just the OKF bundles into dist/scriptling-okf-bundles.zip
bundle-pack: okf
	@rm -f dist/scriptling-okf-bundles.zip
	@mkdir -p dist
	cd okf && zip -qr ../dist/scriptling-okf-bundles.zip scriptling-docs scriptling-reference scriptling-libraries
	@echo "Built dist/scriptling-okf-bundles.zip"

## Regenerate OKF bundles; commit and push them if anything changed
okf-sync: okf
	@if ! git diff --quiet -- okf/; then \
		echo "OKF bundles changed; committing and pushing"; \
		git add okf/ && git commit -m "Regenerate OKF bundles" && git push; \
	else \
		echo "OKF bundles up to date"; \
	fi

## Tag and publish a GitHub release with the OKF bundles archive.
## The bundles are regenerated and pushed first so the release always matches
## the committed docs.
release: okf-sync bundle-pack
	@test -d ../scriptling || { echo "scriptling repo not found at ../scriptling"; exit 1; }
	@command -v gh >/dev/null 2>&1 || { echo "gh CLI not installed"; exit 1; }
	@V=$$(cd ../scriptling && go run ./tools/getversion); \
	echo "Releasing scriptling-okf-bundles v$$V"; \
	if git tag -l v$$V | grep -q v$$V; then \
		echo "Tag v$$V already exists, skipping tag creation"; \
	else \
		git tag -a v$$V -m "Release $$V" && git push origin v$$V; \
	fi; \
	gh release create v$$V dist/scriptling-okf-bundles.zip \
		-t "Release $$V" -n "Scriptling OKF knowledge bundles $$V"

.PHONY: help okf okf-sync bundle-pack release
## This help screen
help:
	@printf "Available targets:\n\n"
	@awk '/^[a-zA-Z\-_0-9%:\\]+/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = $$1; \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			gsub("\\\\", "", helpCommand); \
			gsub(":+$$", "", helpCommand); \
			printf "  \x1b[32;01m%-20s\x1b[0m %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -u
	@printf "\n"
