import click
from rich.console import Console
from .config import get_workspace_path, CONFIG
from .utils import run_external_tool, save_json_artifact

console = Console()

@click.group()
def recon():
    """Reconnaissance and Discovery commands."""
    pass

@recon.command()
@click.argument("target")
def subdomains(target):
    """
    Performs passive subdomain enumeration using subfinder.
    Results are saved to the target's workspace.
    """
    console.print(f"[bold]Starting passive subdomain enumeration for {target}...[/bold]")
    workspace = get_workspace_path(target)
    
    tool_path = CONFIG["tools"]["subfinder"]
    output_file = "subdomains_raw.txt"
    
    args = [
        "-d", target,
        "-o", str(workspace / output_file),
        "-silent"
    ]
    
    run_external_tool(
        tool_path=tool_path,
        args=args,
        target=target,
        workspace_path=workspace,
        output_filename=output_file,
        check_scope=True,
    )
    
    console.print(f"[bold green]Subdomain enumeration complete.[/bold green] Results saved to {workspace / output_file}")

@recon.command()
@click.argument("target")
def probe(target):
    """
    Probes collected subdomains for live HTTP/S services using httpx.
    Requires subdomains_raw.txt to exist in the workspace.
    """
    console.print(f"[bold]Starting live host probing for {target}...[/bold]")
    workspace = get_workspace_path(target)
    
    input_file = workspace / "subdomains_raw.txt"
    if not input_file.exists():
        console.print(f"[bold red]Error:[/bold red] Input file {input_file} not found. Run 'hackmate recon subdomains {target}' first.")
        return

    tool_path = CONFIG["tools"]["httpx"]
    output_file = "live_hosts_raw.txt"
    
    args = [
        "-l", str(input_file),
        "-o", str(workspace / output_file),
        "-silent",
        "-status-code",
        "-title",
        "-tech-detect",
        "-threads", str(CONFIG["concurrency"])
    ]
    
    run_external_tool(
        tool_path=tool_path,
        args=args,
        target=target,
        workspace_path=workspace,
        output_filename=output_file,
    )
    
    console.print(f"[bold green]Live host probing complete.[/bold green] Results saved to {workspace / output_file}")

if __name__ == '__main__':
    recon()
