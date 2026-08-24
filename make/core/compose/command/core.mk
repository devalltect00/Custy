include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🐋 DOCKER COMPOSE RUN PROJECT
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

COMPOSE_INIT_COMMANDS_LIST := \
	c-init \
	c-init-force \
	c-init-ask \
	c-init-all \
	c-init-all-no-examples \
	c-init-config \
	c-init-templates \
	c-init-examples

COMPOSE_RUN_COMMANDS_LIST := \
	c-run \
	c-run-validate \
	c-run-apply-version \
	c-run-changelog \
	c-run-commit \
	c-run-tag \
	c-run-push \
	c-run-dev \
	c-run-release \
	c-run-full \
	c-run-backup-commit \
	c-run-backup-tag \
	c-run-backup-all \
	c-run-cleanup-backups \
	c-run-cleanup-branches \
	c-run-cleanup-all \
	c-workflow

COMPOSE_UTILITIES_COMMANDS_LIST := \
	c-test \
	c-lint \
	c-lint-fix \
	c-format \
	c-format-check \
	c-docs \
	c-shell \
	c-build-package \
	c-exec-shell \
	c-fix \
	c-check \
	c-qa \
	c-ci

$(foreach cmd,$(COMPOSE_INIT_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		COMPOSE_INIT,$(cmd),COMPOSE)))

$(foreach cmd,$(COMPOSE_RUN_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		COMPOSE_RUN,$(cmd),COMPOSE)))

