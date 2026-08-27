include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# ⚙️ SETUP & INSTALLATION
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

SETUP_INSTALL_COMMANDS_LIST := \
	venv activate install install-dev install-docs install-all upgrade-pip \
	requirements pre-commit-install pre-commit-install-hooks pre-commit-run \
	pre-commit-run-staged pre-commit-update pre-commit-clean pre-commit-gc \
	pre-commit-uninstall pre-commit-validate pre-commit-refresh setup check-python

$(foreach cmd,$(SETUP_INSTALL_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		SETUP_INSTALL,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - 🛠️ INTERNAL HELPERS
# -------------------------------------------------------------------------

.PHONY: check-venv
check-venv:
ifeq ($(PLATFORM),windows)
	@if not exist "$(PYTHON)" ( \
		echo Virtual environment not found. Run 'make venv' first. && exit 1 \
	)
else
	@test -f "$(PYTHON)" || ( \
		echo "Virtual environment not found. Run 'make venv' first."; \
		exit 1 \
	)
endif

# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - Python Environment
# -------------------------------------------------------------------------

.PHONY: venv
venv:
	$(call REQUIRE_PYTHON)
	"$(PYTHON_SYSTEM)" -m venv $(VENV_NAME)
	@echo.
	@echo =========================================================
	@echo Virtual environment created successfully.
	@echo =========================================================
	@echo.

.PHONY: activate
activate:
	@echo.
	@echo =========================================================
	@echo Activation Commands
	@echo =========================================================
	@echo.
ifeq ($(PLATFORM),windows)
	@echo CMD:
	@echo   $(ACTIVATE_COMMAND)
	@echo.
	@echo PowerShell:
	@echo   $(ACTIVATE_COMMAND_PS)
else
	@echo $(ACTIVATE_COMMAND)
endif
	@echo.


# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - Installation
# -------------------------------------------------------------------------

.PHONY: install
install: check-venv
	"$(PIP)" install -e .

.PHONY: install-dev
install-dev: check-venv
	"$(PIP)" install -e ".[dev]"

.PHONY: install-docs
install-docs: check-venv
	"$(PIP)" install -e ".[docs]"

.PHONY: install-all
install-all: check-venv
	"$(PIP)" install -e ".[dev,docs]"


# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - Python Pip
# -------------------------------------------------------------------------

.PHONY: upgrade-pip
upgrade-pip: check-venv
	"$(PIP)" install --upgrade pip

# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - REQUIREMENTS
# -------------------------------------------------------------------------

.PHONY: requirements
requirements: check-venv
	@echo.
	@echo =========================================================
	@echo Generating requirements.txt from virtual environment...
	@echo =========================================================
	@echo.
	@"$(PYTHON)" -c "import subprocess; \
prefixes = tuple('$(REQUIREMENTS_EXCLUDE_PREFIXES)'.split()); \
req = subprocess.check_output([r'$(PIP)', 'freeze'], text=True); \
filtered = '\n'.join(line for line in req.splitlines() if not line.startswith(prefixes)); \
open('requirements.txt', 'w').write(filtered + '\n')"
	@echo Cleaning comment lines from requirements.txt...
	@"$(PYTHON)" -c "from pathlib import Path; \
p = Path('requirements.txt'); \
lines = p.read_text().splitlines(); \
cleaned = '\n'.join(line for line in lines if not line.lstrip().startswith('# Editable install')); \
p.write_text(cleaned + '\n')"
	@echo.
	@echo requirements.txt generated successfully (filtered).


# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - Pre-Commit
# -------------------------------------------------------------------------

.PHONY: \
	pre-commit-install \
	pre-commit-install-hooks \
	pre-commit-run \
	pre-commit-run-staged \
	pre-commit-update \
	pre-commit-clean \
	pre-commit-gc \
	pre-commit-uninstall \
	pre-commit-validate \
	pre-commit-refresh

pre-commit-install: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) install

pre-commit-install-hooks: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) install --install-hooks

pre-commit-run: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) run --all-files

pre-commit-run-staged: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) run

pre-commit-update: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) autoupdate

pre-commit-clean: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) clean

pre-commit-gc: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) gc

pre-commit-uninstall: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) uninstall

pre-commit-validate: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) validate-config .pre-commit-config.yaml

pre-commit-refresh: check-venv
	"$(PYTHON)" -m $(PRE_COMMIT) autoupdate
	"$(PYTHON)" -m $(PRE_COMMIT) clean
	"$(PYTHON)" -m $(PRE_COMMIT) install --install-hooks
	"$(PYTHON)" -m $(PRE_COMMIT) run --all-files


# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - Full Setup
# -------------------------------------------------------------------------

.PHONY: setup
setup: venv upgrade-pip install-all pre-commit-install
	@echo.
	@echo =========================================================
	@echo Project setup completed successfully.
	@echo =========================================================
	@echo.


# -------------------------------------------------------------------------
# ⚙️ SETUP & INSTALLATION - Others
# -------------------------------------------------------------------------

.PHONY: check-python
check-python:
	"$(PYTHON_SYSTEM)" --version
