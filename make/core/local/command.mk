include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🚀 LOCAL COMMANDS
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

LOCAL_INITIALIZATION_COMMANDS_LIST := \
	l-init \
	l-init-force \
	l-init-ask \
	l-init-all \
	l-init-all-no-examples \
	l-init-config \
	l-init-templates \
	l-init-examples

LOCAL_RUN_COMMANDS_LIST := \
	l-run \
	l-run-validate \
	l-run-apply-version \
	l-run-changelog \
	l-run-commit \
	l-run-tag \
	l-run-push \
	l-run-dev \
	l-run-release \
	l-run-full \
	l-run-backup-commit \
	l-run-backup-tag \
	l-run-backup-all \
	l-run-cleanup-backups \
	l-run-cleanup-branches \
	l-run-cleanup-all \
	l-workflow

$(foreach cmd,$(LOCAL_INITIALIZATION_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		LOCAL_INITIALIZATION,$(cmd),LOCAL)))

$(foreach cmd,$(LOCAL_RUN_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		LOCAL_RUN,$(cmd),LOCAL)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

.PHONY: l-init
l-init: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		init \
		$(LOCAL_CUSTY_INIT_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-init-force
l-init-force:
	@$(MAKE) l-init \
		LOCAL_CUSTY_INIT_ARGS="--force"

.PHONY: l-init-ask
l-init-ask:
	@$(MAKE) l-init \
		LOCAL_CUSTY_INIT_ARGS="--ask"

.PHONY: l-init-all
l-init-all:
	@$(MAKE) l-init \
		LOCAL_CUSTY_INIT_ARGS="--mode all"

.PHONY: l-init-config
l-init-config:
	@$(MAKE) l-init \
		LOCAL_CUSTY_INIT_ARGS="--mode config"

.PHONY: l-init-all-no-examples
l-init-all-no-examples:
	@$(MAKE) l-init \
		LOCAL_CUSTY_INIT_ARGS="--mode all_no_examples"

.PHONY: l-init-templates
l-init-templates:
	@$(MAKE) l-init \
		LOCAL_CUSTY_INIT_ARGS="--mode templates"

.PHONY: l-init-examples
l-init-examples:
	@$(MAKE) l-init \
		LOCAL_CUSTY_INIT_ARGS="--mode examples"

# --------------------------------------------------
# Run - Base
# --------------------------------------------------

##### References
# .PHONY: l-run
# l-run:
# 	# Add validation
# 	@if [ -z "$(LOCAL_CUSTY_RUN_SUBCOMMAND)" ]; then \
# 		echo "Error: LOCAL_CUSTY_RUN_SUBCOMMAND is required"; \
# 		exit 1; \
# 	fi

.PHONY: l-run
l-run: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		run \
		$(LOCAL_CUSTY_RUN_SUBCOMMAND) \
		$(LOCAL_CUSTY_RUN_ARGS) \
		$(LOCAL_CUSTY_RUN_SUBCOMMAND_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

# --------------------------------------------------
# Run - Command
# --------------------------------------------------

.PHONY: l-run-validate
l-run-validate: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		validate \
		$(LOCAL_CUSTY_VALIDATE_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-run-apply-version
l-run-apply-version: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		version update \
		$(LOCAL_CUSTY_VERSION_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-run-changelog
l-run-changelog: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		changelog generate \
		$(LOCAL_CUSTY_CHANGELOG_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-run-commit
l-run-commit:
	@$(MAKE) l-run \
		LOCAL_CUSTY_RUN_SUBCOMMAND="commit" \
		LOCAL_CUSTY_RUN_SUBCOMMAND_ARGS="$(LOCAL_CUSTY_COMMIT_ARGS)"

.PHONY: l-run-tag
l-run-tag:
	@$(MAKE) l-run \
		LOCAL_CUSTY_RUN_SUBCOMMAND="tag" \
		LOCAL_CUSTY_RUN_SUBCOMMAND_ARGS="$(LOCAL_CUSTY_TAG_ARGS)"

.PHONY: l-run-push
l-run-push:
	@$(MAKE) l-run \
		LOCAL_CUSTY_RUN_SUBCOMMAND="push" \
		LOCAL_CUSTY_RUN_SUBCOMMAND_ARGS="$(LOCAL_CUSTY_PUSH_ARGS)"

.PHONY: l-run-dev
l-run-dev:
	@$(MAKE) l-run \
		LOCAL_CUSTY_RUN_SUBCOMMAND="dev" \
		LOCAL_CUSTY_RUN_SUBCOMMAND_ARGS="$(LOCAL_CUSTY_RUN_DEV_ARGS)"

.PHONY: l-run-release
l-run-release:
	@$(MAKE) l-run \
		LOCAL_CUSTY_RUN_SUBCOMMAND="release" \
		LOCAL_CUSTY_RUN_SUBCOMMAND_ARGS="$(LOCAL_CUSTY_RUN_RELEASE_ARGS)"

.PHONY: l-run-full
l-run-full:
	@$(MAKE) l-run \
		LOCAL_CUSTY_RUN_SUBCOMMAND="full" \
		LOCAL_CUSTY_RUN_SUBCOMMAND_ARGS="$(LOCAL_CUSTY_RUN_FULL_ARGS)"

.PHONY: l-run-backup-commit
l-run-backup-commit: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		backup commit \
		$(LOCAL_CUSTY_BACKUP_ARGS) \
		$(LOCAL_CUSTY_BACKUP_COMMIT_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-run-backup-tag
l-run-backup-tag: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		backup tag \
		$(LOCAL_CUSTY_BACKUP_ARGS) \
		$(LOCAL_CUSTY_BACKUP_TAG_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-run-backup-all
l-run-backup-all: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		backup all \
		$(LOCAL_CUSTY_BACKUP_ARGS) \
		$(LOCAL_CUSTY_BACKUP_ALL_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-run-cleanup-backups
l-run-cleanup-backups: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		cleanup backups \
		$(LOCAL_CUSTY_CLEANUP_ARGS) \
		$(LOCAL_CUSTY_CLEANUP_BACKUPS_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-run-cleanup-branches
l-run-cleanup-branches: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		cleanup branches \
		$(LOCAL_CUSTY_CLEANUP_ARGS) \
		$(LOCAL_CUSTY_CLEANUP_BRANCHES_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

.PHONY: l-run-cleanup-all
l-run-cleanup-all: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		cleanup all \
		$(LOCAL_CUSTY_CLEANUP_ARGS) \
		$(LOCAL_CUSTY_CLEANUP_ALL_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)

# Still in development
.PHONY: l-workflow
l-workflow: check-venv
	$(LOCAL_RUN) \
		$(LOCAL_CUSTY_GLOBAL_ARGS) \
		workflow branch \
		$(LOCAL_CUSTY_WORKFLOW_ARGS) \
		$(LOCAL_CUSTY_EXTRA_ARGS)
