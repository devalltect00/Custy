include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🆘 HELP HEADER
# -------------------------------------------------------------------------

.PHONY: help-header
help-header:
	@echo.
	@echo =========================================================
	@echo  $(APP_NAME) - Available Commands
	@echo =========================================================
	@echo.

# -------------------------------------------------------------------------
# 🆘 HELP FOOTER
# -------------------------------------------------------------------------

help-footer:
# 	@echo.
ifeq ($(GROUP),ALL)
	@echo Total Commands: $(call COMMAND_COUNT,ALL)
else
	@echo Commands in $(GROUP_DISPLAY_$(GROUP)): $(call COMMAND_COUNT,$(GROUP))
endif
	@echo.
	@echo =========================================================

# -------------------------------------------------------------------------
# 🆘 HELP - Help
# -------------------------------------------------------------------------

.PHONY: help-help
help-help:
	@echo [Help] (Total: $(call COMMAND_COUNT,HELP))
	@echo $(HELP_SEPARATOR)

	@echo   make help                           ^|    Show all available commands
	@echo   make help-local                     ^|    Show local development commands
	@echo   make help-docker                    ^|    Show Docker commands
	@echo   make help-compose                   ^|    Show Docker Compose commands
	@echo   make help-remote                    ^|    Show remote environment commands

	@echo $(HELP_SEPARATOR)
	@echo.
