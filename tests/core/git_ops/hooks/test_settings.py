# tests/core/git_ops/hooks/test_settings.py

"""Tests for typed Git hook policy configuration."""

import pytest

from app.core.git_ops.hooks import GitHookMode, GitHookSettings
from app.core.shared import ConfigurationError


class TestGitHookSettings:
    """Validate defaults, supported modes, and invalid TOML values."""

    def test_defaults_to_auto(self) -> None:
        """Missing configuration keeps adaptive safe behavior enabled."""

        assert GitHookSettings.from_mapping(None).mode is GitHookMode.AUTO

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("auto", GitHookMode.AUTO),
            ("native", GitHookMode.NATIVE),
            ("pre_commit", GitHookMode.PRE_COMMIT),
            ("pre-commit", GitHookMode.PRE_COMMIT),
        ],
    )
    def test_accepts_supported_modes(
        self,
        raw: str,
        expected: GitHookMode,
    ) -> None:
        """Documented spellings resolve to the expected enum."""

        assert GitHookSettings.from_mapping({"mode": raw}).mode is expected

    @pytest.mark.parametrize("raw", ["skip", 3, True])
    def test_rejects_unsupported_modes(self, raw: object) -> None:
        """Custy does not expose a silent hook-bypass configuration."""

        with pytest.raises(ConfigurationError):
            GitHookSettings.from_mapping({"mode": raw})
