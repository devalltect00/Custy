include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - HELP
# -------------------------------------------------------------------------

.PHONY: help-setup-installation
help-setup-installation:
	@echo [Setup ^& Installation] (Total: $(call COMMAND_COUNT,SETUP_INSTALL))
	@echo $(HELP_SEPARATOR)

	@echo   make venv                           ^|    Create virtual environment
	@echo   make activate                       ^|    Show virtual environment activation commands
	@echo.
	@echo   make install                        ^|    Install package
	@echo   make install-dev                    ^|    Install package with development dependencies
	@echo   make install-docs                   ^|    Install package with documentation dependencies
	@echo   make install-all                    ^|    Install package with all optional dependencies
	@echo.
	@echo   make upgrade-pip                    ^|    Upgrade pip inside virtual environment
	@echo   make requirements                   ^|    Generate requirements.txt from installed packages
	@echo.
	@echo   make pre-commit-install             ^|    Install the pre-commit Git hook
	@echo   make pre-commit-install-hooks       ^|    Install the Git hook and hook environments
	@echo   make pre-commit-run                 ^|    Run all hooks against all repository files
	@echo   make pre-commit-run-staged          ^|    Run hooks against currently staged files
	@echo   make pre-commit-update              ^|    Update hook revisions in the pre-commit config
	@echo   make pre-commit-clean               ^|    Remove cached pre-commit hook environments
	@echo   make pre-commit-gc                  ^|    Remove unused pre-commit cached repositories
	@echo   make pre-commit-uninstall           ^|    Remove the pre-commit Git hook
	@echo   make pre-commit-validate            ^|    Validate .pre-commit-config.yaml
	@echo   make pre-commit-refresh             ^|    Update, clean, reinstall, and run all pre-commit hooks
	@echo.
	@echo   make setup                          ^|    Run complete project setup workflow
	@echo   make check-python                   ^|    Show system Python version

	@echo $(HELP_SEPARATOR)
	@echo.
