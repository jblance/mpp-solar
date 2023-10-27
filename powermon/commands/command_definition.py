import re

from powermon.commands.result import ResultType
from powermon.dto.command_definition_dto import CommandDefinitionDTO
from powermon.commands.reading import Reading
from powermon.commands.parameter import Parameter
from powermon.commands.reading_definition import ReadingDefinition

class CommandDefinition:
    def __init__(self, code, description, help_text: str, response_type : ResultType, 
                 reading_definitions, parameters, test_responses: list, regex: str, command_definition_type: str):
        if reading_definitions is None or len(reading_definitions) == 0:
            raise ValueError(f"response definitions cannot be None for command_code: {code}")
        if test_responses is None or len(test_responses) == 0:
            raise ValueError(f"test_responses cannot be None for command_code: {code}")
        self.code = code
        self.description = description
        self.help_text = help_text
        self.result_type : ResultType = response_type
        self.reading_definitions : dict[int,ReadingDefinition] = reading_definitions
        self.parameters : dict[str,Parameter] = parameters
        self.test_responses : list[bytes] = test_responses
        self.regex : str | None = regex
        self.command_definition_type : str = command_definition_type
        
    def to_DTO(self) -> CommandDefinitionDTO:
        return CommandDefinitionDTO(
            command_code=self.code,
            description=self.description,
            help_text=self.help_text,
            response_type=str(self.result_type),
            #responses=self.response_definitions, #TODO: make DTOs for the response definitions
            #test_responses=self.test_responses,
            regex=self.regex
        )
        
    def is_command_code_valid(self, command_code : str) -> bool:
        if self.regex is None:
            return self.code == command_code
        return re.match(self.regex, command_code) is not None
        
    def get_type(self) -> str:
        return self.command_definition_type
        
    def get_response_definition_count(self) -> int:
        if(self.reading_definitions is None):
            return 0
        else:
            return len(self.reading_definitions)
        
    def set_parameter_value(self, parameter_value: str):
        if self.parameters is None:
            raise ValueError(f"Parameters not definted but parameter value set for command_code: {self.code}, Check the command definitions")
        
        for parameter in self.parameters.values():
            parameter.set_value(parameter_value)
            return
        
        
        
        
        
    @classmethod
    def from_config(cls, protocol_dictionary : dict, command_definition_type) -> "CommandDefinition":
        code = protocol_dictionary.get("name")
        description = protocol_dictionary.get("description")
        help_text = protocol_dictionary.get("help_text")
        response_type = protocol_dictionary.get("result_type")
        reading_definitions : dict[int,ReadingDefinition] = ReadingDefinition.multiple_from_config(protocol_dictionary.get("reading_definitions"))
        parameters : dict[str,Parameter] = Parameter.multiple_from_config(protocol_dictionary.get("parameters"))
        test_responses = protocol_dictionary.get("test_responses")
        regex = protocol_dictionary.get("regex", None)
        return cls(code=code, description=description, help_text=help_text, response_type=response_type, 
                   reading_definitions=reading_definitions, parameters=parameters, test_responses=test_responses, regex=regex, command_definition_type=command_definition_type)