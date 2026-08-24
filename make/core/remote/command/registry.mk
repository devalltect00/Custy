include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🌐 Remote Registry Commands
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

REMOTE_PHS_REGISTRY_COMMANDS_LIST := \
	r-phs-info \
	r-phs-pull \
	r-phs-push \
	r-phs-remove

REMOTE_DOC_GEN_REGISTRY_COMMANDS_LIST := \
	r-doc-gen-info \
	r-doc-gen-pull \
	r-doc-gen-push \
	r-doc-gen-remove

REMOTE_CUSTY_REGISTRY_COMMANDS_LIST := \
	r-custy-info \
	r-custy-pull \
	r-custy-push \
	r-custy-remove

REMOTE_REFLOW_REGISTRY_COMMANDS_LIST := \
	r-reflow-info \
	r-reflow-pull \
	r-reflow-push \
	r-reflow-remove

$(foreach cmd,$(REMOTE_PHS_REGISTRY_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		REMOTE_PHS_REGISTRY,$(cmd),REMOTE)))

$(foreach cmd,$(REMOTE_DOC_GEN_REGISTRY_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		REMOTE_DOC_GEN_REGISTRY,$(cmd),REMOTE)))

$(foreach cmd,$(REMOTE_CUSTY_REGISTRY_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		REMOTE_CUSTY_REGISTRY,$(cmd),REMOTE)))

$(foreach cmd,$(REMOTE_REFLOW_REGISTRY_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		REMOTE_REFLOW_REGISTRY,$(cmd),REMOTE)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# 🌐 Remote Registry Commands - Path Header Scanner
# -------------------------------------------------------------------------

.PHONY: r-phs-info
r-phs-info:
	$(call REQUIRE_REMOTE)
	$(call PRINT_REMOTE_INFO,REMOTE_IMAGE_PHS)

.PHONY: r-phs-pull
r-phs-pull:
	$(call REQUIRE_REMOTE)
	$(call PULL_REMOTE_IMAGE,REMOTE_IMAGE_PHS)

.PHONY: r-phs-push
r-phs-push:
	$(call REQUIRE_REMOTE_PUSH)
	$(call PUSH_REMOTE_IMAGE,REMOTE_IMAGE_PHS)

.PHONY: r-phs-remove
r-phs-remove:
	$(call REQUIRE_REMOTE)
	$(call REMOVE_REMOTE_IMAGE,REMOTE_IMAGE_PHS)

# -------------------------------------------------------------------------
# 🌐 Remote Registry Commands - Doc Gen
# -------------------------------------------------------------------------

.PHONY: r-doc-gen-info
r-doc-gen-info:
	$(call REQUIRE_REMOTE)
	$(call PRINT_REMOTE_INFO,REMOTE_IMAGE_DOC_GEN)

.PHONY: r-doc-gen-pull
r-doc-gen-pull:
	$(call REQUIRE_REMOTE)
	$(call PULL_REMOTE_IMAGE,REMOTE_IMAGE_DOC_GEN)

.PHONY: r-doc-gen-push
r-doc-gen-push:
	$(call REQUIRE_REMOTE_PUSH)
	$(call PUSH_REMOTE_IMAGE,REMOTE_IMAGE_DOC_GEN)

.PHONY: r-doc-gen-remove
r-doc-gen-remove:
	$(call REQUIRE_REMOTE)
	$(call REMOVE_REMOTE_IMAGE,REMOTE_IMAGE_DOC_GEN)

# -------------------------------------------------------------------------
# 🌐 Remote Registry Commands - Custy
# -------------------------------------------------------------------------

.PHONY: r-custy-info
r-custy-info:
	$(call REQUIRE_REMOTE)
	$(call PRINT_REMOTE_INFO,REMOTE_IMAGE_CUSTY)

.PHONY: r-custy-pull
r-custy-pull:
	$(call REQUIRE_REMOTE)
	$(call PULL_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)

.PHONY: r-custy-push
r-custy-push:
	$(call REQUIRE_REMOTE_PUSH)
	$(call PUSH_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)

.PHONY: r-custy-remove
r-custy-remove:
	$(call REQUIRE_REMOTE)
	$(call REMOVE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)

# -------------------------------------------------------------------------
# 🌐 Remote Registry Commands - Reflow
# -------------------------------------------------------------------------

.PHONY: r-reflow-info
r-reflow-info:
	$(call REQUIRE_REMOTE)
	$(call PRINT_REMOTE_INFO,REMOTE_IMAGE_REFLOW)

.PHONY: r-reflow-pull
r-reflow-pull:
	$(call REQUIRE_REMOTE)
	$(call PULL_REMOTE_IMAGE,REMOTE_IMAGE_REFLOW)

.PHONY: r-reflow-push
r-reflow-push:
	$(call REQUIRE_REMOTE_PUSH)
	$(call PUSH_REMOTE_IMAGE,REMOTE_IMAGE_REFLOW)

.PHONY: r-reflow-remove
r-reflow-remove:
	$(call REQUIRE_REMOTE)
	$(call REMOVE_REMOTE_IMAGE,REMOTE_IMAGE_REFLOW)
