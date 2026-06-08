class BotException(Exception):
    handled: bool = False

    def __init__(self, *args: object, handled: bool = False) -> None:
        self.handled = handled
        super().__init__(*args)

class PermissionException(BotException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args, handled=True)

class ConfigurationException(BotException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args, handled=True)