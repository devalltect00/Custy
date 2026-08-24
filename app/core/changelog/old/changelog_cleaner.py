# app/core/changelog/old/changelog_cleaner.py

import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ChangelogCleaner:
    """
    Cleans commit message bodies by removing noise and extracting meaningful lines.

    This class is driven by configuration under [changelog.cleaning].
    """

    def __init__(self, config: Optional[Dict] = None) -> None:
        """
        Initialize cleaner with configuration.

        Args:
            config (dict | None): Cleaning configuration.

        Raises:
            TypeError: If config is not a dictionary.
        """
        if config is not None and not isinstance(config, dict):
            raise TypeError("config must be a dictionary or None")

        self.config: Dict = config or {}

        self.remove_separators: List[str] = self.config.get("remove_separators", ["---"])
        self.remove_headers: bool = self.config.get("remove_headers", True)
        self.remove_hash_lines: bool = self.config.get("remove_hash_lines", True)
        self.remove_release_notes: bool = self.config.get("remove_release_notes", True)
        self.remove_metadata: bool = self.config.get("remove_metadata", True)
        self.remove_keywords: List[str] = self.config.get("remove_keywords", [])

    def _is_separator(self, line: str) -> bool:
        return any(line.strip() == sep for sep in self.remove_separators)

    def _is_header(self, line: str) -> bool:
        return line.startswith("#")
    
    def _is_hash_line(self, line: str) -> bool:
        return line.startswith("#")

    def _contains_keyword(self, line: str) -> bool:
        return any(kw.lower() in line.lower() for kw in self.remove_keywords)

    def _is_release_noise(self, line: str) -> bool:
        patterns = ["final release", "production-ready", "includes all feature"]
        return any(p in line.lower() for p in patterns)

    def _is_metadata(self, line: str) -> bool:
        patterns = ["🔖", "type:", "stability:"]
        return any(p in line.lower() for p in patterns)

    def clean_commit(self, commit: Dict) -> List[str]:
        """
        Clean commit body and extract meaningful lines.

        Args:
            commit (dict): Parsed commit object.

        Returns:
            list[str]: Cleaned lines.

        Raises:
            KeyError: If commit structure is invalid (rare).
        """
        try:
            body: str = commit.get("body", "")
            lines = body.splitlines()

            cleaned: List[str] = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # -------------------------
                # REMOVE BASED ON CONFIG
                # -------------------------

                # separators (---)
                if self.remove_separators and self._is_separator(line):
                    continue

                # markdown headers (#, ##)
                if self.remove_headers and self._is_header(line):
                    continue

                # hash lines (# Conflicts:)
                if self.remove_hash_lines and self._is_hash_line(line):
                    continue

                # keyword-based removal (MOST IMPORTANT)
                if self.remove_keywords and self._contains_keyword(line):
                    continue

                # release narrative
                if self.remove_release_notes and self._is_release_noise(line):
                    continue

                # metadata
                if self.remove_metadata and self._is_metadata(line):
                    continue

                # conflicts
                if line.lower().startswith("conflicts"):
                    continue

                # -------------------------
                # KEEP ONLY BULLETS OR MEANINGFUL LINES
                # -------------------------
                if line.startswith("- "):
                    # KEEP ONLY BULLETS
                    cleaned.append(line[2:].strip())
                else:
                    ### Handle if the message is not in bullet format but still meaningful
                    cleaned.append(line.strip())

            return cleaned

        except Exception as e:
            logger.exception("Failed to clean commit")
            return []
