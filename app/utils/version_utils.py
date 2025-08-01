# app\utils\version_utils.py

import re
import sys

ALLOWED_COMMIT_TYPES = {"feat", "fix", "perf", "docs", "refactor", "release"}


def assert_is_final_version(version: str, context: str = "changelog") -> bool:
    """
    Ensures the given version is a final release (not pre-release).
    Exists if version is a pre-release like a1, b1, rc1, or dev1.

    """
    # validate final version version if used in release context
    if re.search(r"(a|b|rc|dev)\d+", version):
        print(f"❌ Cannot generate {context} for pre-release versions: {version}")
        print("ℹ️ Only final versions like v1.2.3 are allowed.")
        return False
        # sys.exit(1)
    return True


def maybe_assert_is_final(version: str, context: str, force: bool = False) -> bool:
    """
    Optionally asserts the version is final, unless force is True.
    """
    if force:
        print(
            f"⚠️  Skipping final version check for {context} due to --force-changelog flag."
        )
        return True
    return assert_is_final_version(version, context)


def contains_allowed_commit_type(commits: list[str]) -> bool:
    """
    Check if any commit in the list matches an allowed semantic type.
    """
    pattern = re.compile(r"(\w+)(\(.*\))?!?:")
    for msg in commits:
        first_line = msg.strip().splitlines()[0] if msg else ""
        match = pattern.match(first_line)
        if match and match.group(1) in ALLOWED_COMMIT_TYPES:
            return True
        return False
