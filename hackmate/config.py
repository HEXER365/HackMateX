import os
from pathlib import Path
from tinydb import TinyDB
import yaml

# Define the base directory for HackMate configuration and data
HACKMATE_HOME = Path.home() / ".hackmate"
HACKMATE_CONFIG_FILE = HACKMATE_HOME / "config.yaml"
HACKMATE_DB_FILE = HACKMATE_HOME / "notes.json"

# Default configuration
DEFAULT_CONFIG = {
    "workspace_dir": str(HACKMATE_HOME / "workspaces"),
    "concurrency": 10,
    "safe_defaults": {
        "masscan_rate": 1000,
        "nmap_timing": "T3",
        "allow_destructive": False,
    },
    "tools": {
        "subfinder": "subfinder",
        "httpx": "httpx",
        "nmap": "nmap",
        "masscan": "masscan",
        "ffuf": "ffuf",
        "nuclei": "nuclei",
    },
    "ai": {
        "enabled": False,
        "model": "gpt-4.1-mini",
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
    }
}

def init_hackmate_home():
    """Initializes the .hackmate directory and default config file."""
    HACKMATE_HOME.mkdir(parents=True, exist_ok=True)
    Path(DEFAULT_CONFIG["workspace_dir"]).mkdir(parents=True, exist_ok=True)
    
    if not HACKMATE_CONFIG_FILE.exists():
        with open(HACKMATE_CONFIG_FILE, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
        print(f"Created default config at {HACKMATE_CONFIG_FILE}")

def load_config():
    """Loads the configuration from the YAML file."""
    init_hackmate_home()
    try:
        with open(HACKMATE_CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
        # Merge with defaults to ensure all keys exist
        merged_config = DEFAULT_CONFIG.copy()
        # Simple merge for top-level keys
        merged_config.update(config)
        # Deep merge for nested keys like 'safe_defaults' and 'tools'
        for key in ["safe_defaults", "tools", "ai"]:
            if key in config and isinstance(config[key], dict):
                merged_config[key].update(config[key])
        return merged_config
    except Exception as e:
        # print(f"Warning: Could not load config file. Using defaults. Error: {e}")
        return DEFAULT_CONFIG

def get_workspace_path(target: str) -> Path:
    """Returns the path to the workspace directory for a given target."""
    config = load_config()
    workspace_root = Path(config["workspace_dir"])
    # Sanitize target name for directory creation
    sanitized_target = target.lower().replace("http://", "").replace("https://", "").replace("/", "_").replace(":", "_")
    target_path = workspace_root / sanitized_target
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path

def get_notes_db() -> TinyDB:
    """Returns the TinyDB instance for notes."""
    init_hackmate_home()
    return TinyDB(HACKMATE_DB_FILE)

# Initialize on import
init_hackmate_home()
CONFIG = load_config()
