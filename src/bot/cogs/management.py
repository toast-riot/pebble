from typing import final, override

import discord
from discord import app_commands
from discord.ext import commands

from ..helpers import interactions


@final
class management(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.original_error_handler = bot.tree.on_error
        self.bot.tree.error(self.on_app_command_error)

    @override
    async def cog_unload(self):
        self.bot.tree.error(self.original_error_handler)

    async def on_app_command_error(self, interaction: discord.Interaction[commands.Bot], error: discord.app_commands.AppCommandError):
        await interactions.error(interaction, "An error occurred.")
        await self.original_error_handler(interaction, error)

    @app_commands.command() # TODO: rm
    async def test(self, interaction: discord.Interaction[commands.Bot]):
        await interactions.respond(interaction, "Test message")