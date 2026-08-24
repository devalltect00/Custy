# app/cli/commands/main/help.old.py

old_help="""
🚀 [bold cyan]Custy — Git Automation CLI[/bold cyan]

Automate your Git workflow with structured commits, versioning,
changelog generation, and release pipelines.

[dim]Designed for speed, consistency, and automation[/dim]

────────────────────────────────────────

📦 [bold]Core Capabilities:[/bold]

  • [green]Commit[/green] with structured messages
  • [green]Tag[/green] versions using SemVer / PEP 440
  • [green]Generate[/green] changelogs automatically
  • [green]Automate[/green] full release pipelines

────────────────────────────────────────

⚡ [bold]Common Commands:[/bold]

  [yellow]custy init[/yellow]
      Initialize project (config, templates, examples)

  [yellow]custy commit[/yellow]
      Create a structured commit

  [yellow]custy tag[/yellow]
      Create or bump version tag

  [yellow]custy push[/yellow]
      Push commits and tags to remote(s)

  [yellow]custy changelog[/yellow]
      Generate or manage changelog

────────────────────────────────────────

🔁 [bold]Pipeline Usage:[/bold]

  Run multiple steps in one command:

    [yellow]custy run commit tag push[/yellow]
    [yellow]custy run release[/yellow]

  [dim]Presets like "release" expand into full workflows[/dim]

────────────────────────────────────────

🧠 [bold]Getting Started:[/bold]

  1. [yellow]custy init[/yellow]
  2. [yellow]custy run commit tag[/yellow]

  [dim]Optional:[/dim]
    [yellow]custy run release[/yellow]

────────────────────────────────────────

🧰 [bold]Additional Tools:[/bold]

  [yellow]custy validate[/yellow]     Check project readiness
  [yellow]custy backup[/yellow]       Backup message templates
  [yellow]custy cleanup[/yellow]      Remove old backups & branches
  [yellow]custy version[/yellow]      Sync version across files

────────────────────────────────────────

❓ [bold]Need Help?[/bold]

  Use [cyan]--help[/cyan] on any command:

    [yellow]custy run --help[/yellow]
    [yellow]custy tag --help[/yellow]

────────────────────────────────────────
"""
