include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🔧 GIT UTILITIES - Help
# -------------------------------------------------------------------------

.PHONY: help-git
help-git:
	@echo [Git Utilities] (Total: $(call COMMAND_COUNT,GIT))
	@echo $(HELP_SEPARATOR)

	@echo   make git-current-branch             ^|    Show current Git branch
	@echo   make git-url-origin                 ^|    Show Git remote origin URL
	@echo   make git-log                        ^|    Show recent commit history
	@echo   make git-tags                       ^|    Show repository tags

	@echo $(HELP_SEPARATOR)
	@echo.
