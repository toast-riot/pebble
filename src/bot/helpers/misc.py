from discord.abc import GuildChannel
from discord.permissions import Permissions

from .exceptions import PermissionException


def missing_perms(target: Permissions, current: Permissions) -> list[str]:
    return [k for k, v in (target & ~current) if v]


def check_perms(channel: GuildChannel, perms: Permissions) -> None:
    current = channel.permissions_for(channel.guild.me)
    missing = missing_perms(perms, current)

    # if the bot can't view the channel, the missing permissions list is generally incorrect
    if "read_messages" in missing:
        raise PermissionException(
            f"Missing permission to view channel {channel.mention}"
        )

    if missing:
        lst = "\n".join("\\- " + perm for perm in missing)
        msg = f"Missing permissions for {channel.mention}:\n{lst}"
        raise PermissionException(msg)