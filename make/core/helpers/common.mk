include $(ROOT_DIR)/make/core/variables/variable.mk

# ============================================================================
# 🛠️ Validation Helpers
# ============================================================================

define REQUIRE_PYTHON
	@"$(PYTHON_SYSTEM)" --version >NUL 2>&1 || (echo Python is not installed. && exit 1)
endef

define REQUIRE_DOCKER
	@$(DOCKER) --version >NUL 2>&1 || (echo Docker is not installed. && exit 1)
	@$(DOCKER) info >NUL 2>&1 || (echo Docker is installed but not running. && exit 1)
endef

# =========================================================
# 🌐 Remote Helpers
# =========================================================

# -------------------------------------------------------------------------
# Remote Validation
# -------------------------------------------------------------------------

define REQUIRE_REMOTE
	$(call REQUIRE_DOCKER)
endef

define REQUIRE_REMOTE_PUSH
	$(call REQUIRE_DOCKER)
endef

# -------------------------------------------------------------------------
# Image Resolution
# -------------------------------------------------------------------------

define REMOTE_IMAGE_FULL
$(GHCR_REGISTRY)/$(GHCR_OWNER)/$($(1)):$(REMOTE_TAG)
endef

# -------------------------------------------------------------------------
# Image Management
# -------------------------------------------------------------------------

define ENSURE_REMOTE_IMAGE
	@$(DOCKER) image inspect $(call REMOTE_IMAGE_FULL,$(1)) >NUL 2>&1 || \
	( \
		echo Pulling $(call REMOTE_IMAGE_FULL,$(1))... && \
		$(DOCKER) pull $(call REMOTE_IMAGE_FULL,$(1)) \
	)
endef

define PULL_REMOTE_IMAGE
	$(DOCKER) pull $(call REMOTE_IMAGE_FULL,$(1))
endef

define PUSH_REMOTE_IMAGE
	$(DOCKER) push $(call REMOTE_IMAGE_FULL,$(1))
endef

define REMOVE_REMOTE_IMAGE
	$(DOCKER) image rm $(call REMOTE_IMAGE_FULL,$(1))
endef

# -------------------------------------------------------------------------
# Container Runtime
# -------------------------------------------------------------------------

define REMOTE_RUN
$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_REMOTE_WORKSPACE) \
	$(call REMOTE_IMAGE_FULL,$(1))
endef

# -------------------------------------------------------------------------
# Information
# -------------------------------------------------------------------------

define PRINT_REMOTE_INFO
	@echo Image : $($(1))
	@echo Tag   : $(REMOTE_TAG)
	@echo Full  : $(call REMOTE_IMAGE_FULL,$(1))
endef
