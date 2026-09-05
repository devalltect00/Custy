# tests/core/editor/test_docker_assets.py

"""Regression tests for editor tools and keybindings shipped in Docker."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
EDITOR_ASSETS = PROJECT_ROOT / "docker" / "editors"


class TestDockerEditorAssets:
    """Tests for image packages and non-conflicting editor configuration."""

    def test_dockerfile_installs_and_copies_supported_editors(self) -> None:
        """The production-capable base contains every default container editor."""

        dockerfile = (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")

        for package in ("micro", "nano", "vim"):
            assert f"    {package} " in dockerfile
        assert "COPY docker/editors /etc/custy/editors" in dockerfile
        assert "ENV CUSTY_CONTAINER=1" in dockerfile

    def test_production_image_installs_optional_hook_runtime(self) -> None:
        """Cross-platform pre-commit fallback is available in production."""

        dockerfile = (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")

        assert 'pip install --no-cache-dir ".[commitizen,hooks]"' in dockerfile

    def test_micro_adds_alt_undo_and_redo_aliases(self) -> None:
        """Micro receives aliases without replacing its native Ctrl shortcuts."""

        bindings = json.loads(
            (EDITOR_ASSETS / "micro" / "bindings.json").read_text(encoding="utf-8")
        )

        assert bindings == {"Alt-z": "Undo", "Alt-y": "Redo"}

    def test_nano_preserves_non_conflicting_native_meta_keys(self) -> None:
        """Nano keeps M-U/M-E because M-Z/M-Y already control UI features."""

        nanorc = (EDITOR_ASSETS / "nanorc").read_text(encoding="utf-8")

        assert "bind M-U undo main" in nanorc
        assert "bind M-E redo main" in nanorc
        assert "bind M-Z" not in nanorc
        assert "bind M-Y" not in nanorc

    def test_vim_adds_alt_aliases_in_normal_and_insert_modes(self) -> None:
        """Vim aliases cover normal and insert mode while native keys remain."""

        vimrc = (EDITOR_ASSETS / "vimrc").read_text(encoding="utf-8")

        assert "nnoremap <silent> <M-z> u" in vimrc
        assert "nnoremap <silent> <M-y> <C-r>" in vimrc
        assert "inoremap <silent> <M-z> <C-o>u" in vimrc
        assert "inoremap <silent> <M-y> <C-o><C-r>" in vimrc
