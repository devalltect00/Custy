# tests/regression/test_step_registry_regressions.py

"""
tests/regression/test_step_registry_regressions.py

Regression tests for StepRegistry.

These tests protect the registration system against future
refactoring mistakes.
"""

import pytest

from app.core.pipeline.registry import StepRegistry
from app.core.pipeline.steps.base_step import BaseStep


class DummyStep(BaseStep):
    """
    Dummy pipeline step for registry testing.
    """

    @property
    def name(self) -> str:
        return "dummy"

    def execute(self, ctx):
        pass


class TestStepRegistryRegressions:
    """
    Regression tests for StepRegistry.
    """

    def test_registered_step_can_be_created(self):
        """
        Regression:
        A registered step should always be creatable.
        """
        name = "dummy_step"

        if name in StepRegistry._registry:
            del StepRegistry._registry[name]

        StepRegistry.register(name, DummyStep)

        step = StepRegistry.create(name)

        assert isinstance(step, DummyStep)

        del StepRegistry._registry[name]

    def test_duplicate_registration_raises_error(self):
        """
        Regression:
        Registering the same step twice must raise ValueError.
        """
        name = "dummy_step"

        if name in StepRegistry._registry:
            del StepRegistry._registry[name]

        StepRegistry.register(name, DummyStep)

        with pytest.raises(ValueError):
            StepRegistry.register(name, DummyStep)

        del StepRegistry._registry[name]

    def test_unknown_step_raises_key_error(self):
        """
        Regression:
        Creating an unknown step must raise KeyError.
        """
        with pytest.raises(KeyError):
            StepRegistry.create("__unknown_step__")

    def test_registered_step_returns_correct_class(self):
        """
        Regression:
        get() should return the registered class.
        """
        name = "dummy_step"

        if name in StepRegistry._registry:
            del StepRegistry._registry[name]

        StepRegistry.register(name, DummyStep)

        assert StepRegistry.get(name) is DummyStep

        del StepRegistry._registry[name]

    def test_registry_does_not_modify_existing_entries(self):
        """
        Regression:
        Registering another step must not affect existing ones.
        """
        first = "dummy_step_1"
        second = "dummy_step_2"

        for key in (first, second):
            if key in StepRegistry._registry:
                del StepRegistry._registry[key]

        StepRegistry.register(first, DummyStep)
        StepRegistry.register(second, DummyStep)

        assert StepRegistry.get(first) is DummyStep
        assert StepRegistry.get(second) is DummyStep

        del StepRegistry._registry[first]
        del StepRegistry._registry[second]
