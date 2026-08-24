include $(ROOT_DIR)/make/core/variables/variable.mk
include $(ROOT_DIR)/make/core/helpers/common.mk
include $(ROOT_DIR)/make/core/helpers/registry.mk

# =========================================================
# 🌐 Remote Runtime Commands
# =========================================================

# -------------------------------------------------------------------------
# 🔧 Registry
# -------------------------------------------------------------------------

REMOTE_PHS_RUNTIME_COMMANDS_LIST := \
	r-phs-init \
	r-phs-init-all \
	r-phs-init-force \
	r-phs-init-ask \
	r-phs-scan

REMOTE_DOC_GEN_RUNTIME_COMMANDS_LIST := \
	r-doc-init \
	r-doc-init-all \
	r-doc-init-force \
	r-doc-init-ask \
	r-doc-generate \
	r-doc-generate-smart \
	r-doc-print \
	r-doc-print-smart \
	r-doc-analyze

REMOTE_CUSTY_RUNTIME_COMMANDS_LIST := \
	r-custy-init \
	r-custy-init-all \
	r-custy-init-all-no-examples \
	r-custy-init-config \
	r-custy-init-templates \
	r-custy-init-examples \
	r-custy-init-force \
	r-custy-init-ask \
	r-custy-run \
	r-custy-run-validate \
	r-custy-run-apply-version \
	r-custy-run-changelog \
	r-custy-run-commit \
	r-custy-run-tag \
	r-custy-run-push \
	r-custy-run-dev \
	r-custy-run-release \
	r-custy-run-full \
	r-custy-run-backup-commit \
	r-custy-run-backup-tag \
	r-custy-run-backup-all \
	r-custy-run-cleanup-backups \
	r-custy-run-cleanup-branches \
	r-custy-run-cleanup-all \
	r-custy-workflow

REMOTE_REFLOW_RUNTIME_COMMANDS_LIST := \
	r-reflow-init \
	r-reflow-init-dryrun \
	r-reflow-init-all \
	r-reflow-init-config \
	r-reflow-init-force \
	r-reflow-init-ask \
	r-reflow-releases-recover \
	r-reflow-releases-recover-dryrun \
	r-reflow-tags-replay \
	r-reflow-tags-replay-dryrun \
	r-reflow-tags-convert \
	r-reflow-tags-convert-dryrun \
	r-reflow-dockerize \
	r-reflow-dockerize-dryrun

$(foreach cmd,$(REMOTE_PHS_RUNTIME_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		REMOTE_PHS_RUNTIME,$(cmd),REMOTE)))

$(foreach cmd,$(REMOTE_DOC_GEN_RUNTIME_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		REMOTE_DOC_GEN_RUNTIME,$(cmd),REMOTE)))

$(foreach cmd,$(REMOTE_CUSTY_RUNTIME_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		REMOTE_CUSTY_RUNTIME,$(cmd),REMOTE)))

$(foreach cmd,$(REMOTE_REFLOW_RUNTIME_COMMANDS_LIST),\
	$(eval $(call REGISTER_COMMAND,\
		REMOTE_REFLOW_RUNTIME,$(cmd),REMOTE)))

# -------------------------------------------------------------------------
# 🔧 Commands
# -------------------------------------------------------------------------

# GITHUB REMOTE CONTAINER

# -------------------------------------------------------------------------
# 🌐 Remote Runtime Commands - Path Header Scanner
# -------------------------------------------------------------------------

.PHONY: r-phs-init
r-phs-init:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_PHS)
	$(call REMOTE_RUN,REMOTE_IMAGE_PHS) \
		$(REMOTE_PHS_GLOBAL_ARGS) \
		init \
		$(REMOTE_PHS_INIT_ARGS) \
		$(REMOTE_PHS_EXTRA_ARGS)

.PHONY: r-phs-init-all
r-phs-init-all:
	@$(MAKE) r-phs-init \
		REMOTE_PHS_INIT_ARGS="--mode all"

