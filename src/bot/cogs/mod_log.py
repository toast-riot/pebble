import discord
from discord import app_commands
from discord.ext import commands
from .. import config

from ..helpers.misc import BotException

class mod_log(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.add_listener(self.on_audit_log_entry_create, "on_audit_log_entry_create")


    async def cog_unload(self) -> None:
        self.bot.remove_listener(self.on_audit_log_entry_create, "on_audit_log_entry_create")


    async def mod_log(guild: discord.Guild, message: str):
        mod_log_channel = await channel_by_name(guild, CONFIG["mod_log_channel"])
        if not mod_log_channel:
            print(f"WARNING: Mod log channel not found (looking for #{CONFIG['mod_log_channel']})")
            return
        if not mod_log_channel.permissions_for(guild.me).view_channel:
            print(f"WARNING: Missing permissions to view #{CONFIG['mod_log_channel']}")
            return
        if not mod_log_channel.permissions_for(guild.me).send_messages:
            print(f"WARNING: Missing permissions to send messages in #{CONFIG['mod_log_channel']}")
            return
        await mod_log_channel.send(message, allowed_mentions = discord.AllowedMentions(users=False))


    async def perm_error(interaction: discord.Interaction, message: str):
        await interaction.edit_original_response(content=f"{CONFIG["permission_error_message"]} {message}")


    class AuditLogMessage():
        def __init__(self, entry: discord.AuditLogEntry):
            self.initiator: discord.User = None
            self.action: str = None
            self.target: discord.User = None
            self.reason: str = None
            self.extra: str = None

        # async def build_log(initiator: discord.User, action: str, target: discord.User, reason: str = None, extra: str = None):
            # reason = f" with reason `{reason}`" if reason else ""
            # extra = f" {extra}" if extra else ""
            # return f"{initiator.mention} (`{initiator.name}`) {action} {target.mention} (`{target.name}`){extra}{reason}"


    async def on_audit_log_entry_create(entry: discord.AuditLogEntry):
        message = mod_log.AuditLogMessage(entry)

        if entry.action == discord.AuditLogAction.member_update and entry.changes.after.timed_out_until:
            message.action = "timed out"
            message.extra = f"until <t:{int(entry.changes.after.timed_out_until.timestamp())}:R>"
        elif entry.action == discord.AuditLogAction.ban:
            message.action = "banned"
        elif entry.action == discord.AuditLogAction.kick:
            message.action = "kicked"
        else:
            return

        # message["initiator"] = await bot.fetch_user(entry.user_id)
        # message.initiator = await entry.guild.fetch_member(entry.user.id)
        message["target"] = await bot.fetch_user(entry.target.id)
        message.reason = entry.reason
        message = await build_log(**message)
        await mod_log(entry.guild, message)