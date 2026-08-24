include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🧶 QA
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

QA_COMMANDS_LIST := \
	fix \
	check \
	qa \
	ci

$(foreach cmd,$(QA_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		QA,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

.PHONY: fix
fix: check-venv
	@echo =========================================================
	@echo Run Ruff autofix + Black formatter
	@echo =========================================================
	@$(MAKE) format
	@$(MAKE) lint-fix

.PHONY: check
check: check-venv
	@echo =========================================================
	@echo Run local validation workflow
	@echo Run formatting, lint, and tests
	@echo =========================================================
	@$(MAKE) format-check
	@$(MAKE) lint
	@$(MAKE) test

.PHONY: qa
qa:
	@$(MAKE) fix
	@$(MAKE) check

.PHONY: ci
ci: c-ci
