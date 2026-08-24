# app/core/git_ops/tag_strategy/date_strategy.py
"""
Date-based tag strategy.
"""

from datetime import datetime

# =======================
# 🔧 Concrete Strategies
# =======================


class DateStrategy:
    """
    Generate version based on current date.

    Format:
        vYYYY.MM.DD

    Args:
        use_prefix_v (bool): whether to prefix with 'v'
    """
    def __init__(
        self,
        use_prefix_v: bool = True,
    ) -> None:
        self.use_prefix_v = use_prefix_v

    def get_next_tag(self) -> str:
        next_version = datetime.now().strftime("%Y.%m.%d")
        if self.use_prefix_v:
            # return "v" + next_version
            return f"v{next_version}"
        return next_version
