include $(ROOT_DIR)/make/core/help/variable.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# -------------------------------------------------------------------------
# 🧹 PROJECT CLEANUP - Help
# -------------------------------------------------------------------------

.PHONY: help-cleanup-project
help-cleanup-project:
	@echo [Project Cleanup] (Total: $(call COMMAND_COUNT,PROJECT_CLEANUP))
	@echo $(HELP_SEPARATOR)

	@echo   make clean-cache                    ^|    Remove tool cache directories
	@echo   make clean-build                    ^|    Remove build artifacts
	@echo   make clean-pyc                      ^|    Remove Python cache files
	@echo   make clean-coverage                 ^|    Remove coverage files and reports
	@echo   make clean-pip-cache                ^|    Remove pip cache
	@echo   make clean-venv                     ^|    Remove virtual environment
	@echo.
	@echo   make clean                          ^|    Run standard project cleanup
	@echo   make clean-all                      ^|    Run complete project cleanup

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🐳 DOCKER CLEANUP - Help
# -------------------------------------------------------------------------

.PHONY: help-cleanup-docker
help-cleanup-docker:
	@echo [Docker Cleanup] (Total: $(call COMMAND_COUNT,DOCKER_CLEANUP))
	@echo $(HELP_SEPARATOR)

	@echo   make d-remove-images                ^|    Remove project Docker images
	@echo   make d-prune                        ^|    Remove unused Docker resources
	@echo   make d-prune-all                    ^|    Remove all unused Docker resources and volumes

	@echo $(HELP_SEPARATOR)
	@echo.
