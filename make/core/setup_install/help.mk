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
	@echo   make pre-commit-install             ^|    Install pre-commit Git hooks
	@echo   make pre-commit-run                 ^|    Run pre-commit hooks manually
	@echo   make pre-commit-update              ^|    Update pre-commit hook versions
	@echo.
	@echo   make setup                          ^|    Run complete project setup workflow
	@echo   make check-python                   ^|    Show system Python version

	@echo $(HELP_SEPARATOR)
	@echo.
