from enum import Enum, auto
import logging

from powermon.commands.response import Response
from powermon.commands.response_definition import ResponseDefinition
from powermon.dto.resultDTO import ResultDTO

log = logging.getLogger("result")

class ResultType(Enum):
    DEFAULT = auto()
    ACK = auto()
    MULTIVALUED = auto()
    INDEXED = auto()
    POSITIONAL = auto()

class Result:
    def __str__(self):
        return f"Result: {self.is_valid=}, {self.error=} - {self.error_messages=}, {self.raw_response=}, {self.responses=}"

    def __init__(self, command_code: str, response_definitions: list[ResponseDefinition]=None, raw_response=None):
        self.device_id = "default"
        self.command_code = command_code
        self.raw_response = raw_response
        self.responses :list[Response] = []
        self.response_definitions = response_definitions
        self.is_valid = False
        self.error = False
        self.error_messages = []
        log.debug("Result: %s" % (self))

    def to_DTO(self) -> ResultDTO:
        response_dtos = []
        for response in self.responses:
            response_dtos.append(response.to_DTO())
        return ResultDTO(device_identifier=self.get_device_id(), command_code=self.command_code, data=response_dtos)
    
    def get_command_code(self) -> str:
        return self.command_code
    
    def set_device_id(self, device_id):
        self.device_id = device_id

    def get_device_id(self) -> str:
        return self.device_id
    
    def get_responses(self) -> list[Response]:
        return self.responses
    
    def add_responses(self, responses: list[Response]) -> bool:
        self.responses.extend(responses)
        return True
    
    def process_raw_response(self, raw_response):
        self.raw_response = raw_response
        return



        
        