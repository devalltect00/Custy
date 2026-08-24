include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 📦 BUILD & PUBLISH - Help
# -------------------------------------------------------------------------

.PHONY: help-build-publish
help-build-publish:
	@echo [Build ^& Publish] (Total: $(call COMMAND_COUNT,BUILD_PUBLISH))
	@echo $(HELP_SEPARATOR)

	@echo   make build                          ^|    Build package artifacts
	@echo   make publish                        ^|    Publish package to package registry
	@echo   make build-all                      ^|    Build package and all Docker images

	@echo $(HELP_SEPARATOR)
	@echo.
