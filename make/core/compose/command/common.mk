include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🐋 DOCKER COMPOSE
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

COMPOSE_INFRASTRUCTURE_COMMANDS_LIST := \
	c-build-base \
	c-build-dev \
	c-build-prod \
	c-build-all \
	c-up \
	c-up-build \
	c-up-detached \
	c-down \
	c-down-clean \
	c-logs

$(foreach cmd,$(COMPOSE_INFRASTRUCTURE_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		COMPOSE_INFRASTRUCTURE,$(cmd),COMPOSE)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# 🐋 DOCKER COMPOSE - Common
# -------------------------------------------------------------------------

.PHONY: c-build-base
c-build-base: docker-check
	@echo.
	@echo ==============================================================
	@echo.
	$(COMPOSE_BASE) build base

.PHONY: c-build-dev
c-build-dev: c-build-base
	@echo.
	@echo ==============================================================
	@echo.
	$(COMPOSE_DEV) build $(DOCKER_BUILD_VERSION_ARG) app

.PHONY: c-build-prod
c-build-prod: c-build-base
	@echo.
	@echo ==============================================================
	@echo.
	$(COMPOSE_PROD) build $(DOCKER_BUILD_VERSION_ARG) app

.PHONY: c-build-all
c-build-all: docker-check
	@echo.
	@echo ==============================================================
	@echo.
	$(COMPOSE_BASE) build base
	@echo.
	@echo ==============================================================
	@echo.
	$(COMPOSE_DEV) build $(DOCKER_BUILD_VERSION_ARG) app
	@echo.
	@echo ==============================================================
	@echo.
	$(COMPOSE_PROD) build $(DOCKER_BUILD_VERSION_ARG) app

.PHONY: c-up
c-up: docker-check
	$(COMPOSE_DEV) up

.PHONY: c-up-build
c-up-build: docker-check
	$(COMPOSE_DEV) build $(DOCKER_BUILD_VERSION_ARG) app
	$(COMPOSE_DEV) up

.PHONY: c-up-detached
c-up-detached: docker-check
	$(COMPOSE_DEV) up -d

.PHONY: c-down
c-down: docker-check
	$(COMPOSE_DEV) down

.PHONY: c-down-clean
c-down-clean: docker-check
	$(COMPOSE_DEV) down -v --remove-orphans

.PHONY: c-logs
c-logs: docker-check
	$(COMPOSE_DEV) logs -f
