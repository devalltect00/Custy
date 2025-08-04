# app\utils\workflow_manager.py
"""
workflow_manager.py

Orchestrates Git branching and versioning consistency using strategy-specific helpers.

Supports both PEP 440 and SemVer standards by dynamically delegating logic
to PEP440VersionHelper or SemverVersionHelper depending on project language.

Responsibilities:
- Enforces consistency rules for each branch type
- Suggests the next version based on branch context
- Validates allowed version transitions between branch/tag combinations
"""

import re

from .git import GitHelper
from .pep440_helper import PEP440VersionHelper
from .project_detector import detect_project_strategy
from .semver_helper import SemverVersionHelper


class WorkflowManager:
    """
    WorkflowManager enforces Git workflow policies, tag consistency, and versioning transitions.

    Attributes:
        branch (str): Current Git branch
        tag (str): Latest Git tag
        strategy (str): 'pep440' or 'semver'
        helper (VersionHelperBase): Strategy-specific helper

    Usage:
        manager = WorkflowManager()
        manager.enforce_consistency()
        manager.check_transition(from_branch="develop", to_branch="release/1.3")

    Available Transition Cases:
        - CASE 1: main → develop (starting new feature work)
        - CASE 2: develop → release (promote dev → rc)
        - CASE 3: release → main (final release)
        - CASE 4: main → develop (start new cycle after release)
        - CASE 5: main → hotfix
        - CASE 6: hotfix → main

    """

    def __init__(self, no_debug: bool | None = False):
        self.git = GitHelper()
        self.git.runner.silent = no_debug
        self.branch = self.git.get_current_branch()
        self.tag = self.git.get_latest_tag()
        self.strategy = detect_project_strategy(no_debug=no_debug)

        if self.strategy == "pep440":
            self.helper = PEP440VersionHelper(self.tag)
        else:
            self.helper = SemverVersionHelper(self.tag)

    def enforce_consistency(self) -> None:
        print(f"✨ Current branch: {self.branch}")
        print(f"📅 Latest tag: {self.tag}\n")

        if self.branch == "develop":
            print("🔄️ Enforcing dev/beta/alpha versioning...")
            self._check_pep440_pre("dev", "alpha", "beta")
        elif self.branch.startswith("release/"):
            print("🔄️ Enforcing RC versioning...")
            self._check_pep440_pre("rc")
        elif self.branch == "main":
            print("🚀 Enforcing stable release versioning...")
            self._check_final_release()
        elif self.branch.startswith("hotfix/"):
            print("🔧 Enforcing post-release versioning...")
            self._check_post_release()
        elif self.branch.startswith("ci/"):
            print("🧪 CI branch: No tag needed.")
        elif self.branch.startswith("feature/"):
            print("✨ Feature branch: Tagging not enforced.")
        elif self.branch.startswith("archive/"):
            print("📁 Archive branch: Tagging skipped.")
        else:
            print("❗ Unrecognized branch type. Consider standardizing.")

    def _check_pep440_pre(self, *tiers: str):
        tag = self.tag.lstrip("v")
        if re.search(rf"({'|'.join(tiers)})\d+", tag):
            print(f"✅ Tag '{self.tag}' matches allowed pre-release tiers: {tiers}")
        else:
            print(
                f"❌ Tag '{self.tag}' does NOT match expected pre-release tier {tiers} for this branch."
            )

    def _check_final_release(self):
        tag = self.tag.lstrip("v")
        if re.search(r"(a|b|rc|dev|post)\d*", tag):
            print("❌ Final release must not include pre/post/dev suffix.")
        else:
            print("✅ Tag looks like a valid stable release.")

    def _check_post_release(self):
        tag = self.tag.lstrip("v")
        if ".post" in tag:
            print("✅ Tag includes '.post' suffix expected.")
        else:
            print("❌ Post-release tag expected to have '.postN' suffix.")

    def suggest_tag_for_current_branch(self) -> str:
        return self.helper.suggest_tag(self.branch)

    def check_transition(
        self,
        from_branch: str = None,
        from_tag: str = None,
        to_branch: str = None,
        to_tag: str = None,
    ) -> None:
        """
        Validates transition between two branches and version types.

        - Allows defined CASE transitions (e.g., CASE 1–6)
        - Allows same-branch tier progression (e.g., dev → a → b)
        - Allows same-branch stable updates (e.g., rc1 → rc2)
        - Flags others as unrecognized
        """
        #  Auto-detect if not given
        f_branch = from_branch or self.git.get_current_branch()
        f_tag = from_tag or self.git.get_latest_tag()
        t_branch = to_branch or f_branch
        t_tag = to_tag or f_tag

        f_ver = self.helper.classify(f_tag.lstrip("v"))
        t_ver = self.helper.classify(t_tag.lstrip("v"))

        # Summary view
        print(f"📦  From: {f_branch} ({f_ver})")
        print(f"➡️  To: {t_branch} ({t_ver})\n")

        # ✅ Allow stable, same-branch transitions
        if f_branch == t_branch and f_ver == t_ver:
            print(f"✅ Stable iteration: {f_branch} ({f_ver}) → {t_branch} ({t_tag})")
            return

        # ✅ Allow in-place tier progression (e.g. dev → a → b → rc)
        if f_branch == t_branch:
            tier_order = self.helper.tier_order()
            if tier_order.get(f_ver, -1) < tier_order.get(t_ver):
                print(
                    f"✅ Valid in-place promotion: {f_branch} ({f_ver}) → {t_branch} ({t_tag})"
                )
                return

        case_key = (f_branch.split("/")[0], f_ver, t_branch.split("/")[0], t_ver)
        cases = self.helper.get_transaction_cases()

        if case_key in cases:
            print(
                f"✅ Valid transition {cases[case_key]} — {f_branch} ({f_ver}) → {t_branch} ({t_ver})"
            )
        else:
            print(
                f"❌ Invalid or unrecognized transitions: {f_branch} ({f_ver}) → {t_branch} ({t_ver})"
            )
