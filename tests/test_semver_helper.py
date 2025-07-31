# tests\test_semver_helper.py

import pytest

from app.utils.semver_helper import SemverVersionHelper


@ pytest.mark.parametrize("current, kwargs, expected", [
    # ✅ Same tier bumps
    # 5 tests
    ("1.2.3-alpha.2", {"target_pre": "alpha"}, "1.2.3-alpha.3"),
    ("1.2.3-beta.2", {"target_pre": "beta"}, "1.2.3-beta.3"),
    ("1.2.3-rc.2", {"target_pre": "rc"}, "1.2.3-rc.3"),
    ("1.2.3-alpha.2", {"level": "patch", "target_pre": "alpha"}, "1.2.3-alpha.3"),
    ("1.2.3-beta.2", {"level": "patch", "target_pre": "beta"}, "1.2.3-beta.3"),
    ("1.2.3-rc.2", {"level": "patch", "target_pre": "rc"}, "1.2.3-rc.3"),

    # ✅ Tier upgrades
    # 10 tests
    ("1.2.3-alpha.2", {"target_pre": "beta"}, "1.2.3-beta.1"),
    ("1.2.3-alpha.2", {"target_pre": "rc"}, "1.2.3-rc.1"),
    ("1.2.3-beta.2", {"target_pre": "rc"}, "1.2.3-rc.1"),
    ("1.2.3-alpha.2", {"level": "patch", "target_pre": "beta"}, "1.2.3-beta.1"),
    ("1.2.3-alpha.2", {"level": "patch", "target_pre": "rc"}, "1.2.3-rc.1"),
("1.2.3-beta.2", {"level": "patch", "target_pre": "rc"}, "1.2.3-rc.1"),

    # 🔁 Final to pre-release
    # 1 tests
    ("1.2.3", {"target_pre": "alpha"}, "1.2.4-alpha.1"),
    ("1.2.3", {"target_pre": "beta"}, "1.2.4-beta.1"),
    ("1.2.3", {"target_pre": "rc"}, "1.2.4-rc.1"),
    ("1.2.3", {"level": "patch", "target_pre": "alpha"}, "1.2.4-alpha.1"),
    ("1.2.3", {"level": "patch", "target_pre": "alpha"}, "1.2.4-alpha.1"),
    ("1.2.3", {"level": "patch", "target_pre": "beta"}, "1.2.4-beta.1"),
    ("1.2.3", {"level": "minor", "target_pre": "beta"}, "1.3.0-beta.1"),
    ("1.2.3", {"level": "minor", "target_pre": "rc"}, "1.3.0-rc.1"),
    ("1.2.3", {"level": "minor", "target_pre": "rc"}, "1.3.0-rc.1"),
    ("1.2.3", {"level": "major", "target_pre": "alpha"}, "2.0.0-alpha.1"),
    ("1.2.3", {"level": "major", "target_pre": "beta"}, "2.0.0-beta.1"),
    ("1.2.3", {"level": "major", "target_pre": "rc"}, "2.0.0-rc.1"),

    # 🔁 Final to Final (no pre)
    # 1 tests
    ("1.2.3", {}, "1.2.4"),
    ("1.2.3", {"level": "patch"}, "1.2.4"),
    ("1.2.3", {"level": "minor"}, "1.3.0"),
    ("1.2.3", {"level": "major"}, "2.0.0"),

    # ✅ pre-release to Final
    ("1.2.3-beta.2", {}, "1.2.3"),
    ("1.2.3-rc.2", {}, "1.2.3"),
    ("1.2.3-alpha.2", {}, "1.2.3"),
    ("1.2.3-beta.2", {"level": "patch"}, "1.2.3"),
    ("1.2.3-rc.2", {"level": "patch"}, "1.2.3"),
    ("1.2.3-alpha.2", {"level": "patch"}, "1.2.3"),

    # ✅ Add build metadata
    # 4 tests
    ("1.2.3", {"build": "sha.abc123"}, "1.2.4+sha.abc123"),
    ("1.2.3-beta.2", {"target_pre": "beta", "build": "sha.abc123"}, "1.2.3-beta.3+sha.abc123"),
    ("1.2.3", {"level": "patch", "build": "sha.abc123"}, "1.2.4+sha.abc123"),
    ("1.2.3-beta.2", {"level": "patch", "target_pre": "beta", "build": "sha.abc123"}, "1.2.3-beta.3+sha.abc123"),

    # ✅ v-prefix
    # 4 tests
    ("1.2.3", {"prefix_v": True}, "v1.2.4"),
    ("1.2.3", {"target_pre": "alpha", "prefix_v": True}, "v1.2.4-alpha.1"),
    ("1.2.3", {"level": "patch", "prefix_v": True}, "v1.2.4"),
    ("1.2.3", {"level": "patch", "target_pre": "alpha", "prefix_v": True}, "v1.2.4-alpha.1"),
])
def test_semver_valid_transitions(current, kwargs, expected):
    helper = SemverVersionHelper(current)
    result = helper.get_bump_version(**kwargs)
    assert result == expected

# tests\test_semver_helper.py

import pytest

from app.utils.semver_helper import SemverVersionHelper


@ pytest.mark.parametrize("current, kwargs", [
    # ❌ Invalid regressions
    ("1.2.3-beta.2", {"target_pre": "alpha"}),
    ("1.2.3-rc.2", {"target_pre": "alpha"}),
    ("1.2.3-rc.2", {"target_pre": "beta"}),
    ("1.2.3-beta.2", {"level": "patch", "target_pre": "alpha"}),
    ("1.2.3-rc.2", {"level": "patch", "target_pre": "alpha"}),
    ("1.2.3-rc.2", {"level": "patch", "target_pre": "beta"}),
])
def test_semver_tier_regression_disallowed(current, kwargs):
    helper = SemverVersionHelper(current)
    with pytest.raises(ValueError):
        helper.get_bump_version(**kwargs)

