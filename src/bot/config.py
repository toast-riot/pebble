from . import constants
from .helpers import config

CFG_FILE = config.Config_File(constants.CONFIG_FILE)
CFG: config.Config_Object = CFG_FILE.config # type checker seems to struggle with this