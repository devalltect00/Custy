# app/core/changelog/old/pipeline.py

import logging
from typing import List, Dict

from app.core.git_ops.git.service import GitService

logger = logging.getLogger(__name__)


class CommitPipeline:
    """
    Pipeline to process commit messages through multiple stages.
    """

    def __init__(self, stages: List) -> None:
        self.stages = stages

    def run(self, messages: List[str], git: GitService) -> List[Dict]:
        """
        Process messages through pipeline.

        Args:
            messages (list[str]): Raw commit messages.
            git (GitService): Git service instance.

        Returns:
            list[dict]: Processed commit items.
        """
        parsed = []

        for msg in messages:
            try:
                commit = git.parse_commit(msg)

                # 🔥 SAFETY GUARD (IMPORTANT)
                if not commit or not isinstance(commit, dict):
                    continue

                # Ensure required fields exist
                commit.setdefault("type", "other")
                commit.setdefault("scope", "general")
                commit.setdefault("subject", "")
                commit.setdefault("body", "")

                # Skip completely empty commit
                if not commit["subject"] and not commit["body"]:
                    continue

                ctx = {
                    "commit": commit,
                    "items": None,
                    "skip": False,
                }

                for stage in self.stages:
                    stage.process(ctx)
                    if ctx.get("skip"):
                        break

                if ctx.get("items"):
                    parsed.extend(ctx["items"])

            except Exception:
                logger.exception("Pipeline failed on message")

        return parsed


# =========================================================
# ===================== STAGES =============================
# =========================================================

class SkipMergeStage:
    """
    Skip merge commits.

    Args:
        ignore (bool): Whether to ignore merge commits
    """

    def __init__(self, ignore: bool = True) -> None:
        self.ignore = ignore

    def process(self, ctx: Dict) -> None:
        if self.ignore and ctx["commit"].get("skip"):
            ctx["skip"] = True


class CleanStage:
    """
    Clean commit body using cleaner.

    Args:
        cleaner: ChangelogCleaner instance
    """

    def __init__(self, cleaner) -> None:
        self.cleaner = cleaner

    def process(self, ctx: Dict) -> None:
        ctx["cleaned_lines"] = self.cleaner.clean_commit(ctx["commit"])


class BreakingChangeStage:
    """
    Detect breaking changes.

    Args:
        enabled (bool): Enable detection
        keywords (list[str]): Keywords indicating breaking changes
    """
    
    def __init__(self, enabled: bool, keywords: List[str]) -> None:
        self.enabled = enabled
        self.keywords = keywords

    # =========================
    # BREAKING DETECTION
    # =========================
    def process(self, ctx: Dict) -> None:
        commit = ctx["commit"]
        is_breaking = False

        if self.enabled:
            header = commit.get("subject", "")

            if "!" in header.split(":")[0]:
                is_breaking = True

            for kw in self.keywords:
                if kw.lower() in commit.get("body", "").lower():
                    is_breaking = True
                    break

        ctx["is_breaking"] = is_breaking


class ReleaseTransformStage:
    """
    Transform release commits into structured entries.
    """

    # =========================
    # RELEASE COMMIT
    # =========================
    def process(self, ctx: Dict) -> None:
        commit = ctx["commit"]

        if commit["type"] != "release":
            return

        lines = ctx.get("cleaned_lines", [])
        is_breaking = ctx.get("is_breaking", False)

        ctx["items"] = [
            {
                "type": "breaking" if is_breaking else "fix",
                "scope": commit["scope"],
                "subject": line,
            }
            for line in lines
        ]


class NormalTransformStage:
    """
    Transform standard commits into structured entries.
    """
    
    # =========================
    # NORMAL COMMIT
    # =========================
    def process(self, ctx: Dict) -> None:
        if ctx.get("items"):
            return

        commit = ctx["commit"]
        lines = ctx.get("cleaned_lines", [])
        is_breaking = ctx.get("is_breaking", False)

        #####
        # if not lines:
        #     if commit.get("body"):
        #         lines = [
        #             l.strip()
        #             for l in commit["body"].splitlines()
        #             if l.strip()
        #         ]
        #     else:
        #         subject = commit.get("subject", "").strip()
        #         if subject:
        #             lines = [subject]
        #         else:
        #             # 🔥 fallback safety
        #             return
        #####

        if not lines:
            lines = commit.get("body", "").splitlines() or [commit.get("subject", "")]

        ctx["items"] = [
            {
                "type": "breaking" if is_breaking else commit.get("type", "other"),
                "scope": commit.get("scope", "general"),
                "subject": line.strip(),
            }
            for line in lines if line.strip()
        ]
