include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🛡️ QA - Help
# -------------------------------------------------------------------------

.PHONY: help-quality-assurance
help-quality-assurance:
	@echo [Quality Assurance] (Total: $(call COMMAND_COUNT,QA))
	@echo $(HELP_SEPARATOR)

	@echo   make fix                            ^|    Run formatter and lint autofix workflow
	@echo   make check                          ^|    Run formatting, lint, and test validation workflow
	@echo   make qa                             ^|    Run complete fix and validation workflow
	@echo   make ci                             ^|    Run CI validation workflow

	@echo $(HELP_SEPARATOR)
	@echo.
