# =========================================================
# 📦 COMMAND REGISTRY
# =========================================================

# ALL_COMMANDS :=

# -------------------------------------------------------------------------
# 📦 Register Command
#
# Usage:
#   $(eval $(call REGISTER_COMMAND,\
		GIT,git-log))
#
# Creates:
#   GIT_COMMANDS += git-log
#   ALL_COMMANDS += git-log
# -------------------------------------------------------------------------

define REGISTER_COMMAND
	$(1)_COMMANDS += $(2)

	$(foreach grp,$(3),\
		$(eval $(grp)_COMMANDS += $(2)))

	COMMAND_GROUPS_$(2) := $(3)

	ALL_COMMANDS += $(2)
endef

# -------------------------------------------------------------------------
# 📦 Count Helpers
# -------------------------------------------------------------------------

COMMAND_COUNT = $(words $($(1)_COMMANDS))
