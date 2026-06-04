from typing import Any

import discord
from discord.utils import MISSING


# placeholder for potential future styling
async def error(interaction: discord.Interaction, message: str):
    await respond(interaction, message)


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