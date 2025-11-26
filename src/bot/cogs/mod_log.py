import discord
from discord.ext import commands
from .. import config
from ..helpers.exceptions import *

class mod_log(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.add_listener(self.on_audit_log_entry_create, "on_audit_log_entry_create")

    async def cog_unload(self) -> None:
        self.bot.remove_listener(self.on_audit_log_entry_create, "on_audit_log_entry_create")


    class AuditLogMessage():
        initiator: discord.User | discord.Member
        action: str
        target: discord.User | discord.Member
        reason: str | None = None
        extra: str | None = None

        async def build_log(self):
            reason = f" with reason `{self.reason}`" if self.reason else ""
            extra = f" {self.extra}" if self.extra else ""
            return "{0} (`{1}`) {2} {3} (`{4}`){5}{6}".format(
                self.initiator.mention, self.initiator.name,
                self.action,
                self.target.mention, self.target.name,
                extra, reason
            )


    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        message = mod_log.AuditLogMessage()
        
        if entry.action == discord.AuditLogAction.member_update and entry.changes.after.timed_out_until:
            message.action = "timed out"
            message.extra = f"until <t:{int(entry.changes.after.timed_out_until.timestamp())}:R>"
        elif entry.action == discord.AuditLogAction.ban:
            message.action = "banned"
        elif entry.action == discord.AuditLogAction.kick:
            message.action = "kicked"
        else:
            return
        
        # should always be present if the entry.action is relevant
        if not entry.user: raise BotException("Audit log entry missing user")
        if not entry.target: raise BotException("Audit log entry missing target")
        if not isinstance(entry.target, (discord.User, discord.Member)):
            raise BotException("Audit log entry target is not a User or Member")

        message.initiator = entry.user
        message.target = entry.target
        message.reason = entry.reason

        mod_log_channel_id = config.cfg.servers[entry.guild.id].channel_mod_log
        if not mod_log_channel_id:
            raise ConfigurationException(f"Mod log channel ID not set")
        
        mod_log_channel = entry.guild.get_channel(mod_log_channel_id)
        if not mod_log_channel:
            raise ConfigurationException(f"Mod log channel not found")
        
        if not isinstance(mod_log_channel, discord.TextChannel):
            raise ConfigurationException(f"Mod log channel is not a text channel")

        message = await message.build_log()
        await mod_log_channel.send(message, allowed_mentions = discord.AllowedMentions(users=False))