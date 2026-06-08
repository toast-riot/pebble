from typing import final, override

import discord
from discord import app_commands
from discord.ext import commands

from ..helpers import interactions
from ..helpers.exceptions import BotException


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
        error_ = error
        if isinstance(error, app_commands.CommandInvokeError):
            error_ = error.original

        handled = False
        try:
            command = interaction.command
            if (command is not None) and (command._has_any_error_handlers()): # pyright: ignore[reportPrivateUsage]
                return

            # to avoid potential log leaking, only sends messages for known exceptions
            if isinstance(error_, BotException):
                handled = True
                await interactions.error(interaction, str(error_))
            else:
                await interactions.error(interaction)
        finally:
            if not handled:
                await self.original_error_handler(interaction, error)

    @app_commands.command() # TODO: rm
    async def test(self, interaction: discord.Interaction[commands.Bot]):
        await interactions.respond(interaction, "Test message")