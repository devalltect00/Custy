import unittest

from app.utils.workflow_manager import WorkflowManager


class DummyHelper:
    def get_transaction_cases(self1):
        return {
            # PEP440 Version
            ("develop", "release", "develop", "dev"): "CASE 1",
            ("develop", "release", "develop", "a"): "CASE 1",
            ("develop", "release", "develop", "b"): "CASE 1",
            ("develop", "dev", "develop", "rc"): "CASE 2",
            ("develop", "a", "develop", "rc"): "CASE 2",
            ("develop", "b", "develop", "rc"): "CASE 2",
            ("release", "rc", "release", "release"): "CASE 3",
            ("main", "release", "main", "dev"): "CASE 4",
            ("main", "release", "main", "a"): "CASE 4",
            ("main", "release", "main", "b"): "CASE 4",
            ("main", "release", "main", "post"): "CASE 5",
            ("hotfix", "post", "hotfix", "release"): "CASE 6",
            ("feature", "release", "feature", "dev"): "CASE 7",
            ("feature", "dev", "feature", "dev"): "CASE 7",
            ("archive", "release", "archive", "release"): "CASE 8",
            ("archive", "dev", "archive", "release"): "CASE 8",
            ("ci", "release", "ci", "dev"): "CASE 9",
            ("ci", "dev", "ci", "dev"): "CASE 9",

            # SemVer (Semantic Version)
            ("develop", "release", "develop", "alpha"): "CASE 1",
            ("develop", "release", "develop", "beta"): "CASE 1",
            ("develop", "alpha", "develop", "rc"): "CASE 2",
            ("develop", "beta", "develop", "rc"): "CASE 2",
            ("release", "rc", "release", "release"): "CASE 3",
            ("main", "release", "main", "alpha"): "CASE 4",
            ("main", "release", "main", "beta"): "CASE 4",

        }

class DummyWorkfloManager:
    def __init__(self, helper) -> None:
        self.helper = helper

    def check_transition(
        self,
        from_branch: str = None,
        from_tier: str = None,
        to_branch: str = None,
        to_tier: str = None,
    ) -> str | None:
        key = (from_branch, from_tier, to_branch, to_tier)
        return self.helper.get_transaction_cases().get(key, None)

class testWorkflowCaseDetection(unittest.TestCase):
    def setUp(self):
        self.helper = DummyHelper()
        self.manager = DummyWorkfloManager(self.helper)

    def test_case_1(self):
        self.assertEqual(self.manager.check_transition("develop", "release", "develop", "dev"), "CASE 1")
        self.assertEqual(self.manager.check_transition("develop", "release", "develop", "a"), "CASE 1")
        self.assertEqual(self.manager.check_transition("develop", "release", "develop", "b"), "CASE 1")
        self.assertEqual(self.manager.check_transition("develop", "release", "develop", "alpha"), "CASE 1")
        self.assertEqual(self.manager.check_transition("develop", "release", "develop", "beta"), "CASE 1")

    def test_case_2(self):
        self.assertEqual(self.manager.check_transition("develop", "dev", "develop", "rc"), "CASE 2")
        self.assertEqual(self.manager.check_transition("develop", "a", "develop", "rc"), "CASE 2")
        self.assertEqual(self.manager.check_transition("develop", "b", "develop", "rc"), "CASE 2")
        self.assertEqual(self.manager.check_transition("develop", "alpha", "develop", "rc"), "CASE 2")
        self.assertEqual(self.manager.check_transition("develop", "beta", "develop", "rc"), "CASE 2")

    def test_case_3(self):
        self.assertEqual(self.manager.check_transition("release", "rc", "release", "release"), "CASE 3")

    def test_case_4(self):
        self.assertEqual(self.manager.check_transition("main", "release", "main", "dev"), "CASE 4")
        self.assertEqual(self.manager.check_transition("main", "release", "main", "a"), "CASE 4")
        self.assertEqual(self.manager.check_transition("main", "release", "main", "b"), "CASE 4")
        self.assertEqual(self.manager.check_transition("main", "release", "main", "alpha"), "CASE 4")
        self.assertEqual(self.manager.check_transition("main", "release", "main", "beta"), "CASE 4")

    def test_case_5(self):
        self.assertEqual(self.manager.check_transition("main", "release", "main", "post"), "CASE 5")

    def test_case_6(self):
        self.assertEqual(self.manager.check_transition("hotfix", "post", "hotfix", "release"), "CASE 6")

    def test_case_7(self):
        self.assertEqual(self.manager.check_transition("feature", "release", "feature", "dev"), "CASE 7")
        self.assertEqual(self.manager.check_transition("feature", "dev", "feature", "dev"), "CASE 7")

    def test_case_8(self):
        self.assertEqual(self.manager.check_transition("archive", "release", "archive", "release"), "CASE 8")
        self.assertEqual(self.manager.check_transition("archive", "dev", "archive", "release"), "CASE 8")

    def test_case_8(self):
        self.assertEqual(self.manager.check_transition("ci", "release", "ci", "dev"), "CASE 9")
        self.assertEqual(self.manager.check_transition("ci", "dev", "ci", "dev"), "CASE 9")

if __name__ == "__main__":
    unittest.main()
