from . import constants
from .helpers import config

CFG_FILE = config.Config_File(constants.CONFIG_FILE)
CFG = CFG_FILE.config