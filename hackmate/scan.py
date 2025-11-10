import click
from rich.console import Console
from .config import get_workspace_path, CONFIG
from .utils import run_external_tool

console = Console()

@click.group()
def scan():
    """Scanning and Enumeration commands."""
    pass

@scan.command()
@click.argument("target")
@click.option("--ports", default="1-65535", help="Port range for masscan (e.g., 1-1000, 80,443).")
@click.option("--rate", type=int, default=CONFIG["safe_defaults"]["masscan_rate"], help="Packet rate for masscan.")
@click.option("--confirm-scope", is_flag=True, help="Explicitly confirm scope for the target.")
@click.option("--execute", is_flag=True, help="Explicitly confirm execution of intrusive steps.")
def masscan(target, ports, rate, confirm_scope, execute):
    """
    Performs a fast masscan and saves the results.
    This is considered an intrusive step and requires --execute.
    """
    console.print(f"[bold]Starting masscan for {target} on ports {ports}...[/bold]")
    workspace = get_workspace_path(target)
    
    tool_path = CONFIG["tools"]["masscan"]
    output_file = "masscan_raw.txt"
    
    args = [
        target,
        "-p", ports,
        "--rate", str(rate),
        "-oG", str(workspace / output_file), # Greppable output for simplicity
    ]
    
    run_external_tool(
        tool_path=tool_path,
        args=args,
        target=target,
        workspace_path=workspace,
        output_filename=None, # masscan writes directly to file via -oG
        check_scope=confirm_scope,
        is_intrusive=True,
        confirm_execute=execute,
    )
    
    console.print(f"[bold green]Masscan complete.[/bold green] Results saved to {workspace / output_file}")

@scan.command()
@click.argument("target")
@click.option("--ports", default="80,443,21,22,23,25,110,139,445,3389", help="Comma-separated list of ports for Nmap.")
@click.option("--fast", is_flag=True, help="Use a faster Nmap profile (-T4 -F).")
@click.option("--full", is_flag=True, help="Use a full Nmap profile (-sC -sV -O -A).")
@click.option("--confirm-scope", is_flag=True, help="Explicitly confirm scope for the target.")
@click.option("--execute", is_flag=True, help="Explicitly confirm execution of intrusive steps.")
def nmap(target, ports, fast, full, confirm_scope, execute):
    """
    Performs a targeted Nmap scan.
    This is considered an intrusive step and requires --execute.
    """
    console.print(f"[bold]Starting Nmap scan for {target} on ports {ports}...[/bold]")
    workspace = get_workspace_path(target)
    
    tool_path = CONFIG["tools"]["nmap"]
    output_file_base = "nmap_scan"
    
    args = [
        "-p", ports,
        "-oA", str(workspace / output_file_base), # Output in all formats (XML, Nmap, Grepable)
        target,
    ]
    
    # Timing profile
    if fast:
        args.extend(["-T4"]) # Removed -F to allow -p
    elif full:
        args.extend(["-sC", "-sV", "-O", "-A", "-T3"]) # Use T3 for safety
    else:
        args.append(f"-T{CONFIG['safe_defaults']['nmap_timing'][-1]}") # e.g., -T3
        args.extend(["-sC", "-sV"]) # Default to script and version scan

    run_external_tool(
        tool_path=tool_path,
        args=args,
        target=target,
        workspace_path=workspace,
        output_filename=None, # Nmap writes directly to file via -oA
        check_scope=confirm_scope,
        is_intrusive=True,
        confirm_execute=execute,
    )
    
    console.print(f"[bold green]Nmap scan complete.[/bold green] Results saved to {workspace / output_file_base}.*")

if __name__ == '__main__':
    scan()
