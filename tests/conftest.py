# tests/conftest.py

"""
tests/conftest.py

Global pytest fixtures.

This module performs one-time initialization required by the
test suite before any tests are executed.
"""

import pytest

from app.core.pipeline.registry import StepRegistry
from app.core.pipeline.step_registry import register_all_steps


@pytest.fixture(scope="session", autouse=True)
def register_pipeline_steps():
    """
    Register all pipeline steps once for the entire test session.

    PipelineBuilder relies on StepRegistry to dynamically create
    pipeline step instances. Production code performs this during
    application startup, but tests must initialize the registry
    explicitly.
    """
    if not StepRegistry._registry:
        register_all_steps()
