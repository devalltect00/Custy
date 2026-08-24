# app/cli/constants/completions.py

def completion_initialization_mode():
    return ["all", "all_no_examples", "config", "templates", "examples"]

def completion_commit_message_file():
    return ["templates/custy/commit-message.txt"]

def completion_tag_message_file():
    return ["templates/custy/tag-message.txt"]

def completion_version_file():
    return ["app/__version__.py", "src/__version__.py"]

def completion_commit_message_backup_dir():
    return ["tools/custy/templates/backups/commit"]

def completion_tag_message_backup_dir():
    return ["tools/custy/templates/backups/tag"]

def completion_tag():
    return ["v1.0.0", "1.0.0"]

def completion_tag_message():
    return ["v1.0.0", "1.0.0", "Release v1.0.0", "Release 1.0.0"]

def completion_meta():
    return ["sha.abc123"]

def completion_remote_name():
    return ["origin", "backup"]

def completion_steps():
    return ["commit", "tag", "push", "dev", "release", "all"]
