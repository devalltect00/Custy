include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 📚 DOCUMENTATION - Help
# -------------------------------------------------------------------------

.PHONY: help-documentation
help-documentation:
	@echo [Documentation] (Total: $(call COMMAND_COUNT,DOCUMENTATION))
	@echo $(HELP_SEPARATOR)

	@echo   make docs-serve                     ^|    Serve documentation locally
	@echo   make docs-build                     ^|    Build documentation site

	@echo $(HELP_SEPARATOR)
	@echo.
