from powermon.protocols import ResponseType
from powermon.dto.command_definition_dto import CommandDefinitionDTO

class CommandDefinition:
    def __init__(self, code, description, help_text: str, response_type : ResponseType, 
                 responses, test_responses: list[bytes], regex: str, type: str):
        if responses is None:
            raise ValueError(f"responses cannot be None for command_code: {code}")
        if test_responses is None:
            raise ValueError(f"test_responses cannot be None for command_code: {code}")
        self.code = code
        self.description = description
        self.help_text = help_text
        self.response_type : ResponseType = response_type
        self.responses = responses
        self.test_responses : list[bytes] = test_responses
        self.regex : str | None = regex
        self.type : str = type
        
    def to_DTO(self) -> CommandDefinitionDTO:
        return CommandDefinitionDTO(
            command_code=self.code,
            description=self.description,
            help_text=self.help_text,
            response_type=str(self.response_type),
            responses=self.responses,
            #test_responses=self.test_responses,
            regex=self.regex
        )
        
    def get_type(self) -> str:
        return self.type
        
    def get_response_count(self) -> int:
        if(self.responses is None):
            return 0
        else:
            return len(self.responses)
        
        
    @classmethod
    def from_config(cls, dict, type) -> "CommandDefinition":
        code = dict.get("name")
        description = dict.get("description")
        help_text = dict.get("help_text")
        response_type = dict.get("response_type")
        responses = dict.get("response")
        test_responses = dict.get("test_responses")
        regex = dict.get("regex", None)
        return cls(code=code, description=description, help_text=help_text, response_type=response_type, 
                   responses=responses, test_responses=test_responses, regex=regex, type=type)