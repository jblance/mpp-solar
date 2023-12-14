""" result.py """
import logging
from enum import Enum, auto

from powermon.commands.reading import Reading
from powermon.commands.reading_definition import (ReadingDefinition,
                                                  ReadingDefinitionMessage,
                                                  ResponseType)
from powermon.dto.resultDTO import ResultDTO

log = logging.getLogger("result")


class ResultType(Enum):
    """ enum of valid types of Results """
    ERROR = auto()
    ACK = auto()  # ack / nak type result, normally from a setter command
    SINGLE = auto()  # single value in result
    ORDERED = auto()  # the order of the values determines what they are

    MULTIVALUED = auto()
    INDEXED = auto()
    POSITIONAL = auto()


class Result:
    """
    object to contain all the info of a result, including
    - command definition
    - 'raw response' from the device (also the trimmed version)
    - list of Readings (processed results)
    """
    def __str__(self):
        return f"Result: {self.is_valid=}, {self.error=} - {self.error_messages=}, {self.raw_response=}, " + \
        ','.join(str(reading) for reading in self._readings)

    def __init__(self, result_type: ResultType, command_definition, raw_response: bytes, trimmed_response: bytes):
        self.raw_response = raw_response
        self.trimmed_response = trimmed_response

        self.is_valid = True
        self.error = False
        self.error_messages = []

        self.result_type = result_type
        self.command_definition = command_definition
        self.readings: list[Reading] = trimmed_response

        log.debug("Result: %s", self)

    @property
    def raw_response(self):
        """ the raw_response as received from the device """
        return self._raw_response

    @raw_response.setter
    def raw_response(self, value):
        if value is None:
            raise ValueError("raw_response cannot be None")
        self._raw_response = value

    @property
    def trimmed_response(self):
        """ the raw_response trimmed of unneeded bits """
        return self._trimmed_response

    @trimmed_response.setter
    def trimmed_response(self, value):
        self._trimmed_response = value

    @property
    def result_type(self):
        """ the type of the result """
        return self._result_type

    @result_type.setter
    def result_type(self, value):
        self._result_type = value
        if value == ResultType.ERROR:
            self.is_valid = False
            self.error = True
            self.error_messages = [self.raw_response]

    @property
    def readings(self) -> list[Reading]:
        """ list of processed readings """
        return self._readings

    @readings.setter
    def readings(self, trimmed_response):
        self._readings = self.decode_response(response=trimmed_response)

    def add_readings(self, responses: list[Reading]) -> bool:
        """ add a list of readings to the current list """
        self._readings.extend(responses)
        return True

    # If we split results into different types then each type can have its own decode_response
    def decode_response(self, response) -> list[Reading]:
        """
        Take the response and decode into a list of Readings depending on the result type
        """

        log.info("result.response passed to decode: %s, result_type %s", response, self.result_type)

        all_readings : list[Reading] = []

        # Process response based on result type
        match self.result_type:
            case ResultType.SINGLE:
                reading = self.reading_from_response(response)
                all_readings.append(reading)
            case ResultType.ACK:
                reading = self.reading_from_response(response)
                all_readings.append(reading)
            case ResultType.ORDERED:
                # Response is splitable and order of each item determines decode logic
                for i, _raw_response in enumerate(self.split_responses(response)):
                    log.debug("ResultType.ORDERED, i: %s, _raw_response: %s", i, _raw_response)
                    readings = self.validate_and_translate_raw_value(_raw_response, index=i)
                    all_readings.extend(readings)
            case ResultType.MULTIVALUED:
                # while response has multiple values, the all relate to a single result
                readings = self.validate_and_translate_raw_value(response, index=0)
                all_readings.extend(readings)
            case ResultType.ERROR:
                readings = self.validate_and_translate_raw_value(response, index=0)
                all_readings.extend(readings)
            case _:
                # unknown result type
                raise ValueError(f"Unknown result type: {self.result_type}")
        log.debug("got readings: %s", ",".join(str(i) for i in all_readings))
        return all_readings

    def split_responses(self, response) -> list:
        """
        Default implementation of split and trim
        """
        # CRC should be removed by protocol, so just split split
        return response.split(None)  # split differs by protocol

    def reading_from_response(self, response) -> Reading:
        """ return a reading from a raw_response that applies to a single reading """
        reading_definition: ReadingDefinition = self.command_definition.reading_definitions[0]
        try:
            return reading_definition.reading_from_raw_response(response)[0]
        except ValueError:
            error = Reading(data_name=reading_definition.get_description(),
                            data_value=reading_definition.get_invalid_message(response), data_unit="")
            error.is_valid = False
            return [error]


    def validate_and_translate_raw_value(self, raw_value: str, index: int) -> list[Reading]:
        if len(self.command_definition.reading_definitions) <= index:
            log.debug("Index %s is out of range for command %s", index, self.command_definition.command_code)
            reading_definition: ReadingDefinition = ReadingDefinitionMessage(index=index, response_type=ResponseType.STRING , description=f"Unused response {index}")
        else:
            reading_definition: ReadingDefinition = self.command_definition.reading_definitions[index]
        try:
            return reading_definition.reading_from_raw_response(raw_value)
        except ValueError:
            error = Reading(
                data_name=reading_definition.get_description(), data_value=reading_definition.get_invalid_message(raw_value), data_unit=""
            )
            error.is_valid = False
            return [error]

    def to_dto(self) -> ResultDTO:
        """ convert result object to data transfer object """
        reading_dtos = []
        for reading in self.readings:
            reading_dtos.append(reading.to_dto())
        return ResultDTO(device_identifier="self.device_id", command_code="self.command_code", data=reading_dtos)
