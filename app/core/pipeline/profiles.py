# app/core/pipeline/profiles.py

"""
Pipeline Profiles

Defines reusable, high-level workflows.

Each profile represents a complete, intentional flow—not just a shortcut.

Design Principles:
- Each command has its own REQUIRED pre-steps
- No hidden logic inside resolver
- Profiles are the single source of truth for workflow sequences
- Steps are explicit and readable

Naming:
- validate → validation only
- commit → full commit flow
- tag → full tagging flow
- push → minimal safe push flow
- dev → commit + push flow
"""

PIPELINE_PROFILES = {
    # 🔍 Validation only
    # "validate-sub-common": [
    "validate-sub-repo": [
        {"name": "ensure_git_repo_step"},
    ],
    "validate-sub-pre-commit": [
        {"name": "ensure_staged_changes_step"},
        {"name": "ensure_commit_validation_provider_step"},
        {"name": "ensure_commit_hook_policy_step"},
        {"name": "ensure_commit_message_file_step"},
        {"name": "ensure_commit_message_file_exists_step"},
    ],
    "validate-sub-pre-tag": [
        {"name": "ensure_version_file_step"},
        {"name": "ensure_tag_message_file_step"},
        {"name": "ensure_tag_message_file_exists_step"},
    ],
    "validate-sub-pre-push": [
        {"name": "ensure_remote_exists_step"},
    ],
    "validate": [
        {"name": "ensure_git_repo_step"},
        {"name": "ensure_remote_exists_step"},
        {"name": "ensure_version_file_step"},
        {"name": "ensure_staged_changes_step"},
        {"name": "ensure_commit_validation_provider_step"},
        {"name": "ensure_commit_hook_policy_step"},
        {"name": "ensure_commit_message_file_step"},
        {"name": "ensure_commit_message_file_exists_step"},
        {"name": "ensure_tag_message_file_step"},
        {"name": "ensure_tag_message_file_exists_step"},
    ],
    # Changelog
    "changelog": [{"name": "generate_changelog_step"}],
    # Apply version update
    "apply_version": [
        {"name": "validate-sub-repo"},
        {"name": "ensure_version_file_step"},
        {"name": "prepare_version_step"},
        # {"name": "workflow_init_step"},
        {"name": "prepare_tag_message_step"},
        {"name": "apply_version_step"},
        # {"name": "changelog"},
    ],
    # 🧾 Commit flow (with all required preparation)
    "commit": [
        {"name": "validate-sub-repo"},
        {"name": "validate-sub-pre-commit"},
        {"name": "prepare_version_step"},
        {"name": "workflow_init_step"},
        {"name": "generate_artifacts_step"},
        {"name": "edit_files_step"},
        {"name": "validate_edited_step"},
        {"name": "apply_version_step"},
        {"name": "changelog"},
        {"name": "backup_commit_message_files_step"},
        {"name": "cleanup_backup_step"},
        {"name": "stage_step"},
        {"name": "commit_step"},
    ],
    # 🏷️ Tag flow (with version + message preparation)
    "tag": [
        {"name": "validate-sub-repo"},
        {"name": "validate-sub-pre-tag"},
        {"name": "prepare_version_step"},
        {"name": "workflow_init_step"},
        {"name": "prepare_tag_message_step"},
        {"name": "generate_artifacts_step"},
        {"name": "edit_files_step"},
        {"name": "apply_version_step"},
        {"name": "backup_tag_message_files_step"},
        {"name": "cleanup_backup_step"},
        {"name": "tag_step"},
    ],
    # 🚀 Push flow (minimal but safe)
    "push": [
        {"name": "validate-sub-repo"},
        {"name": "validate-sub-pre-push"},
        {"name": "push_step"},
    ],
    # ⚡ Dev flow (commit + push)
    "dev": [
        {"name": "validate-sub-repo"},
        {"name": "prepare_version_step"},
        {"name": "workflow_init_step"},
        {"name": "generate_artifacts_step"},
        {"name": "edit_files_step"},
        {"name": "validate_edited_step"},
        {"name": "changelog"},
        {"name": "backup_commit_message_files_step"},
        {"name": "cleanup_backup_step"},
        {"name": "stage_step"},
        {"name": "commit_step"},
        {"name": "push_step"},
    ],
    # 🚀 Full release (complete pipeline)
    "release": [
        {"name": "validate-sub-repo"},
        {"name": "validate-sub-pre-commit"},
        {"name": "validate-sub-pre-tag"},
        {"name": "validate-sub-pre-push"},
        {"name": "prepare_version_step"},
        {"name": "workflow_init_step"},
        {"name": "prepare_tag_message_step"},
        {"name": "generate_artifacts_step"},
        {"name": "edit_files_step"},
        {"name": "validate_edited_step"},
        {"name": "apply_version_step"},
        {"name": "changelog"},
        {"name": "backup_commit_message_files_step"},
        {"name": "backup_tag_message_files_step"},
        {"name": "cleanup_backup_step"},
        {"name": "stage_step"},
        {"name": "commit_step"},
        {"name": "tag_step"},
        {"name": "push_step"},
    ],
    "full": [
        # {"name": "validate"},
        {"name": "validate-sub-repo"},
        {"name": "validate-sub-pre-commit"},
        {"name": "validate-sub-pre-tag"},
        {"name": "validate-sub-pre-push"},
        {"name": "prepare_version_step"},
        {"name": "workflow_init_step"},
        {"name": "prepare_tag_message_step"},
        {"name": "generate_artifacts_step"},
        {"name": "edit_files_step"},
        {"name": "validate_edited_step"},
        {"name": "apply_version_step"},
        {"name": "changelog"},
        {"name": "backup_commit_message_files_step"},
        {"name": "backup_tag_message_files_step"},
        {"name": "cleanup_backup_step"},
        {"name": "stage_step"},
        {"name": "commit_step"},
        {"name": "tag_step"},
        {"name": "push_step"},
        {"name": "finalize_step"},
    ],
    # 🗂️ Backup only
    "backup_commit_message": [
        {"name": "backup_commit_message_files_step"},
    ],
    "backup_tag_message": [
        {"name": "backup_tag_message_files_step"},
    ],
    "backup_all": [
        {"name": "backup_commit_message_files_step"},
        {"name": "backup_tag_message_files_step"},
    ],
    # 🧹 Cleanup only
    "cleanup_backups": [
        {"name": "cleanup_backup_step"},
    ],
    "cleanup_branches": [
        {"name": "cleanup_branches_step"},
    ],
    "cleanup_all": [
        {"name": "cleanup_backup_step"},
        {"name": "cleanup_branches_step"},
    ],
    "init": [
        {"name": "Initialization_custy_step"},
    ],
}

