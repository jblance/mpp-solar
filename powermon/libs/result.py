import logging

log = logging.getLogger("result")


class Result:
    def __str__(self):
        return f"Result: command: {self.command}, error: {self.error} - {self.error_message}, raw: {self.raw_response}, decoded: {self.decoded_response}"

    def __init__(self, command=None):
        self.command = command
        self.raw_response = None
        self.decoded_response = None
        self.error = False
        self.error_message = None
        log.debug("Result: %s" % (self))
