include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🐋 DOCKER RUN (DEV)
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

DOCKER_TESTING_COMMANDS_LIST := \
	d-test \

DOCKER_INITIALIZATION_COMMANDS_LIST := \
	d-init \
	d-init-force \
	d-init-ask \
	d-init-all \
	d-init-all-no-examples \
	d-init-config \
	d-init-templates \
	d-init-examples

DOCKER_RUN_COMMANDS_LIST := \
	d-run \
	d-run-validate \
	d-run-apply-version \
	d-run-changelog \
	d-run-commit \
	d-run-tag \
	d-run-push \
	d-run-dev \
	d-run-release \
	d-run-full \
	d-run-backup-commit \
	d-run-backup-tag \
	d-run-backup-all \
	d-run-cleanup-backups \
	d-run-cleanup-branches \
	d-run-cleanup-all \
	d-workflow

$(foreach cmd,$(DOCKER_TESTING_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		DOCKER_TESTING,$(cmd),DOCKER)))

$(foreach cmd,$(DOCKER_INITIALIZATION_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		DOCKER_INITIALIZATION,$(cmd),DOCKER)))

$(foreach cmd,$(DOCKER_RUN_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		DOCKER_RUN,$(cmd),DOCKER)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

.PHONY: d-test
d-test: d-build-dev
	$(DOCKER_RUN_NO_ENTRYPOINT) $(DOCKER_WORKSPACE) $(DOCKER_IMAGE_DEV) python -m pytest -v

# =========================================================
# 🐋 DOCKER RUN (PROD)
# =========================================================

.PHONY: d-init
d-init: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		init \
		$(DOCKER_CUSTY_INIT_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-init-force
d-init-force: docker-check
	@$(MAKE) d-init \
		DOCKER_CUSTY_INIT_ARGS="--force"

.PHONY: d-init-ask
d-init-ask: docker-check
	@$(MAKE) d-init \
		DOCKER_CUSTY_INIT_ARGS="--ask"

.PHONY: d-init-all
d-init-all: docker-check
	@$(MAKE) d-init \
		DOCKER_CUSTY_INIT_ARGS="--mode all"

.PHONY: d-init-config
d-init-config: docker-check
	@$(MAKE) d-init \
		DOCKER_CUSTY_INIT_ARGS="--mode config"

.PHONY: d-init-all-no-examples
d-init-all-no-examples: docker-check
	@$(MAKE) d-init \
		DOCKER_CUSTY_INIT_ARGS="--mode all_no_examples"

.PHONY: d-init-templates
d-init-templates: docker-check
	@$(MAKE) d-init \
		DOCKER_CUSTY_INIT_ARGS="--mode templates"

.PHONY: d-init-examples
d-init-examples: docker-check
	@$(MAKE) d-init \
		DOCKER_CUSTY_INIT_ARGS="--mode examples"

.PHONY: d-run
d-run: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		run \
		$(DOCKER_CUSTY_RUN_SUBCOMMAND) \
		$(DOCKER_CUSTY_RUN_ARGS) \
		$(DOCKER_CUSTY_RUN_SUBCOMMAND_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-validate
d-run-validate: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		validate \
		$(DOCKER_CUSTY_VALIDATE_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-apply-version
d-run-apply-version: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		version update \
		$(DOCKER_CUSTY_VERSION_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-changelog
d-run-changelog: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		changelog generate \
		$(DOCKER_CUSTY_CHANGELOG_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-commit
d-run-commit:
	@$(MAKE) d-run \
		DOCKER_CUSTY_RUN_SUBCOMMAND="commit" \
		DOCKER_CUSTY_RUN_SUBCOMMAND_ARGS="$(DOCKER_CUSTY_COMMIT_ARGS)"

.PHONY: d-run-tag
d-run-tag:
	@$(MAKE) d-run \
		DOCKER_CUSTY_RUN_SUBCOMMAND="tag" \
		DOCKER_CUSTY_RUN_SUBCOMMAND_ARGS="$(DOCKER_CUSTY_TAG_ARGS)"

.PHONY: d-run-push
d-run-push:
	@$(MAKE) d-run \
		DOCKER_CUSTY_RUN_SUBCOMMAND="push" \
		DOCKER_CUSTY_RUN_SUBCOMMAND_ARGS="$(DOCKER_CUSTY_PUSH_ARGS)"

.PHONY: d-run-dev
d-run-dev:
	@$(MAKE) d-run \
		DOCKER_CUSTY_RUN_SUBCOMMAND="dev" \
		DOCKER_CUSTY_RUN_SUBCOMMAND_ARGS="$(DOCKER_CUSTY_RUN_DEV_ARGS)"

.PHONY: d-run-release
d-run-release:
	@$(MAKE) d-run \
		DOCKER_CUSTY_RUN_SUBCOMMAND="release" \
		DOCKER_CUSTY_RUN_SUBCOMMAND_ARGS="$(DOCKER_CUSTY_RUN_RELEASE_ARGS)"

.PHONY: d-run-full
d-run-full:
	@$(MAKE) d-run \
		DOCKER_CUSTY_RUN_SUBCOMMAND="full" \
		DOCKER_CUSTY_RUN_SUBCOMMAND_ARGS="$(DOCKER_CUSTY_RUN_FULL_ARGS)"

.PHONY: d-run-backup-commit
d-run-backup-commit: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		backup commit \
		$(DOCKER_CUSTY_BACKUP_ARGS) \
		$(DOCKER_CUSTY_BACKUP_COMMIT_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-backup-tag
d-run-backup-tag: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		backup tag \
		$(DOCKER_CUSTY_BACKUP_ARGS) \
		$(DOCKER_CUSTY_BACKUP_TAG_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-backup-all
d-run-backup-all: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		backup all \
		$(DOCKER_CUSTY_BACKUP_ARGS) \
		$(DOCKER_CUSTY_BACKUP_ALL_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-cleanup-backups
d-run-cleanup-backups: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		cleanup backups \
		$(DOCKER_CUSTY_CLEANUP_ARGS) \
		$(DOCKER_CUSTY_CLEANUP_BACKUPS_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-cleanup-branches
d-run-cleanup-branches: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		cleanup branches \
		$(DOCKER_CUSTY_CLEANUP_ARGS) \
		$(DOCKER_CUSTY_CLEANUP_BRANCHES_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

.PHONY: d-run-cleanup-all
d-run-cleanup-all: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		cleanup all \
		$(DOCKER_CUSTY_CLEANUP_ARGS) \
		$(DOCKER_CUSTY_CLEANUP_ALL_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)

# Still in development
.PHONY: d-workflow
d-workflow: docker-check
	$(DOCKER_RUN_INTERACTIVE) \
	$(DOCKER_WORKSPACE) \
	$(DOCKER_IMAGE_PROD) \
		$(DOCKER_CUSTY_GLOBAL_ARGS) \
		workflow branch \
		$(DOCKER_CUSTY_WORKFLOW_ARGS) \
		$(DOCKER_CUSTY_EXTRA_ARGS)
