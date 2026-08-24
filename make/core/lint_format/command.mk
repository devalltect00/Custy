include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🧶 LINT & FORMAT
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

LINT_FORMAT_COMMANDS_LIST := \
	lint \
	lint-fix \
	lint-fix-unsafe \
	format-ruff \
	format \
	format-check

$(foreach cmd,$(LINT_FORMAT_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		LINT_FORMAT,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

##### RUFF + BLACK

.PHONY: lint
lint: check-venv
	@echo =========================================================
	@echo Running lint checks (ruff)
	@echo =========================================================
	"$(PYTHON)" -m $(RUFF) check $(SOURCE_DIRS)

.PHONY: lint-fix
lint-fix: check-venv
	@echo =========================================================
	@echo Fixing lint issues (ruff)
	@echo =========================================================
	"$(PYTHON)" -m $(RUFF) check $(SOURCE_DIRS) --fix

.PHONY: lint-fix-unsafe
lint-fix-unsafe:
	@echo =========================================================
	@echo Fixing lint issues (ruff) with unsafe-fixes
	@echo =========================================================
	$(PYTHON) -m $(RUFF) check $(SOURCE_DIRS) --fix --unsafe-fixes

.PHONY: format-ruff
format-ruff: check-venv
	@echo =========================================================
	@echo Formatting code (ruff formatter)
	@echo =========================================================
	"$(PYTHON)" -m $(RUFF) format $(SOURCE_DIRS)

.PHONY: format
format: check-venv
	@echo =========================================================
	@echo Formatting code (black)
	@echo =========================================================
	"$(PYTHON)" -m $(BLACK) $(SOURCE_DIRS)

.PHONY: format-check
format-check: check-venv
	@echo =========================================================
	@echo Checking code format (black)
	@echo =========================================================
	@"$(PYTHON)" -m $(BLACK) $(SOURCE_DIRS) --check || ( \
		echo. && \
		echo Code is not formatted. Run 'make format' first. && \
		exit 1 \
	)
