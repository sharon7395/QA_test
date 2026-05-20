import os
import yaml
from typing import Dict

def load_config(config_path: str) -> Dict:
    """
        טעינת קובץ הקונפיגורציה
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if not config:
        raise ValueError("Config file is empty")

    return config