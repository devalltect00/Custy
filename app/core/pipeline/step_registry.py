# app/core/pipeline/step_registry.py

"""
Step Registry Setup

Responsible for registering all steps.

This avoids circular imports by separating registration from definition.

Auto-register all pipeline steps.

Importing this module ensures all steps are registered.
"""

from app.core.pipeline.registry import StepRegistry

from app.core.pipeline.steps import (
    PrepareVersionStep,
    WorkflowInitStep,
    PrepareTagMessageStep,
    GenerateArtifactsStep,
    EditFilesStep,
    ValidateEditedStep,
    ApplyVersionStep,
    GenerateChangelogStep,
    BackupStep,
    CleanupBackupsStep,
    StageStep,
    CommitStep,
    TagStep,
    PushStep,
    FinalizeWorkflowStep,

    CleanupBranchesStep,

    EnsureGitRepoStep,
    EnsureRemoteExistsStep,
    EnsureVersionFileStep,
    EnsureCommitMessageFileStep,
    EnsureTagMessageFileStep,
    EnsureStagedChangesStep,
    EnsureCommitizenConventionStep,
    EnsureCommitMessageFileExistsStep,
    EnsureTagMessageFileExistsStep,

    BackupCommitMessageStep,
    BackupTagMessageStep,

    InitStep,
)

def register_all_steps() -> None:
    """
    Register all pipeline steps.

    This should be called ONCE during application startup
    before building any pipeline.

    Example:
        register_all_steps()
    """

    StepRegistry.register("prepare_version_step", PrepareVersionStep)
    StepRegistry.register("workflow_init_step", WorkflowInitStep)
    StepRegistry.register("prepare_tag_message_step", PrepareTagMessageStep)
    StepRegistry.register("generate_artifacts_step", GenerateArtifactsStep)
    StepRegistry.register("edit_files_step", EditFilesStep)
    StepRegistry.register("validate_edited_step", ValidateEditedStep)
    StepRegistry.register("apply_version_step", ApplyVersionStep)
    StepRegistry.register("generate_changelog_step", GenerateChangelogStep)
    StepRegistry.register("backup_step", BackupStep)
    StepRegistry.register("cleanup_backup_step", CleanupBackupsStep)
    StepRegistry.register("stage_step", StageStep)
    StepRegistry.register("commit_step", CommitStep)
    StepRegistry.register("tag_step", TagStep)
    StepRegistry.register("push_step", PushStep)
    StepRegistry.register("finalize_step", FinalizeWorkflowStep)

    StepRegistry.register("cleanup_branches_step", CleanupBranchesStep)

    StepRegistry.register("ensure_git_repo_step", EnsureGitRepoStep)
    StepRegistry.register("ensure_remote_exists_step", EnsureRemoteExistsStep)
    StepRegistry.register("ensure_version_file_step", EnsureVersionFileStep)
    StepRegistry.register("ensure_commit_message_file_step", EnsureCommitMessageFileStep)
    StepRegistry.register("ensure_tag_message_file_step", EnsureTagMessageFileStep)
    StepRegistry.register("ensure_staged_changes_step", EnsureStagedChangesStep)
    StepRegistry.register("ensure_commitizen_convention_step", EnsureCommitizenConventionStep)
    StepRegistry.register("ensure_commit_message_file_exists_step", EnsureCommitMessageFileExistsStep)
    StepRegistry.register("ensure_tag_message_file_exists_step", EnsureTagMessageFileExistsStep)

    StepRegistry.register("backup_commit_message_files_step", BackupCommitMessageStep)
    StepRegistry.register("backup_tag_message_files_step", BackupTagMessageStep)

    StepRegistry.register("Initialization_custy_step", InitStep)
