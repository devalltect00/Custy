# app/core/changelog/config/repository.py

"""Resolve safe repository URLs for changelog comparison links."""

from __future__ import annotations

import logging
from urllib.parse import urlsplit

from app.core.changelog.config.models import LinksConfig

logger = logging.getLogger(__name__)

_PLACEHOLDER_PATHS = {
    "org/project",
    "owner/repo",
    "your-org/your-project",
    "your-organization/your-project",
}


def resolve_compare_repository(links: LinksConfig) -> str | None:
    """Return a normalized browser URL when compare links are safe to build.

    Args:
        links: Repository-link configuration resolved from ``config.toml``.

    Returns:
        The normalized repository URL, or ``None`` when comparison links are
        disabled or cannot be configured safely.

    Notes:
        Invalid link configuration is recoverable. Custy logs an actionable
        warning and continues changelog generation without comparison links.
    """

    if not links.enable_compare:
        return None

    raw_repository = links.repository

    if raw_repository is not None and not isinstance(raw_repository, str):
        _warn_and_skip("repository must be a string")
        return None

    repository = (raw_repository or "").strip().rstrip("/")

    if not repository:
        _warn_and_skip("repository is empty")
        return None

    parsed = urlsplit(repository)
    repository_path = parsed.path.strip("/")

    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or not repository_path
        or any(character.isspace() for character in repository)
    ):
        _warn_and_skip(
            "repository must be a valid HTTP or HTTPS browser URL",
        )
        return None

    normalized_path = repository_path.removesuffix(".git").casefold()

    if normalized_path in _PLACEHOLDER_PATHS:
        _warn_and_skip(
            "repository still contains an example owner/project value",
        )
        return None

    return repository.removesuffix(".git")


def _warn_and_skip(reason: str) -> None:
    """Log one actionable explanation for omitted comparison links.

    Args:
        reason: Human-readable reason the repository URL was rejected.
    """

    logger.warning(
        "Changelog comparison links were skipped because %s. "
        "Set tool.custy.changelog.links.repository to the project's browser "
        "URL, or set enable_compare = false.",
        reason,
    )
