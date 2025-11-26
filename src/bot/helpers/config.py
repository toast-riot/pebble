import json
import os
import sys
from .config_types import ConfigObj, AutoDict, cfg, create_auto_dict
from pathlib import Path

class Config_Object(ConfigObj):
    servers: AutoDict[int, 'Config_Object.Server']

    def __init__(self, config: dict = {}):
        self.servers = create_auto_dict(int, Config_Object.Server, cfg(config, "servers", dict[str, dict], {}))

    class Server(ConfigObj):
        channel_mod_log: int | None
        channel_pins: int | None
        channel_pins_nsfw: int | None
        duplicate_pins_check_count: int
        nsfw_extras: list[int]
        nsfw_pin_channel_check_enabled: bool

        def __init__(self, config: dict = {}):
            self.channel_mod_log = cfg(config, "channel_mod_log", int | None, None)
            self.channel_pins = cfg(config, "channel_pins", int | None, None)
            self.channel_pins_nsfw = cfg(config, "channel_pins_nsfw", int | None, None)
            self.duplicate_pins_check_count = cfg(config, "duplicate_pins_check_count", int, 50)
            self.nsfw_extras = cfg(config, "nsfw_extras", list[int], [])
            self.nsfw_pin_channel_check_enabled = cfg(config, "nsfw_pin_channel_check_enabled", bool, True)


class Config_File:
    def __init__(self, file_path: Path):
        if file_path.is_absolute():
            self.file_path = file_path
        else:
            self.file_path = Path(sys.modules["__main__"].__file__).parent / file_path
        self.load()

    def load(self) -> None:
        self.config = Config_Object(self._load())

    def save(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump(self.config._data, file, indent=4)

    def _load(self) -> dict:
        if not os.path.exists(self.file_path): return {}
        if os.path.getsize(self.file_path) == 0: return {}
        with open(self.file_path, "r") as file:
            return json.load(file)