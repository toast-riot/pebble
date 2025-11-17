import discord
from discord.ext import commands
from . import cogs_manager
from sys import argv

class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.moderation = True
        intents.message_content = True # For consistency, might not be needed

        super().__init__(command_prefix="", intents=intents)

        @self.event
        async def setup_hook():
            await cogs_manager.add_all(self)

        @self.event
        async def on_ready():
            print(f"Connected => {self.user}")

            if len(argv) > 1 and argv[1] == "sync":
                print("Syncing commands..." )
                await self.tree.sync()
                print("Commands synced")

            # for guild in bot.guilds:
            #     if not guild.me.guild_permissions.view_audit_log:
            #         print(f"WARNING: Missing permissions to view audit log in {guild.name}")

        @self.event
        async def on_message(message: discord.Message) -> None: # This intentionally prevents the bot checking for plaintext commands
            pass