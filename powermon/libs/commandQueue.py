import logging
from powermon.commands.command import Command

# from time import time


# Set-up logger
log = logging.getLogger("commandQueue")


class CommandQueue:
    def __str__(self):
        return f"CommandQueue, number of commands: {len(self.commands)}"

    def __init__(self, config={}):
        log.debug(f"commandQueue, config: {config}")
        self.commands = []
        if not config:
            log.debug("no commands config passed to commandQueue")
            return

        for command in config:
            try:
                _command = Command(config=command)
            except TypeError:
                _command = None
            if _command is not None:
                self.commands.append(_command)
