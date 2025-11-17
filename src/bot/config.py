from .helpers import config as _config

CONFIG_FILE = "../config.json"

file = _config.Config_File(CONFIG_FILE)
cfg = file.config