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
- Executes initial and final Git workflow commands based on workflow case
"""

import re

from .dry_run_support import DryRunSupport
from .git import GitHelper
from .pep440_helper import PEP440VersionHelper
from .project_detector import detect_project_strategy
from .semver_helper import SemverVersionHelper


class WorkflowManager(DryRunSupport):
    """
    WorkflowManager

    Handles Git workflow validation and branching operations
    according to version transition CASEs and project strategy.

    - Detects versioning strategy (PEP 440 or SemVer)
    - Validates transitions between branch/tag combinations (e.g. dev → rc, rc → final)
    - Provides initial and final Git workflow steps based on transition case
    - run_initial_workflow(): prepares appropriate branch before tagging
    - run_final_workflow(): performs necessary merges or cleanup after tagging

    Transition CASEs:
    - CASE 1: develop (dev/beta/alpha) → develop (next pre)
    - CASE 2: develop (pre) → release/x.y (rc)
    - CASE 3: release/x.y (rc) → main (final)
    - CASE 4: main (final) → develop (next dev)
    - CASE 5: main (final) → hotfix/x.y.z (post)
    - CASE 6: hotfix/x.y.z (post) → main (final)
    - CASE 7: feature/* → develop
    - CASE 8: archive/* cleanup only
    - CASE 9: ci/* integration only
    """

    def __init__(
        self,
        no_debug: bool | None = False,
        sync_backup: bool | None = False,
        dry_run: bool | None = False,
    ):
        super().__init__(dry_run=dry_run)
        self.git = GitHelper()
        self.git.runner.set_silent(no_debug)
        self.branch = self.git.get_current_branch()
        self.tag = self.git.get_latest_tag()
        self.strategy = detect_project_strategy(no_debug=no_debug)
        self.runner.set_silent(no_debug)
        self.sync_backup = sync_backup

        if self.strategy == "pep440":
            self.helper = PEP440VersionHelper(self.tag)
        else:
            self.helper = SemverVersionHelper(self.tag)

    def enforce_consistency(self) -> None:
        """
        Validates that the current branch and latest tag follow expected conventions.

        - Checks if tags match expected tier (e.g., dev/beta on develop, rc on release/x.y)
        - Helps enforce clean separation of version stages across branches
        """
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
                f"❌ Tag '{self.tag}' does NOT match expected pre-release tier {tiers} for this branch.",
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
        """
        Suggests the next tag based on current branch context.

        For example:
        - develop → 1.4.0.dev1
        - release/1.4 → 1.4.0rc1
        - main → 1.4.0
        """
        return self.helper.suggest_tag(self.branch)

    def check_transition(
        self,
        from_branch: str = None,
        from_tag: str = None,
        to_branch: str = None,
        to_tag: str = None,
    ) -> str:
        """
        Validates transition between two branches and version types.

        - Allows defined CASE transitions (e.g., CASE 1–6)
        - Allows same-branch tier progression (e.g., dev → a → b)
        - Allows same-branch stable updates (e.g., rc1 → rc2)
        - Flags others as unrecognized

        Returns the matching CASE identifier if transition is valid,
        or empty string if it’s an in-place promotion.

        Returns:
            str: CASE identifier (e.g. 'CASE 2') or "" for stable/in-place bump

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

        simplified_key = (f_branch.split("/")[0], f_ver, t_branch.split("/")[0], t_ver)
        simplified_cases = self.helper.get_transaction_cases()
        reference_cases = self.helper.get_transaction_cases()

        # Match simplified case, then get its full canonical reference
        if simplified_key in simplified_cases:
            case_id = simplified_cases[simplified_key]
            for ref_key, ref_case in reference_cases.items():
                if ref_case == case_id:
                    ref_from_branch, _, ref_to_branch, _ = ref_key
                    print(
                        f"✅ Valid transition {case_id} — {ref_from_branch} ({f_ver}) → {ref_to_branch} ({t_ver})",
                    )
                    return case_id

        # ✅ Allow stable, same-branch transitions
        if f_branch == t_branch and f_ver == t_ver:
            print(f"✅ Stable iteration: {f_branch} ({f_ver}) → {t_branch} ({t_tag})")
            return ""

        # ✅ Allow in-place tier progression (e.g. dev → a → b → rc)
        if f_branch == t_branch:
            tier_order = self.helper.tier_order()
            if tier_order.get(f_ver, -1) < tier_order.get(t_ver):
                print(
                    f"✅ Valid in-place promotion: {f_branch} ({f_ver}) → {t_branch} ({t_tag})",
                )
                return ""

        print(
            f"❌ Invalid or unrecognized transitions: {f_branch} ({f_ver}) → {t_branch} ({t_ver})",
        )

        return ""

    def run_initial_workflow(self, case: str, to_tag: str):
        """
        Executes necessary Git commands to prepare branch context
        before commit/tag/bump is performed.

        Args:
            case (str): CASE identifier from check_transition()
            to_tag (str): Target tag version string

        """
        # self.helper.set_version(to_tag)

        match case:
            # CASE 1: Restart dev cycle after release
            # e.g., main → develop, release → dev
            case "CASE 1":
                self.runner.run(["git", "checkout", "develop"], check=True)
                self.runner.run(["git", "pull", "origin", "develop"], check=True)

            # CASE 2: Prepare a release candidate branch
            # e.g., develop → release/x.y
            case "CASE 2":
                release_branch = f"release/{self.helper.major}.{self.helper.minor}"
                if self.git.branch_exists(release_branch):
                    print(f"🧹 Cleaning up existing branch: {release_branch}")
                    self.cleanup_release_branch()
                self.runner.run(["git", "checkout", "-b", release_branch], check=True)

            # CASE 3: Final release merge setup
            # e.g., release/x.y → main
            case "CASE 3":
                release_branch = f"release/{self.helper.major}.{self.helper.minor}"
                self.runner.run(["git", "checkout", "main"], check=True)
                self.runner.run(["git", "pull", "origin", "main"], check=True)
                self.runner.run(["git", "merge", release_branch], check=True)

            # CASE 4: Return to development after release (continue on develop)
            # Continue development after release
            # e.g., develop remains active
            case "CASE 4":
                self.runner.run(["git", "checkout", "develop"], check=True)
                self.runner.run(["git", "pull", "origin", "develop"], check=True)

            # CASE 5: Start post-release hotfix from main
            # e.g., main → hotfix/x.y.z
            case "CASE 5":
                hotfix_branch = f"hotfix/{self.helper.major}.{self.helper.minor}.{self.helper.patch}"
                self.runner.run(["git", "checkout", "main"], check=True)
                self.runner.run(["git", "pull", "origin", "main"], check=True)
                self.runner.run(["git", "checkout", "-b", hotfix_branch], check=True)

            # CASE 6: No-op
            case "CASE 6":
                print("📦 CASE 6: hotfix merging is finalized in run_final_workflow.")

            # CASE 7: Merge feature into develop
            # e.g., feature/foo → develop
            case "CASE 7":
                self.runner.run(["git", "checkout", "develop"], check=True)
                self.runner.run(["git", "pull", "origin", "develop"], check=True)
                self.runner.run(["git", "merge", self.branch], check=True)

            # CASE 8: Archive branch (no-op)
            case "CASE 8":
                print("🗃️ Archive branch — no initial workflow actions required")

            # CASE 9: Merge CI changes into develop
            # e.g., ci/* → develop
            case "CASE 9":
                self.runner.run(["git", "checkout", "develop"], check=True)
                self.runner.run(["git", "merge", self.branch], check=True)

    def run_final_workflow(self, case: str, to_tag: str) -> bool:
        """
        Executes follow-up Git operations after push/tagging step,
        such as merging hotfix branches or cleaning up.

        Args:
            case (str): CASE identifier from check_transition()
            to_tag (str): Target tag version string

        """
        # self.helper.set_version(to_tag)
        executed = False

        match case:
            # CASE 1: No final steps required after restart
            case "CASE 1":
                print("ℹ️ CASE 1: No final merge needed. Development cycle restarted.")

            # CASE 2: No final step needed after release/x.y branch is created
            case "CASE 2":
                print("ℹ️ CASE 2: No final merge needed. RC development in progress.")

            # CASE 3: Finalize main branch and push
            case "CASE 3":
                self.runner.run(["git", "checkout", "develop"], check=True)
                self.runner.run(["git", "rebase", "main"], check=True)
                self.runner.run(
                    ["git", "push", "--follow-tags", "origin", "develop"],
                    check=True,
                )
                if self.sync_backup:
                    self.runner.run(
                        ["git", "push", "--follow-tags", "backup", "develop"],
                        check=True,
                    )
                # self.cleanup_release_branch()
                executed = True

            # CASE 4: No final merge needed
            case "CASE 4":
                print("ℹ️ CASE 4: No final merge needed. Continue working in 'develop'.")

            # CASE 5: No-op
            case "CASE 5":
                print(
                    "📦 CASE 5: Hotfix branch created. Finalization handled in CASE 6.",
                )

            # CASE 6: Merge hotfix/x.y.z → main and cleanup
            case "CASE 6":
                hotfix_branch = f"hotfix/{self.helper.major}.{self.helper.minor}.{self.helper.patch}"
                self.runner.run(["git", "checkout", "main"], check=True)
                self.runner.run(["git", "merge", hotfix_branch], check=True)
                self.runner.run(["git", "push", "origin", "main"], check=True)
                if self.sync_backup:
                    self.runner.run(["git", "push", "backup", "main"], check=True)
                # self.cleanup_hotfix_branch()
                executed = True

            # CASE 7: No final merge needed
            case "CASE 7":
                print(
                    "ℹ🔁 CASE 7: Feature branch merged into develop. You may delete it if desired.",
                )

            # CASE 8: Archive branch finalization (informational)
            case "CASE 8":
                print("✅ Archived branch is finalized. You may delete or preserve it.")

            # CASE 9: Finalize CI/CD logic merge to main
            case "CASE 9":
                self.runner.run(["git", "checkout", "main"], check=True)
                self.runner.run(["git", "merge", self.branch], check=True)
                self.runner.run(["git", "push", "origin", "main"], check=True)
                if self.sync_backup:
                    self.runner.run(["git", "push", "backup", "main"], check=True)
                executed = True

        return executed

    def cleanup_release_branch(self):
        release_branch = f"release/{self.helper.major}.{self.helper.minor}"
        self.runner.run(["git", "branch", "-d", release_branch], check=True)
        self.runner.run(["git", "push", "origin", "--delete", release_branch], check=True)
        if self.sync_backup: self.runner.run(["git", "push", "backup", "--delete", release_branch], check=True)

    def cleanup_hotfix_branch(self):
        hotfix_branch = f"hotfix/{self.helper.major}.{self.helper.minor}.{self.helper.patch}"
        self.runner.run(["git", "branch", "-d", hotfix_branch], check=True)
        self.runner.run(["git", "push" "origin", "--delete", hotfix_branch], check=True)
        if self.sync_backup: self.runner.run(["git", "push", "backup", "--delete", hotfix_branch], check=True)
