#!/bin/bash

# --- HackMate Auto-Installer for Kali Linux ---

# Exit immediately if a command exits with a non-zero status.
set -e

# 1. Check for root privileges (required for apt install)
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root or with sudo for package installation." 
   exit 1
fi

# 2. Update package lists
echo "Updating package lists..."
apt update

# 3. Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# 4. Install/Check External Tools
echo "Installing/Checking required external tools..."

# List of tools to install via apt
APT_TOOLS="nmap masscan ffuf whatweb"

# List of tools to install via go get (assuming go is installed on Kali)
GO_TOOLS="github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest github.com/projectdiscovery/httpx/cmd/httpx@latest"

# Install APT tools
for tool in $APT_TOOLS; do
    if ! command -v $tool &> /dev/null; then
        echo "Installing $tool..."
        apt install -y $tool
    else
        echo "$tool is already installed."
    fi
done

# Install GO tools (requires go to be installed)
if command -v go &> /dev/null; then
    echo "Installing Go-based tools..."
    for tool_path in $GO_TOOLS; do
        tool_name=$(basename $tool_path | cut -d'@' -f1)
        if ! command -v $tool_name &> /dev/null; then
            echo "Installing $tool_name..."
            go install $tool_path
        else
            echo "$tool_name is already installed."
        fi
    done
else
    echo "Go is not installed. Skipping installation of subfinder and httpx. Please install Go and run 'go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest' and 'go install github.com/projectdiscovery/httpx/cmd/httpx@latest' manually."
fi

# 5. Create the executable link
echo "Creating symbolic link for 'hackmate' command..."
# Make the main script executable
chmod +x hackmate/cli.py

# Create a wrapper script to run the Python module
echo '#!/bin/bash
python3 -m hackmate "$@"
' > /usr/local/bin/hackmate_wrapper
chmod +x /usr/local/bin/hackmate_wrapper

# Create the final symlink
ln -sf /usr/local/bin/hackmate_wrapper /usr/local/bin/hackmate

# 6. Final message
echo ""
echo "=================================================="
echo "HackMate installation complete!"
echo "You can now run 'hackmate' from any terminal."
echo "=================================================="
echo ""
echo "NEXT STEPS:"
echo "1. Run 'hackmate config' to see your configuration file."
echo "2. Edit ~/.hackmate/config.yaml to set your AI API key (optional)."
echo "3. Start a recon: hackmate recon subdomains example.com"
echo "4. Run a flow: hackmate flow run flows/quick-recon.yaml example.com --confirm-scope"
echo ""
