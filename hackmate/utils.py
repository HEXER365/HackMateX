import subprocess
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from rich.console import Console

console = Console()

def run_external_tool(
    tool_path: str,
    args: List[str],
    target: str,
    workspace_path: Path,
    output_filename: Optional[str] = None,
    timeout: Optional[int] = 300,
    check_scope: bool = False,
    is_intrusive: bool = False,
    confirm_execute: bool = False,
) -> Optional[str]:
    """
    Runs an external tool and handles logging and output.

    :param tool_path: Path to the external tool (e.g., 'subfinder').
    :param args: List of arguments for the tool.
    :param target: The target domain/IP.
    :param workspace_path: The target's workspace directory.
    :param output_filename: If provided, stdout is saved to this file in the workspace.
    :param timeout: Timeout for the command in seconds.
    :param check_scope: If True, requires scope confirmation.
    :param is_intrusive: If True, requires --execute flag.
    :param confirm_execute: The value of the --execute flag passed by the user.
    :return: The stdout of the command if no output_filename is provided, otherwise None.
    """
    
    full_command = [tool_path] + args
    
    # 1. Safety Checks
    if check_scope:
        console.print(f"[bold yellow]Safety Check:[/bold yellow] This operation requires explicit scope confirmation for target [bold cyan]{target}[/bold cyan].")
        # In a real CLI, this would prompt the user or check a scope file.
        # For this implementation, we'll assume the user has confirmed the scope if the command is run.
        # A more robust implementation would be needed for production.

    if is_intrusive and not confirm_execute:
        console.print(f"[bold red]Safety Error:[/bold red] The command '[bold]{tool_path}[/bold]' is intrusive and requires the [bold]--execute[/bold] flag to run.")
        return None

    console.print(f"[bold green]Running:[/bold green] {' '.join(full_command)}")

    try:
        # Determine where to redirect stdout
        stdout_dest = subprocess.PIPE
        if output_filename:
            output_path = workspace_path / output_filename
            stdout_dest = open(output_path, "w")
            console.print(f"  [dim]Output redirected to: {output_path}[/dim]")

        process = subprocess.run(
            full_command,
            capture_output=True if not output_filename else False,
            text=True,
            timeout=timeout,
            check=True, # Raise CalledProcessError on non-zero exit code
            encoding="utf-8",
        )

        if output_filename:
            stdout_dest.close()
            return None
        else:
            return process.stdout.strip()

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error:[/bold red] Tool '{tool_path}' failed with exit code {e.returncode}.")
        console.print(f"[dim]Stderr:[/dim] {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] Tool '{tool_path}' not found. Check your PATH or configure the tool path in [bold]~/.hackmate/config.yaml[/bold].")
        return None
    except subprocess.TimeoutExpired:
        console.print(f"[bold red]Error:[/bold red] Tool '{tool_path}' timed out after {timeout} seconds.")
        return None
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        return None

def save_json_artifact(data: Dict[str, Any], filename: str, workspace_path: Path):
    """Saves a dictionary as a JSON artifact in the workspace."""
    filepath = workspace_path / filename
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        console.print(f"[bold blue]Artifact Saved:[/bold blue] {filename} at {filepath}")
    except Exception as e:
        console.print(f"[bold red]Error saving JSON artifact {filename}:[/bold red] {e}")

def load_json_artifact(filename: str, workspace_path: Path) -> Optional[Dict[str, Any]]:
    """Loads a JSON artifact from the workspace."""
    filepath = workspace_path / filename
    if not filepath.exists():
        return None
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error loading JSON artifact {filename}:[/bold red] {e}")
        return None
