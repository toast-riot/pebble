from .management import management
from .pins import pins

_COGS = [
    management,
    pins
]

COGS = {cog.__cog_name__: cog for cog in _COGS}