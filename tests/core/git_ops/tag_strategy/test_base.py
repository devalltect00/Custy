# tests/core/git_ops/tag_strategy/test_base.py

"""
tests/core/git_ops/tag_strategy/test_base.py

Unit tests for the tag strategy protocol.
"""

from app.core.git_ops.tag_strategy.base import TagStrategy


class DummyStrategy:
    """Simple implementation of the TagStrategy protocol."""

    def get_next_tag(self) -> str:
        """Return a fixed version."""
        return "v1.0.0"


class TestTagStrategy:
    """Tests for TagStrategy."""

    def test_dummy_strategy_satisfies_protocol(self):
        """A class implementing the protocol can be assigned to TagStrategy."""

        strategy: TagStrategy = DummyStrategy()

        assert strategy.get_next_tag() == "v1.0.0"

    def test_protocol_declares_get_next_tag(self):
        """The protocol exposes the expected method."""

        assert hasattr(TagStrategy, "get_next_tag")
