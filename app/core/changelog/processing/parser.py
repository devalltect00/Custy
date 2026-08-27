# app/core/changelog/processing/parser.py

"""
Commit Parser

Parses Conventional Commit messages into strongly typed
commit models.

The parser is responsible only for interpreting commit
message content. It does not communicate with Git or
perform any changelog processing.
"""

from __future__ import annotations

import re

from app.core.changelog.models.commit import (
    Commit,
)
from app.core.changelog.models.commit_section import (
    CommitSection,
)
from app.core.changelog.models.commit_subsection import (
    CommitSubsection,
)


class CommitParser:
    """
    Parse Conventional Commit messages.
    """

    HEADER_PATTERN = re.compile(
        r"^"
        r"(?P<type>\w+)"
        r"(?:\((?P<scope>[^\)]+)\))?"
        r"(?P<breaking>!)?"
        r":\s*"
        r"(?P<subject>.+)"
        r"$"
    )

    BREAKING_KEYWORD = "BREAKING CHANGE"

    SECTION_PATTERN = re.compile(r"^###\s+(.+)$")

    SUBSECTION_PATTERN = re.compile(r"^####\s+(.+)$")

    BULLET_PATTERN = re.compile(r"^(?:[-*+]|\u2022)\s+(.+)$")

    TAG_FOOTER_PATTERN = re.compile(
        r"^(?:\U0001f516\s*)?(?:\*\*)?tags(?:\*\*)?:?$",
        re.IGNORECASE,
    )

    TAG_LINE_PATTERN = re.compile(
        r"^_?tag\s*:",
        re.IGNORECASE,
    )

    def parse(
        self,
        message: str,
        *,
        commit_hash: str = "",
        commit_date: str = "",
    ) -> Commit:
        """
        Parse a raw commit message.

        Args:
            message:
                Full commit message.

            commit_hash:
                Git commit hash.

            commit_date:
                Commit creation date.

        Returns:
            Parsed commit model.
        """

        lines = message.strip().splitlines()

        if not lines:
            raise ValueError("Commit message cannot be empty.")

        header = lines[0].strip()

        body = "\n".join(lines[1:]).strip()

        commit_type = "other"
        scope = None
        subject = header
        breaking = False

        match = self.HEADER_PATTERN.fullmatch(header)

        if match:
            commit_type = match.group("type")

            scope = match.group("scope")

            subject = match.group("subject").strip()

            breaking = bool(match.group("breaking"))

        if self.BREAKING_KEYWORD in body:
            breaking = True

        return Commit(
            subject=subject,
            body=body,
            sections=self._parse_sections(
                body,
            ),
            commit_type=commit_type,
            scope=scope,
            breaking=breaking,
            commit_date=commit_date,
            hash=commit_hash,
        )

    def parse_many(
        self,
        messages: list[str],
    ) -> list[Commit]:
        """
        Parse multiple commit messages.

        Args:
            messages:
                Raw commit messages.

        Returns:
            Parsed commit models.
        """

        return [self.parse(message) for message in messages]

    def _parse_sections(
        self,
        body: str,
    ) -> list[CommitSection]:
        """
        Parse Markdown sections and subsections from
        the commit body.

        Supported hierarchy::

            ### Section

            -Item

            #### Subsection

            -Item

        Any heading deeper than level 4 is flattened
        into the current subsection.
        """

        sections: list[CommitSection] = []

        current_section: CommitSection | None = None

        current_subsection: CommitSubsection | None = None

        for line in body.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            if (
                self.TAG_FOOTER_PATTERN.match(stripped)
                or self.TAG_LINE_PATTERN.match(stripped)
                or stripped.casefold().startswith("changelog:")
            ):
                break

            #
            # -------------------------------------------------
            # ### Section
            # -------------------------------------------------
            #
            match = self.SECTION_PATTERN.match(
                stripped,
            )

            if match:
                current_section = CommitSection(
                    title=match.group(
                        1,
                    ).strip(),
                )

                sections.append(
                    current_section,
                )

                current_subsection = None

                continue

            #
            # -------------------------------------------------
            # #### Subsection
            # -------------------------------------------------
            #
            match = self.SUBSECTION_PATTERN.match(
                stripped,
            )

            if match:
                if current_section is None:
                    current_section = CommitSection(
                        title="",
                    )
                    sections.append(current_section)

                current_subsection = CommitSubsection(
                    title=match.group(
                        1,
                    ).strip(),
                )

                current_section.subsections.append(
                    current_subsection,
                )

                continue

            #
            # -------------------------------------------------
            # ##### or deeper
            #
            # Flatten into current subsection.
            # -------------------------------------------------
            #
            if stripped.startswith("#####"):
                if current_subsection:
                    current_subsection.title += " > " + stripped.lstrip("#").strip()

                continue

            #
            # -------------------------------------------------
            # Bullet
            # -------------------------------------------------
            #
            match = self.BULLET_PATTERN.match(
                stripped,
            )

            if match:
                if current_section is None:
                    current_section = CommitSection(
                        title="",
                    )
                    sections.append(current_section)

                item = match.group(
                    1,
                ).strip()

                if current_subsection:
                    current_subsection.items.append(
                        item,
                    )

                else:
                    current_section.items.append(
                        item,
                    )

        return sections
