# tests/cli/commands/version/test_models_version.py

"""
tests/cli/commands/version/test_models.py

Unit tests for VersionArgs.
"""

from pathlib import Path

from app.cli.commands.version.models import VersionArgs
from app.cli.constants import StrategyChoices, BumpChoices


class TestVersionArgs:

    def test_construct_with_explicit_values(self):
        args = VersionArgs(
            version_file=Path("app/__version__.py"),
            tag="v1.2.3",
            strategy=StrategyChoices.SEMVER,
            bump=BumpChoices.PATCH,
        )

        assert args.version_file == Path("app/__version__.py")
        assert args.tag == "v1.2.3"
        assert args.strategy == StrategyChoices.SEMVER
        assert args.bump == BumpChoices.PATCH

    def test_dataclass_equality(self):
        left = VersionArgs(None, None, None, None)
        right = VersionArgs(None, None, None, None)
        assert left == right

    def test_repr_contains_fields(self):
        args = VersionArgs(None, "v1.0.0", None, None)
        text = repr(args)
        assert "tag='v1.0.0'" in text
