# tests/cli/commands/init/test_models.py

"""
tests/cli/commands/init/test_models.py

Unit tests for InitArgs.
"""

from app.cli.commands.init.models import InitArgs
from app.cli.constants.enums import InitMode


class TestInitArgs:
    def test_construct_with_explicit_values(self):
        args = InitArgs(
            mode=InitMode.ALL,
            force_init=True,
            ask=False,
        )
        assert args.mode == InitMode.ALL
        assert args.force_init is True
        assert args.ask is False

    def test_construct_with_false_values(self):
        args = InitArgs(
            mode=InitMode.CONFIG,
            force_init=False,
            ask=False,
        )
        assert args.mode == InitMode.CONFIG
        assert args.force_init is False
        assert args.ask is False

    def test_instances_with_same_values_are_equal(self):
        left = InitArgs(
            mode=InitMode.TEMPLATES,
            force_init=True,
            ask=True,
        )
        right = InitArgs(
            mode=InitMode.TEMPLATES,
            force_init=True,
            ask=True,
        )
        assert left == right

    def test_repr_contains_field_values(self):
        args = InitArgs(
            mode=InitMode.EXAMPLES,
            force_init=False,
            ask=True,
        )
        representation = repr(args)
        assert "force_init=False" in representation
        assert "ask=True" in representation
