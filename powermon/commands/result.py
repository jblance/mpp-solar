""" result.py """
from enum import Enum, auto
import logging

from powermon.commands.reading import Reading
from powermon.commands.parameter import Parameter
from powermon.commands.reading_definition import ReadingDefinition, ReadingDefinitionMessage, ResponseType
from powermon.dto.resultDTO import ResultDTO

log = logging.getLogger("result")


class ResultType(Enum):
    """ enum of valid types of Results """
    ERROR = auto()
    ACK = auto()
    COMMAND = auto()
    MULTIVALUED = auto()
    INDEXED = auto()
    SINGLE = auto()
    POSITIONAL = auto()


class Result:
    """ object to contain all the info of a result """
    def __str__(self):
        return f"Result: {self.is_valid=}, {self.error=} - {self.error_messages=}, {self.raw_response=}, {' '.join(str(i) for i in self.readings)}"

    def __init__(self, command_code: str, result_type: str, raw_response: bytes, reading_definitions: list[ReadingDefinition] = None,
                 parameters: dict[str, Parameter] = None):
        if raw_response is None:
            raise ValueError("raw_response cannot be None")

        self.device_id = "default"
        self.command_code = command_code
        self.result_type = result_type
        self.raw_response = raw_response
        self.parameters = parameters
        
        self.reading_definitions = reading_definitions
        if(self.reading_definitions is None):
            reading_definition = ReadingDefinitionMessage(index=0, name="default", response_type=ResponseType.STRING , description="default")
            self.reading_definitions = [reading_definition]
            
        self.readings: list[Reading] = self.decode_response(raw_response=raw_response)
        self.is_valid = True
        self.error = False
        self.error_messages = []
        
        if result_type == ResultType.ERROR:
            self.is_valid = False
            self.error = True
            self.error_messages = [self.raw_response]
        
        log.debug("Result: %s", self)

    def to_dto(self) -> ResultDTO:
        """ convert result object to data transfer object """
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

    # If we split results into different types then each type can have its own decode_response
    def decode_response(self, raw_response) -> list[Reading]:
        """
        Take the raw response and decode into a list of Readings depending on the result type
        """

        log.info("result.raw_response passed to decode: %s", raw_response)

        all_readings : list[Reading] = []

        # Process response based on result type
        match self.result_type:
            case ResultType.SINGLE:
                readings = self.validate_and_translate_raw_value(self.raw_response, index=0)
                all_readings.extend(readings)
            case ResultType.ACK:
                readings = self.validate_and_translate_raw_value(self.raw_response, index=0)
                all_readings.extend(readings)
            case ResultType.INDEXED:
                # Response is splitable and order of each item determines decode logic
                for i, _raw_response in enumerate(self.split_responses(self.raw_response)):
                    print(f"i: {i}, _raw_response: {_raw_response}")
                    readings = self.validate_and_translate_raw_value(_raw_response, index=i)
                    all_readings.extend(readings)
            case ResultType.MULTIVALUED:
                # while response has multiple values, the all relate to a single result
                readings = self.validate_and_translate_raw_value(self.raw_response, index=0)
                all_readings.extend(readings)
            case ResultType.ERROR:
                readings = self.validate_and_translate_raw_value(self.raw_response, index=0)
                all_readings.extend(readings)
            case _:
                # unknown result type
                raise ValueError(f"Unknown result type: {self.result_type}")

        return all_readings

    def split_responses(self, response) -> list:
        """
        Default implementation of split and trim
        """
        # CRC should be removed by protocol, so just split split
        return response.split(None) # split differs by protocol

    def validate_and_translate_raw_value(self, raw_value: str, index: int) -> list[Reading]:
        if len(self.reading_definitions) <= index:
            log.debug("Index %s is out of range for command %s", index, self.command_code)
            reading_definition: ReadingDefinition = ReadingDefinitionMessage(index=index, name="default", response_type=ResponseType.STRING , description=f"Unused response {index}")
        else:
            reading_definition: ReadingDefinition = self.reading_definitions[index]
        try:
            return reading_definition.reading_from_raw_response(raw_value)
        except ValueError:
            error = Reading(
                data_name=reading_definition.get_description(), data_value=reading_definition.get_invalid_message(raw_value), data_unit=""
            )
            error.is_valid = False
            return [error]
