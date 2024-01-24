""" commands / command_definition.py """
import logging
import re

from powermon.commands.reading_definition import ReadingDefinition, ReadingType
from powermon.commands.result import ResponseType, ResultType
from powermon.dto.command_definition_dto import CommandDefinitionDTO

log = logging.getLogger("CommandDefinition")


class CommandDefinition:
    """ object the contains the definition and other metadata about a command, including: 
    - code
    - regex (opt)
    - description
    - result type
    - reading definitions
    - test responses
    """
    def __str__(self):
        return f"CommandDefinition: {self.code=}, {self.description=}, {self.result_type=}"

    def __init__(self, code, description, help_text: str, result_type : ResultType, reading_definitions, test_responses: list = None, regex: str = None):
        """ init CommandDefinition class """
        if reading_definitions is None or len(reading_definitions) == 0:
            raise ValueError(f"reading definitions cannot be None for command_code: {code}")

        self.code = code
        self.description = description
        self.help_text = help_text
        self.result_type : ResultType = result_type
        self.reading_definitions : dict[int, ReadingDefinition] = reading_definitions  # TODO: this is incorrect, needs positional and str indexes as well
        self.test_responses : list[bytes] = test_responses
        self.regex : str | None = regex
        self.device_command_type = None
        self.device_command_code : str = None

    @classmethod
    def from_config(cls, protocol_dictionary : dict) -> "CommandDefinition":
        """ build command definition object from config dict """
        code = protocol_dictionary.get("name")
        description = protocol_dictionary.get("description")
        help_text = protocol_dictionary.get("help_text")
        test_responses = protocol_dictionary.get("test_responses")
        regex = protocol_dictionary.get("regex", None)
        result_type = protocol_dictionary.get("result_type")
        match result_type:
            case ResultType.ACK:
                # All ResultType.ACK are the same, so put config here instead of duplicating it in the protocol
                log.debug("ResultType.ACK so defaulting reading_definitions")
                reading_definitions : dict[int, ReadingDefinition] = \
                    ReadingDefinition.multiple_from_config([{"description": description, "response_type": ResponseType.ACK, "reading_type": ReadingType.ACK}])
                test_responses = [b"(NAK\x73\x73\r", b"(ACK\x39\x20\r",]
            case _:
                reading_definitions : dict[int, ReadingDefinition] = \
                    ReadingDefinition.multiple_from_config(protocol_dictionary.get("reading_definitions"))

        log.debug("code: %s description: %s reading_definitions: %s", code, description, reading_definitions)
        _command_definition = cls(
            code=code, description=description, help_text=help_text, result_type=result_type,
            reading_definitions=reading_definitions, test_responses=test_responses,
            regex=regex
        )
        _command_definition.device_command_type = protocol_dictionary.get("device_command_type")
        _command_definition.device_command_code = protocol_dictionary.get("device_command_code")
        return _command_definition

    def to_dto(self) -> CommandDefinitionDTO:
        """ convert command definition object to data transfer object """
        return CommandDefinitionDTO(
            command_code=self.code,
            description=self.description,
            help_text=self.help_text,
            result_type=str(self.result_type),
            # responses=self.response_definitions, #TODO: make DTOs for the response definitions
            # test_responses=self.test_responses,
            regex=self.regex
        )

    def is_command_code_valid(self, command_code : str) -> bool:
        """ determines if a command code is valid """
        if self.regex is None:
            return self.code == command_code
        return re.match(self.regex, command_code) is not None

    def get_reading_definition(self, lookup=None, position=0) -> ReadingDefinition:
        """ return the reading definition that corresponds to lookup """
        log.debug("looking for reading definition with: %s, result_type is: %s", lookup, self.result_type)
        if self.reading_definitions is None:
            result = None
        match self.result_type:
            case ResultType.ACK | ResultType.SINGLE | ResultType.MULTIVALUED:
                result = self.reading_definitions[0]
            case ResultType.ORDERED | ResultType.SLICED:
                result = self.reading_definitions[position]
            case ResultType.VED_INDEXED:
                try:
                    result = self.reading_definitions[lookup]
                except KeyError:
                    log.warning("no reading definition found for key: %s", lookup)
                    result = None
            case _:
                print(f"no get_reading_definition for {self.result_type=}")
                exit()
        log.debug("found reading definition: %s", result)
        return result

    def reading_definition_count(self) -> int:
        """ return the number of reading_definitions for this command_definition """
        return 0 if self.reading_definitions is None else len(self.reading_definitions)
