include $(ROOT_DIR)/make/core/help/variable.mk

# -------------------------------------------------------------------------
# 🐳 COMPOSE BUILD - Help
# -------------------------------------------------------------------------

.PHONY: help-compose-infrastructure
help-compose-infrastructure:
	@echo [Docker Compose Infrastructure] (Total: $(call COMMAND_COUNT,COMPOSE_INFRASTRUCTURE))
	@echo $(HELP_SEPARATOR)

	@echo   make c-build-base                   ^|    Build base compose image
	@echo   make c-build-dev                    ^|    Build development app image
	@echo   make c-build-prod                   ^|    Build production app image
	@echo   make c-build-all                    ^|    Build all Custy compose images
	@echo.
	@echo   make c-up                           ^|    Start development compose stack
	@echo   make c-up-build                     ^|    Start compose stack and rebuild images
	@echo   make c-up-detached                  ^|    Start compose stack in background
	@echo   make c-down                         ^|    Stop compose stack
	@echo   make c-down-clean                   ^|    Stop compose stack and remove volumes
	@echo   make c-logs                         ^|    Follow compose service logs

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🐳 COMPOSE CORE - Help
# -------------------------------------------------------------------------

.PHONY: help-compose-init
help-compose-init:
	@echo [Docker Compose Initialization] (Total: $(call COMMAND_COUNT,COMPOSE_INIT))
	@echo $(HELP_SEPARATOR)

	@echo   make c-init                         ^|    Run initialization using compose
	@echo   make c-init-force                   ^|    Initialize and overwrite existing files
	@echo   make c-init-ask                     ^|    Initialize with confirmation prompts
	@echo   make c-init-all                     ^|    Initialize all resources
	@echo   make c-init-all-no-examples         ^|    Initialize configuration and templates only
	@echo   make c-init-config                  ^|    Initialize configuration files only
	@echo   make c-init-templates               ^|    Initialize message templates only
	@echo   make c-init-examples                ^|    Initialize example resources only

	@echo $(HELP_SEPARATOR)
	@echo.

.PHONY: help-compose-run
help-compose-run:
	@echo [Docker Compose Run Commands] (Total: $(call COMMAND_COUNT,COMPOSE_RUN))
	@echo $(HELP_SEPARATOR)

	@echo   make c-run                          ^|    Run compose command with custom arguments
	@echo.
	@echo   make c-run-validate                 ^|    Run the validate command
	@echo   make c-run-apply-version            ^|    Run version update
	@echo   make c-run-changelog                ^|    Run changelog generate
	@echo   make c-run-commit                   ^|    Create Git commit
	@echo   make c-run-tag                      ^|    Create Git tag
	@echo   make c-run-push                     ^|    Push commits and tags
	@echo   make c-run-dev                      ^|    Run daily development workflow
	@echo   make c-run-release                  ^|    Run release workflow
	@echo   make c-run-full                     ^|    Run full workflow
	@echo.
	@echo   make c-run-backup-commit            ^|    Backup commit message templates
	@echo   make c-run-backup-tag               ^|    Backup tag message templates
	@echo   make c-run-backup-all               ^|    Backup all templates
	@echo.
	@echo   make c-run-cleanup-backups          ^|    Remove backup files
	@echo   make c-run-cleanup-branches         ^|    Remove temporary branches
	@echo   make c-run-cleanup-all              ^|    Run complete cleanup workflow
	@echo.
	@echo   make c-workflow                     ^|    Run experimental workflow branch command

	@echo $(HELP_SEPARATOR)
	@echo.

.PHONY: help-compose-utilities
help-compose-utilities:
	@echo [Docker Compose Utilities] (Total: $(call COMMAND_COUNT,COMPOSE_UTILITIES))
	@echo $(HELP_SEPARATOR)

	@echo   make c-test                         ^|    Run tests using compose
	@echo   make c-lint                         ^|    Run linter using compose
	@echo   make c-lint-fix                     ^|    Run lint autofix using compose
	@echo   make c-format                       ^|    Run formatter using compose
	@echo   make c-format-check                 ^|    Check formatting using compose
	@echo.
	@echo   make c-docs                         ^|    Start documentation service
	@echo   make c-shell                        ^|    Open compose shell session
	@echo   make c-build-package                ^|    Build package using compose
	@echo   make c-exec-shell                   ^|    Execute shell in running container
	@echo.
	@echo   make c-fix                          ^|    Run formatter and lint autofix workflow
	@echo   make c-check                        ^|    Run validation workflow
	@echo   make c-qa                           ^|    Run full quality assurance workflow
	@echo   make c-ci                           ^|    Run compose-based CI workflow

	@echo $(HELP_SEPARATOR)
	@echo.
