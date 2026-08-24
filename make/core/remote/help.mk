include $(ROOT_DIR)/make/core/help/variable.mk

# -------------------------------------------------------------------------
# 🌐 REMOTE PATH HEADER SCANNER - Registry Help
# -------------------------------------------------------------------------

.PHONY: help-remote-phs-registry
help-remote-phs-registry:
	@echo [Remote - Path Header Scanner Registry] (Total: $(call COMMAND_COUNT,REMOTE_PHS_REGISTRY))
	@echo $(HELP_SEPARATOR)

	@echo   make r-phs-info                     ^|    Show remote image information
	@echo   make r-phs-pull                     ^|    Pull remote image from registry
	@echo   make r-phs-push                     ^|    Push remote image to registry
	@echo   make r-phs-remove                   ^|    Remove local copy of remote image

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🌐 REMOTE PATH HEADER SCANNER - Runtime Help
# -------------------------------------------------------------------------

.PHONY: help-remote-phs-runtime
help-remote-phs-runtime:
	@echo [Remote - Path Header Scanner Runtime] (Total: $(call COMMAND_COUNT,REMOTE_PHS_RUNTIME))
	@echo $(HELP_SEPARATOR)

	@echo   make r-phs-init                     ^|    Run initialization from remote image
	@echo   make r-phs-init-all                 ^|    Initialize all resources
	@echo   make r-phs-init-force               ^|    Initialize and overwrite files
	@echo   make r-phs-init-ask                 ^|    Initialize with confirmation prompts
	@echo.
	@echo   make r-phs-scan                     ^|    Run scanner using remote image
	@echo   make r-phs-scan-apply               ^|    Run scanner and apply changes
	@echo   make r-phs-scan-debug               ^|    Run scanner in debug mode
	@echo   make r-phs-scan-apply-debug         ^|    Apply changes and enable debug mode
	@echo   make r-phs-scan-apply-all           ^|    Apply scanner to all configured targets

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🌐 REMOTE DOC GEN - Registry Help
# -------------------------------------------------------------------------

.PHONY: help-remote-docgen-registry
help-remote-docgen-registry:
	@echo [Remote - Doc Gen Registry] (Total: $(call COMMAND_COUNT,REMOTE_DOC_GEN_REGISTRY))
	@echo $(HELP_SEPARATOR)

	@echo   make r-doc-gen-info                 ^|    Show remote image information
	@echo   make r-doc-gen-pull                 ^|    Pull remote image from registry
	@echo   make r-doc-gen-push                 ^|    Push remote image to registry
	@echo   make r-doc-gen-remove               ^|    Remove local copy of remote image

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🌐 REMOTE DOC GEN - Runtime Help
# -------------------------------------------------------------------------

.PHONY: help-remote-docgen-runtime
help-remote-docgen-runtime:
	@echo [Remote - Doc Gen Runtime] (Total: $(call COMMAND_COUNT,REMOTE_DOC_GEN_RUNTIME))
	@echo $(HELP_SEPARATOR)

	@echo   make r-doc-init                     ^|    Run initialization from remote image
	@echo   make r-doc-init-all                 ^|    Initialize all resources
	@echo   make r-doc-init-force               ^|    Initialize and overwrite files
	@echo   make r-doc-init-ask                 ^|    Initialize with confirmation prompts
	@echo.
	@echo   make r-doc-generate                 ^|    Generate project documentation
	@echo   make r-doc-generate-smart           ^|    Generate documentation using smart mode
	@echo   make r-doc-print                    ^|    Print project structure
	@echo   make r-doc-print-smart              ^|    Print project structure using smart mode
	@echo   make r-doc-analyze                  ^|    Analyze project structure

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🌐 REMOTE CUSTY - Registry Help
# -------------------------------------------------------------------------

.PHONY: help-remote-custy-registry
help-remote-custy-registry:
	@echo [Remote - Custy Registry] (Total: $(call COMMAND_COUNT,REMOTE_CUSTY_REGISTRY))
	@echo $(HELP_SEPARATOR)

	@echo   make r-custy-info                   ^|    Show remote image information
	@echo   make r-custy-pull                   ^|    Pull remote image from registry
	@echo   make r-custy-push                   ^|    Push remote image to registry
	@echo   make r-custy-remove                 ^|    Remove local copy of remote image

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🌐 REMOTE CUSTY - Runtime Help
# -------------------------------------------------------------------------

