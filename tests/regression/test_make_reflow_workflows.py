# tests/regression/test_make_reflow_workflows.py

"""Regression tests for Custy's published-image Reflow Make workflows."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAKE_CORE = PROJECT_ROOT / "make" / "core"


def _read(relative_path: str) -> str:
    """Read a Make module using a path relative to ``make/core``."""
    return (MAKE_CORE / relative_path).read_text(encoding="utf-8")


def _target_names(text: str) -> set[str]:
    """Return explicit Make target names from module text."""
    targets: set[str] = set()
    for line in text.splitlines():
        if line.startswith(("\t", "#", ".")) or ":" not in line:
            continue
        target_text = line.split(":", maxsplit=1)[0]
        if "$" in target_text or "=" in target_text:
            continue
        targets.update(target_text.split())
    return targets


def _make_list(text: str, variable: str) -> list[str]:
    """Return ordered words assigned to a continued Make variable list."""
    lines = text.splitlines()
    prefix = f"{variable} :="
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue

        parts = [line.split(":=", maxsplit=1)[1].strip()]
        while parts[-1].endswith("\\"):
            index += 1
            parts.append(lines[index].strip())
        return " ".join(parts).replace("\\", "").split()

    raise AssertionError(f"Make variable list not found: {variable}")


def test_reflow_runtime_registry_is_complete_and_unique() -> None:
    """Every supported Reflow target should be registered exactly once."""
    runtime = _read("remote/command/runtime.mk")
    registered = _make_list(runtime, "REMOTE_REFLOW_RUNTIME_COMMANDS_LIST")
    expected = {
        "r-reflow-init",
        "r-reflow-init-dryrun",
        "r-reflow-init-all",
        "r-reflow-init-config",
        "r-reflow-init-force",
        "r-reflow-init-ask",
        "r-reflow-releases-recover",
        "r-reflow-releases-recover-dryrun",
        "r-reflow-tags-replay",
        "r-reflow-tags-replay-dryrun",
        "r-reflow-tags-convert",
        "r-reflow-tags-convert-dryrun",
        "r-reflow-dockerize",
        "r-reflow-dockerize-dryrun",
    }

    assert set(registered) == expected
    assert len(registered) == len(set(registered))
    assert expected.issubset(_target_names(runtime))


def test_reflow_targets_use_current_commands_and_safe_dry_runs() -> None:
    """Canonical commands and dry runs should preserve caller arguments."""
    runtime = _read("remote/command/runtime.mk")

    assert "releases recover" in runtime
    assert "tags convert" in runtime
    assert "\n\t\tdockerize" in runtime
    assert "\n\t\ttags replay" not in runtime
    assert "is deprecated - use r-reflow-releases-recover" in runtime
    assert 'REMOTE_REFLOW_GLOBAL_ARGS="--dry-run"' not in runtime

    for target in (
        "r-reflow-init-dryrun",
        "r-reflow-releases-recover-dryrun",
        "r-reflow-tags-convert-dryrun",
        "r-reflow-dockerize-dryrun",
    ):
        assert f"{target}: override REMOTE_REFLOW_GLOBAL_ARGS += --dry-run" in runtime


def test_reflow_arguments_and_docker_socket_are_configurable() -> None:
    """The remote wrapper should expose current options and Docker access."""
    variables = _read("variables/variable.mk")
    runtime = _read("remote/command/runtime.mk")

    for variable in (
        "REMOTE_REFLOW_GLOBAL_ARGS",
        "REMOTE_REFLOW_EXTRA_ARGS",
        "REMOTE_REFLOW_INIT_ARGS",
        "REMOTE_REFLOW_RELEASES_RECOVER_ARGS",
        "REMOTE_REFLOW_TAGS_CONVERT_ARGS",
        "REMOTE_REFLOW_DOCKERIZE_ARGS",
    ):
        assert f"{variable} ?=" in variables

    assert "DOCKER_SOCKET ?=" in variables
    assert "DOCKER_SOCKET_MOUNT :=" in variables
    dockerize = runtime.split("r-reflow-dockerize:", maxsplit=1)[1].split(
        ".PHONY: r-reflow-dockerize-dryrun", maxsplit=1
    )[0]
    assert "$(DOCKER_SOCKET_MOUNT)" in dockerize


def test_custy_init_targets_do_not_use_reflow_arguments() -> None:
    """Custy initialization aliases should remain isolated from Reflow."""
    runtime = _read("remote/command/runtime.mk")
    custy_section = runtime.split("# 🌐 Remote Runtime Commands - Custy", maxsplit=1)[
        1
    ].split("# 🌐 Remote Runtime Commands - Reflow", maxsplit=1)[0]

    assert "REMOTE_CUSTY_INIT_ARGS" in custy_section
    assert "REMOTE_REFLOW_INIT_ARGS" not in custy_section


def test_reflow_help_and_documentation_match_runtime_targets() -> None:
    """Help and developer documentation should describe current behavior."""
    runtime = _read("remote/command/runtime.mk")
    remote_help = _read("remote/help.mk")
    variables_help = _read("variables/help.mk")
    guide = (PROJECT_ROOT / "docs" / "guides" / "make_workflows.md").read_text(
        encoding="utf-8"
    )

    registered = _make_list(runtime, "REMOTE_REFLOW_RUNTIME_COMMANDS_LIST")
    for target in registered:
        assert f"make {target}" in remote_help

    assert "Deprecated release-recovery alias" in remote_help
    assert "REMOTE_REFLOW_RELEASES_RECOVER_ARGS" in variables_help
    assert "reflow releases recover" in guide
    assert "make --help" in guide
