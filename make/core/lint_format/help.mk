include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🧶 LINT & FORMAT - Help
# -------------------------------------------------------------------------

.PHONY: help-lint-format
help-lint-format:
	@echo [Lint ^& Format] (Total: $(call COMMAND_COUNT,LINT_FORMAT))
	@echo $(HELP_SEPARATOR)

	@echo   make lint                           ^|    Run Ruff lint checks
	@echo   make lint-fix                       ^|    Run Ruff autofix
	@echo   make lint-fix-unsafe                ^|    Run Ruff autofix with unsafe fixes
	@echo.
	@echo   make format-ruff                    ^|    Format code using Ruff formatter
	@echo   make format                         ^|    Format code using Black
	@echo   make format-check                   ^|    Check Black formatting without modifying files

	@echo $(HELP_SEPARATOR)
	@echo.
