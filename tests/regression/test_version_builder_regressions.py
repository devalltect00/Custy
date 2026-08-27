# tests/regression/test_version_builder_regressions.py

"""
Regression tests for VersionBridge.

These tests protect version conversion helpers against
future regressions.
"""

from app.core.git_ops.versioning.version_bridge import VersionBridge


class TestVersionBridgeRegressions:
    """
    Regression tests for VersionBridge.
    """

    def test_pep440_to_semver_final(self):
        """
        Final releases should remain unchanged.
        """
        assert VersionBridge.pep440_to_semver("1.2.3") == "v1.2.3"

    def test_pep440_to_semver_prerelease(self):
        """
        Pre-release identifiers should convert correctly.
        """
        assert VersionBridge.pep440_to_semver("1.2.3rc1") == "v1.2.3-rc.1"

        assert VersionBridge.pep440_to_semver("1.2.3a2") == "v1.2.3-alpha.2"

        assert VersionBridge.pep440_to_semver("1.2.3b4") == "v1.2.3-beta.4"

    def test_semver_to_pep440_final(self):
        """
        Final SemVer releases should remain unchanged.
        """
        assert VersionBridge.semver_to_pep440("2.5.1") == "2.5.1"

    def test_semver_to_pep440_prerelease(self):
        """
        SemVer prereleases should convert correctly.
        """
        assert VersionBridge.semver_to_pep440("1.2.3-alpha.1") == "1.2.3a1"

        assert VersionBridge.semver_to_pep440("1.2.3-beta.2") == "1.2.3b2"

        assert VersionBridge.semver_to_pep440("1.2.3-rc.3") == "1.2.3rc3"

    def test_round_trip_final_release(self):
        """
        Converting back and forth should preserve final versions.
        """
        version = "3.4.5"

        semver = VersionBridge.pep440_to_semver(version)

        pep440 = VersionBridge.semver_to_pep440(semver)

        assert pep440 == version

    def test_round_trip_prerelease(self):
        """
        Converting prereleases back and forth should preserve
        version information.
        """
        version = "5.0.0rc2"

        semver = VersionBridge.pep440_to_semver(version)

        pep440 = VersionBridge.semver_to_pep440(semver)

        assert pep440 == version

    def test_multiple_calls_are_stateless(self):
        """
        Conversion helpers should remain stateless.
        """
        for _ in range(10):
            assert VersionBridge.pep440_to_semver("1.0.0") == "v1.0.0"

            assert VersionBridge.semver_to_pep440("1.0.0") == "1.0.0"
