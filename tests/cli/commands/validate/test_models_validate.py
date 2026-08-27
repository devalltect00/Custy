# tests/cli/commands/validate/test_models_validate.py

"""
tests/cli/commands/validate/test_models.py

Unit tests for ValidateArgs.
"""

from pathlib import Path

from app.cli.commands.validate.models import ValidateArgs


class TestValidateArgs:
    def test_construct_with_explicit_values(self):
        args = ValidateArgs(
            commit_message_file=Path("commit.txt"),
            tag_message_file=Path("tag.txt"),
            version_file=Path("app/__version__.py"),
            auto_stage=True,
            stage_mode="all",
            check_cz=True,
        )

        assert args.commit_message_file == Path("commit.txt")
        assert args.tag_message_file == Path("tag.txt")
        assert args.version_file == Path("app/__version__.py")
        assert args.auto_stage is True
        assert args.stage_mode == "all"
        assert args.check_cz is True

    def test_dataclass_equality(self):
        left = ValidateArgs(None, None, None, False, None, False)
        right = ValidateArgs(None, None, None, False, None, False)
        assert left == right

    def test_repr_contains_field_names(self):
        args = ValidateArgs(None, None, None, False, None, False)
        text = repr(args)
        assert "auto_stage" in text
        assert "check_cz" in text