.PHONY: help-remote-custy-runtime
help-remote-custy-runtime:
	@echo [Remote - Custy Runtime] (Total: $(call COMMAND_COUNT,REMOTE_CUSTY_RUNTIME))
	@echo $(HELP_SEPARATOR)

	@echo   make r-custy-init                   ^|    Run initialization from remote image
	@echo   make r-custy-init-all               ^|    Initialize all resources
	@echo   make r-custy-init-all-no-examples   ^|    Initialize configuration and templates only
	@echo   make r-custy-init-config            ^|    Initialize configuration files only
	@echo   make r-custy-init-templates         ^|    Initialize templates only
	@echo   make r-custy-init-examples          ^|    Initialize examples only
	@echo   make r-custy-init-force             ^|    Initialize and overwrite files
	@echo   make r-custy-init-ask               ^|    Initialize with confirmation prompts
	@echo.
	@echo   make r-custy-run                    ^|    Run remote command with custom arguments
	@echo   make r-custy-run-validate           ^|    Run the validate command
	@echo   make r-custy-run-apply-version      ^|    Run version update
	@echo   make r-custy-run-changelog          ^|    Run changelog generate
	@echo   make r-custy-run-commit             ^|    Create Git commit
	@echo   make r-custy-run-tag                ^|    Create Git tag
	@echo   make r-custy-run-push               ^|    Push commits and tags
	@echo   make r-custy-run-dev                ^|    Run daily development workflow
	@echo   make r-custy-run-release            ^|    Run release workflow
	@echo   make r-custy-run-full               ^|    Run full workflow
	@echo.
	@echo   make r-custy-run-backup-commit      ^|    Backup commit message templates
	@echo   make r-custy-run-backup-tag         ^|    Backup tag message templates
	@echo   make r-custy-run-backup-all         ^|    Backup all templates
	@echo.
	@echo   make r-custy-run-cleanup-backups    ^|    Remove backup files
	@echo   make r-custy-run-cleanup-branches   ^|    Remove temporary branches
	@echo   make r-custy-run-cleanup-all        ^|    Run complete cleanup workflow
	@echo.
	@echo   make r-custy-workflow               ^|    Run experimental workflow branch command

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🌐 REMOTE REFLOW - Registry Help
# -------------------------------------------------------------------------

.PHONY: help-remote-reflow-registry
help-remote-reflow-registry:
	@echo [Remote - Reflow Registry] (Total: $(call COMMAND_COUNT,REMOTE_REFLOW_REGISTRY))
	@echo $(HELP_SEPARATOR)

	@echo   make r-reflow-info                  ^|    Show remote image information
	@echo   make r-reflow-pull                  ^|    Pull remote image from registry
	@echo   make r-reflow-push                  ^|    Push remote image to registry
	@echo   make r-reflow-remove                ^|    Remove local copy of remote image

	@echo $(HELP_SEPARATOR)
	@echo.

# -------------------------------------------------------------------------
# 🌐 REMOTE REFLOW - Runtime Help
# -------------------------------------------------------------------------

.PHONY: help-remote-reflow-runtime
help-remote-reflow-runtime:
	@echo [Remote - Reflow Runtime] (Total: $(call COMMAND_COUNT,REMOTE_REFLOW_RUNTIME))
	@echo $(HELP_SEPARATOR)

	@echo   make r-reflow-init                  ^|    Run initialization from remote image
	@echo   make r-reflow-init-dryrun           ^|    Preview initialization
	@echo   make r-reflow-init-all              ^|    Initialize all resources
	@echo   make r-reflow-init-config           ^|    Initialize configuration files only
	@echo   make r-reflow-init-force            ^|    Initialize and overwrite files
	@echo   make r-reflow-init-ask              ^|    Initialize with confirmation prompts
	@echo.
	@echo   make r-reflow-releases-recover      ^|    Recover missing release automation
	@echo   make r-reflow-releases-recover-dryrun ^|  Preview release recovery
	@echo   make r-reflow-tags-convert          ^|    Convert version-tag formats
	@echo   make r-reflow-tags-convert-dryrun   ^|    Preview tag conversion
	@echo   make r-reflow-dockerize             ^|    Build and publish configured images
	@echo   make r-reflow-dockerize-dryrun      ^|    Preview Docker release automation
	@echo.
	@echo   make r-reflow-tags-replay           ^|    Deprecated release-recovery alias
	@echo   make r-reflow-tags-replay-dryrun    ^|    Deprecated dry-run alias

	@echo $(HELP_SEPARATOR)
	@echo.
