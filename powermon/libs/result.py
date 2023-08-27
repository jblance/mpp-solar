import logging

log = logging.getLogger("result")


class Result:
    def __str__(self):
        return f"Result: {self.is_valid=}, {self.error=} - {self.error_messages=}, {self.raw_response=}, {self.decoded_responses=}"

    def __init__(self, command_code: str, raw_response=None):
        self.device_id = "default"
        self.command_code = command_code
        self.raw_response = raw_response
        self.responses = []
        self.decoded_responses = None
        self.is_valid = False
        self.error = False
        self.error_messages = []
        log.debug("Result: %s" % (self))

    def to_DTO(self):
        return None
    
    def get_command_code(self) -> str:
        return self.command_code
    
    def set_device_id(self, device_id):
        self.device_id = device_id

    def get_device_id(self) -> str:
        return self.device_id
    
    def get_decoded_responses(self) -> dict:
        return self.decoded_responses