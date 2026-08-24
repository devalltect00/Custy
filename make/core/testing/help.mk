include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🧪 TESTING - Help
# -------------------------------------------------------------------------

.PHONY: help-testing
help-testing:
	@echo [Testing] (Total: $(call COMMAND_COUNT,TESTING))
	@echo $(HELP_SEPARATOR)

	@echo   make test                           ^|    Run test suite
	@echo   make test-verbose                   ^|    Run test suite with verbose output
	@echo   make test-cov                       ^|    Run test suite with terminal coverage report
	@echo   make test-cov-html                  ^|    Run test suite with HTML coverage report

	@echo $(HELP_SEPARATOR)
	@echo.
