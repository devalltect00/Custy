# app/core/changelog/old/message_aggregator.py

import logging
from typing import List

logger = logging.getLogger(__name__)


class MessageAggregator:
    """
    Aggregates messages from multiple providers (git, template, etc).
    """

    def __init__(self, providers: List, mode: str = "append_top") -> None:
        """
        Args:
            providers (list): Message providers.
            mode (str): Merge strategy.
        """
        self.providers = providers
        self.mode = mode

    def get_messages(self, prev: str, current: str, is_latest: bool = False) -> List[str]:
        """
        Collect and merge messages from providers.

        Args:
            prev (str): Previous tag.
            current (str): Current tag.
            is_latest (bool): Whether this is latest release.

        Returns:
            list[str]: Combined messages.
        """
        try:
            collected = [
                p.get_messages(prev, current, is_latest=is_latest)
                for p in self.providers
            ]

            git_msgs = collected[0] if collected else []
            template_msgs = collected[1] if len(collected) > 1 else []

            # print("self.mode",self.mode)

            # print("template_msgs",template_msgs)
            # print("git_msgs",git_msgs)

            if self.mode == "override":
                return template_msgs

            if self.mode == "append_top":
                return template_msgs + git_msgs

            if self.mode == "append_bottom":
                return git_msgs + template_msgs

            if self.mode == "merge":
                return git_msgs + template_msgs

            return git_msgs + template_msgs

        except Exception:
            logger.exception("Failed to aggregate messages")
            return []
