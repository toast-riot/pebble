from discord.abc import GuildChannel
from discord.permissions import Permissions

from .exceptions import PermissionException


def check_perms(channel: GuildChannel, perms: Permissions) -> None:
    current = channel.permissions_for(channel.guild.me)
    missing_perms = [k for k, v in (perms & ~current) if v]

    # if the bot can't view the channel, the missing permissions list is generally incorrect
    if "read_messages" in missing_perms:
        raise PermissionException(f"Missing permission to view channel {channel.mention}")

    if missing_perms:
        lst = "\n".join("\\- " + perm for perm in missing_perms)
        msg = f"Missing permissions for {channel.mention}:\n{lst}"
        raise PermissionException(msg)