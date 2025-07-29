# app\utils\tag_strategy\base.py
"""
TagStrategy protocol/interface
"""

# =======================
# 🔧 Tag Strategy Pattern
# =======================

from typing import Protocol


class TagStrategy(Protocol):
    def get_next_tag(self) -> str: ...
