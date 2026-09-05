# scripts/docs/render_mermaid.py

"""
scripts/docs/render_mermaid.py

Purpose:
- Render Mermaid diagram files (`.mmd` by default) into image/document outputs
  (e.g. png, svg, pdf) using Mermaid CLI (`mmdc`).

Why this script:
- Reusable across projects with flexible input and output paths.
- Keeps folder structure from input directory into output directory.
- Supports optional render settings and clean output mode.

Requirements:
- Mermaid CLI installed and available in PATH, or pass an explicit executable path:
    npm install -g @mermaid-js/mermaid-cli
  Then use:
    mmdc --version

Usage examples:
1) Basic (default docs/diagrams -> docs/diagrams/generated, png):
    python scripts/docs/render_mermaid.py

2) Custom source and destination:
    python scripts/docs/render_mermaid.py ^
      --input-dir docs/diagrams ^
      --output-dir docs/diagrams/out

3) SVG output with recursive search:
    python scripts/docs/render_mermaid.py --recursive --format svg

4) Use explicit Mermaid CLI executable:
    python scripts/docs/render_mermaid.py --mmdc "C:/tools/mmdc.cmd"

5) With render options:
    python scripts/docs/render_mermaid.py ^
      --theme neutral ^
      --background transparent ^
      --width 1920 --height 1080 --scale 2

6) Custom
python scripts/docs/render_mermaid.py --format png --width 2400 --height 1800 --scale 2 --background white

Exit codes:
- 0: all files rendered successfully.
- 1: one or more files failed, or setup/validation error.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

SUPPORTED_FORMATS = ("png", "svg", "pdf")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Mermaid (.mmd) files to image/document formats using Mermaid CLI (mmdc)."
    )
    parser.add_argument(
        "--input-dir",
        default="docs/docs_v2/diagrams",
        help="Directory containing Mermaid files (default: docs/diagrams).",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/docs_v2/diagrams/generated",
        help="Directory to write rendered files (default: docs/diagrams/generated).",
    )
    parser.add_argument(
        "--input-glob",
        default="*.mmd",
        help="Glob pattern for Mermaid files (default: *.mmd).",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search input directory recursively.",
    )
    parser.add_argument(
        "--format",
        default="png",
        choices=SUPPORTED_FORMATS,
        help="Output format (default: png).",
    )
    parser.add_argument(
        "--mmdc",
        default="mmdc",
        help="Mermaid CLI executable path or command name (default: mmdc).",
    )
    parser.add_argument(
        "--theme",
        default=None,
        help="Optional Mermaid theme (default, dark, forest, neutral).",
    )
    parser.add_argument(
        "--background",
        default=None,
        help="Optional background color (e.g. transparent, white, #ffffff).",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Optional output width.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="Optional output height.",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=None,
        help="Optional output scale factor.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete output directory before rendering.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable Rich progress bar (useful for CI or plain logs).",
    )
    return parser.parse_args()


def discover_files(input_dir: Path, input_glob: str, recursive: bool) -> list[Path]:
    if recursive:
        return sorted(input_dir.rglob(input_glob))
    return sorted(input_dir.glob(input_glob))


def build_output_path(
    src_file: Path, input_dir: Path, output_dir: Path, fmt: str
) -> Path:
    relative = src_file.relative_to(input_dir)
    return output_dir / relative.with_suffix(f".{fmt}")


def resolve_mmdc_executable(mmdc: str) -> str:
    # Explicit path or file-like value: use as-is.
    if any(sep in mmdc for sep in ("/", "\\")) or "." in Path(mmdc).name:
        return mmdc
    found = shutil.which(mmdc)
    if found:
        return found
    if sys.platform.startswith("win"):
        found_cmd = shutil.which(f"{mmdc}.cmd")
        if found_cmd:
            return found_cmd
    return mmdc


def build_mmdc_command(
    mmdc: str,
    input_file: Path,
    output_file: Path,
    *,
    theme: str | None = None,
    background: str | None = None,
    width: int | None = None,
    height: int | None = None,
    scale: float | None = None,
) -> list[str]:
    resolved_mmdc = resolve_mmdc_executable(mmdc)
    cmd: list[str] = [resolved_mmdc, "-i", str(input_file), "-o", str(output_file)]

    if theme:
        cmd.extend(["-t", theme])
    if background:
        cmd.extend(["-b", background])
    if width is not None:
        cmd.extend(["-w", str(width)])
    if height is not None:
        cmd.extend(["-H", str(height)])
    if scale is not None:
        cmd.extend(["-s", str(scale)])

    return cmd


def run_command(cmd: Sequence[str]) -> tuple[int, str]:
    try:
        process = subprocess.run(
            list(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        return process.returncode, process.stdout.strip()
    except FileNotFoundError as exc:
        return 1, f"Executable not found: {cmd[0]} ({exc})"


def ensure_mmdc_available(mmdc: str) -> bool:
    # If mmdc looks like an explicit path or file, validate existence.
    if any(sep in mmdc for sep in ("/", "\\")) or "." in Path(mmdc).name:
        return Path(mmdc).exists()
    # On Windows, npm-installed Mermaid CLI usually resolves as mmdc.cmd.
    if shutil.which(mmdc):
        return True
    if sys.platform.startswith("win") and shutil.which(f"{mmdc}.cmd"):
        return True
    return False


def format_paths(paths: Iterable[Path]) -> str:
    return ", ".join(str(p).replace("\\", "/") for p in paths)


def main() -> int:
    args = parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists() or not input_dir.is_dir():
        print(
            f"ERROR: input directory does not exist or is not a directory: {input_dir}"
        )
        return 1

    if not ensure_mmdc_available(args.mmdc):
        print(
            "ERROR: Mermaid CLI not found. Install it with:\n"
            "  npm install -g @mermaid-js/mermaid-cli\n"
            "or pass explicit executable path via --mmdc."
        )
        return 1

    files = discover_files(input_dir, args.input_glob, args.recursive)
    if not files:
        print(
            f"NO_FILES_FOUND: input_dir={input_dir} pattern={args.input_glob} recursive={args.recursive}"
        )
        return 0

    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"INPUT_DIR={input_dir}")
    print(f"OUTPUT_DIR={output_dir}")
    print(f"FORMAT={args.format}")
    print(f"FILES_FOUND={len(files)}")

    failed: list[Path] = []
    succeeded: list[Path] = []

    def render_one(src: Path) -> None:
        out_file = build_output_path(src, input_dir, output_dir, args.format)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        cmd = build_mmdc_command(
            args.mmdc,
            src,
            out_file,
            theme=args.theme,
            background=args.background,
            width=args.width,
            height=args.height,
            scale=args.scale,
        )

        code, output = run_command(cmd)
        rel_src = src.relative_to(input_dir)

        if code == 0:
            succeeded.append(src)
            print(f"OK: {rel_src} -> {out_file.relative_to(output_dir)}")
        else:
            failed.append(src)
            print(f"FAILED: {rel_src}")
            if output:
                print(output)

    if args.no_progress:
        for src in files:
            render_one(src)
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Rendering[/bold blue]"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            TextColumn("• {task.fields[current_file]}"),
        ) as progress:
            task_id = progress.add_task(
                "render",
                total=len(files),
                current_file="-",
            )
            for src in files:
                progress.update(task_id, current_file=str(src.relative_to(input_dir)))
                render_one(src)
                progress.advance(task_id, 1)

    print("----- SUMMARY -----")
    print(f"TOTAL={len(files)}")
    print(f"SUCCESS={len(succeeded)}")
    print(f"FAILED={len(failed)}")

    if failed:
        print("FAILED_FILES=" + format_paths(f.relative_to(input_dir) for f in failed))
        return 1

    print("ALL_RENDERED_SUCCESSFULLY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
