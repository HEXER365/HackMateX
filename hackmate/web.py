import click
from rich.console import Console
from .config import get_workspace_path, CONFIG
from .utils import run_external_tool

console = Console()

@click.group()
def web():
    """Web Application Testing commands."""
    pass

@web.command()
@click.option("-u", "--url", required=True, help="Target URL (e.g., https://example.com).")
@click.option("--wordlist", default="/usr/share/wordlists/dirb/common.txt", help="Path to the wordlist for fuzzing.")
@click.option("--dirs", is_flag=True, help="Perform directory brute forcing with ffuf.")
@click.option("--cms", is_flag=True, help="Perform CMS and technology fingerprinting.")
@click.option("--confirm-scope", is_flag=True, help="Explicitly confirm scope for the target.")
@click.option("--execute", is_flag=True, help="Explicitly confirm execution of intrusive steps.")
def test(url, wordlist, dirs, cms, confirm_scope, execute):
    """
    Performs web application testing including directory brute forcing and CMS checks.
    """
    console.print(f"[bold]Starting web application testing for {url}...[/bold]")
    # Use the base domain/IP for the workspace name
    target = url.split("//")[-1].split("/")[0]
    workspace = get_workspace_path(target)

    if dirs:
        console.print("[bold yellow]Running directory brute forcing (ffuf)...[/bold yellow]")
        tool_path = CONFIG["tools"]["ffuf"]
        output_file = "ffuf_dirs_raw.txt"
        
        args = [
            "-u", f"{url}/FUZZ",
            "-w", wordlist,
            "-o", str(workspace / output_file),
            "-of", "json", # Output as JSON for easier parsing later
            "-t", str(CONFIG["concurrency"]),
            "-recursion",
            "-recursion-depth", "1",
            "-v", # Verbose output to see progress
        ]
        
        run_external_tool(
            tool_path=tool_path,
            args=args,
            target=target,
            workspace_path=workspace,
            output_filename=None, # ffuf writes to file via -o
            check_scope=confirm_scope,
            is_intrusive=True,
            confirm_execute=execute,
        )
        console.print(f"[bold green]Directory brute forcing complete.[/bold green] Results saved to {workspace / output_file}")

    if cms:
        console.print("[bold yellow]Running CMS and technology fingerprinting (whatweb/wpscan)...[/bold yellow]")
        # Note: whatweb is often pre-installed on Kali. We'll use it as a placeholder.
        # A full implementation would integrate multiple tools like wpscan, droopescan, etc.
        tool_path = "whatweb"
        output_file = "whatweb_raw.txt"
        
        args = [
            url,
            "-v",
            "-a", "3", # Aggressive scan
        ]
        
        run_external_tool(
            tool_path=tool_path,
            args=args,
            target=target,
            workspace_path=workspace,
            output_filename=output_file,
            check_scope=confirm_scope,
            is_intrusive=False, # Considered less intrusive than fuzzing
            confirm_execute=execute,
        )
        console.print(f"[bold green]CMS fingerprinting complete.[/bold green] Results saved to {workspace / output_file}")

if __name__ == '__main__':
    web()
