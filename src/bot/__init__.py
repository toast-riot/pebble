from sys import argv

import discord
from discord.ext import commands

from . import cogs
from .config import CFG, CFG_FILE

# pyright: reportUnusedFunction=hint

class Bot(commands.Bot):
    __slots__: tuple[()] = ()

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.moderation = True
        intents.message_content = True

        super().__init__(command_prefix="", intents=intents)

        @self.event
        async def setup_hook():
            # create missing server configurations and write back
            for guild in self.guilds:
                CFG.get_server(guild.id)
            CFG_FILE.save()

            await cogs.add_all(self)

        @self.event
        async def on_ready():
            print(f"Connected => {self.user}")

            if len(argv) > 1 and argv[1] == "sync":
                print("Syncing commands..." )
                await self.tree.sync()
                print("Commands synced")

        @self.event
        async def on_message(_: discord.Message) -> None:
            # TODO: possible to add hooks to this in cogs?
            pass