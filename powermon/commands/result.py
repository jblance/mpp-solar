""" result.py """
import logging
from enum import Enum, auto

from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ResponseType
from powermon.dto.resultDTO import ResultDTO

log = logging.getLogger("result")


class ResultType(Enum):
    """ enum of valid types of Results """
    ERROR = auto()
    ACK = auto()  # ack / nak type result, normally from a setter command
    SINGLE = auto()  # single value in result
    ORDERED = auto()  # the order of the values determines what they are
    SLICED = auto()  # the response needs to be sliced into separate values
    MULTIVALUED = auto()  # the response has multiple values, but they all correspond to one result
    VED_INDEXED = auto()  # the response has a key / value pair (separated by \t, each pair separated by \r\n), with the key used to find the definition


class Result:
    """
    object to contain all the info of a result, including
    - command definition <- should this be the command object???
    - 'raw response' from the device
    - list of Readings (processed results)
    """
    def __str__(self):
        return f"Result: {self.is_valid=}, {self.error=} - {self.error_messages=}, {self.raw_response=}, " + ','.join(str(reading) for reading in self._readings)

    # def __init__(self, result_type: ResultType, command_definition, raw_response: bytes, responses: list | dict):
    def __init__(self, command, raw_response: bytes, responses: list | dict):
        self.is_valid = True
        self.error = False
        self.error_messages = []

        self.command = command
        self.result_type = command.command_definition.result_type
        # self.command_definition = command.command_definition

        self.raw_response = raw_response
        self.readings: list[Reading] = responses

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
    def readings(self, responses):
        self._readings = self.decode_responses(responses=responses)

    def add_readings(self, readings: list[Reading]) -> bool:
        """ add a list of readings to the current list """
        self._readings.extend(readings)
        return True

    def decode_responses(self, responses=None) -> list[Reading]:
        """
        Take the response and decode into a list of Readings depending on the result type
        """
        log.info("result.response passed to decode: %s, result_type %s", responses, self.result_type)
        all_readings : list[Reading] = []

        if responses is None:
            return all_readings

        # Process response based on result type
        match self.result_type:
            case ResultType.ACK | ResultType.SINGLE | ResultType.MULTIVALUED:
                # Get the reading definition (there is only one)
                reading_definition: ReadingDefinition = self.command.command_definition.get_reading_definition()
                # Process the response using the reading_definition, into readings
                readings = self.readings_from_response(responses, reading_definition)
                all_readings.extend(readings)
            case ResultType.ORDERED | ResultType.SLICED:
                # Have a list of reading_definitions and a list of responses that correspond to each other
                # possibly additional INFO definitions (at end of definition list??)
                definition_count = self.command.command_definition.reading_definition_count()
                response_count = len(responses)
                for position in range(definition_count):
                    reading_definition: ReadingDefinition = self.command.command_definition.get_reading_definition(position=position)
                    if position < response_count:
                        readings = self.readings_from_response(responses[position], reading_definition)
                        all_readings.extend(readings)
                    else:
                        # More definitions than results, either INFO type definitions or too little data
                        if reading_definition.response_type == ResponseType.INFO_FROM_COMMAND:
                            # INFO is contained in supplied command eg QEY2023 -> 2023
                            readings = self.readings_from_response(self.command.code, reading_definition)
                            all_readings.extend(readings)
            case ResultType.VED_INDEXED:
                # have a list of (index,value) tuples
                for key, value in responses:
                    reading_definition: ReadingDefinition = self.command.command_definition.get_reading_definition(lookup=key)
                    if reading_definition is not None:
                        # Process the response using the reading_definition, into readings
                        readings = self.readings_from_response(value, reading_definition)
                        all_readings.extend(readings)
            case ResultType.ERROR:
                # Get the reading_definition - this may need fixing for errors
                reading_definition: ReadingDefinition = self.command.command_definition.get_reading_definition()
                # Process the response using the reading_definition, into readings
                readings = self.readings_from_response(responses, reading_definition)
                all_readings.extend(readings)
            case _:
                # unknown result type
                raise ValueError(f"Unknown result type: {self.result_type}")
        log.debug("got readings: %s", ",".join(str(i) for i in all_readings))
        # print(','.join(str(reading) for reading in all_readings))
        return all_readings

    def readings_from_response(self, response, reading_definition) -> list[Reading]:
        """ return readings from a raw_response using the supplied reading definition """
        try:
            return reading_definition.reading_from_raw_response(response, override=self.command.override)
        except ValueError:
            error = Reading(data_name=reading_definition.description,
                            data_value=reading_definition.get_invalid_message(response), data_unit="")
            error.is_valid = False
            return [error]

    def to_dto(self) -> ResultDTO:
        """ convert result object to data transfer object """
        reading_dtos = []
        for reading in self.readings:
            reading_dtos.append(reading.to_dto())
        return ResultDTO(device_identifier="self.device_id", command_code="self.command_code", data=reading_dtos)


class ResultError(Result):
    """ docstring todo """
    def __init__(self, command, raw_response: bytes, responses: list | dict):
        self.command = command
        self.raw_response = raw_response
        self.result_type = ResultType.ERROR

        self.is_valid = False
        self.error = True
        self.error_messages = responses

        # self.command_definition = command.command_definition

        self.readings: list[Reading] = None

        log.debug("Result: %s", self)
