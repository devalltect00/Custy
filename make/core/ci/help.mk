include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🧶 CI - Help
# -------------------------------------------------------------------------

.PHONY: help-ci
help-ci:
	@echo [Continuous Integration] (Total: $(call COMMAND_COUNT,CI))
	@echo $(HELP_SEPARATOR)

	@echo   make lint-ci                        ^|    Run Ruff lint checks without virtual environment dependency
	@echo   make format-check-ci                ^|    Check Black formatting without virtual environment dependency
	@echo   make test-ci                        ^|    Run tests in CI-compatible mode
	@echo   make check-ci                       ^|    Run complete CI validation workflow

	@echo $(HELP_SEPARATOR)
	@echo.
