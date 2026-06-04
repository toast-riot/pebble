from discord.ext import commands

from .management import management
from .mod_log import mod_log
from .pins import pins

_COGS = [
    management,
    pins,
    mod_log
]
COGS = {cog.__cog_name__: cog for cog in _COGS}

async def add_all(bot: commands.Bot) -> None:
    for _, cog in COGS.items():
        await bot.add_cog(cog(bot))