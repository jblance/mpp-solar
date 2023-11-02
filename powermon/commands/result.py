from enum import Enum, auto
import logging

from powermon.commands.reading import Reading
from powermon.commands.parameter import Parameter
from powermon.commands.reading_definition import ReadingDefinition
from powermon.dto.resultDTO import ResultDTO

log = logging.getLogger("result")

class ResultType(Enum):
    DEFAULT = auto()
    ACK = auto()
    COMMAND = auto()
    MULTIVALUED = auto()
    INDEXED = auto()
    SINGLE = auto()
    POSITIONAL = auto()

class Result:
    def __str__(self):
        return f"Result: {self.is_valid=}, {self.error=} - {self.error_messages=}, {self.raw_response=}, {self.readings=}"

    def __init__(self, command_code: str,result_type: str, reading_definitions: list[ReadingDefinition]=None, parameters: dict[str,Parameter]=None, raw_response=None):
        if raw_response is None:
            raise ValueError("raw_response cannot be None")
        
        self.device_id = "default"
        self.command_code = command_code
        self.result_type = result_type
        self.raw_response = raw_response
        self.parameters = parameters
        self.reading_definitions = reading_definitions
        self.readings :list[Reading] = self.decode_response(raw_response=raw_response)
        self.is_valid = False
        self.error = False
        self.error_messages = []
        log.debug("Result: %s", self)

    def to_dto(self) -> ResultDTO:
        reading_dtos = []
        for reading in self.readings:
            reading_dtos.append(reading.to_dto())
        return ResultDTO(device_identifier=self.get_device_id(), command_code=self.command_code, data=reading_dtos)
    
    def get_command_code(self) -> str:
        return self.command_code

    def set_device_id(self, device_id):
        self.device_id = device_id

    def get_device_id(self) -> str:
        return self.device_id
    
    def get_responses(self) -> list[Reading]:
        return self.readings
    
    def add_readings(self, responses: list[Reading]) -> bool:
        self.readings.extend(responses)
        return True
    
    #If we split reults into different types then each type can have its own decode_response
    def decode_response(self, raw_response) -> list[Reading]:
        """
        Take the raw response and decode into a list of Readings depending on the result type
        """
        
        log.info(f"result.raw_response passed to decode: {raw_response}")
        
        all_readings : list[Reading] = []

        if self.result_type is ResultType.MULTIVALUED:
            readings = self.validate_and_translate_raw_value(self.raw_response, index=0)
            all_readings.extend(readings)
        else:
            # Split the response into individual responses
            for i, raw_response in enumerate(self.split_responses(self.raw_response)):
                readings = self.validate_and_translate_raw_value(raw_response, index=i)
                all_readings.extend(readings)

        return all_readings
    
    def split_responses(self, response) -> list:
        """
        Default implementation of split and trim
        """
        # CRC should be removed by protocol, so just split split
        return response.split(None)
    
    def validate_and_translate_raw_value(self, raw_value: str, index: int) -> list[Reading]:
        if len(self.reading_definitions) <= index:
            raise IndexError(f"Index {index} is out of range for command {self.command_code}")
        response_definition: ReadingDefinition = self.reading_definitions[index]
        try:
            return response_definition.reading_from_raw_response(raw_value)
        except ValueError:
            error = Reading(
                data_name=response_definition.get_description(), data_value=response_definition.get_invalid_message(raw_value), data_unit=""
            )
            error.is_valid = False
            return [error]
