# app/theme/theme.py

import os
from dataclasses import dataclass

from rich.theme import Theme as RichTheme


@dataclass
class Theme:
    # Core
    primary: str
    secondary: str

    # Semantic colors (🔥 important)
    info: str
    warning: str
    success: str
    error: str
    dry_run: str
    pointing: str

    # (for help UI)
    help_title: str
    help_text: str
    help_hint: str
    help_option: str
    help_example: str

    # Progress-specific
    progress_title: str
    progress_step: str
    progress_done: str

    center: int = 50

    def to_rich_theme(self) -> RichTheme:
        return RichTheme(
            {
                "primary": self.primary,  # --help, --version
                "secondary": self.secondary,
                # Typer help styling
                "option": self.primary,  # --help, --version
                "switch": self.primary,
                "metavar": self.primary,
                "help": self.secondary,
                "text": self.secondary,
                "command": self.primary,
                # 🔥 custom styles
                "info": self.info,
                "warning": self.warning,
                "success": self.success,
                "error": self.error,
                "dry_run": self.dry_run,
                "pointing": self.pointing,
                # (for help UI)
                "help.title": f"bold {self.help_title}",
                "help.text": self.help_text,
                "help.hint": f"dim {self.help_hint}",
                "help.option": f"bold {self.help_option}",
                "help.example": f"italic {self.help_example}",
                "progress.title": self.progress_title,
                "progress.step": self.progress_step,
                "progress.done": self.progress_done,
            }
        )


def load_theme() -> Theme:
    return Theme(
        primary=os.getenv("CUSTY_PRIMARY", "cyan"),
        secondary=os.getenv("CUSTY_SECONDARY", "#B0B0B0"),
        center=50,
        info=os.getenv("CUSTY_INFO", "cyan"),
        warning=os.getenv("CUSTY_WARNING", "yellow"),
        success=os.getenv("CUSTY_SUCCESS", "green"),
        error=os.getenv("CUSTY_ERROR", "red"),
        dry_run=os.getenv("CUSTY_DRY_RUN", "magenta"),
        pointing=os.getenv("CUSTY_POINTING", "yellow"),
        help_title=os.getenv("CUSTY_HELP_TITLE", "cyan"),
        help_text=os.getenv("CUSTY_HELP_TEXT", "#B0B0B0"),
        help_hint=os.getenv("CUSTY_HELP_HINT", "bright_black"),
        help_option=os.getenv("CUSTY_HELP_OPTION", "cyan"),
        help_example=os.getenv("CUSTY_HELP_EXAMPLE", "green"),
        progress_title=os.getenv("CUSTY_PROGRESS_TITLE", "cyan"),
        progress_step=os.getenv("CUSTY_PROGRESS_STEP", "yellow"),
        progress_done=os.getenv("CUSTY_PROGRESS_DONE", "green"),
    )


theme = load_theme()


def helpTitle(title: str):
    return f"bold {title}"


def helpText(text: str):
    return f"{text}"


def helpHint(hint: str):
    return f"dim {hint}"


def helpOption(option: str):
    return f"bold {option}"


def helpExample(example: str):
    return f"italic {example}"


class HelpTheme:
    theme: Theme = load_theme()
    title: str = theme.help_title
    title_cyan: str = helpTitle("cyan")
    title_yellow: str = helpTitle("yellow")
    title_green: str = helpTitle("green")
    title_red: str = helpTitle("red")
    text: str = theme.help_text
    hint: str = theme.help_hint
    option: str = theme.help_option
    example: str = theme.help_example
