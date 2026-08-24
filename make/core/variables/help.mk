include $(ROOT_DIR)/make/core/help/variable.mk

# -------------------------------------------------------------------------
# 🔡 VARIABLES - Help
# -------------------------------------------------------------------------

.PHONY: help-variables
help-variables:
	@echo [Common Variables]
	@echo $(HELP_SEPARATOR)

	@echo   TARGET=^<path^>                       ^|    Target directory to process
	@echo   WORKDIR=^<path^>                      ^|    Working directory
	@echo   VENV_NAME=^<name^>                    ^|    Virtual environment directory

	@echo.
	@echo   DOCKER_TAG=^<tag^>                    ^|    Docker image tag

	@echo.
	@echo   REMOTE_TAG=^<tag^>                    ^|    Remote image tag
	@echo   REMOTE_WORKSPACE=^<path^>             ^|    Workspace mounted into remote container
	@echo   DOCKER_SOCKET=^<path^>                 ^|    Docker socket used by Reflow dockerize

	@echo.
	@echo   REMOTE_REFLOW_GLOBAL_ARGS="args"       ^|    Global Reflow options and repository target
	@echo   REMOTE_REFLOW_INIT_ARGS="args"         ^|    Options passed to reflow init
	@echo   REMOTE_REFLOW_RELEASES_RECOVER_ARGS="args" ^| Options passed to releases recover
	@echo   REMOTE_REFLOW_TAGS_CONVERT_ARGS="args" ^|    Options passed to tags convert
	@echo   REMOTE_REFLOW_DOCKERIZE_ARGS="args"    ^|    Options passed to dockerize

	@echo.
	@echo   GHCR_OWNER=^<name^>                   ^|    GitHub Container Registry owner
	@echo   GHCR_REGISTRY=^<registry^>            ^|    Container registry host


	@echo $(HELP_SEPARATOR)
	@echo.
