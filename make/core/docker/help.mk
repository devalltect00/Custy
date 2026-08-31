include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🐳 DOCKER BUILD - Help
# -------------------------------------------------------------------------

.PHONY: help-docker-build
help-docker-build:
	@echo [Docker Infrastructure] (Total: $(call COMMAND_COUNT,DOCKER_INFRASTRUCTURE))
	@echo $(HELP_SEPARATOR)

	@echo   make d-build-base                   ^|    Build base Docker image
	@echo   make d-build-dev                    ^|    Build development Docker image
	@echo   make d-build-prod                   ^|    Build production Docker image
	@echo   make d-build-all                    ^|    Build all Docker images

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🐳 DOCKER CORE - Help
# -------------------------------------------------------------------------

.PHONY: help-docker-testing
help-docker-testing:
	@echo [Docker Testing] (Total: $(call COMMAND_COUNT,DOCKER_TESTING))
	@echo $(HELP_SEPARATOR)

	@echo   make d-test                         ^|    Run test suite inside Docker

	@echo $(HELP_SEPARATOR)
	@echo.

.PHONY: help-docker-init
help-docker-init:
	@echo [Docker Initialization] (Total: $(call COMMAND_COUNT,DOCKER_INITIALIZATION))
	@echo $(HELP_SEPARATOR)

	@echo   make d-init                         ^|    Run initialization inside Docker
	@echo   make d-init-force                   ^|    Initialize and overwrite existing files
	@echo   make d-init-ask                     ^|    Initialize with confirmation prompts
	@echo   make d-init-all                     ^|    Initialize all resources
	@echo   make d-init-all-no-examples         ^|    Initialize configuration and templates only
	@echo   make d-init-config                  ^|    Initialize configuration files only
	@echo   make d-init-templates               ^|    Initialize message templates only
	@echo   make d-init-examples                ^|    Initialize example resources only

	@echo $(HELP_SEPARATOR)
	@echo.

.PHONY: help-docker-run
help-docker-run:
	@echo [Docker Run Commands] (Total: $(call COMMAND_COUNT,DOCKER_RUN))
	@echo $(HELP_SEPARATOR)

	@echo   make d-run                          ^|    Run Docker command with custom arguments
	@echo.
	@echo   make d-credentials-set-github       ^|    Store a GitHub PAT in the external credential directory
	@echo   make d-credentials-set-gitlab       ^|    Store a GitLab PAT in the external credential directory
	@echo   make d-credentials-status           ^|    Inspect credential availability without showing tokens
	@echo   make d-credentials-test             ^|    Test read-only access to CUSTY_CREDENTIALS_REMOTE
	@echo.
	@echo   make d-run-validate                 ^|    Run the validate command
	@echo   make d-run-apply-version            ^|    Run version update
	@echo   make d-run-changelog                ^|    Run changelog generate
	@echo   make d-run-commit                   ^|    Create Git commit
	@echo   make d-run-tag                      ^|    Create Git tag
	@echo   make d-run-push                     ^|    Push commits and tags
	@echo   make d-run-dev                      ^|    Run daily development workflow
	@echo   make d-run-release                  ^|    Run release workflow
	@echo   make d-run-full                     ^|    Run full workflow
	@echo.
	@echo   make d-run-backup-commit            ^|    Backup commit message templates
	@echo   make d-run-backup-tag               ^|    Backup tag message templates
	@echo   make d-run-backup-all               ^|    Backup all templates
	@echo.
	@echo   make d-run-cleanup-backups          ^|    Remove backup files
	@echo   make d-run-cleanup-branches         ^|    Remove temporary branches
	@echo   make d-run-cleanup-all              ^|    Run complete cleanup workflow
	@echo.
	@echo   make d-workflow                     ^|    Run experimental workflow branch command

	@echo $(HELP_SEPARATOR)
	@echo.
