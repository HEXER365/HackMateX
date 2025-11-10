import click
from rich.console import Console
from .recon import recon
from .scan import scan
from .web import web
from .exploit import exploit
from .osint import osint
from .notes_report import notes, report
from .flow_plugin import flow
from .config import CONFIG, HACKMATE_CONFIG_FILE

console = Console()

@click.group()
@click.version_option("0.1.0", prog_name="HackMate")
def cli():
    """
    HackMate: A modular, extensible command-line assistant for Kali Linux.
    """
    pass

# Add command groups
cli.add_command(recon)
cli.add_command(scan)
cli.add_command(web)
cli.add_command(exploit)
cli.add_command(osint)
cli.add_command(notes)
cli.add_command(report)
cli.add_command(flow)

@cli.command()
def config():
    """Shows the current configuration file path."""
    console.print(f"[bold cyan]HackMate Configuration File:[/bold cyan] {HACKMATE_CONFIG_FILE}")
    console.print(f"[bold cyan]Workspace Root:[/bold cyan] {CONFIG['workspace_dir']}")
    console.print("\n[dim]Edit this file to change tool paths, safe defaults, and AI settings.[/dim]")

@cli.command()
def tools():
    """Lists the external tools configured for HackMate."""
    console.print("[bold cyan]Configured External Tools:[/bold cyan]")
    for tool, path in CONFIG["tools"].items():
        console.print(f"  [bold]{tool}:[/bold] {path}")
    console.print("\n[dim]Ensure these tools are installed and accessible in your PATH, or update the paths in the config file.[/dim]")

def main():
    cli()

if __name__ == '__main__':
    main()
