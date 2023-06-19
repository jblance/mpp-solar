import logging
from powermon.commands.command import Command

log = logging.getLogger("result")


class Result:
    def __str__(self):
        return f"Result: {self.command}, {self.is_valid=}, {self.error=} - {self.error_messages=}, {self.raw_response=}, {self.decoded_responses=}"

    def __init__(self, command : Command, raw_response=None):
        self.command = command
        self.raw_response = raw_response
        self.responses = []
        self.decoded_responses = None
        self.is_valid = False
        self.error = False
        self.error_messages = []
        log.debug("Result: %s" % (self))
