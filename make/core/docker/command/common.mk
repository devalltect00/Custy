include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🐋 DOCKER BUILD
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

DOCKER_INFRASTRUCTURE_COMMANDS_LIST := \
	d-build-base \
	d-build-dev \
	d-build-prod \
	d-build-all

$(foreach cmd,$(DOCKER_INFRASTRUCTURE_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		DOCKER_INFRASTRUCTURE,$(cmd),DOCKER)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# 🐋 DOCKER BUILD - 🛠️ INTERNAL HELPERS
# -------------------------------------------------------------------------

docker-check:
	$(call REQUIRE_DOCKER)
	@echo.
	@echo Docker is ready.

# -------------------------------------------------------------------------
# 🐋 DOCKER BUILD - build
# -------------------------------------------------------------------------

.PHONY: d-build-base
d-build-base: docker-check
	@echo.
	@echo ==============================================================
	@echo.
	$(DOCKER) build -f $(DOCKERFILE_BASE) --target base -t $(DOCKER_IMAGE_BASE) .

.PHONY: d-build-dev
d-build-dev: d-build-base
	@echo.
	@echo ==============================================================
	@echo.
	$(DOCKER) build -f $(DOCKERFILE_BASE) --target development -t $(DOCKER_IMAGE_DEV) .

.PHONY: d-build-prod
d-build-prod: d-build-base
	@echo.
	@echo ==============================================================
	@echo.
	$(DOCKER) build -f $(DOCKERFILE_BASE) --target production -t $(DOCKER_IMAGE_PROD) .

.PHONY: d-build-all
d-build-all: docker-check
	@echo.
	@echo ==============================================================
	@echo.
	$(DOCKER) build -f $(DOCKERFILE_BASE) --target base -t $(DOCKER_IMAGE_BASE) .
	@echo.
	@echo ==============================================================
	@echo.
	$(DOCKER) build -f $(DOCKERFILE_BASE) --target development -t $(DOCKER_IMAGE_DEV) .
	@echo.
	@echo ==============================================================
	@echo.
	$(DOCKER) build -f $(DOCKERFILE_BASE) --target production -t $(DOCKER_IMAGE_PROD) .

