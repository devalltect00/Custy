# tests/cli/utils/test_validators.py

"""
tests/cli/utils/test_validators.py

Unit tests for CLI validators.
"""

import pytest
import typer

from app.cli.constants import StepChoices
from app.cli.utils.validators import validate_steps, validate_tag


class TestValidateTag:
    @pytest.mark.parametrize(
        ("tag", "expected"),
        [
            ("v1.2.3", "v1.2.3"),
            ("1.2.3", "v1.2.3"),
            ("v1.2.3-alpha.1", "v1.2.3-alpha.1"),
            ("v1.2.3-beta.2", "v1.2.3-beta.2"),
            ("v1.2.3-rc.3", "v1.2.3-rc.3"),
            ("1.2.3-dev.4", "v1.2.3-dev.4"),
            ("1.2.3-post.5", "v1.2.3-post.5"),
            ("1.2.3a1", "v1.2.3a1"),
            ("1.2.3b2", "v1.2.3b2"),
            ("1.2.3rc3", "v1.2.3rc3"),
            ("1.2.3.dev4", "v1.2.3.dev4"),
            ("1.2.3.post5", "v1.2.3.post5"),
            ("v1.2.3+linux.x86", "v1.2.3+linux.x86"),
            ("v1.2.3-rc.1+build.7", "v1.2.3-rc.1+build.7"),
        ],
    )
    def test_accepts_supported_release_tags(self, tag, expected):
        assert validate_tag(tag) == expected

    def test_none(self):
        assert validate_tag(None) is None

    @pytest.mark.parametrize(
        "tag",
        [
            "v1",
            "v1.2",
            "1.2",
            "hello",
            "v1.2.x",
            "v01.2.3",
            "v1.2.3-rc",
            "v1.2.3-rc.x",
            "v1.2.3-preview.1",
            "v1.2.3-rc.1.extra",
            "v1.2.3+",
            "v1.2.3 rc1",
        ],
    )
    def test_invalid(self, tag):
        with pytest.raises(typer.BadParameter):
            validate_tag(tag)


class TestValidateSteps:
    def test_manual_steps(self):
        assert validate_steps(
            [
                StepChoices.COMMIT,
                StepChoices.TAG,
                StepChoices.PUSH,
            ]
        ) == ["commit", "tag", "push"]

    def test_release_preset(self):
        assert validate_steps([StepChoices.RELEASE]) == ["release"]

    def test_empty_steps(self):
        with pytest.raises(typer.Exit):
            validate_steps([])

    def test_duplicate_steps(self):
        with pytest.raises(typer.Exit):
            validate_steps(
                [
                    StepChoices.COMMIT,
                    StepChoices.COMMIT,
                ]
            )

    def test_mixed_manual_and_preset(self):
        with pytest.raises(typer.Exit):
            validate_steps(
                [
                    StepChoices.COMMIT,
                    StepChoices.RELEASE,
                ]
            )
