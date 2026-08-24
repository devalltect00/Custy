# Makefile for custy

# =========================================================
# Makefile Root Directory
# =========================================================

ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))


# =========================================================
#
# 🔡 VARIABLES
#
# =========================================================

include $(ROOT_DIR)/make/core/variables/variable.mk

# =========================================================
# 🌐 Remote Helpers
# =========================================================

include $(ROOT_DIR)/make/core/helpers/common.mk


# =========================================================
# ⚙️ SETUP & INSTALLATION
# =========================================================

include $(ROOT_DIR)/make/core/setup_install/command.mk


# =========================================================
# 🚀 LOCAL COMMANDS
# =========================================================

include $(ROOT_DIR)/make/core/local/command.mk


# =========================================================
# 🧪 TESTING
# =========================================================

include $(ROOT_DIR)/make/core/testing/command.mk


# =========================================================
# 🧶 LINT & FORMAT
# =========================================================

include $(ROOT_DIR)/make/core/lint_format/command.mk
include $(ROOT_DIR)/make/core/qa/command.mk
include $(ROOT_DIR)/make/core/ci/command.mk


# =========================================================
# 📚 Documentation
# =========================================================

include $(ROOT_DIR)/make/core/documentation/command.mk


# =========================================================
# 📦 BUILD & PUBLISH
# =========================================================

include $(ROOT_DIR)/make/core/build_publish/command.mk


# =========================================================
# 🐋 DOCKER BUILD
# =========================================================

include $(ROOT_DIR)/make/core/docker/command/common.mk


# =========================================================
# 🐋 DOCKER RUN
# =========================================================

include $(ROOT_DIR)/make/core/docker/command/core.mk


# =========================================================
# 🐋 DOCKER COMPOSE
# =========================================================

include $(ROOT_DIR)/make/core/compose/command/common.mk


# =========================================================
# 🐋 DOCKER COMPOSE RUN PROJECT
# =========================================================

include $(ROOT_DIR)/make/core/compose/command/core.mk


# =========================================================
# 🌐 Remote Registry Commands
# =========================================================

include $(ROOT_DIR)/make/core/remote/command/registry.mk


# =========================================================
# 🌐 Remote Runtime Commands
# =========================================================

include $(ROOT_DIR)/make/core/remote/command/runtime.mk


# =========================================================
# 🔧 GIT UTILITIES
# =========================================================

include $(ROOT_DIR)/make/core/git/command.mk


# =========================================================
# 🧹 CLEANUP
# =========================================================

include $(ROOT_DIR)/make/core/cleanup/command.mk


# =========================================================
# 🆘 HELP
# =========================================================

include $(ROOT_DIR)/make/core/help/command.mk
