include $(ROOT_DIR)/make/core/help/variable.mk

# -------------------------------------------------------------------------
# 💡 EXAMPLES - Help
# -------------------------------------------------------------------------

.PHONY: help-examples
help-examples:
	@echo [Examples]
	@echo $(HELP_SEPARATOR)

	@echo   make l-init-all
	@echo   make l-run-full
	@echo.

	@echo   make d-init-all
	@echo   make d-run-full
	@echo.

	@echo   make c-init-all
	@echo   make c-run-full
	@echo.

	@echo   make r-custy-pull
	@echo   make r-custy-run-release
	@echo.

	@echo   make clean-all
	@echo.

	@echo   # --------------------------------------------------
	@echo   # Local Workflow
	@echo   # --------------------------------------------------
	@echo   make setup
	@echo   make l-init-all
	@echo   make l-run-validate
	@echo   make test
	@echo   make check
	@echo.

	@echo   # --------------------------------------------------
	@echo   # Release Workflow
	@echo   # --------------------------------------------------
	@echo   make l-run-dev
	@echo   make l-run-release
	@echo   make l-run-full
	@echo.

	@echo   # --------------------------------------------------
	@echo   # Docker Workflow
	@echo   # --------------------------------------------------
	@echo   make d-build-dev
	@echo   make d-init-all
	@echo   make d-run-validate
	@echo   make d-test
	@echo.

	@echo   # --------------------------------------------------
	@echo   # Docker Compose Workflow
	@echo   # --------------------------------------------------
	@echo   make c-build-dev
	@echo   make c-up
	@echo   make c-run-validate
	@echo   make c-check
	@echo.

	@echo   # --------------------------------------------------
	@echo   # Remote Custy Workflow
	@echo   # --------------------------------------------------
	@echo   make r-custy-pull
	@echo   make r-custy-init-all
	@echo   make r-custy-run-release
	@echo.

	@echo   # --------------------------------------------------
	@echo   # Cleanup Workflow
	@echo   # --------------------------------------------------
	@echo   make clean
	@echo   make clean-all
	@echo   make d-prune
	@echo.


	@echo $(HELP_SEPARATOR)
	@echo.
