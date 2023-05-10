# from powermon.dto.commandDTO import CommandDTO
import logging

# from powermon.ports.abstractport import AbstractPort
# from powermon.outputs.abstractoutput import AbstractOutput


log = logging.getLogger("Command")


class Command:
    def __str__(self):
        return f"Command: {self.command}, type: {self.type}, last run: {self.last_run}, next run: {self.next_run}, trigger: {self.trigger}"

    def __init__(self, config):
        if not config:
            log.warning("Invalid command config")
            return None

        self.command = config.get("command")
        self.type = config.get("type", "basic")
        self.last_run = None
        self.trigger = config.get("trigger")
        self.next_run = None
