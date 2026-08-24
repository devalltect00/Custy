# tests/cli/utils/test_validators.py

"""
tests/cli/utils/test_validators.py

Unit tests for CLI validators.
"""

import pytest
import typer

from app.cli.utils.validators import validate_tag, validate_steps
from app.cli.constants import StepChoices


class TestValidateTag:

    def test_accepts_prefixed_tag(self):
        assert validate_tag("v1.2.3") == "v1.2.3"

    def test_adds_prefix(self):
        assert validate_tag("1.2.3") == "v1.2.3"

    def test_none(self):
        assert validate_tag(None) is None

    @pytest.mark.parametrize("tag",[
        "v1",
        "v1.2",
        "1.2",
        "hello",
        "v1.2.x",
    ])
    def test_invalid(self, tag):
        with pytest.raises(typer.BadParameter):
            validate_tag(tag)


class TestValidateSteps:

    def test_manual_steps(self):
        assert validate_steps([
            StepChoices.COMMIT,
            StepChoices.TAG,
            StepChoices.PUSH,
        ]) == ["commit","tag","push"]

    def test_release_preset(self):
        assert validate_steps([StepChoices.RELEASE]) == ["release"]

    def test_empty_steps(self):
        with pytest.raises(typer.Exit):
            validate_steps([])

    def test_duplicate_steps(self):
        with pytest.raises(typer.Exit):
            validate_steps([
                StepChoices.COMMIT,
                StepChoices.COMMIT,
            ])

    def test_mixed_manual_and_preset(self):
        with pytest.raises(typer.Exit):
            validate_steps([
                StepChoices.COMMIT,
                StepChoices.RELEASE,
            ])
