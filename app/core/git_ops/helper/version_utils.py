# app/core/git_ops/helper/version_utils.py

import logging
import re

from app.constants.git_workflow_rules import ALLOWED_COMMIT_TYPES

logger = logging.getLogger(__name__)


def assert_is_final_version(version: str, context: str = "changelog") -> bool:
    """
    Ensures the given version is a final release (not pre-release).
    Exists if version is a pre-release like a1, b1, rc1, or dev1.

    Logic:
        - Reject versions containing:
            a, b, rc, dev (PEP440)
            -alpha, -beta, -rc, -dev (SemVer)

    Args:
        version (str): Version string
        context (str): Context name (e.g., "changelog")

    Returns:
        bool:
            True if valid final version
            False otherwise

    Examples:
        >>> assert_is_final_version("1.2.3")
        True
        >>> assert_is_final_version("1.2.3rc1")
        False
    """
    # PEP440 + SemVer pre/dev detection
    pattern = r"(a|b|rc|dev)\d+|-(alpha|beta|rc|dev)\.\d+"

    # validate final version version if used in release context
    # if re.search(r"(a|b|rc|dev)\d+", version):
    if re.search(pattern, version):
        logger.warning(
            f"⚠️ Skipping {context} generation for pre-release versions: {version}"
        )
        logger.info("ℹ️ Only final versions like v1.2.3 are allowed.")
        return False

    return True


def maybe_assert_is_final(
    version: str,
    context: str,
    force: bool = False,
) -> bool:
    """
    Optionally asserts the version is final, unless force is True.

    Args:
        version (str): Version string
        context (str): Context name
        force (bool): Skip validation if True

    Returns:
        bool
    """
    if force:
        print(
            f"⚠️  Skipping final version check for {context} due to --force-changelog flag.",
        )
        return True

    return assert_is_final_version(version, context)


# =========================================================
# ===================== COMMIT ANALYSIS ====================
# =========================================================


def contains_allowed_commit_type(commits: list[str]) -> bool:
    """
    Check if any commit in the list matches an allowed semantic type.

    Logic:
        - Parse first line of each commit
        - Match against Conventional Commit format
        - Validate against ALLOWED_COMMIT_TYPES

    Args:
        commits (List[str]): List of commit messages

    Returns:
        bool: True if at least one valid commit exists

    Examples:
        >>> contains_allowed_commit_type(["feat: add feature"])
        True
    """
    pattern = re.compile(r"(\w+)(\(.*\))?!?:")

    for msg in commits:
        first_line = msg.strip().splitlines()[0] if msg else ""

        match = pattern.match(first_line)
        if match:
            commit_type = match.group(1)

            if commit_type in ALLOWED_COMMIT_TYPES:
                return True

        return False


def classify_commit_type(first_line: str) -> str | None:
    """
    Extract the commit type (e.g., feat, fix, fix, chore) from the first line of a commit message.
    Returns None if not matched.

    Args:
        first_line (str): First line of commit message

    Returns:
        str | None: Commit type or None if not matched

    Examples:
        >>> classify_commit_type("feat(auth): add login")
        'feat'
    """
    match = re.match(r"(\w+)(\(.*\))?!?:", first_line)
    return match.group(1) if match else None


# =========================================================
# ===================== TAG NORMALIZATION ==================
# =========================================================


def normalize_version_tag(tag: str) -> str:
    """
    Normalize version tag by removing prefix.

    Args:
        tag (str): Version tag (e.g., 'v1.2.3')

    Returns:
        str: Normalized version (e.g., '1.2.3')
    """
    return tag.lstrip("v")


def is_semver(tag: str) -> bool:
    """
    Check if version follows SemVer pattern.

    Args:
        tag (str): Version string

    Returns:
        bool
    """
    tag = tag.lstrip("v")
    return bool(re.match(r"\d+\.\d+\.\d+(-[a-z]+\.\d+)?(\+.*)?", tag))


def is_pep440(tag: str) -> bool:
    """
    Check if version follows PEP440 pattern (basic).

    Args:
        tag (str): Version string

    Returns:
        bool
    """
    tag = tag.lstrip("v")
    return bool(
        re.match(r"\d+\.\d+\.\d+([a-z]+\d+)?(\.post\d+)?(\.dev\d+)?(\+.*)?", tag)
    )
