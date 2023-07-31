import logging

from .pi17 import pi17


log = logging.getLogger("pi17infini")

QUERY_COMMANDS = {}
SETTER_COMMANDS = {}
COMMANDS_TO_REMOVE = []


class pi17infini(pi17):
    def __str__(self):
        return "PI17INFINI protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI17INFINI"
        # Add pi17infini specific commands to pi17 commands
        self.COMMANDS.update(QUERY_COMMANDS)
        # Add pi17infini specific setter commands
        self.COMMANDS.update(SETTER_COMMANDS)
        # remove and unwanted pi30 commands
        for item in COMMANDS_TO_REMOVE:
            if item in self.COMMANDS:
                self.COMMANDS.pop(item)
