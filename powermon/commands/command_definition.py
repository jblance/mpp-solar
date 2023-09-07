from powermon.protocols import ResponseType
from powermon.dto.command_definition_dto import CommandDefinitionDTO

class CommandDefinition:
    def __init__(self, code, description, help_text: str, response_type : ResponseType, 
                 responses, text_response: list[bytes], regex: str, type: str):
        self.code = code
        self.description = description
        self.help_text = help_text
        self.response_type : ResponseType = response_type
        self.responses = responses
        self.text_responses : list[bytes] = text_response
        self.regex : str | None = regex
        self.type : str = type
        
    def to_DTO(self) -> CommandDefinitionDTO:
        return CommandDefinitionDTO(
            command_code=self.code,
            description=self.description,
            help_text=self.help_text,
            response_type=str(self.response_type),
            responses=self.responses,
            text_responses=self.text_responses,
            regex=self.regex
        )
        
    def get_type(self) -> str:
        return self.type
        
        
        
    @classmethod
    def from_config(cls, dict, type) -> "CommandDefinition":
        code = dict.get("name")
        description = dict.get("description")
        help_text = dict.get("help_text")
        response_type = dict.get("response_type")
        responses = dict.get("responses")
        text_response = dict.get("text_response")
        regex = dict.get("regex", None)
        return cls(code=code, description=description, help_text=help_text, response_type=response_type, 
                   responses=responses, text_response=text_response, regex=regex, type=type)