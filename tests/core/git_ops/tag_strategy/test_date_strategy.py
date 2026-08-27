# tests/core/git_ops/tag_strategy/test_date_strategy.py

"""
tests/core/git_ops/tag_strategy/test_date_strategy.py

Unit tests for the date-based tag generation strategy.

These tests verify that DateStrategy generates version tags based on the
current date, with or without the optional 'v' prefix.
"""

from datetime import datetime

import pytest

from app.core.git_ops.tag_strategy import date_strategy
from app.core.git_ops.tag_strategy.date_strategy import DateStrategy


class DummyDateTime:
    """Simple datetime replacement used for deterministic testing."""

    @classmethod
    def now(cls):
        """Return a fixed point in time."""

        return datetime(
            2026,
            6,
            27,
            12,
            34,
            56,
        )


class TestDateStrategy:
    """Tests for DateStrategy."""

    @pytest.mark.parametrize(
        ("use_prefix_v", "expected"),
        [
            (True, "v2026.06.27"),
            (False, "2026.06.27"),
        ],
    )
    def test_construct_with_explicit_values(
        self,
        use_prefix_v,
        expected,
        monkeypatch,
    ):
        """Constructs the strategy using explicit configuration."""

        monkeypatch.setattr(
            date_strategy,
            "datetime",
            DummyDateTime,
        )

        strategy = DateStrategy(
            use_prefix_v=use_prefix_v,
        )

        assert strategy.use_prefix_v is use_prefix_v
        assert strategy.get_next_tag() == expected

    def test_default_configuration_uses_prefix_v(
        self,
        monkeypatch,
    ):
        """Uses the 'v' prefix by default."""

        monkeypatch.setattr(
            date_strategy,
            "datetime",
            DummyDateTime,
        )

        strategy = DateStrategy()

        assert strategy.use_prefix_v is True
        assert strategy.get_next_tag() == "v2026.06.27"
