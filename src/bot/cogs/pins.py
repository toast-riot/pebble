from typing import final, override

import discord
from discord import MessageReferenceType, app_commands
from discord.ext import commands
from discord.permissions import Permissions

from ..config import CFG
from ..helpers import interactions
from ..helpers.exceptions import BotException, ConfigurationException
from ..helpers.misc import check_perms


@final
class pins(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.message_pin_ctx = app_commands.ContextMenu(
            name="Pin Message",
            callback=self.message_pin_message_context,
            allowed_contexts=app_commands.AppCommandContext(
                guild=True,
                dm_channel=False,
                private_channel=False
            )
        )
        self.bot.tree.add_command(self.message_pin_ctx)

    @override
    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.message_pin_ctx.name, type=self.message_pin_ctx.type
        )

    async def message_pin_message_context(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        await interaction.response.defer()
        await self.pinboard(interaction, message)

    async def pinboard(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        assert interaction.guild
        assert isinstance(message.channel, discord.abc.GuildChannel)

        server_config = CFG.get_server(interaction.guild.id)

        is_nsfw = message.channel.is_nsfw() or message.channel.id in server_config.nsfw_extras
        pin_channel_id = server_config.channel_pins_nsfw if is_nsfw else server_config.channel_pins

        if not pin_channel_id:
            if is_nsfw:
                raise ConfigurationException("NSFW pinboard channel not configured")
            raise ConfigurationException("Pinboard channel not configured")

        pin_channel = interaction.guild.get_channel(pin_channel_id)

        if not pin_channel:
            raise BotException(f"Pinboard channel `{pin_channel_id}` not found")
        
        if not isinstance(pin_channel, discord.TextChannel):
            raise BotException(f"Pinboard channel {pin_channel.mention} is not a text channel")

        perms = Permissions(view_channel=True, send_messages=True)
        if server_config.duplicate_pins_check_count > 0:
            perms.read_message_history = True
        check_perms(pin_channel, perms)

        if server_config.duplicate_pins_check_count > 0:
            async for pin_message in pin_channel.history(limit=server_config.duplicate_pins_check_count):
                if (
                    pin_message.reference and
                    pin_message.reference.message_id == message.id and
                    pin_message.reference.type == MessageReferenceType.forward
                ):
                    raise BotException(f"Message is already pinned at {pin_message.jump_url}")

        try:
            await pin_channel.send(f"-# {message.author.mention}", allowed_mentions=discord.AllowedMentions.none())
            pin = await message.forward(pin_channel)
        except discord.HTTPException as e:
            raise BotException(e.text, handled=False) from e

        await interactions.respond(interaction, content=f"Message pinned: {pin.jump_url}")