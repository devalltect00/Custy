# tests/core/git_ops/git/test_factory.py

"""
Tests for app.core.git_ops.git.factory.

Coverage target:
    100%
"""

from unittest.mock import MagicMock, patch

from app.core.git_ops.git.factory import create_git_service


class TestCreateGitService:
    """
    Tests for create_git_service().
    """

    @patch("app.core.git_ops.git.factory.GitCommandExecutor")
    @patch("app.core.git_ops.git.factory.GitService")
    def test_default_arguments(
        self,
        service_cls,
        executor_cls,
    ):
        """
        Factory creates executor then GitService using default values.
        """

        executor = MagicMock()
        service = MagicMock()

        executor_cls.return_value = executor
        service_cls.return_value = service

        result = create_git_service()

        executor_cls.assert_called_once_with(
            dry_run=False,
            # no_debug=False,
            is_silent=False,
        )

        # service_cls.assert_called_once_with(executor)

        assert result is service

        service_cls.assert_called_once()

        _, kwargs = service_cls.call_args

        assert kwargs["executor"] is executor
        assert "config" in kwargs

    @patch("app.core.git_ops.git.factory.GitCommandExecutor")
    @patch("app.core.git_ops.git.factory.GitService")
    def test_custom_arguments(
        self,
        service_cls,
        executor_cls,
    ):
        """
        Factory forwards constructor options.
        """

        executor = MagicMock()
        service = MagicMock()

        executor_cls.return_value = executor
        service_cls.return_value = service

        result = create_git_service(
            dry_run=True,
            no_debug=True,
        )

        executor_cls.assert_called_once_with(
            dry_run=True,
            # no_debug=True,
            is_silent=True,
        )

        # service_cls.assert_called_once_with(executor)

        assert result is service

        service_cls.assert_called_once()

        args, kwargs = service_cls.call_args

        assert args == ()
        assert kwargs["executor"] is executor
        # assert "config" in kwargs
        assert kwargs["config"] is not None
