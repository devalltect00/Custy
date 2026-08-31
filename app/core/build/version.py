"""Resolve a PEP 440 package version from a Git worktree description.

Docker excludes ``.git`` from its normal build context, so setuptools-scm
cannot discover a source version while installing Custy in an image. Make uses
this helper on the host and passes the normalized result as a Docker build
argument. No repository metadata is copied into an image layer.
"""

from __future__ import annotations

import logging
import re
import subprocess
from collections.abc import Callable
from pathlib import Path

from packaging.version import InvalidVersion, Version

logger = logging.getLogger(__name__)

DEFAULT_BUILD_VERSION = "0.1.0"
GitRunner = Callable[..., subprocess.CompletedProcess[str]]

_GIT_DESCRIPTION = re.compile(
    r"^(?P<tag>.+)-(?P<distance>\d+)-g(?P<revision>[0-9a-f]+)" r"(?:-dirty)?$",
    flags=re.IGNORECASE,
)


def version_from_git_description(
    description: str,
    *,
    fallback: str = DEFAULT_BUILD_VERSION,
) -> str:
    """Convert ``git describe --long`` output into a PEP 440 version.

    Args:
        description: Git description containing a tag, distance, and revision.
        fallback: Version returned when the description has no usable tag.

    Returns:
        Normalized PEP 440 version suitable for setuptools-scm's pretend-version
        environment variable.

    Notes:
        SemVer prerelease tags such as ``v2.0.0-rc.1`` normalize to their PEP
        440 package representation, such as ``2.0.0rc1``. Git tag spelling is
        unchanged.
    """

    match = _GIT_DESCRIPTION.fullmatch(description.strip())
    if match is None:
        return fallback

    raw_tag = match.group("tag")
    if len(raw_tag) > 1 and raw_tag[0].lower() == "v" and raw_tag[1].isdigit():
        raw_tag = raw_tag[1:]

    try:
        tagged_version = Version(raw_tag)
    except InvalidVersion:
        logger.warning("Unable to normalize Git tag as a package version: %s", raw_tag)
        return fallback

    distance = int(match.group("distance"))
    if distance == 0:
        return tagged_version.public

    if tagged_version.dev is not None:
        next_dev = tagged_version.dev + distance
        return f"{tagged_version.base_version}.dev{next_dev}"

    if tagged_version.post is not None:
        next_post = tagged_version.post + 1
        return f"{tagged_version.base_version}.post{next_post}.dev{distance}"

    return f"{tagged_version.public}.post{distance}"


def resolve_repository_version(
    root: str | Path = ".",
    *,
    fallback: str = DEFAULT_BUILD_VERSION,
    runner: GitRunner = subprocess.run,
) -> str:
    """Resolve a build version from the nearest repository tag.

    Args:
        root: Git worktree used for version discovery.
        fallback: Version returned when Git metadata is unavailable.
        runner: Injectable subprocess runner used by tests.

    Returns:
        A normalized package version or the configured fallback.

    Notes:
        The command is read-only and runs with ``shell=False``.
    """

    try:
        result = runner(
            ["git", "describe", "--tags", "--long", "--always"],
            cwd=Path(root),
            check=True,
            capture_output=True,
            text=True,
            shell=False,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        logger.warning("Unable to resolve Git build version: %s", error)
        return fallback

    return version_from_git_description(result.stdout, fallback=fallback)


def main() -> None:
    """Print the current repository version for Make and other build tools."""

    print(resolve_repository_version())


if __name__ == "__main__":
    main()
