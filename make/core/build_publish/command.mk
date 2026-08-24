include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 📦 BUILD & PUBLISH
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

BUILD_PUBLISH_COMMANDS_LIST := \
	build \
	publish \
	build-all

$(foreach cmd,$(BUILD_PUBLISH_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		BUILD_PUBLISH,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# 📦 BUILD & PUBLISH - 🛠️ INTERNAL HELPERS
# -------------------------------------------------------------------------

validate-package-resources:
	@echo.
	@echo ==============================================================
	@echo.
	@echo Validating packaged resources...
	$(DOCKER) run --rm --entrypoint python $(DOCKER_IMAGE_PROD) \
	-c "from importlib.resources import files; r=files('$(PROJECT_PACKAGE).templates').joinpath('config.toml'); assert r.is_file(); print('OK')"

# -------------------------------------------------------------------------
# 📦 BUILD & PUBLISH - build
# -------------------------------------------------------------------------

.PHONY: build
build: check-venv clean-cache
	"$(PYTHON)" -m $(BUILD)

.PHONY: publish
publish: check-venv
	"$(PYTHON)" -m $(TWINE) upload dist/*

.PHONY: build-all
build-all: build d-build-all
