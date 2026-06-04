import json
from pathlib import Path
from pydantic import BaseModel, Field

class ServerConfig(BaseModel):
    channel_mod_log: int | None = None
    channel_pins: int | None = None
    channel_pins_nsfw: int | None = None
    duplicate_pins_check_count: int = 50
    nsfw_extras: list[int] = Field(default_factory=list)
    nsfw_pin_channel_check_enabled: bool = True

class Config_Object(BaseModel):
    servers: dict[int, ServerConfig] = Field(default_factory=dict)

    def get_server(self, server_id: int):
        if server_id not in self.servers:
            self.servers[server_id] = ServerConfig()
        return self.servers[server_id]

class Config_File:
    file_path: Path
    config: Config_Object

    def __init__(self, file_path: Path):
        self.file_path = file_path.resolve()
        self.config = self.load()

    def load(self) -> Config_Object:
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return Config_Object()
        with self.file_path.open("r") as file:
            data = json.load(file)
            return Config_Object.model_validate(data)

    def save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w") as file:
            json.dump(self.config.model_dump(), file, indent=4)