include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🧪 TESTING
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

TESTING_COMMANDS_LIST := \
	test \
	test-verbose \
	test-cov \
	test-cov-html

$(foreach cmd,$(TESTING_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		TESTING,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

.PHONY: test
test: check-venv
	@echo =========================================================
	@echo Running tests
	@echo =========================================================
	"$(PYTHON)" -m $(PYTEST)

.PHONY: test-verbose
test-verbose: check-venv
	@echo =========================================================
	@echo Running tests (verbose)
	@echo =========================================================
	"$(PYTHON)" -m $(PYTEST) -v

.PHONY: test-cov
test-cov: check-venv
	@echo =========================================================
	@echo Running tests with coverage
	@echo =========================================================
	"$(PYTHON)" -m $(PYTEST) \
		--cov=$(PROJECT_PACKAGE) \
		--cov-report=term-missing

.PHONY: test-cov-html
test-cov-html: check-venv
	@echo =========================================================
	@echo Running tests with HTML coverage report
	@echo =========================================================
	"$(PYTHON)" -m $(PYTEST) \
		--cov=$(PROJECT_PACKAGE) \
		--cov-report=html