.PHONY: r-phs-init-force
r-phs-init-force:
	@$(MAKE) r-phs-init \
		REMOTE_PHS_INIT_ARGS="--force --mode all"

.PHONY: r-phs-init-ask
r-phs-init-ask:
	@$(MAKE) r-phs-init \
		REMOTE_PHS_INIT_ARGS="--ask --mode all"

.PHONY: r-phs-scan
r-phs-scan:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_PHS)
	$(call REMOTE_RUN,REMOTE_IMAGE_PHS) \
		$(REMOTE_PHS_GLOBAL_ARGS) \
		scan $(TARGET) \
		$(REMOTE_PHS_SCAN_ARGS) \
		$(REMOTE_PHS_EXTRA_ARGS)

r-phs-scan-apply:
	@$(MAKE) r-phs-scan \
		TARGET="$(TARGET)" \
		REMOTE_PHS_SCAN_ARGS="--apply"

r-phs-scan-debug:
	@$(MAKE) r-phs-scan \
		TARGET="$(TARGET)" \
		REMOTE_PHS_SCAN_ARGS="--debug"

r-phs-scan-apply-debug:
	@$(MAKE) r-phs-scan \
		TARGET="$(TARGET)" \
		REMOTE_PHS_SCAN_ARGS="--apply --debug"

r-phs-scan-apply-all:
ifeq ($(PLATFORM),windows)
	@for %%t in ($(PHS_SCAN_TARGETS)) do ( \
		$(MAKE) r-phs-scan TARGET=%%t REMOTE_PHS_SCAN_ARGS="--apply" \
	)
else
	@for target in $(PHS_SCAN_TARGETS); do \
		$(MAKE) r-phs-scan \
			TARGET="$$target" \
			REMOTE_PHS_SCAN_ARGS="--apply"; \
	done
endif

# -------------------------------------------------------------------------
# 🌐 Remote Runtime Commands - Doc Gen
# -------------------------------------------------------------------------

.PHONY: r-doc-init
r-doc-init:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_DOC_GEN)
	$(call REMOTE_RUN,REMOTE_IMAGE_DOC_GEN) \
		$(REMOTE_DOC_GEN_GLOBAL_ARGS) \
		init \
		$(REMOTE_DOC_GEN_INIT_ARGS) \
		$(REMOTE_DOC_GEN_EXTRA_ARGS)

.PHONY: r-doc-init-all
r-doc-init-all:
	@$(MAKE) r-doc-init \
		REMOTE_DOC_GEN_INIT_ARGS="--mode all"

.PHONY: r-doc-init-force
r-doc-init-force:
	@$(MAKE) r-doc-init \
		REMOTE_DOC_GEN_INIT_ARGS="--force --mode all"

.PHONY: r-doc-init-ask
r-doc-init-ask:
	@$(MAKE) r-doc-init \
		REMOTE_DOC_GEN_INIT_ARGS="--ask --mode all"

.PHONY: r-doc-generate
r-doc-generate:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_DOC_GEN)
	$(call REMOTE_RUN,REMOTE_IMAGE_DOC_GEN) \
		$(REMOTE_DOC_GEN_GLOBAL_ARGS) \
		structure generate \
		$(REMOTE_DOC_GEN_STRUCTURE_ARGS) \
		$(REMOTE_DOC_GEN_GENERATE_ARGS) \
		$(REMOTE_DOC_GEN_EXTRA_ARGS)

.PHONY: r-doc-generate-smart
r-doc-generate-smart:
	@$(MAKE) r-doc-generate \
		REMOTE_DOC_GEN_GENERATE_ARGS="--smart"

.PHONY: r-doc-print
r-doc-print:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_DOC_GEN)
	$(call REMOTE_RUN,REMOTE_IMAGE_DOC_GEN) \
		$(REMOTE_DOC_GEN_GLOBAL_ARGS) \
		structure print \
		$(REMOTE_DOC_GEN_STRUCTURE_ARGS) \
		$(REMOTE_DOC_GEN_PRINT_ARGS) \
		$(REMOTE_DOC_GEN_EXTRA_ARGS)

