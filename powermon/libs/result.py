import logging

log = logging.getLogger("result")


class Result:
    def __str__(self):
        return f"Result: command: {self.command}, error: {self.error} - {self.error_messages}, raw: {self.raw_response}, decoded: {self.decoded_responses}"

    def __init__(self, command=None):
        self.command = command
        self.raw_response = None
        self.responses = []
        self.decoded_responses = None
        self.is_valid = False
        self.error = False
        self.error_messages = []
        log.debug("Result: %s" % (self))
