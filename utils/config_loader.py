import yaml
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, "r") as file:
        return yaml.safe_load(file)