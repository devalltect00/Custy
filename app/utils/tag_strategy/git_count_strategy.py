# app\utils\tag_strategy\git_count_strategy.py
"""
GitCountStrategy class
"""

import subprocess
import sys

# =======================
# 🔧 Concrete Strategies
# =======================


class GitCountStrategy:
    def get_next_tag(self) -> str:
        try:
            command = ["git", "rev-list", "--count", "HEAD"]
            count = subprocess.check_output(
                command,
                text=True,
            ).strip()
            # count = result.stdout.strip()
            return f"v{count}"
        except subprocess.CalledProcessError:
            print("❌ Error: Failed to count Git commits.")
            sys.exit(1)
