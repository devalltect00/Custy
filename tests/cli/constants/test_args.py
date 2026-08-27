# tests/cli/constants/test_args.py

"""
tests/cli/constants/test_args.py

Unit tests for CliArgs.
"""

from app.cli.constants.args import CliArgs


class TestCliArgs:
    def test_empty_instance(self):
        args = CliArgs()

        assert args.__dict__ == {}

    def test_single_argument(self):
        args = CliArgs(dry_run=True)

        assert args.dry_run is True

    def test_multiple_arguments(self):
        args = CliArgs(
            dry_run=True,
            debug=False,
            remote="origin",
            strategy="semver",
        )

        assert args.dry_run is True
        assert args.debug is False
        assert args.remote == "origin"
        assert args.strategy == "semver"

    def test_dynamic_attributes(self):
        values = {
            "foo": 123,
            "bar": "hello",
            "baz": True,
        }

        args = CliArgs(**values)

        for key, value in values.items():
            assert getattr(args, key) == value

    def test_mutable_after_creation(self):
        args = CliArgs()

        args.remote = "backup"

        assert args.remote == "backup"
