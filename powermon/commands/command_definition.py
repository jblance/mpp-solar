""" commands / command_definition.py """
import logging
import re

from powermon.commands.parameter import Parameter
# from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition
from powermon.commands.result import ResultType
from powermon.dto.command_definition_dto import CommandDefinitionDTO

log = logging.getLogger("CommandDefinition")


class CommandDefinition:
    """ object the contains the definition and other metadata about a command """
    def __str__(self):
        return f"{self.code=}, {self.description=}, {self.result_type=}"

    def __init__(self, code, description, help_text: str, result_type : ResultType,
                 reading_definitions, parameters, test_responses: list, regex: str):
        if reading_definitions is None or len(reading_definitions) == 0:
            raise ValueError(f"reading definitions cannot be None for command_code: {code}")
        # if test_responses is None or len(test_responses) == 0:
        #     raise ValueError(f"test_responses cannot be None for command_code: {code}")
        self.code = code
        self.description = description
        self.help_text = help_text
        self.result_type : ResultType = result_type
        self.reading_definitions : dict[int, ReadingDefinition] = reading_definitions
        self.parameters : dict[str, Parameter] = parameters
        self.test_responses : list[bytes] = test_responses
        self.regex : str | None = regex

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

    def get_type(self) -> ResultType:
        """ return the command definition type """
        return self.result_type

    def get_response_definition_count(self) -> int:
        """ return the number of reading definitions """
        if self.reading_definitions is None:
            return 0
        return len(self.reading_definitions)

    def set_parameter_value(self, parameter_value: str):
        """ sets the parameter value """
        if self.parameters is None:
            raise ValueError(f"Parameters not defined but parameter value set for command_code: {self.code}, \
                Check the command definitions")

        for parameter in self.parameters.values():
            parameter.set_value(parameter_value)
            return

    @classmethod
    def from_config(cls, protocol_dictionary : dict) -> "CommandDefinition":
        """ build command definition object from config dict """
        code = protocol_dictionary.get("name")
        description = protocol_dictionary.get("description")
        help_text = protocol_dictionary.get("help_text")
        result_type = protocol_dictionary.get("result_type")  # QUESTION: this where ResultType.ACK logic could differ
        reading_definitions : dict[int, ReadingDefinition] = \
            ReadingDefinition.multiple_from_config(protocol_dictionary.get("reading_definitions"))
        parameters : dict[str, Parameter] = Parameter.multiple_from_config(protocol_dictionary.get("parameters"))
        test_responses = protocol_dictionary.get("test_responses")
        regex = protocol_dictionary.get("regex", None)
        log.debug("code: %s description: %s reading_definitions: %s", code, description, reading_definitions)
        return cls(
            code=code, description=description, help_text=help_text, result_type=result_type,
            reading_definitions=reading_definitions, parameters=parameters, test_responses=test_responses,
            regex=regex
        )
