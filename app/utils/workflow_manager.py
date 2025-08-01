# app\utils\workflow_manager.py

import re

from .git import GitHelper
from .pep440_helper import PEP440VersionHelper
from .semver_helper import SemverVersionHelper


class WorkflowManager:
    """
    WorkflowManager handles Git workflow enforcement and validation based on branching and tagging strategy.

    It ensures consistency between branch names and version tags by detecting the correct strategy (PEP440 or SemVer).

    Strategy Selection:
    - Uses detect_project_strategy() to choose between PEP440VersionHelper (for Python) or SemverVersionHelper (for JS, PHP).

    Features:
    - enforce_consistency(): Validates current branch/tag rules
    - suggest_tag_for_current_branch(): Suggests next semantic version
    - check_transition(): Validates state changes between branches and tag states (e.g. develop → release)
    """
    """
    WorkflowManager handles Git workflow enforcement and validation based on branching and tagging strategy.

    It ensures consistency between branch names and PEP 440-compliant version tags,
    and validates transitions across stages like develop → release → main.

    Supported Use Cases:
    - Enforce version rules on current branch (e.g., dev on develop, rc on release/*, etc.)
    - Suggest next tag based on branch context
    - Validate branch + version transitions (e.g., Case 1–5 logic)
    """
    def __init(self):
        self.git = GitHelper()
        self.branch = self.git.get_current_branch()
        self.tag = self.git.get_latest_tag()

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
            print(f"❌ Tag '{self.tag}' does NOT match expected pre-release tier {tiers} for this branch.")

    def _check_final_release(self):
        tag = self.tag.lstrip("v")
        if re.search(r"(a|b|rc|dev|post)\d*", tag):
            print(f"❌ Final release must not include pre/post/dev suffix.")
        else:
            print(f"✅ Tag looks like a valid stable release.")

    def _check_post_release(self):
        tag = self.tag.lstrip("v")
        if ".post" in tag:
            print(f"✅ Tag includes '.post' suffix expected.")
        else:
            print(f"❌ Post-release tag expected to have '.postN' suffix.")

    def suggest_tag_for_current_branch(self) -> str:
        # Optional: Generate suggested tag
        from .project_detector import detect_project_strategy
        strategy = detect_project_strategy()

        if strategy == "pep440":
            helper = PEP440VersionHelper(self.tag)
        else:
            helper = SemverVersionHelper(self.tag)
        if self.branch == "develop":
            return helper.get_bump_version(target_pre="dev")
        elif self.branch.startswith("release/"):
            return helper.get_bump_version(target_pre="rc")
        elif self.branch == "main":
            return helper.get_bump_version()  # final
        elif self.branch.startswith("hotfix/"):
            return helper.get_bump_version(post=True)
        else:
            return self.tag  # No change

    def check_transition(
            self,
            from_branch: str = None,
            from_tag: str = None,
            to_branch: str = None,
            to_tag: str = None
        ) -> None:
        def classify(tag: str) -> str:
            if re.search(r"\.post\d+", tag):
                return "post"
            elif re.search(r"(a|alpha)\d+", tag):
                return "a"
            elif re.search(r"(b|beta)\d+", tag):
                return "b"
            elif re.search(r"(rc\d+", tag):
                return "rc"
            elif re.search(r"dev\d+", tag):
                return "dev"
            else:
                return "release"

        #  Auto-detect if not given
        f_branch = from_branch or self.git.get_current_branch()
        f_tag = from_tag or self.git.get_latest_tag()
        t_branch = to_branch or f_branch
        t_tag = to_tag or f_tag

        f_ver = classify(f_tag.lstrip("v"))
        t_ver = classify(t_tag.lstrip("v"))

        # Summary view
        print(f"📦 From: {f_branch} ({f_ver})")
        print(f"➡️ To: {t_branch} ({t_ver})\n")

        # Case transition map
        cases = {
            ("main", "release", "develop", "dev"): "CASE 1",
            ("develop", "dev", "release", "rc"): "CASE 2",
            ("release", "rc", "main", "release"): "CASE 3",
            ("main", "release", "develop", "dev"): "CASE 4",
            ("main", "release", "hotfix", "post"): "CASE 5",
            ("hotfix", "post", "main", "release"): "CASE 6",
        }

        matched_case = cases.get((f_branch.split("/")[0], f_ver, t_branch.split("/")[0], t_ver))
        if matched_case:
            print(f"✅ Valid transition {matched_case} — {f_branch} ({f_ver}) → {t_branch} ({t_ver})")
        else:
            print(f"❌ Invalid or unrecognized transitions: {f_branch} ({f_ver}) → {t_branch} ({t_ver})")
