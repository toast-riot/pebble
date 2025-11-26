from .management import management
from .pins import pins
from .mod_log import mod_log

_COGS = [
    management,
    pins,
    mod_log
]

COGS = {cog.__cog_name__: cog for cog in _COGS}