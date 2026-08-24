# tests/core/initialize/models/test_scaffold_generator.py

"""
tests/core/initialize/test_scaffold_generator.py

Unit tests for the project scaffold generator.

These tests verify that ScaffoldGenerator correctly creates project
directories, generates template files, copies packaged template
directories, tracks execution statistics, and returns structured
execution results.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.core.initialize.models.template_dir import TemplateDir
from app.core.initialize.models.template_file import TemplateFile
from app.core.initialize.services.scaffold_generator import (
    InitializationResult,
    ScaffoldGenerator,
)
from app.core.initialize.services import scaffold_generator


class TestScaffoldGeneratorConstructor:
    """Tests for ScaffoldGenerator construction."""

    def test_construct_with_default_values(self):
        """Constructs the generator using default options."""

        generator = ScaffoldGenerator()

        assert generator.force is False
        assert generator.interactive is False
        assert generator.dry_run is False

        assert generator.created_files == 0
        assert generator.copied_files == 0
        assert generator.skipped_files == 0
        assert generator.created_directories == 0

    def test_construct_with_explicit_values(self):
        """Constructs the generator using explicit options."""

        generator = ScaffoldGenerator(
            force=True,
            interactive=True,
            dry_run=True,
        )

        assert generator.force is True
        assert generator.interactive is True
        assert generator.dry_run is True


class TestShowedSkip:
    """Tests for skip message rendering."""

    def test_prints_skip_message(self, monkeypatch):
        """Displays a skipped file message."""

        printed = MagicMock()

        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            printed,
        )

        generator = ScaffoldGenerator()

        generator._showed_skip(
            Path("example.txt"),
            "already exists",
        )

        printed.assert_called_once()


class TestCreateDirectories:
    """Tests for directory creation."""

    def test_creates_all_directories(
        self,
        tmp_path,
    ):
        """Creates every requested directory."""

        directories = [
            str(tmp_path / "one"),
            str(tmp_path / "two" / "three"),
        ]

        generator = ScaffoldGenerator()

        generator.create_directories(
            directories,
        )

        assert (tmp_path / "one").is_dir()
        assert (tmp_path / "two" / "three").is_dir()

        assert generator.created_directories == 2

    def test_dry_run_does_not_create_directories(self, tmp_path):
        """Reports planned directories without creating them."""

        target = tmp_path / "planned" / "nested"
        generator = ScaffoldGenerator(dry_run=True)

        generator.create_directories([str(target)])

        assert not target.exists()
        assert generator.created_directories == 1


class TestShouldWrite:
    """Tests for overwrite decision logic."""

    def test_returns_true_when_file_does_not_exist(
        self,
        tmp_path,
    ):
        """Allows writing new files."""

        generator = ScaffoldGenerator()

        assert generator.should_write(
            tmp_path / "missing.txt",
        )

    def test_returns_true_when_force_enabled(
        self,
        tmp_path,
    ):
        """Allows overwriting when force mode is enabled."""

        file = tmp_path / "file.txt"
        file.write_text("existing")

        generator = ScaffoldGenerator(
            force=True,
        )

        assert generator.should_write(file)

    def test_returns_false_when_file_exists(
        self,
        tmp_path,
    ):
        """Skips overwriting existing files."""

        file = tmp_path / "file.txt"
        file.write_text("existing")

        generator = ScaffoldGenerator()

        assert not generator.should_write(file)

    @pytest.mark.parametrize(
        ("answer", "expected"),
        [
            ("y", True),
            ("Y", True),
            ("n", False),
            ("", False),
        ],
    )
    def test_interactive_mode(
        self,
        monkeypatch,
        tmp_path,
        answer,
        expected,
    ):
        """Uses interactive confirmation before overwriting."""

        file = tmp_path / "file.txt"
        file.write_text("existing")

        monkeypatch.setattr(
            "builtins.input",
            lambda _: answer,
        )

        generator = ScaffoldGenerator(
            interactive=True,
        )

        assert generator.should_write(file) is expected


class TestWriteFile:
    """Tests for template file generation."""

    def test_writes_template_file(
        self,
        tmp_path,
        monkeypatch,
    ):
        """Generates a template file."""

        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )

        template = TemplateFile(
            target_path=str(tmp_path / "hello.txt"),
            content="hello",
        )

        generator = ScaffoldGenerator()

        generator.write_file(template)

        assert (tmp_path / "hello.txt").read_text() == "hello"
        assert generator.created_files == 1

    def test_skips_existing_file(
        self,
        tmp_path,
        monkeypatch,
    ):
        """Skips files that should not be overwritten."""

        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )

        file = tmp_path / "hello.txt"
        file.write_text("existing")

        template = TemplateFile(
            target_path=str(file),
            content="new",
        )

        generator = ScaffoldGenerator()

        generator.write_file(template)

        assert file.read_text() == "existing"
        assert generator.skipped_files == 1

    def test_dry_run_does_not_write_template_file(
        self,
        tmp_path,
        monkeypatch,
    ):
        """Renders a planned template without creating its target."""

        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )

        target = tmp_path / "missing" / "hello.txt"
        template = TemplateFile(
            target_path=str(target),
            content="hello",
        )
        generator = ScaffoldGenerator(dry_run=True)

        generator.write_file(template)

        assert not target.exists()
        assert not target.parent.exists()
        assert generator.created_files == 1

    def test_forced_dry_run_preserves_existing_file(
        self,
        tmp_path,
        monkeypatch,
    ):
        """Forced preview reports an overwrite without applying it."""

        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )

        target = tmp_path / "config.toml"
        target.write_text("original", encoding="utf-8")
        template = TemplateFile(
            target_path=str(target),
            content="replacement",
        )

        generator = ScaffoldGenerator(force=True, dry_run=True)
        generator.write_file(template)

        assert target.read_text(encoding="utf-8") == "original"
        assert generator.created_files == 1


class TestCopyPackageDir:
    """Tests for packaged directory copying."""

    def test_merges_into_existing_destination(
        self,
        tmp_path,
        monkeypatch,
    ):
        """Copies missing files while preserving existing files."""

        package_root = tmp_path / "package"
        source = package_root / "examples"
        source.mkdir(parents=True)
        (source / "existing.txt").write_text("replacement", encoding="utf-8")
        (source / "new.txt").write_text("new", encoding="utf-8")

        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )
        monkeypatch.setattr(
            scaffold_generator,
            "files",
            lambda _: package_root,
        )

        destination = tmp_path / "examples"
        destination.mkdir()
        (destination / "existing.txt").write_text("original", encoding="utf-8")

        generator = ScaffoldGenerator()

        generator.copy_package_dir(
            "examples",
            str(destination),
        )

        assert (
            destination / "existing.txt"
        ).read_text(encoding="utf-8") == "original"
        assert (destination / "new.txt").read_text(encoding="utf-8") == "new"
        assert generator.copied_files == 1
        assert generator.skipped_files == 1

    def test_copies_packaged_directory(self, tmp_path, monkeypatch):
        """Copies nested packaged text files during normal execution."""

        package_root = tmp_path / "package"
        source = package_root / "examples"
        (source / "nested").mkdir(parents=True)
        (source / "root.txt").write_text("root", encoding="utf-8")
        (source / "nested" / "child.txt").write_text(
            "child",
            encoding="utf-8",
        )
        destination = tmp_path / "destination"

        monkeypatch.setattr(
            scaffold_generator,
            "files",
            lambda _: package_root,
        )
        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )

        generator = ScaffoldGenerator()
        generator.copy_package_dir("examples", str(destination))

        assert (destination / "root.txt").read_text(encoding="utf-8") == "root"
        assert (
            destination / "nested" / "child.txt"
        ).read_text(encoding="utf-8") == "child"
        assert generator.copied_files == 2

    def test_force_overwrites_nested_existing_files(self, tmp_path, monkeypatch):
        """Force mode overwrites existing files throughout the resource tree."""

        package_root = tmp_path / "package"
        source = package_root / "examples"
        (source / "nested").mkdir(parents=True)
        (source / "root.txt").write_text("new root", encoding="utf-8")
        (source / "nested" / "child.txt").write_text(
            "new child",
            encoding="utf-8",
        )

        destination = tmp_path / "destination"
        (destination / "nested").mkdir(parents=True)
        (destination / "root.txt").write_text("old root", encoding="utf-8")
        (destination / "nested" / "child.txt").write_text(
            "old child",
            encoding="utf-8",
        )

        monkeypatch.setattr(
            scaffold_generator,
            "files",
            lambda _: package_root,
        )
        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )

        generator = ScaffoldGenerator(force=True)
        generator.copy_package_dir(
            "examples",
            str(destination),
            force=generator.force,
        )

        assert (
            destination / "root.txt"
        ).read_text(encoding="utf-8") == "new root"
        assert (
            destination / "nested" / "child.txt"
        ).read_text(encoding="utf-8") == "new child"
        assert generator.copied_files == 2
        assert generator.skipped_files == 0

    def test_dry_run_does_not_copy_packaged_directory(
        self,
        tmp_path,
        monkeypatch,
    ):
        """Packaged files are counted but not created during preview."""

        package_root = tmp_path / "package"
        source = package_root / "examples"
        source.mkdir(parents=True)
        (source / "example.txt").write_text("content", encoding="utf-8")
        destination = tmp_path / "destination"

        monkeypatch.setattr(
            scaffold_generator,
            "files",
            lambda _: package_root,
        )
        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )

        generator = ScaffoldGenerator(dry_run=True)
        generator.copy_package_dir("examples", str(destination))

        assert not destination.exists()
        assert generator.copied_files == 1


class TestRun:
    """Tests for the initialization workflow."""

    def test_run_returns_execution_summary(
        self,
        monkeypatch,
    ):
        """Runs the initialization workflow."""

        generator = ScaffoldGenerator()

        monkeypatch.setattr(
            generator,
            "create_directories",
            MagicMock(),
        )

        monkeypatch.setattr(
            generator,
            "write_file",
            MagicMock(),
        )

        monkeypatch.setattr(
            generator,
            "copy_package_dir",
            MagicMock(),
        )

        template = MagicMock()
        template_dir = TemplateDir(
            target="target",
            source="source",
        )

        result = generator.run(
            mode="all",
            templates=[template],
            dirs=["dir"],
            template_dirs=[template_dir],
        )

        assert isinstance(
            result,
            InitializationResult,
        )

        generator.create_directories.assert_called_once_with(
            ["dir"],
        )

        generator.write_file.assert_called_once_with(
            template,
        )

        generator.copy_package_dir.assert_called_once_with(
            "source",
            "target",
            force=False,
        )

    def test_run_handles_empty_inputs(self):
        """Runs successfully without templates or directories."""

        generator = ScaffoldGenerator()

        result = generator.run(
            mode="config",
        )

        assert isinstance(
            result,
            InitializationResult,
        )
        assert result.mode == "config"

    def test_run_marks_dry_run_result(self):
        """Execution summaries retain preview state."""

        result = ScaffoldGenerator(dry_run=True).run(mode="config")

        assert result.dry_run is True

    def test_run_copies_examples_after_creating_destination(
        self,
        tmp_path,
        monkeypatch,
    ):
        """Example files are copied after init creates their directories."""

        package_root = tmp_path / "package"
        source = package_root / "examples"
        (source / "commit_message" / "since_custy_v2").mkdir(parents=True)
        (source / "commit_message" / "since_custy_v2" / "example.txt").write_text(
            "example",
            encoding="utf-8",
        )
        destination = tmp_path / ".config" / "custy" / "templates" / "examples"

        monkeypatch.setattr(
            scaffold_generator,
            "files",
            lambda _: package_root,
        )
        monkeypatch.setattr(
            scaffold_generator.console,
            "print",
            MagicMock(),
        )

        result = ScaffoldGenerator().run(
            mode="examples",
            dirs=[
                str(destination),
                str(destination / "commit_message"),
            ],
            template_dirs=[
                TemplateDir(
                    target=str(destination),
                    source="examples",
                )
            ],
        )

        copied = destination / "commit_message" / "since_custy_v2" / "example.txt"
        assert copied.read_text(encoding="utf-8") == "example"
        assert result.copied_files == 1
