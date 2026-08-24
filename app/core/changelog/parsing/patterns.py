# app/core/changelog/parsing/patterns.py

from __future__ import annotations

import re

RC_PATTERN = re.compile(
    r"rc\d+$",
    re.IGNORECASE,
)

BETA_PATTERN = re.compile(
    r"b\d+$",
    re.IGNORECASE,
)

ALPHA_PATTERN = re.compile(
    r"a\d+$",
    re.IGNORECASE,
)

DEV_PATTERN = re.compile(
    r"(?:\.?dev\d+)$",
    re.IGNORECASE,
)

POST_PATTERN = re.compile(
    r"(?:\.?post\d+)$",
    re.IGNORECASE,
)

PROMOTED_FROM_PATTERN = re.compile(
    r"Includes\s+all\s+feature\s+and\s+fixes\s+from\s+pre-releases:\s*(.+)",
    re.IGNORECASE,
)

TAG_SECTION_PATTERN = re.compile(
    r"^-\s*(.+?):\s*(.+)$",
    re.MULTILINE,
)
