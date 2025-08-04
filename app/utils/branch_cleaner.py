# app\utils\branch_cleaner.py
""" """

import subprocess
from datetime import datetime, timedelta

from .dry_run_support import DryRunSupport


class BranchCleaner(DryRunSupport):
    def __init__(
        self, prefix: str, merged_only: bool = False, older_than: str | None = None
    ) -> None:
        self.prefix = prefix
        self.merged_only = merged_only
        self.cutoff = self._parsse_older_than(older_than)

    def _parsse_older_than(self, text: str | None) -> datetime | None:
        if not text:
            return None
        if text.endswith("d"):
            days = int(text[:-1])
            return datetime.now() - timedelta(days=days)
        raise ValueError("Invalid --older-than format. Use '30d', '14d', etc.")

    def _get_branches(self) -> list[str]:
        cmd = ["git", "branch", "--merged"] if self.merged_only else ["git", "branch"]
        branches = subprocess.check_output(cmd).decode().splitlines()
        return [b.strip().lstrip("* ") for b in branches if b.strip()]

    def _is_old_enough(self, branch: str) -> bool:
        if not self.cutoff:
            return True
        timestamp = (
            subprocess.check_output(
                ["git", "log", "-1", "--format=%ct", branch],
            )
            .decode()
            .strip()
        )
        last_commit = datetime.fromtimestamp(int(timestamp))
        return last_commit < self.cutoff

    def clean(self) -> None:
        for branch in self._get_branches():
            if not branch.startswith(self.prefix) or branch in ("main", "develop"):
                continue
            if not self._is_old_enough(branch):
                continue
            print(f"🧹 Deleting branch: {branch}")
            self.runner.run(["git", "branch", "-D", branch])
            self.runner.run(["git", "push", "origin", "--delete", branch])
