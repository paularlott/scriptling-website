default: help

## Generate architecture diagram
architecture: asset-src/distributed-architecture.d2 asset-src/architecture-single-location.d2 asset-src/architecture-local-docker.d2 asset-src/multi-server-cluster.d2 asset-src/multi-server-load-balancer.d2
	d2 --sketch --bundle --layout elk asset-src/architecture-single-location.d2 content/docs/getting-started/architecture-single-location.svg
	d2 --sketch --bundle --layout elk asset-src/architecture-local-docker.d2 content/docs/getting-started/architecture-local-docker.svg
	d2 --sketch --bundle --layout elk asset-src/distributed-architecture.d2 content/docs/getting-started/distributed-architecture.svg
	d2 --sketch --bundle --layout elk asset-src/restricted-leaf-server.d2 content/docs/getting-started/restricted-leaf-server.svg
	d2 --sketch --bundle --layout elk asset-src/multi-server-cluster.d2 content/docs/quick-start/local-containers/multi-server-cluster.svg
	d2 --sketch --bundle --layout elk asset-src/multi-server-load-balancer.d2 content/docs/quick-start/local-containers/multi-server-load-balancer.svg

.PHONY: help
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
