include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🔧 GIT UTILITIES
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

GIT_COMMANDS_LIST := \
	git-current-branch \
	git-url-origin \
	git-log \
	git-tags

$(foreach cmd,$(GIT_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		GIT,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

.PHONY: git-current-branch
git-current-branch:
	git branch --show-current

.PHONY: git-url-origin
git-url-origin:
	git remote get-url origin

.PHONY: git-log
git-log:
	git log --oneline --graph --decorate --all -n 25

.PHONY: git-tags
git-tags:
	git log --no-walk --tags --pretty="format:%h %d %s"
