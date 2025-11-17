import discord
from discord import app_commands
from discord.ext import commands
from urllib.parse import urlparse
from .. import config
from ..helpers import interactions

from ..helpers.misc import BotException

class pins(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.message_pin_ctx = app_commands.ContextMenu(
            name='Pin Message',
            callback=self.message_pin_message_context
        )
        self.bot.tree.add_command(self.message_pin_ctx)


    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.message_pin_ctx.name, type=self.message_pin_ctx.type)


    async def message_pin_message_context(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.defer()
        await self.pinboard(interaction, message)


    async def get_embed(self, message: discord.Message) -> discord.Embed:
        embed = discord.Embed(
            description = message.content,
            color = 0x2b2d31,
            url=message.jump_url # Used to quickly find duplicate pins
        )
        embed.add_field(name="", value="", inline=False) # Spacer

        if message.embeds:
            data = message.embeds[0]
            if data.type == "image":
                embed.set_image(url=data.url)

        if message.attachments:
            attachment = message.attachments[0]
            path = urlparse(attachment.url).path
            if path.lower().endswith(("png", "jpeg", "jpg", "gif", "webp")):
                embed.set_image(url=attachment.url)
            else:
                embed.add_field(name="Attachment", value=f"-# {attachment.url}", inline=False)

        embed.add_field(name="User", value=f"-# {message.author.mention}")
        embed.add_field(name="Link", value=f"-# {message.jump_url}")
        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)

        return embed


    async def pinboard(self, interaction: discord.Interaction, message: discord.Message) -> None:
        is_nsfw = message.channel.is_nsfw() or message.channel.id in config.server(interaction.guild.id).nsfw_extras

        if is_nsfw:
            channel_to_get = config.server(interaction.guild.id).channel_pins_nsfw
        else:
            channel_to_get = config.server(interaction.guild.id).channel_pins

        pin_channel = interaction.guild.get_channel(channel_to_get)

        if not pin_channel:
            raise BotException(f"Pinboard channel not found (looking for `#{channel_to_get}`)")
            # await interaction.edit_original_response(content=f"Pinboard channel not found (looking for `#{channel_to_get}`)")
            # return

        # if not pin_channel.permissions_for(message.guild.me).view_channel:
        #     await perm_error(interaction, f"view {pin_channel.mention}")
        #     return
        # if not pin_channel.permissions_for(message.guild.me).send_messages:
        #     await perm_error(interaction, f"send messages in {pin_channel.mention}")
        #     return
        # if not pin_channel.permissions_for(message.guild.me).embed_links:
        #     await perm_error(interaction, f"embed links in {pin_channel.mention}")
        #     return
        # if CONFIG["nsfw_pin_channel_check_enabled"] and (should_be_nsfw and not pin_channel.is_nsfw()):
        #     await interaction.edit_original_response(content=f"{pin_channel.mention} must be marked as NSFW")
        #     return

        # Check if message is already pinned
        if config.server(interaction.guild.id).duplicate_pins_check_count > 0:
            # if not pin_channel.permissions_for(message.guild.me).read_message_history:
            #     await perm_error(interaction, f"read message history in {pin_channel.mention}")
            #     return

            async for pin_message in pin_channel.history(limit=config.server(interaction.guild.id).duplicate_pins_check_count):
                current = pin_message.embeds and pin_message.embeds[0] and pin_message.embeds[0].url or None
                if current == message.jump_url:
                    await interactions.respond(interaction, content=f"Message is already pinned at {pin_message.jump_url}")
                    return

        embed = await self.get_embed(message)
        await pin_channel.send(embed=embed)
        await interactions.respond(interaction, content=f"Message pinned to {pin_channel.mention}")