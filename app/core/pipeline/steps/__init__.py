# app/core/pipeline/steps/__init__.py

"""
Steps package.

Only expose step classes. No registration here.
"""

from .prepare_version_step import PrepareVersionStep
from .workflow_init_step import WorkflowInitStep
from .prepare_tag_message_step import PrepareTagMessageStep
from .generate_artifacts_step import GenerateArtifactsStep
from .edit_files_step import EditFilesStep
from .validate_edited_step import ValidateEditedStep
from .apply_version_step import ApplyVersionStep
from .generate_changelog_step import GenerateChangelogStep


from .backup_step import BackupStep
from .cleanup_backups_step import CleanupBackupsStep
from .stage_step import StageStep

from .commit_step import CommitStep

from .tag_step import TagStep
from .push_step import PushStep
from .finalize_workflow_step import FinalizeWorkflowStep

from .cleanup_branches_step import CleanupBranchesStep

from .validation import (
    EnsureGitRepoStep,
    EnsureRemoteExistsStep,
    EnsureVersionFileStep,
    EnsureCommitMessageFileStep,
    EnsureTagMessageFileStep,
    EnsureStagedChangesStep,
    EnsureCommitizenConventionStep,
    EnsureCommitMessageFileExistsStep,
    EnsureTagMessageFileExistsStep,
)

from .backup import (
  BackupCommitMessageStep,
  BackupTagMessageStep,
)

from .initialization import InitStep

__all__ = [
    "PrepareVersionStep",
    "WorkflowInitStep",
    "PrepareTagMessageStep",
    "GenerateArtifactsStep",
    "EditFilesStep",
    "ValidateEditedStep",
    "ApplyVersionStep",
    "GenerateChangelogStep",
    "BackupStep",
    "CleanupBackupsStep",
    "StageStep",
    "CommitStep",
    "TagStep",
    "PushStep",
    "FinalizeWorkflowStep",

    "CleanupBranchesStep",

    "EnsureGitRepoStep",
    "EnsureRemoteExistsStep",
    "EnsureVersionFileStep",
    "EnsureCommitMessageFileStep",
    "EnsureTagMessageFileStep",
    "EnsureStagedChangesStep",
    "EnsureCommitizenConventionStep",
    "EnsureCommitMessageFileExistsStep",
    "EnsureTagMessageFileExistsStep",

    "BackupCommitMessageStep",
    "BackupTagMessageStep",

    "InitStep",
]
