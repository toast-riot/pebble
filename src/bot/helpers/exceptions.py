class BotException(Exception):
    handled: bool = True

    def __init__(self, *args: object, handled: bool = True) -> None:
        self.handled = handled
        super().__init__(*args)

class PermissionException(BotException):
    pass

class ConfigurationException(BotException):
    pass