STEP_ORDER = {
    # Initialization
    "Initialization_custy_step": 0,
    # Validation
    "ensure_git_repo_step": 10,
    "ensure_staged_changes_step": 11,
    "ensure_commit_validation_provider_step": 12,
    "ensure_commit_hook_policy_step": 13,
    "ensure_commit_message_file_step": 14,
    "ensure_commit_message_file_exists_step": 15,
    "ensure_version_file_step": 16,
    "ensure_tag_message_file_step": 17,
    "ensure_tag_message_file_exists_step": 18,
    "ensure_remote_exists_step": 19,
    # Preparation
    "prepare_version_step": 30,
    "workflow_init_step": 31,
    "prepare_tag_message_step": 32,
    # Generation / Editing
    "generate_artifacts_step": 40,
    "edit_files_step": 41,
    "validate_edited_step": 42,
    "apply_version_step": 43,
    "generate_changelog_step": 44,
    # Backup / Cleanup
    "backup_commit_message_files_step": 50,
    "backup_tag_message_files_step": 51,
    "cleanup_backup_step": 52,
    # Execution
    "stage_step": 70,
    "commit_step": 71,
    "tag_step": 72,
    "push_step": 73,
    # Branches Migrations
    "cleanup_branches_step": 80,
    # Finalize
    "finalize_step": 90,
}
