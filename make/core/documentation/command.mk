include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 📚 Documentation
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

DOCUMENTATION_COMMANDS_LIST := \
	docs-serve \
	docs-build

$(foreach cmd,$(DOCUMENTATION_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		DOCUMENTATION,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

.PHONY: docs-serve
docs-serve: check-venv
	"$(PYTHON)" -m $(MKDOCS) serve

.PHONY: docs-build
docs-build: check-venv
	"$(PYTHON)" -m $(MKDOCS) build
