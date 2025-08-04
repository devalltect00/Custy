# app\utils\project_detector.py
""" """

import os

import toml


def detect_project_strategy(
    cli_value: str | None = None, no_debug: bool | None = False
) -> str:
    """
    Detects the appropriate versioning strategy for the project.

    Order of resolution
    1. CLI override
    2. Config file: .custor.toml
    3. Auto-detect via file presence
    4. Default fallback: 'semver
    """
    # Step 1: Use CLI override if provided
    if cli_value:
        return cli_value

    # Step 2: Try reading from config file
    config_files = [".custor.toml", "custor.toml"]
    for path in config_files:
        if os.path.exists(path):
            try:
                config = toml.load(path)
                strategy = config.get("versioning", {}).get("strategy")
                if strategy:
                    if not no_debug:
                        print(f"⚙️  Detected strategy from config: {strategy}")
                    return strategy
            except Exception as e:
                print(f"⚠️ Failed to parse config '{path}': {e}")

    # Step 3: Auto-detect by common project markers
    if (
        os.path.exists("pyproject.toml")
        or os.path.exists("setup.py")
        or os.path.exists("requirements.txt")
    ):
        if not no_debug:
            print("🧠 Detected Python project → strategy: pep440")
        return "pep440"
    if os.path.exists("package.json"):
        if not no_debug:
            print("🧠 Detected Javascript project → strategy: semver")
        return "semver"
    if os.path.exists("composer.json"):
        if not no_debug:
            print("🧠 Detected PHP project → strategy: semver")

    # step 4: Default fallback
    if not no_debug:
        print("⚠️ No strategy detected, using default: semver")
    return "semver"
