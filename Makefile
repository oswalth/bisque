DCO ?= docker-compose
DOCKER_SERVICE ?= app

build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 $(DCO) build

build-no-cache:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 $(DCO) build --no-cache

up:
	$(DCO) up -d --no-build
	$(DCO) ps

restart:
	$(DCO) restart $(DOCKER_SERVICE)
	$(DCO) ps

rebuild: build
	$(DCO) up -d
	$(DCO) ps

rebuild-no-cache: build-no-cache
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE) ps

down:
	$(DCO) down --remove-orphans

bash:
	$(DCO) exec $(DOCKER_SERVICE) bash

ps:
	$(DCO) ps
