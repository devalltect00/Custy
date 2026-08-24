include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🚀 LOCAL COMMANDS - Help
# -------------------------------------------------------------------------

.PHONY: help-local-init
help-local-init:
	@echo [Local Initialization Commands] (Total: $(call COMMAND_COUNT,LOCAL_INITIALIZATION))
	@echo $(HELP_SEPARATOR)

	@echo   make l-init                         ^|    Run initialization locally
	@echo   make l-init-force                   ^|    Initialize and overwrite existing files
	@echo   make l-init-ask                     ^|    Initialize with confirmation prompts
	@echo   make l-init-all                     ^|    Initialize all resources
	@echo   make l-init-all-no-examples         ^|    Initialize configuration and templates only
	@echo   make l-init-config                  ^|    Initialize configuration files only
	@echo   make l-init-templates               ^|    Initialize message templates only
	@echo   make l-init-examples                ^|    Initialize example resources only

	@echo $(HELP_SEPARATOR)
	@echo.

.PHONY: help-local-run
help-local-run:
	@echo [Local Run Commands] (Total: $(call COMMAND_COUNT,LOCAL_RUN))
	@echo   make l-run                          ^|    Run local command with custom arguments
	@echo.

	@echo   make l-run-validate                 ^|    Run the validate command
	@echo   make l-run-apply-version            ^|    Run version update
	@echo   make l-run-changelog                ^|    Run changelog generate
	@echo   make l-run-commit                   ^|    Create Git commit
	@echo   make l-run-tag                      ^|    Create Git tag
	@echo   make l-run-push                     ^|    Push commits and tags
	@echo   make l-run-dev                      ^|    Run daily development workflow
	@echo   make l-run-release                  ^|    Run release workflow
	@echo   make l-run-full                     ^|    Run full workflow
	@echo.
	@echo   make l-run-backup-commit            ^|    Backup commit message templates
	@echo   make l-run-backup-tag               ^|    Backup tag message templates
	@echo   make l-run-backup-all               ^|    Backup all templates
	@echo.
	@echo   make l-run-cleanup-backups          ^|    Remove backup files
	@echo   make l-run-cleanup-branches         ^|    Remove temporary branches
	@echo   make l-run-cleanup-all              ^|    Run complete cleanup workflow
	@echo.
	@echo   make l-workflow                     ^|    Run experimental workflow branch command

	@echo $(HELP_SEPARATOR)
	@echo.
