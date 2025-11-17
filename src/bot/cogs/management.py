import discord
from discord import app_commands
from discord.ext import commands
from ..helpers import interactions

class management(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction) -> None:
        await interactions.respond(interaction, "Test command", ephemeral=True)