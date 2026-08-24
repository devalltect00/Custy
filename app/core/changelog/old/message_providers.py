# app/core/changelog/old/message_providers.py

import logging
from typing import List, Protocol

from app.core.git_ops.git.service import GitService

logger = logging.getLogger(__name__)


class MessageProvider(Protocol):
    """
    Protocol for message providers.

    Implementations must define:
        get_messages(prev, current, is_latest)

    Returns:
        list[str]: commit messages
    """

    def get_messages(self, prev: str, current: str, is_latest: bool = False) -> List[str]:
        # raise NotImplementedError
        ...


class GitMessageProvider(MessageProvider):
    """
    Fetch commit messages from Git history.

    This provider retrieves commit messages between two tags
    using GitService.

    Args:
        git (GitService): Git service instance
    """

    def __init__(self, git: GitService) -> None:
        self.git = git

    def get_messages(self, prev: str, current: str, is_latest: bool = False) -> List[str]:
        try:
            return self.git.get_commits_between(prev, current)
        except Exception:
            logger.exception("Failed to get git messages")
            return []


class TemplateMessageProvider(MessageProvider):
    """
    Load messages from a commit message template.

    This provider injects template content as a synthetic commit message.

    Useful for:
        - Unreleased section
        - Manual notes
        - Release highlights

    Args:
        loader (callable): Function returning template content
        only_unreleased (bool): Inject only for latest/unreleased
    """

    def __init__(self, loader, only_unreleased: bool = True) -> None:
        self.loader = loader
        self.only_unreleased = only_unreleased

    def get_messages(self, prev: str, current: str, is_latest: bool = False) -> List[str]:
        """
        Treat template as ONE commit message
        Only inject into "Unreleased" (current == "")

        Load template content as message.

        Logic:
            - Inject only when current == "" (Unreleased)
            - Treat template as a single commit message

        Args:
            prev (str): Previous tag
            current (str): Current tag
            is_latest (bool): Whether latest release

        Returns:
            list[str]: List containing template message or empty

        Raises:
            None (fails safely)
        """
        try:
            if self.only_unreleased and current != "":
                return []

            content = self.loader()

            if not content:
                logger.debug("Template is empty")
                return []

            return [content.strip()]

        except Exception:
            logger.exception("Failed to load template messages")
            return []
