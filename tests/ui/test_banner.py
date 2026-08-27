# tests/ui/test_banner.py

"""
tests/ui/test_banner.py

Unit tests for the shared application banner.

These tests verify that the module exposes a BannerService instance
configured with the expected application metadata.
"""

from app.services.banner_service import BannerService
from app.ui.banner import banner


class TestBanner:
    """Tests for the shared banner instance."""

    def test_banner_is_banner_service_instance(self):
        """Exposes a BannerService instance."""

        assert isinstance(
            banner,
            BannerService,
        )

    def test_banner_uses_expected_package_name(self):
        """Uses the expected application package name."""

        assert banner.package_name == "Custy"

    def test_banner_uses_expected_font(self):
        """Uses the expected banner font."""

        assert banner.font == "cosmic"
