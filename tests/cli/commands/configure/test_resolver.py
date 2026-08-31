# tests/cli/commands/configure/test_resolver.py

"""Tests for credential CLI normalization."""

import pytest

from app.cli.commands.configure.resolver import (
    resolve_provider,
    resolve_setup_args,
    resolve_source,
)
from app.core.git_ops.credentials import CredentialProvider, CredentialSource
from app.core.shared import ConfigurationError


def test_provider_and_source_are_resolved():
    assert resolve_provider("github") is CredentialProvider.GITHUB
    assert resolve_source("environment") is CredentialSource.ENVIRONMENT


def test_invalid_environment_name_is_rejected():
    with pytest.raises(ConfigurationError, match="environment-variable"):
        resolve_setup_args(
            provider=CredentialProvider.GITHUB,
            source=CredentialSource.ENVIRONMENT,
            username=None,
            token_file=None,
            token_env="NOT VALID",
            replace=False,
        )
