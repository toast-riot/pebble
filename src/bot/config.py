from pathlib import Path
from .helpers import config as _config

CONFIG_FILE = Path("../config.json")

file = _config.Config_File(CONFIG_FILE)
cfg = file.config