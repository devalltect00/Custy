# tests/core/pipeline/steps/validation/test_ensure_commit_validation_provider_step.py

"""Tests for the provider-aware validation preflight step."""

from unittest.mock import MagicMock

from app.core.pipeline.steps.validation.ensure_commit_validation_provider_step import (
    EnsureCommitValidationProviderStep,
)


def test_execute_delegates_to_provider_preflight() -> None:
    """The pipeline step delegates without embedding provider logic."""

    context = MagicMock()

    EnsureCommitValidationProviderStep().execute(context)

    context.engine.ensure_commit_validation_provider.assert_called_once_with()
