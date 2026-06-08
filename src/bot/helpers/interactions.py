from typing import Any

import discord
from discord.utils import MISSING


async def error(interaction: discord.Interaction, message: str | None = None):
    try:
        embed = discord.Embed(
            title="Error",
            description = message or "No error details were provided.",
            color = 0xff2930,
        )
        await respond(interaction, embed=embed)
    except Exception:
        msg = f"Error: {message}" if message else "An error occurred, but no details were provided."
        await respond(interaction, msg)


# helpers for interactions
# handles current response state much more gracefully than the default behavior
# this will probably come back to bite me since the methods used have massively varying signatures

async def delete(interaction: discord.Interaction):
    if not interaction.response.is_done():
        await interaction.response.defer(ephemeral=True)
    await interaction.delete_original_response()

async def respond(interaction: discord.Interaction, content: str = MISSING, *, ephemeral: bool = MISSING, **kwargs: Any) -> None:
    if not interaction.response.is_done():
        await interaction.response.send_message(content=content, ephemeral=(ephemeral or False), **kwargs)
        return

    try:
        if (ephemeral is MISSING) or (await interaction.original_response()).flags.ephemeral == ephemeral:
            await interaction.edit_original_response(content=content, **kwargs)
            return
        await interaction.delete_original_response()
    except discord.NotFound:
        pass

    await interaction.followup.send(content=content, ephemeral=ephemeral, **kwargs)