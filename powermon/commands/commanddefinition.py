from powermon.protocols import ResponseType

class CommandDefinition:
    def __init__(self, code, description, help_text: str, response_type : ResponseType, 
                 responses, text_response: list[bytes], regex: str):
        self.code = code
        self.description = description
        self.help_text = help_text
        self.response_type : ResponseType = response_type
        self.responses = responses
        self.text_responses : list[bytes] = text_response
        self.regex : str = regex
        
        
        
        
    @classmethod
    def from_dictionary(cls, dict) -> "CommandDefinition":
        code = dict.get("name")
        description = dict.get("description")
        help_text = dict.get("help_text")
        response_type = dict.get("response_type")
        responses = dict.get("responses")
        text_response = dict.get("text_response")
        regex = dict.get("regex")
        return cls(code=code, description=description, help_text=help_text, response_type=response_type, 
                   responses=responses, text_response=text_response, regex=regex)