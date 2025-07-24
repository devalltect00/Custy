# tools\utils\tag_strategy\date_strategy.py
"""
DateStrategy class
"""

from datetime import datetime

# =======================
# 🔧 Concrete Strategies
# =======================


class DateStrategy:
    def get_next_tag(self) -> str:
        return "v" + datetime.now().strftime("%Y.%m.%d")
