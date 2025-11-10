# HackMate: The Kali CLI Assistant

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/yourusername/hackmate/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/hackmate.svg?style=social)](https://github.com/yourusername/hackmate/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/hackmate.svg?style=social)](https://github.com/yourusername/hackmate/network)

**HackMate** is a modular, extensible command-line assistant for Kali Linux designed to streamline and automate common tasks for penetration testers, red-teamers, and bug-bounty hunters. It acts as a unified wrapper around industry-standard tools, enforcing a structured workflow, prioritizing safety, and organizing results into auditable, per-target workspaces.

## ✨ Features

*   **Unified CLI:** Single interface for tools like `subfinder`, `httpx`, `nmap`, `masscan`, `ffuf`, and `searchsploit`.
*   **Automated Flows:** Define and run complex sequences of commands using simple YAML files.
*   **Safety-by-Default:** Mandatory `--confirm-scope` and `--execute` flags for intrusive operations.
*   **Workspace Management:** Automatic creation of per-target directories for organized results.
*   **Structured Reporting:** Built-in system for adding findings and generating Markdown/PDF reports.
*   **Extensible Architecture:** Designed with placeholders for AI assistance and a custom plugin system.

## 🚀 Installation (Kali Linux / Debian)

The simplest way to install HackMate and its dependencies is by using the provided `install.sh` script.

### Prerequisites

*   Kali Linux (Recommended) or any Debian-based system.
*   Python 3.10+
*   `go` (required for installing `subfinder` and `httpx` via the script).

### Step-by-Step Guide

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/hackmate.git
    cd hackmate
    ```

2.  **Run the Auto-Installer:**
    The installer requires root privileges to install system packages and create the global executable link.
    ```bash
    sudo bash install.sh
    ```

The script will install Python dependencies, check for/install external tools, and create the global `hackmate` command.

## ⚙️ Configuration

HackMate uses a YAML configuration file located at `~/.hackmate/config.yaml`.

To view the current configuration and workspace root:
```bash
hackmate config
```

You can edit this file to customize tool paths, concurrency limits, and enable the AI features.

## ⚠️ Safety and Ethical Use

**HackMate is a professional tool intended for authorized security testing only.** Unauthorized use is illegal and unethical.

The tool enforces the following mandatory safety controls:

| Control | Flag | Description |
| :--- | :--- | :--- |
| **Scope Confirmation** | `--confirm-scope` | **MUST** be used to confirm written authorization for the target. Required for all flows and reconnaissance. |
| **Execution Gating** | `--execute` | **MUST** be used to authorize intrusive or destructive steps (e.g., mass scanning, fuzzing). |

## 📖 Usage Examples

### 1. Reconnaissance & Probing

Perform passive subdomain enumeration and check for live hosts.

```bash
# 1. Find subdomains (requires scope confirmation)
hackmate recon subdomains example.com --confirm-scope

# 2. Probe live hosts (uses results from step 1)
hackmate recon probe example.com
```

### 2. Automated Flow Execution

Run a predefined sequence of commands (e.g., recon -> probe -> nmap).

```bash
# View the example flow file
cat hackmate/flows/quick-recon.yaml

# Run the flow (requires both safety flags)
hackmate flow run hackmate/flows/quick-recon.yaml example.com --confirm-scope --execute
```

### 3. Notes and Reporting

Record a finding and generate a report from the collected data.

```bash
# 1. Add a structured finding
hackmate notes add example.com -t "Reflected XSS" -b "Found on /search?q=PAYLOAD"

# 2. List all findings for the target
hackmate notes list example.com

# 3. Generate the final report (Markdown and PDF)
hackmate report generate example.com --pdf
```

### 4. Exploitation Utility

Quickly generate a reverse shell payload.

```bash
hackmate exploit shell --reverse --lhost 10.0.0.1 --lport 4444
```

## 🛠️ Development and Extensibility

HackMate is designed to be easily extended.

### Plugin System

You can add new commands or tool wrappers by placing Python modules in the `hackmate/hackmate/plugins/` directory.

### AI Assistance

The `hackmate flow suggest <target>` command is a placeholder for an AI module that can analyze workspace artifacts and recommend the next logical steps. Enable this feature by configuring your API key in `~/.hackmate/config.yaml`.

## 🤝 Contributing

We welcome contributions! If you have suggestions for new features, bug fixes, or improvements to the documentation, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
