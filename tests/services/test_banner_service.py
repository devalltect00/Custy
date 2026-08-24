# tests/services/test_banner_service.py

"""
tests/services/test_banner_service.py

Unit tests for BannerService.
"""

from importlib.metadata import PackageNotFoundError
from unittest.mock import MagicMock, mock_open

from app.services.banner_service import BannerService


class TestBannerService:

    def test_render_version(self, monkeypatch):
        svc = BannerService("custy")
        monkeypatch.setattr(svc, "get_version", lambda: "1.2.3")
        assert svc.render_version() == "v1.2.3"

    def test_get_version_from_package(self, monkeypatch):
        monkeypatch.setattr(
            "app.services.banner_service.version",
            lambda _: "2.0.0",
        )
        svc = BannerService("custy")
        assert svc.get_version() == "2.0.0"

    def test_get_version_falls_back(self, monkeypatch):
        def raise_exc(_):
            raise PackageNotFoundError

        monkeypatch.setattr(
            "app.services.banner_service.version",
            raise_exc,
        )
        monkeypatch.setattr(
            BannerService,
            "_get_local_version",
            lambda self: "0.1.0",
        )

        assert BannerService("custy").get_version() == "0.1.0"

    def test_render_banner(self):
        svc = BannerService("custy")
        text = svc.render_banner()
        assert isinstance(text, str)
        assert len(text) > 0

    def test_show(self, monkeypatch):
        svc = BannerService("custy")
        monkeypatch.setattr(svc, "render_banner", lambda: "BANNER")
        monkeypatch.setattr(svc, "render_version", lambda: "v1.0.0")

        printer = MagicMock()
        monkeypatch.setattr("app.services.banner_service.print", printer)

        svc.show()

        assert printer.call_count == 2
