from discord.ext import commands
from .cogs import COGS

async def add_all(bot: commands.Bot) -> None:
    for _, cog in COGS.items():
        await bot.add_cog(cog(bot))