.PHONY: r-doc-print-smart
r-doc-print-smart:
	@$(MAKE) r-doc-print \
		REMOTE_DOC_GEN_PRINT_ARGS="--smart"

.PHONY: r-doc-analyze
r-doc-analyze:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_DOC_GEN)
	$(call REMOTE_RUN,REMOTE_IMAGE_DOC_GEN) \
		$(REMOTE_DOC_GEN_GLOBAL_ARGS) \
		structure analyze \
		$(REMOTE_DOC_GEN_STRUCTURE_ARGS) \
		$(REMOTE_DOC_GEN_ANALYZE_ARGS) \
		$(REMOTE_DOC_GEN_EXTRA_ARGS)

# -------------------------------------------------------------------------
# 🌐 Remote Runtime Commands - Custy
# -------------------------------------------------------------------------

.PHONY: r-custy-init
r-custy-init:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		init \
		$(REMOTE_CUSTY_INIT_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-init-all
r-custy-init-all: override REMOTE_CUSTY_INIT_ARGS += --mode all
r-custy-init-all: r-custy-init

.PHONY: r-custy-init-config
r-custy-init-config: override REMOTE_CUSTY_INIT_ARGS += --mode config
r-custy-init-config: r-custy-init

.PHONY: r-custy-init-all-no-examples
r-custy-init-all-no-examples: override REMOTE_CUSTY_INIT_ARGS += --mode all_no_examples
r-custy-init-all-no-examples: r-custy-init

.PHONY: r-custy-init-templates
r-custy-init-templates: override REMOTE_CUSTY_INIT_ARGS += --mode templates
r-custy-init-templates: r-custy-init

.PHONY: r-custy-init-examples
r-custy-init-examples: override REMOTE_CUSTY_INIT_ARGS += --mode examples
r-custy-init-examples: r-custy-init

.PHONY: r-custy-init-force
r-custy-init-force: override REMOTE_CUSTY_INIT_ARGS += --force --mode all
r-custy-init-force: r-custy-init

.PHONY: r-custy-init-ask
r-custy-init-ask: override REMOTE_CUSTY_INIT_ARGS += --ask --mode all
r-custy-init-ask: r-custy-init

.PHONY: r-custy-run
r-custy-run:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		run \
		$(REMOTE_CUSTY_RUN_SUBCOMMAND) \
		$(REMOTE_CUSTY_RUN_ARGS) \
		$(REMOTE_CUSTY_RUN_SUBCOMMAND_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-validate
r-custy-run-validate:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		validate \
		$(REMOTE_CUSTY_VALIDATE_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-apply-version
r-custy-run-apply-version:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		version update \
		$(REMOTE_CUSTY_VERSION_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-changelog
r-custy-run-changelog:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		changelog generate \
		$(REMOTE_CUSTY_CHANGELOG_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-commit
r-custy-run-commit:
	@$(MAKE) r-custy-run \
		REMOTE_CUSTY_RUN_SUBCOMMAND="commit" \
		REMOTE_CUSTY_RUN_SUBCOMMAND_ARGS="$(REMOTE_CUSTY_COMMIT_ARGS)"

.PHONY: r-custy-run-tag
r-custy-run-tag:
	@$(MAKE) r-custy-run \
		REMOTE_CUSTY_RUN_SUBCOMMAND="tag" \
		REMOTE_CUSTY_RUN_SUBCOMMAND_ARGS="$(REMOTE_CUSTY_TAG_ARGS)"

.PHONY: r-custy-run-push
r-custy-run-push:
	@$(MAKE) r-custy-run \
		REMOTE_CUSTY_RUN_SUBCOMMAND="push" \
		REMOTE_CUSTY_RUN_SUBCOMMAND_ARGS="$(REMOTE_CUSTY_PUSH_ARGS)"

.PHONY: r-custy-run-dev
r-custy-run-dev:
	@$(MAKE) r-custy-run \
		REMOTE_CUSTY_RUN_SUBCOMMAND="dev" \
		REMOTE_CUSTY_RUN_SUBCOMMAND_ARGS="$(REMOTE_CUSTY_RUN_DEV_ARGS)"

.PHONY: r-custy-run-release
r-custy-run-release:
	@$(MAKE) r-custy-run \
		REMOTE_CUSTY_RUN_SUBCOMMAND="release" \
		REMOTE_CUSTY_RUN_SUBCOMMAND_ARGS="$(REMOTE_CUSTY_RUN_RELEASE_ARGS)"

.PHONY: r-custy-run-full
r-custy-run-full:
	@$(MAKE) r-custy-run \
		REMOTE_CUSTY_RUN_SUBCOMMAND="full" \
		REMOTE_CUSTY_RUN_SUBCOMMAND_ARGS="$(REMOTE_CUSTY_RUN_FULL_ARGS)"

.PHONY: r-custy-run-backup-commit
r-custy-run-backup-commit:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		backup commit \
		$(REMOTE_CUSTY_BACKUP_ARGS) \
		$(REMOTE_CUSTY_BACKUP_COMMIT_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-backup-tag
r-custy-run-backup-tag:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		backup tag \
		$(REMOTE_CUSTY_BACKUP_ARGS) \
		$(REMOTE_CUSTY_BACKUP_TAG_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-backup-all
r-custy-run-backup-all:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		backup all \
		$(REMOTE_CUSTY_BACKUP_ARGS) \
		$(REMOTE_CUSTY_BACKUP_ALL_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-cleanup-backups
r-custy-run-cleanup-backups:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		cleanup backups \
		$(REMOTE_CUSTY_CLEANUP_ARGS) \
		$(REMOTE_CUSTY_CLEANUP_BACKUPS_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-cleanup-branches
r-custy-run-cleanup-branches:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		cleanup branches \
		$(REMOTE_CUSTY_CLEANUP_ARGS) \
		$(REMOTE_CUSTY_CLEANUP_BRANCHES_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

.PHONY: r-custy-run-cleanup-all
r-custy-run-cleanup-all:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		cleanup all \
		$(REMOTE_CUSTY_CLEANUP_ARGS) \
		$(REMOTE_CUSTY_CLEANUP_ALL_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

# Still in development
.PHONY: r-custy-workflow
r-custy-workflow:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_CUSTY)
	$(call REMOTE_RUN,REMOTE_IMAGE_CUSTY) \
		$(REMOTE_CUSTY_GLOBAL_ARGS) \
		workflow branch \
		$(REMOTE_CUSTY_WORKFLOW_ARGS) \
		$(REMOTE_CUSTY_EXTRA_ARGS)

# -------------------------------------------------------------------------
# 🌐 Remote Runtime Commands - Reflow
# -------------------------------------------------------------------------

.PHONY: r-reflow-init
r-reflow-init:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_REFLOW)
	$(call REMOTE_RUN,REMOTE_IMAGE_REFLOW) \
		$(REMOTE_REFLOW_GLOBAL_ARGS) \
		init \
		$(REMOTE_REFLOW_INIT_ARGS) \
		$(REMOTE_REFLOW_EXTRA_ARGS)

.PHONY: r-reflow-init-dryrun r-reflow-init-all r-reflow-init-config
.PHONY: r-reflow-init-force r-reflow-init-ask
r-reflow-init-dryrun: override REMOTE_REFLOW_GLOBAL_ARGS += --dry-run
r-reflow-init-dryrun: r-reflow-init

r-reflow-init-all: override REMOTE_REFLOW_INIT_ARGS += --mode all
r-reflow-init-all: r-reflow-init

r-reflow-init-config: override REMOTE_REFLOW_INIT_ARGS += --mode config
r-reflow-init-config: r-reflow-init

r-reflow-init-force: override REMOTE_REFLOW_INIT_ARGS += --force
r-reflow-init-force: r-reflow-init

r-reflow-init-ask: override REMOTE_REFLOW_INIT_ARGS += --ask
r-reflow-init-ask: r-reflow-init

.PHONY: r-reflow-releases-recover
r-reflow-releases-recover:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_REFLOW)
	$(call REMOTE_RUN,REMOTE_IMAGE_REFLOW) \
		$(REMOTE_REFLOW_GLOBAL_ARGS) \
		releases recover \
		$(REMOTE_REFLOW_RELEASES_RECOVER_ARGS) \
		$(REMOTE_REFLOW_EXTRA_ARGS)

.PHONY: r-reflow-releases-recover-dryrun
r-reflow-releases-recover-dryrun: override REMOTE_REFLOW_GLOBAL_ARGS += --dry-run
r-reflow-releases-recover-dryrun: r-reflow-releases-recover

.PHONY: r-reflow-tags-replay r-reflow-tags-replay-dryrun
r-reflow-tags-replay:
	@echo WARNING: r-reflow-tags-replay is deprecated - use r-reflow-releases-recover.
	@$(MAKE) --no-print-directory r-reflow-releases-recover \
		REMOTE_REFLOW_GLOBAL_ARGS="$(REMOTE_REFLOW_GLOBAL_ARGS)" \
		REMOTE_REFLOW_RELEASES_RECOVER_ARGS="$(REMOTE_REFLOW_RELEASES_RECOVER_ARGS)" \
		REMOTE_REFLOW_EXTRA_ARGS="$(REMOTE_REFLOW_EXTRA_ARGS)"

r-reflow-tags-replay-dryrun:
	@echo WARNING: r-reflow-tags-replay-dryrun is deprecated - use r-reflow-releases-recover-dryrun.
	@$(MAKE) --no-print-directory r-reflow-releases-recover-dryrun \
		REMOTE_REFLOW_GLOBAL_ARGS="$(REMOTE_REFLOW_GLOBAL_ARGS)" \
		REMOTE_REFLOW_RELEASES_RECOVER_ARGS="$(REMOTE_REFLOW_RELEASES_RECOVER_ARGS)" \
		REMOTE_REFLOW_EXTRA_ARGS="$(REMOTE_REFLOW_EXTRA_ARGS)"

.PHONY: r-reflow-tags-convert
r-reflow-tags-convert:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_REFLOW)
	$(call REMOTE_RUN,REMOTE_IMAGE_REFLOW) \
		$(REMOTE_REFLOW_GLOBAL_ARGS) \
		tags convert \
		$(REMOTE_REFLOW_TAGS_CONVERT_ARGS) \
		$(REMOTE_REFLOW_EXTRA_ARGS)

.PHONY: r-reflow-tags-convert-dryrun
r-reflow-tags-convert-dryrun: override REMOTE_REFLOW_GLOBAL_ARGS += --dry-run
r-reflow-tags-convert-dryrun: r-reflow-tags-convert

.PHONY: r-reflow-dockerize
r-reflow-dockerize:
	$(call REQUIRE_REMOTE)
	$(call ENSURE_REMOTE_IMAGE,REMOTE_IMAGE_REFLOW)
	$(DOCKER_RUN_INTERACTIVE) \
		$(DOCKER_REMOTE_WORKSPACE) \
		$(DOCKER_SOCKET_MOUNT) \
		$(call REMOTE_IMAGE_FULL,REMOTE_IMAGE_REFLOW) \
		$(REMOTE_REFLOW_GLOBAL_ARGS) \
		dockerize \
		$(REMOTE_REFLOW_DOCKERIZE_ARGS) \
		$(REMOTE_REFLOW_EXTRA_ARGS)

.PHONY: r-reflow-dockerize-dryrun
r-reflow-dockerize-dryrun: override REMOTE_REFLOW_GLOBAL_ARGS += --dry-run
r-reflow-dockerize-dryrun: r-reflow-dockerize
