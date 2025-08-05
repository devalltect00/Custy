import pytest

from app.utils.pep440_helper import PEP440VersionHelper
from app.utils.semver_helper import SemverVersionHelper


@pytest.mark.parametrize("from_branch, from_tier, to_branch, to_tier, expected_case", [
    # PEP 440
    ("develop", "release", "develop", "dev", "CASE 1"),
    ("develop", "release", "develop", "a", "CASE 1"),
    ("develop", "release", "develop", "b", "CASE 1"),
    ("develop", "dev", "develop", "rc", "CASE 2"),
    ("develop", "a", "develop", "rc", "CASE 2"),
    ("develop", "b", "develop", "rc", "CASE 2"),
    ("release", "rc", "release", "release", "CASE 3"),
    ("main", "release", "main", "dev", "CASE 4"),
    ("main", "release", "main", "a", "CASE 4"),
    ("main", "release", "main", "b", "CASE 4"),
    ("main", "release", "main", "post", "CASE 5"),
    ("hotfix", "post", "hotfix", "release", "CASE 6"),
    ("feature", "release", "feature", "dev", "CASE 7"),
    ("feature", "dev", "feature", "dev", "CASE 7"),
    ("archive", "release", "archive", "release", "CASE 8"),
    ("archive", "dev", "archive", "release", "CASE 8"),
    ("ci", "release", "ci", "dev", "CASE 9"),
    ("ci", "dev", "ci", "dev", "CASE 9"),
])
def test_pep440_transaction_cases(from_branch, from_tier, to_branch, to_tier, expected_case):
    helper = PEP440VersionHelper("1.2.3")
    cases = helper.get_transaction_cases()
    assert cases.get((from_branch, from_tier, to_branch, to_tier)) == expected_case

@pytest.mark.parametrize("from_branch, from_tier, to_branch, to_tier, expected_case", [
    # SemVer (Semantic Versioning)
    ("develop", "release", "develop", "alpha", "CASE 1"),
    ("develop", "release", "develop", "beta", "CASE 1"),
    ("develop", "alpha", "develop", "rc", "CASE 2"),
    ("develop", "beta", "develop", "rc", "CASE 2"),
    ("release", "rc", "release", "release", "CASE 3"),
    ("main", "release", "main", "alpha", "CASE 4"),
    ("main", "release", "main", "beta", "CASE 4"),
])
def test_semver_transaction_cases(from_branch, from_tier, to_branch, to_tier, expected_case):
    helper = SemverVersionHelper("1.2.3")
    cases = helper.get_transaction_cases()
    assert cases.get((from_branch, from_tier, to_branch, to_tier)) == expected_case
