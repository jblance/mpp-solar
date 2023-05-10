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
        for command in config:
            self.commands.append(Command(config=command))
