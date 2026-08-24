include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🧶 CI
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

CI_COMMANDS_LIST := \
	lint-ci \
	format-check-ci \
	test-ci \
	check-ci

$(foreach cmd,$(CI_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		CI,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

.PHONY: lint-ci
lint-ci:
	python -m $(RUFF) check $(SOURCE_DIRS)

.PHONY: format-check-ci
format-check-ci:
	python -m $(BLACK) --check $(SOURCE_DIRS)

.PHONY: test-ci
test-ci:
	python -m $(PYTEST) -v

.PHONY: check-ci
check-ci:
	@echo =========================================================
	@echo Run CI validation workflow
	@echo =========================================================
	@$(MAKE) format-check-ci
	@$(MAKE) lint-ci
	@$(MAKE) test-ci
