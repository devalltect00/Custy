include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🧹 CLEANUP
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

PROJECT_CLEANUP_COMMANDS_LIST := \
	clean-cache \
	clean-build \
	clean-pyc \
	clean-coverage \
	clean-pip-cache \
	clean-venv \
	clean \
	clean-all

DOCKER_CLEANUP_COMMANDS_LIST := \
	d-remove-images \
	d-prune \
	d-prune-all


$(foreach cmd,$(PROJECT_CLEANUP_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		PROJECT_CLEANUP,$(cmd),LOCAL)))

$(foreach cmd,$(DOCKER_CLEANUP_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		DOCKER_CLEANUP,$(cmd),DOCKER COMPOSE)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

# 🧹 CLEANUP - CACHE
.PHONY: clean-cache
clean-cache:
	$(call REQUIRE_PYTHON)
	@echo Cleaning tool caches...
	@$(PYTHON_SYSTEM) -c "import shutil; \
for p in ['.pytest_cache', '.ruff_cache', '.mypy_cache']; \
	shutil.rmtree(p, ignore_errors=True)"
	@echo Cache cleanup completed.

# 🧹 CLEANUP - BUILD
.PHONY: clean-build
clean-build:
	$(call REQUIRE_PYTHON)
	@echo Cleaning build artifacts...
	@$(PYTHON_SYSTEM) -c "import shutil; \
for p in ['build', 'dist', 'htmlcov']; \
	shutil.rmtree(p, ignore_errors=True)"
	@$(PYTHON_SYSTEM) -c "import pathlib, shutil; \
[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').glob('*.egg-info')]"
	@echo Build cleanup completed.

# 🧹 CLEANUP - PYTHON CACHE
.PHONY: clean-pyc
clean-pyc:
	$(call REQUIRE_PYTHON)
	@echo Cleaning Python cache files...
	@$(PYTHON_SYSTEM) -c "import pathlib, shutil; \
[p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]; \
[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
	@echo Python cache cleanup completed.

# 🧹 CLEANUP - COVERAGE
.PHONY: clean-coverage
clean-coverage:
	$(call REQUIRE_PYTHON)
	@echo Cleaning coverage files...
	@$(PYTHON_SYSTEM) -c "import pathlib, shutil; \
[pathlib.Path('.coverage').unlink(missing_ok=True)]; \
shutil.rmtree('htmlcov', ignore_errors=True)"
	@echo Coverage cleanup completed.

# 🧹 CLEANUP - PIP CACHE
.PHONY: clean-pip-cache
clean-pip-cache:
	$(call REQUIRE_PYTHON)
	@echo Cleaning pip cache...
	@$(PYTHON_SYSTEM) -m pip cache purge
	@echo Pip cache cleanup completed.

# 🧹 CLEANUP - VIRTUAL ENVIRONMENT
.PHONY: clean-venv
clean-venv:
	@echo Removing virtual environment...
	@$(PYTHON_SYSTEM) -c "import pathlib, shutil; \
venv = pathlib.Path('$(VENV_NAME)'); \
shutil.rmtree(venv, ignore_errors=True) if venv.exists() else None"
	@echo Virtual environment removed.

# -------------------------------------------------------------------------
# 🧹 CLEANUP - AGGREGATE TARGETS
# -------------------------------------------------------------------------

.PHONY: clean
clean: clean-cache clean-build clean-pyc clean-coverage
	@echo Project cleanup completed.

.PHONY: clean-all
clean-all: clean clean-venv
	@echo Full project cleanup completed.

.PHONY: d-remove-images
d-remove-images: docker-check
	@echo Removing Docker images...
	-$(DOCKER) rmi $(DOCKER_IMAGE_BASE)
	-$(DOCKER) rmi $(DOCKER_IMAGE_DEV)
	-$(DOCKER) rmi $(DOCKER_IMAGE_PROD)
	@echo Docker image cleanup completed.

.PHONY: d-prune
d-prune: docker-check
	$(DOCKER) system prune -f

.PHONY: d-prune-all
d-prune-all: docker-check
	$(DOCKER) system prune -a -f --volumes
