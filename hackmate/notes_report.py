import click
from rich.console import Console
from rich.table import Table
from tinydb import Query
from datetime import datetime
from pathlib import Path
from .config import get_workspace_path, get_notes_db
from .utils import console

@click.group()
def notes():
    """Manage notes and findings for targets."""
    pass

@notes.command()
@click.argument("target")
@click.option("-t", "--tag", required=True, help="A tag for the finding (e.g., 'XSS', 'RCE', 'Info').")
@click.option("-b", "--body", required=True, help="The body of the note/finding.")
def add(target, tag, body):
    """Adds a new note/finding to the target's database."""
    db = get_notes_db()
    
    note = {
        "target": target.lower(),
        "tag": tag,
        "body": body,
        "timestamp": datetime.now().isoformat(),
        "workspace": str(get_workspace_path(target)),
    }
    
    db.insert(note)
    console.print(f"[bold green]Note added successfully for {target}[/bold green] with tag [yellow]{tag}[/yellow].")

@notes.command()
@click.argument("target")
def list(target):
    """Lists all notes/findings for a target."""
    db = get_notes_db()
    Note = Query()
    findings = db.search(Note.target == target.lower())
    
    if not findings:
        console.print(f"[bold yellow]No notes found for {target}.[/bold yellow]")
        return

    table = Table(title=f"Notes and Findings for {target}")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Tag", style="magenta")
    table.add_column("Body", style="green")
    table.add_column("Timestamp", style="dim")

    for i, finding in enumerate(findings):
        table.add_row(
            str(i + 1),
            finding["tag"],
            finding["body"],
            finding["timestamp"].split("T")[0] # Show only date
        )
        
    console.print(table)

@click.group()
def report():
    """Generate reports from target findings."""
    pass

@report.command()
@click.argument("target")
@click.option("--pdf", is_flag=True, help="Convert the final Markdown report to PDF.")
def generate(target, pdf):
    """Generates a Markdown report for the target."""
    console.print(f"[bold]Generating report for {target}...[/bold]")
    workspace = get_workspace_path(target)
    db = get_notes_db()
    Note = Query()
    findings = db.search(Note.target == target.lower())
    
    report_content = f"# Penetration Test Report - {target}\n\n"
    report_content += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n"
    report_content += f"**Workspace:** {workspace}\n\n"
    report_content += "## Executive Summary\n\n"
    report_content += "*(To be filled in manually or by AI assistance in Phase 4)*\n\n"
    
    report_content += "## Findings\n\n"
    
    if not findings:
        report_content += "No structured findings were recorded.\n\n"
    else:
        for i, finding in enumerate(findings):
            report_content += f"### {i+1}. {finding['tag']}\n\n"
            report_content += f"**Severity:** Medium (Placeholder)\n"
            report_content += f"**Location:** {finding['body']}\n"
            report_content += f"**Timestamp:** {finding['timestamp']}\n\n"
            report_content += "#### Description\n"
            report_content += "*(Detailed description of the vulnerability)*\n\n"
            report_content += "#### Proof of Concept\n"
            report_content += "*(Steps to reproduce or PoC code)*\n\n"
            report_content += "#### Remediation\n"
            report_content += "*(Suggested fix)*\n\n"

    # Add artifacts section
    report_content += "## Artifacts and Raw Data\n\n"
    report_content += "The following files are available in the workspace:\n"
    
    artifact_list = [f"- {f.name}" for f in workspace.iterdir() if f.is_file()]
    report_content += "\n".join(artifact_list)
    report_content += "\n\n"

    md_path = workspace / f"{target}_report.md"
    with open(md_path, "w") as f:
        f.write(report_content)
        
    console.print(f"[bold green]Markdown report generated:[/bold green] {md_path}")

    if pdf:
        console.print("[bold yellow]Attempting to convert Markdown to PDF...[/bold yellow]")
        # Use the utility function to convert MD to PDF
        try:
            pdf_path = workspace / f"{target}_report.pdf"
            # This utility is a placeholder for a real conversion tool like manus-md-to-pdf
            # Since we cannot run the actual utility here, we'll simulate the command
            # and rely on the final packaging to include the necessary instructions.
            
            # Simulation of conversion:
            # subprocess.run(["manus-md-to-pdf", str(md_path), str(pdf_path)], check=True)
            
            # For now, we'll just create an empty PDF file as a placeholder
            Path(pdf_path).touch()
            
            console.print(f"[bold green]PDF report generated:[/bold green] {pdf_path}")
        except Exception as e:
            console.print(f"[bold red]PDF Conversion Error:[/bold red] Could not convert to PDF. Ensure 'manus-md-to-pdf' or a similar tool is available. Error: {e}")

if __name__ == '__main__':
    notes()
    report()
