# app/core/git_ops/versioning/builder/release_builder.py

import re
from datetime import datetime

from app.config import load_custy_config

from ..models.release_info import ReleaseInfo
from ..models.version_type import VersionType


# -----------------------------
# 🧱 Release Note Builder
# -----------------------------
class ReleaseNoteBuilder:
    """
    Builder for generating structured release note content for commit messages and tag annotations.

    Usage:
        builder = ReleaseNoteBuilder(release_info)
        commit_msg = builder.build_commit_msg()
        tag_msg = builder.build_tag_msg()
    """

    def __init__(self, info: ReleaseInfo):
        self.info = info
        self.settings = load_custy_config()

    def build_commit_msg(self) -> str:
        """
        Generate the commit-message.txt content.
        """
        vt = self.info.version_type
        ver = self.info.version
        app = self.info.app_name
        commit_type = self._commit_type()

        if vt.is_final_release():
            # === Final release commit message ===
            header = f"{commit_type}(main): {ver}"
            description = self._description()
            additional = self._additional_info()
            bullet_placeholder = "- *(Nothing yet)* — See tag message for full context."

            # Merge description and additional  into one cohesive paragraph block
            # body_block = "\n".join(filter(None, [description, additional]))

            lines = [
                header,
                "",
                description,
                "",
            ]

            if additional:
                lines.append(additional)

            lines += [
                "All functionality has been fully validated and production-ready.",
                "",
                bullet_placeholder,
                "",
                "---",
                "",
                f"🎉 **{app} {ver} is now stable and ready for production use.**",
                "",
                "🔖 **Tags**:",
                f"- Type: `#{commit_type}`",
                "- Stability: `#stable`",
                "",
                "Changelog: handled separately",
            ]
        else:
            # === Pre-release commit message ===
            header = f"{self._commit_type()}(release): {self.info.version}"
            description = self._description()
            additional = self._additional_info()
            intro = self._manual_section_intro()
            bullet_placeholder = "- *(Nothing yet)* — See tag message for full context."

            # Merge description and additional  into one cohesive paragraph block
            # body_block = "\n".join(filter(None, [description, additional]))

            lines = [header, "", description]

            if additional:
                lines.append(additional)

            lines += [
                "",
                intro,
                bullet_placeholder,
                "",
                "---",
                "",
                f"_Tag: `{ver}`_",
                "",
                "🔖 **Tags**:",
                f"- Type: `#{commit_type}`",
                f"- Stability: `#{vt.value}`",
            ]

        return "\n".join(lines)

    def build_tag_msg(self) -> str:
        """
        Generate the tag-message.txt content.
        """
        title = self._tag_header()
        description = self._tag_description()
        footer = self._tag_footer()

        lines = [
            title,
            "",
            description,
            "",
            "### ✨ Highlights",
            "",
            "- *(Nothing yet)*",
        ]

        if self.info.version_type == VersionType.FINAL and self.info.latest_prerelease:
            lines += [
                "",
                f"### 🛠️ Other improvements since {self.info.latest_prerelease}",
                "",
                "- *(Nothing yet)*",
            ]

        lines += [
            "",
            "---",
            "",
        ]
        lines.append(footer)
        lines = self._append_footer_metadata(lines)

        return "\n".join(lines)

    def _manual_section_intro(self) -> str:
        vt = self.info.version_type
        return {
            VersionType.FINAL: "This final release includes all validated features and fixes from earlier pre-releases:",
            VersionType.POST: "This post-release includes minor updates and corrections after the official release:",
            VersionType.ALPHA: "This alpha includes early experiments changes, and prototype features:",
            VersionType.BETA: "This beta includes several bug fixes and enhancements:",
            VersionType.RC: "This release candidate consolidates finalized features and bug fixes before the stable release:",
            VersionType.DEV: "This dev snapshot includes unstable changes for internal testing and early validation:",
        }.get(vt, "This release includes:")

    def _commit_type(self) -> str:
        """
        Determine commit type based on version type.
        """
        # return "docs" if self.info.version_type in [VersionType.FINAL, VersionType.POST] else "chore"
        return "<type>"

    def _description(self) -> str:
        """
        Generate the main description for commit/tag message.
        """
        app = self.info.app_name
        vt = self.info.version_type
        ver = self.info.version
        short_ver = re.match(r"v?(\d+)\.(\d+)\.(\d+)", ver).group()

        if vt == VersionType.FINAL:
            return f"Final release of **{app} {short_ver}**, promoted from the latest release candidate."
        if vt == VersionType.POST:
            return f"Post-release patch for **{app} {short_ver}**, addressing minor updates or corrections."
        if vt == VersionType.RC:
            return f"Release candidate for **{app} {short_ver}**, consolidating all pre-release changes and preparing for stable release."
        if vt == VersionType.BETA:
            return f"Beta release for **{app} {short_ver}**, introducing mid-stage features and workflow improvements."
        if vt == VersionType.ALPHA:
            return f"Alpha release for **{app} {short_ver}**, containing early foundational changes and experimental features."
        if vt == VersionType.DEV:
            return f"Internal dev snapshot for **{app} {short_ver}**, used for unstable testing only."
        return ""

    def _additional_info(self) -> str:
        """Generate additional info block under the description."""
        vt = self.info.version_type
        ver = self.info.version
        if vt == VersionType.FINAL:
            tags = ", ".join(self.info.prerelease_tags)
            msg = f"Includes all feature and fixes from pre-releases: {tags}."
            if (
                len(self.info.prerelease_tags) == 1
                and not self.info.has_changes_since_rc
            ):
                msg += f"No Changes since {self.info.latest_prerelease}."
            return msg
        if vt == VersionType.POST:
            return f"Includes minor updates or documentation fixes after release {ver.split('.post')[0]}."
        if vt == VersionType.RC:
            return "Feature-complete and undergoing final validation before stable release."
        if vt == VersionType.BETA:
            return "Partially validated features and improvements. Some issue still remain."
        if vt == VersionType.ALPHA:
            return "Used for early testing and feedback"
        if vt == VersionType.DEV:
            return "Unstable and experimental build and internal testing."
        return ""

    def _tag_header(self) -> str:
        """
        Generate the tag title header.
        """
        label = {
            VersionType.FINAL: "Final",
            VersionType.POST: "Post",
            VersionType.RC: "Release Candidate",
            VersionType.BETA: "Beta",
            VersionType.ALPHA: "Alpha",
            VersionType.DEV: "Dev",
        }.get(self.info.version_type, "Release")

        icon = {
            VersionType.FINAL: "✅",
            VersionType.POST: "📝",
            VersionType.RC: "📦",
            VersionType.BETA: "🧪",
            VersionType.ALPHA: "🧬",
            VersionType.DEV: "⚙️",
        }.get(self.info.version_type, "📌")
        # return f"\U0001f9ea {label} Release {self.info.app_name} {self.info.version}"
        return f"{icon} {label} Release {self.info.app_name} {self.info.version}"

    def _tag_description(self) -> str:
        """
        Generate the tag description section.
        """
        app = self.info.app_name
        ver = self.info.version
        short_ver = re.match(r"v?(\d+)\.(\d+)\.(\d+)", ver).group()
        vt = self.info.version_type
        return {
            VersionType.FINAL: f"**{app} {short_ver}** is now stable and production-ready. All feature and fixes from pre-releases (alpha, beta, rc) are included.",
            VersionType.POST: f"This post-release applies minor corrections or documentation updates to the original **{short_ver}** release.",
            VersionType.RC: f"Release candidate for **{app} {short_ver}** — Including finalized features and fixes. Awaiting final validation.",
            VersionType.BETA: f"Beta release for **{app} {short_ver}** — focusing on mid-stage features and improved automation.",
            VersionType.ALPHA: f"Alpha release for **{app} {short_ver}** — introducing experimental features and foundational changes.",
            VersionType.DEV: "Internal development snapshot for testing unstable or work-in-progress features.",
        }.get(vt, "")

    def _tag_footer(self) -> str:
        """
        Generate the footer notice section.
        """
        return {
            VersionType.FINAL: "✅ This version is **stable** and **suitable** for production use.",
            VersionType.POST: "✅ This version is **stable** and **suitable** for production use.",
            VersionType.RC: "ℹ️ This is a **release-candidate** feature-complete but pending final validation before stable release.",
            VersionType.BETA: "ℹ️ This is a **beta pre-release** and is **not recommended for production use**.",
            VersionType.ALPHA: "ℹ️ This is an **alpha pre-release** and is **not intended for production use**.",
            VersionType.DEV: "⚠️ For internal use only. Experimental and unstable.",
        }.get(self.info.version_type, "")

    def _append_footer_metadata(self, lines: list[str]) -> str:
        author = self.settings.get("custom_author") or None
        show_date = self.settings.get("include_date", False)
        if author:
            lines.append(f"_Author: {author}_")
        if show_date:
            today = datetime.now().strftime("%Y-%m-%d")
            lines.append(f"_Date: {today}_")

        return lines
