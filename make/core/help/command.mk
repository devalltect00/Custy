include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# ⚙️ Helpers
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

HELP_COMMANDS_LIST := \
	help \
	help-local \
	help-docker \
	help-compose \
	help-remote

$(foreach cmd,$(HELP_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		HELP,$(cmd))))

# -------------------------------------------------------------------------
# ⚙️ HELPER - HELP
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/help/helper.mk

# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - HELP
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/setup_install/help.mk

# -------------------------------------------------------------------------
# 🧶 QA - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/qa/help.mk

# -------------------------------------------------------------------------
# 🧶 LINT & FORMAT - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/lint_format/help.mk

# -------------------------------------------------------------------------
# 🧶 CI - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/ci/help.mk

# -------------------------------------------------------------------------
# 🧪 TESTING - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/testing/help.mk

# -------------------------------------------------------------------------
# 📚 DOCUMENTATION - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/documentation/help.mk

# -------------------------------------------------------------------------
# 📦 BUILD & PUBLISH - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/build_publish/help.mk

# -------------------------------------------------------------------------
# 🚀 LOCAL COMMANDS - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/local/help.mk

# -------------------------------------------------------------------------
# 🐳 DOCKER - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/docker/help.mk

# -------------------------------------------------------------------------
# 🐳 COMPOSE - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/compose/help.mk

# -------------------------------------------------------------------------
# 🌐 REMOTE - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/remote/help.mk

# -------------------------------------------------------------------------
# 🔧 GIT UTILITIES - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/git/help.mk

# -------------------------------------------------------------------------
# 🧹 CLEANUP - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/cleanup/help.mk

# -------------------------------------------------------------------------
# 🔡 VARIABLES - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/variables/help.mk

# -------------------------------------------------------------------------
# 💡 EXAMPLES - Help
# -------------------------------------------------------------------------

include $(ROOT_DIR)/make/core/examples/help.mk


# =========================================================
# 🆘 HELP
# =========================================================

# -------------------------------------------------------------------------
# 🆘 Wrapper
# -------------------------------------------------------------------------

define HELP_WRAPPER
	@$(MAKE) --no-print-directory help-header

	@$(MAKE) --no-print-directory help-help

	$(1)

	@$(MAKE) --no-print-directory help-variables
	@$(MAKE) --no-print-directory help-examples

	@$(MAKE) --no-print-directory help-footer GROUP=$(2)
endef

define HELP_CONTENT_LOCAL
	@$(MAKE) --no-print-directory help-setup-installation
	@$(MAKE) --no-print-directory help-quality-assurance
	@$(MAKE) --no-print-directory help-lint-format
	@$(MAKE) --no-print-directory help-ci
	@$(MAKE) --no-print-directory help-testing
	@$(MAKE) --no-print-directory help-documentation
	@$(MAKE) --no-print-directory help-build-publish

	@$(MAKE) --no-print-directory help-local-init
	@$(MAKE) --no-print-directory help-local-run

	@$(MAKE) --no-print-directory help-git

	@$(MAKE) --no-print-directory help-cleanup-project
endef

define HELP_CONTENT_DOCKER
	@$(MAKE) --no-print-directory help-docker-build
	@$(MAKE) --no-print-directory help-docker-testing
	@$(MAKE) --no-print-directory help-docker-init
	@$(MAKE) --no-print-directory help-docker-run

	@$(MAKE) --no-print-directory help-cleanup-docker
endef

define HELP_CONTENT_COMPOSE
	@$(MAKE) --no-print-directory help-compose-infrastructure
	@$(MAKE) --no-print-directory help-compose-init
	@$(MAKE) --no-print-directory help-compose-run
	@$(MAKE) --no-print-directory help-compose-utilities

	@$(MAKE) --no-print-directory help-cleanup-docker
endef

define HELP_CONTENT_REMOTE
	@$(MAKE) --no-print-directory help-remote-phs-registry
	@$(MAKE) --no-print-directory help-remote-phs-runtime

	@$(MAKE) --no-print-directory help-remote-docgen-registry
	@$(MAKE) --no-print-directory help-remote-docgen-runtime

	@$(MAKE) --no-print-directory help-remote-custy-registry
	@$(MAKE) --no-print-directory help-remote-custy-runtime

	@$(MAKE) --no-print-directory help-remote-reflow-registry
	@$(MAKE) --no-print-directory help-remote-reflow-runtime
endef

define HELP_CONTENT_ALL
	@$(MAKE) --no-print-directory help-setup-installation
	@$(MAKE) --no-print-directory help-quality-assurance
	@$(MAKE) --no-print-directory help-lint-format
	@$(MAKE) --no-print-directory help-ci
	@$(MAKE) --no-print-directory help-testing
	@$(MAKE) --no-print-directory help-documentation
	@$(MAKE) --no-print-directory help-build-publish

	@$(MAKE) --no-print-directory help-local-init
	@$(MAKE) --no-print-directory help-local-run

	@$(MAKE) --no-print-directory help-docker-build
	@$(MAKE) --no-print-directory help-docker-testing
	@$(MAKE) --no-print-directory help-docker-init
	@$(MAKE) --no-print-directory help-docker-run

	@$(MAKE) --no-print-directory help-compose-infrastructure
	@$(MAKE) --no-print-directory help-compose-init
	@$(MAKE) --no-print-directory help-compose-run
	@$(MAKE) --no-print-directory help-compose-utilities

	@$(MAKE) --no-print-directory help-remote-phs-registry
	@$(MAKE) --no-print-directory help-remote-phs-runtime

	@$(MAKE) --no-print-directory help-remote-docgen-registry
	@$(MAKE) --no-print-directory help-remote-docgen-runtime

	@$(MAKE) --no-print-directory help-remote-custy-registry
	@$(MAKE) --no-print-directory help-remote-custy-runtime

	@$(MAKE) --no-print-directory help-remote-reflow-registry
	@$(MAKE) --no-print-directory help-remote-reflow-runtime

	@$(MAKE) --no-print-directory help-git

	@$(MAKE) --no-print-directory help-cleanup-project
	@$(MAKE) --no-print-directory help-cleanup-docker
endef

# -------------------------------------------------------------------------
# 🆘 sub local - Help
# -------------------------------------------------------------------------

.PHONY: help-local
help-local:
# 	HELP_CONTENT = 1 + 13 + 4 + 6 + 4 + 4 + 2 + 3 + 22
	$(call HELP_WRAPPER, $(HELP_CONTENT_LOCAL),LOCAL)

# -------------------------------------------------------------------------
# 🆘 sub docker - Help
# -------------------------------------------------------------------------

.PHONY: help-docker
help-docker:
	$(call HELP_WRAPPER, $(HELP_CONTENT_DOCKER),DOCKER)

# -------------------------------------------------------------------------
# 🆘 sub compose - Help
# -------------------------------------------------------------------------

.PHONY: help-compose
help-compose:
	$(call HELP_WRAPPER, $(HELP_CONTENT_COMPOSE),COMPOSE)

# -------------------------------------------------------------------------
# 🆘 sub remote - Help
# -------------------------------------------------------------------------

.PHONY: help-remote
help-remote:
	$(call HELP_WRAPPER, $(HELP_CONTENT_REMOTE),REMOTE)


# -------------------------------------------------------------------------
# 🆘 All - Help
# -------------------------------------------------------------------------

.PHONY: help
help:
	$(call HELP_WRAPPER, $(HELP_CONTENT_ALL),ALL)
