import click
import yaml
from rich.console import Console
from pathlib import Path
from typing import Dict, Any, List
from .config import get_workspace_path, CONFIG
from .utils import console

console = Console()

# --- Plugin System (Placeholder) ---

def load_plugins() -> Dict[str, Any]:
    """Loads all plugins from the hackmate/plugins directory."""
    plugins = {}
    # In a real implementation, this would dynamically load Python modules
    # For now, we'll use a simple placeholder
    console.print("[dim]Plugin system loaded (placeholder).[/dim]")
    return plugins

# --- Flow Engine ---

def run_flow_step(step: Dict[str, Any], target: str, confirm_execute: bool):
    """Executes a single step in the flow."""
    step_name = list(step.keys())[0]
    step_args = step[step_name]
    
    console.print(f"\n[bold magenta]>>> Executing Flow Step: {step_name}[/bold magenta]")
    
    # Simple mapping to existing CLI commands (needs to be robust)
    if step_name == "recon_subdomains":
        from .recon import subdomains
        ctx = click.Context(subdomains, info_name='recon subdomains')
        ctx.invoke(subdomains, target=target)
    elif step_name == "recon_probe":
        from .recon import probe
        ctx = click.Context(probe, info_name='recon probe')
        ctx.invoke(probe, target=target)
    elif step_name == "scan_nmap":
        from .scan import nmap
        ctx = click.Context(nmap, info_name='scan nmap')
        # Example of passing args from flow to command
        ports = step_args.get("ports", "80,443")
        fast = step_args.get("fast", False)
        full = step_args.get("full", False)
        ctx.invoke(nmap, target=target, ports=ports, fast=fast, full=full, confirm_scope=True, execute=confirm_execute)
    else:
        console.print(f"[bold red]Error:[/bold red] Unknown flow step: {step_name}")

@click.group()
def flow():
    """Manage and run automated workflows."""
    pass

@flow.command()
@click.argument("flow_file", type=click.Path(exists=True))
@click.argument("target")
@click.option("--confirm-scope", is_flag=True, help="Explicitly confirm scope for the target.")
@click.option("--execute", is_flag=True, help="Explicitly confirm execution of intrusive steps.")
def run(flow_file, target, confirm_scope, execute):
    """Runs a defined YAML flow against a target."""
    flow_path = Path(flow_file)
    console.print(f"[bold]Starting flow from {flow_path.name} for {target}...[/bold]")
    
    if not confirm_scope:
        console.print("[bold red]Safety Error:[/bold red] Flows require the [bold]--confirm-scope[/bold] flag to run.")
        return

    try:
        with open(flow_path, "r") as f:
            flow_data = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[bold red]Error loading flow file:[/bold red] {e}")
        return

    if "steps" not in flow_data or not isinstance(flow_data["steps"], list):
        console.print("[bold red]Error:[/bold red] Flow file must contain a 'steps' list.")
        return

    for step in flow_data["steps"]:
        run_flow_step(step, target, execute)

    console.print(f"\n[bold green]Flow '{flow_data.get('name', 'Unnamed Flow')}' completed for {target}.[/bold green]")

# --- AI Integration (Placeholder) ---

def ai_suggest_next_steps(target: str):
    """
    Uses AI to suggest the next steps based on current workspace artifacts.
    """
    if not CONFIG["ai"]["enabled"]:
        console.print("[bold yellow]AI is disabled.[/bold yellow] Enable it in ~/.hackmate/config.yaml to use this feature.")
        return

    # Placeholder for OpenAI API call
    console.print(f"[bold cyan]AI Assistant:[/bold cyan] Analyzing workspace for {target}...")
    
    # In a real implementation, you would:
    # 1. Read key artifacts (subdomains_raw.txt, live_hosts_raw.txt, nmap_scan.xml)
    # 2. Construct a prompt summarizing the findings.
    # 3. Call the OpenAI API with the prompt.
    # 4. Print the AI's suggestion.
    
    console.print("[dim]Placeholder: AI suggests running 'hackmate web test -u https://example.com --dirs' based on live hosts found.[/dim]")

@flow.command()
@click.argument("target")
def suggest(target):
    """Uses AI to suggest the next steps based on current findings."""
    ai_suggest_next_steps(target)

if __name__ == '__main__':
    flow()
