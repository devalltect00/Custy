# app/cli/commands/backup/models.py

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class BackupCommitArgs:
  commit_message_file: Optional[Path]
  commit_message_backup_dir: Optional[Path]

@dataclass
class BackupTagArgs:
  tag_message_file: Optional[Path]
  tag_message_backup_dir: Optional[Path]

@dataclass
class BackupAllArgs:
  commit_message_file: Optional[Path]
  tag_message_file: Optional[Path]
  commit_message_backup_dir: Optional[Path]
  tag_message_backup_dir: Optional[Path]