$(foreach cmd,$(COMPOSE_UTILITIES_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		COMPOSE_UTILITIES,$(cmd),COMPOSE)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# 🐋 DOCKER COMPOSE - CORE
# -------------------------------------------------------------------------

.PHONY: c-init
c-init: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		init \
		$(COMPOSE_CUSTY_INIT_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-init-force
c-init-force: docker-check
	@$(MAKE) c-init \
		COMPOSE_CUSTY_INIT_ARGS="--force"

.PHONY: c-init-ask
c-init-ask: docker-check
	@$(MAKE) c-init \
		COMPOSE_CUSTY_INIT_ARGS="--ask"

.PHONY: c-init-all
c-init-all: docker-check
	@$(MAKE) c-init \
		COMPOSE_CUSTY_INIT_ARGS="--mode all"

.PHONY: c-init-config
c-init-config: docker-check
	@$(MAKE) c-init \
		COMPOSE_CUSTY_INIT_ARGS="--mode config"

.PHONY: c-init-all-no-examples
c-init-all-no-examples: docker-check
	@$(MAKE) c-init \
		COMPOSE_CUSTY_INIT_ARGS="--mode all_no_examples"

.PHONY: c-init-templates
c-init-templates: docker-check
	@$(MAKE) c-init \
		COMPOSE_CUSTY_INIT_ARGS="--mode templates"

.PHONY: c-init-examples
c-init-examples: docker-check
	@$(MAKE) c-init \
		COMPOSE_CUSTY_INIT_ARGS="--mode examples"

.PHONY: c-run
c-run: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		run \
		$(COMPOSE_CUSTY_RUN_SUBCOMMAND) \
		$(COMPOSE_CUSTY_RUN_ARGS) \
		$(COMPOSE_CUSTY_RUN_SUBCOMMAND_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-validate
c-run-validate: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		validate \
		$(COMPOSE_CUSTY_VALIDATE_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-apply-version
c-run-apply-version: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		version update \
		$(COMPOSE_CUSTY_VERSION_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-changelog
c-run-changelog: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		changelog generate \
		$(COMPOSE_CUSTY_CHANGELOG_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-commit
c-run-commit:
	@$(MAKE) c-run \
		COMPOSE_CUSTY_RUN_SUBCOMMAND="commit" \
		COMPOSE_CUSTY_RUN_SUBCOMMAND_ARGS="$(COMPOSE_CUSTY_COMMIT_ARGS)"

.PHONY: c-run-tag
c-run-tag:
	@$(MAKE) c-run \
		COMPOSE_CUSTY_RUN_SUBCOMMAND="tag" \
		COMPOSE_CUSTY_RUN_SUBCOMMAND_ARGS="$(COMPOSE_CUSTY_TAG_ARGS)"

.PHONY: c-run-push
c-run-push:
	@$(MAKE) c-run \
		COMPOSE_CUSTY_RUN_SUBCOMMAND="push" \
		COMPOSE_CUSTY_RUN_SUBCOMMAND_ARGS="$(COMPOSE_CUSTY_PUSH_ARGS)"

.PHONY: c-run-dev
c-run-dev:
	@$(MAKE) c-run \
		COMPOSE_CUSTY_RUN_SUBCOMMAND="dev" \
		COMPOSE_CUSTY_RUN_SUBCOMMAND_ARGS="$(COMPOSE_CUSTY_RUN_DEV_ARGS)"

.PHONY: c-run-release
c-run-release:
	@$(MAKE) c-run \
		COMPOSE_CUSTY_RUN_SUBCOMMAND="release" \
		COMPOSE_CUSTY_RUN_SUBCOMMAND_ARGS="$(COMPOSE_CUSTY_RUN_RELEASE_ARGS)"

.PHONY: c-run-full
c-run-full:
	@$(MAKE) c-run \
		COMPOSE_CUSTY_RUN_SUBCOMMAND="full" \
		COMPOSE_CUSTY_RUN_SUBCOMMAND_ARGS="$(COMPOSE_CUSTY_RUN_FULL_ARGS)"

.PHONY: c-run-backup-commit
c-run-backup-commit: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		backup commit \
		$(COMPOSE_CUSTY_BACKUP_ARGS) \
		$(COMPOSE_CUSTY_BACKUP_COMMIT_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-backup-tag
c-run-backup-tag: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		backup tag \
		$(COMPOSE_CUSTY_BACKUP_ARGS) \
		$(COMPOSE_CUSTY_BACKUP_TAG_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-backup-all
c-run-backup-all: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		backup all \
		$(COMPOSE_CUSTY_BACKUP_ARGS) \
		$(COMPOSE_CUSTY_BACKUP_ALL_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-cleanup-backups
c-run-cleanup-backups: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		cleanup backups \
		$(COMPOSE_CUSTY_CLEANUP_ARGS) \
		$(COMPOSE_CUSTY_CLEANUP_BACKUPS_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-cleanup-branches
c-run-cleanup-branches: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		cleanup branches \
		$(COMPOSE_CUSTY_CLEANUP_ARGS) \
		$(COMPOSE_CUSTY_CLEANUP_BRANCHES_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

.PHONY: c-run-cleanup-all
c-run-cleanup-all: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		cleanup all \
		$(COMPOSE_CUSTY_CLEANUP_ARGS) \
		$(COMPOSE_CUSTY_CLEANUP_ALL_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)

# Still in development
.PHONY: c-workflow
c-workflow: docker-check
	$(COMPOSE_PROD_RUN_APP) \
		$(COMPOSE_CUSTY_GLOBAL_ARGS) \
		workflow branch \
		$(COMPOSE_CUSTY_WORKFLOW_ARGS) \
		$(COMPOSE_CUSTY_EXTRA_ARGS)


# -------------------------------------------------------------------------
# 🐋 DOCKER COMPOSE - ADDITIONAL
# -------------------------------------------------------------------------

.PHONY: c-test
c-test: c-build-dev
	$(COMPOSE_DEV_RUN_TEST)

.PHONY: c-lint
c-lint: c-build-dev
	$(COMPOSE_DEV_RUN_LINT)

.PHONY: c-lint-fix
c-lint-fix: c-build-dev
	$(COMPOSE_DEV_RUN_LINT_FIX)

.PHONY: c-format
c-format: c-build-dev
	$(COMPOSE_DEV_RUN_FORMAT)

.PHONY: c-format-check
c-format-check: c-build-dev
	$(COMPOSE_DEV_RUN_FORMAT_CHECK)

.PHONY: c-docs
c-docs: docker-check
	$(COMPOSE_DEV_UP_DOCS) -d

.PHONY: c-shell
c-shell: c-build-dev
	$(COMPOSE_DEV_RUN_SHELL)

.PHONY: c-build-package
c-build-package: c-build-dev
	$(COMPOSE_DEV_RUN_BUILD)

.PHONY: c-exec-shell
c-exec-shell: docker-check
	$(COMPOSE_DEV_EXEC) $(SERVICE_APP) $(SHELL_BIN)

.PHONY: c-fix
c-fix: docker-check
	@echo format and lint autofix
	@$(MAKE) c-format
	@$(MAKE) c-lint-fix

.PHONY: c-check
c-check: docker-check
	@echo Validation only
	@$(MAKE) c-format-check
	@$(MAKE) c-lint
	@$(MAKE) c-test

.PHONY: c-qa
c-qa: docker-check
	@echo Full Quality Workflow
	@$(MAKE) c-fix
	@$(MAKE) c-check

.PHONY: c-ci
c-ci: docker-check
	@echo CI Workflow
	@$(MAKE) c-build-dev
	@$(MAKE) c-check
