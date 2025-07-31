# tests\test_pep440_helper.py

import pytest

from app.utils.pep440_helper import PEP440VersionHelper


@pytest.mark.parametrize("current, kwargs, expected", [
    # ✅ Same tier bumps
    # 5 tests
    ("1.2.3.dev2", {"dev": True}, "1.2.3.dev3"),
    ("1.2.3a2", {"target_pre": "alpha"}, "1.2.3a3"),
    ("1.2.3b2", {"target_pre": "beta"}, "1.2.3b3"),
    ("1.2.3rc2", {"target_pre": "rc"}, "1.2.3rc3"),
    ("1.2.3.post2", {"post": True}, "1.2.3.post3"),

    # ✅ Tier upgrades (no bump needed)
    # 10 tests
    ("1.2.3.dev2", {"target_pre": "alpha"}, "1.2.3a1"),
    ("1.2.3.dev2", {"target_pre": "beta"}, "1.2.3b1"),
    ("1.2.3.dev2", {"target_pre": "rc"}, "1.2.3rc1"),
    ("1.2.3.dev2", {}, "1.2.3"),
    ("1.2.3a2", {"target_pre": "beta"}, "1.2.3b1"),
    ("1.2.3a2", {"target_pre": "rc"}, "1.2.3rc1"),
    ("1.2.3a2", {}, "1.2.3"),
    ("1.2.3b2", {"target_pre": "rc"}, "1.2.3rc1"),
    ("1.2.3b2", {}, "1.2.3"),
    ("1.2.3rc2", {}, "1.2.3"),

    # ✅ Final to post
    # 1 tests
    ("1.2.3", {"post": True}, "1.2.3.post1"),

    # 🔁 Final to Final (no pre)
    # 4 tests
    ("1.2.3", {}, "1.2.4"),
    ("1.2.3", {"level": "patch"}, "1.2.4"),
    ("1.2.3", {"level": "minor"}, "1.3.0"),
    ("1.2.3", {"level": "major"}, "2.0.0"),

    # 🔁 Final to next cycle (auto bump base)
    # 4 tests
    ("1.2.3", {"dev": True}, "1.2.4.dev1"),
    ("1.2.3", {"target_pre": "alpha"}, "1.2.4a1"),
    ("1.2.3", {"target_pre": "beta"}, "1.2.4b1"),
    ("1.2.3", {"target_pre": "rc"}, "1.2.4rc1"),

    # 🔁 Post to next cycle (auto bump base)
    # 4 tests
    ("1.2.3.post2", {"dev": True}, "1.2.4.dev1"),
    ("1.2.3.post2", {"target_pre": "alpha"}, "1.2.4a1"),
    ("1.2.3.post2", {"target_pre": "beta"}, "1.2.4b1"),
    ("1.2.3.post2", {"target_pre": "rc"}, "1.2.4rc1"),

    # Other
    ("1.2.3", {"epoch": 1}, "1!1.2.3"),
    ("1.2.3", {"local": "sha.abc123"}, "1.2.3+sha.abc123"),
])
def test_pep440_valid_transitions(current, kwargs, expected):
    helper = PEP440VersionHelper(current)
    result = helper.get_bump_version(**kwargs)
    assert result == expected

@pytest.mark.parametrize("current, kwargs", [
    # ❌ Invalid regressions
    ("1.2.3.dev2", {"post": True}),
    ("1.2.3a2", {"dev": True}),
    ("1.2.3a2", {"post": True}),
    ("1.2.3b2", {"dev": True}),
    ("1.2.3b2", {"target_pre": "alpha"}),
    ("1.2.3b2", {"post": True}),
    ("1.2.3rc2", {"dev": True}),
    ("1.2.3rc2", {"target_pre": "alpha"}),
    ("1.2.3rc2", {"target_pre": "beta"}),
    ("1.2.3rc2", {"post": True}),
    ("1.2.3.post2", {}),
])
def test_440_invalid_regressions(current, kwargs):
    helper = PEP440VersionHelper(current)
    with pytest.raises(ValueError):
        helper.get_bump_version(**kwargs)
