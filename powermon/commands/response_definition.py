from strenum import LowercaseStrEnum
from enum import auto
from abc import ABC, abstractmethod
from powermon.protocols import ResponseType


class ResponseDefinitionType(LowercaseStrEnum):
    ACK = auto()
    INT = auto()
    OPTION = auto()
    BYTES = "bytes.decode" #can't use auto() for this value
    FLOAT = auto()
    STR_KEYED = auto()
    

class ResponseDefinition(ABC):
    """Create a flat representation to check if a response is valid for the command. It doesn't contain the response value, just the definition of what is valid."""
    
    @abstractmethod  
    def is_valid_response(self, value) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_description(self, value) -> str:
        raise NotImplementedError
    
    @classmethod
    def multiple_from_config(cls, response_definitions_config : list[list]) -> list["ResponseDefinition"]:
        if response_definitions_config is None:
            return []
        else:
            return [cls.from_config(response_definition_config) for response_definition_config in response_definitions_config]
        
    @classmethod
    def from_config(cls, response_definition_config : list) -> "ResponseDefinition":
        response_definition_index = response_definition_config[0]
        response_definition_description = response_definition_config[1]
        response_definition_type = response_definition_config[2]
        
        if response_definition_type == ResponseDefinitionType.ACK:
            ack_values : dict[str, str] = response_definition_config[3]
            ack_codes = list(ack_values.keys())
            fail_code = ack_codes[0]
            fail_description = ack_values.get(fail_code)
            success_code = ack_codes[1]
            success_description = ack_values.get(success_code)
            return ResponseDefinitionACK(index=response_definition_index,
                                         description=response_definition_description,
                                         success_code=success_code,
                                         success_description=success_description,
                                         fail_code=fail_code,
                                         fail_description=fail_description)
        
        elif response_definition_type == ResponseDefinitionType.INT:
            unit = response_definition_config[3]
            return ResponseDefinitionInt(index=response_definition_index,
                                         description=response_definition_description,
                                         unit=unit)
            
        elif response_definition_type == ResponseDefinitionType.OPTION:
            options : list[str] = response_definition_config[3]
            return ResponseDefinitionOption(index=response_definition_index,
                                            description=response_definition_description,
                                            options=options)
        
        elif response_definition_type == ResponseDefinitionType.BYTES:
            unit = response_definition_config[3]
            return ResponseDefinitionBytes(index=response_definition_index,
                                            description=response_definition_description,
                                            unit=unit)
        
        elif response_definition_type == ResponseDefinitionType.FLOAT:
            unit = response_definition_config[3]
            return ResponseDefinitionFloat(index=response_definition_index,
                                            description=response_definition_description,
                                            unit=unit)
            
        elif response_definition_type == ResponseDefinitionType.STR_KEYED:
            options : dict[str, str] = response_definition_config[3]
            return ResponseDefinitionStrKeyed(index=response_definition_index,
                                            description=response_definition_description,
                                            options=options)
    
    
class ResponseDefinitionACK(ResponseDefinition):
    def __init__(self, index: int, description: str, success_code: str, success_description: str, fail_code: str, fail_description: str):
        self.index = index
        self.description = description
        self.success_code = success_code
        self.success_description = success_description
        self.fail_code = fail_code
        self.fail_description = fail_description
    
    def is_valid_response(self, value) -> bool:
        return value == self.success_code or value == self.fail_code
    
    def get_description(self, value) -> str:
        if value == self.success_code:
            return self.success_description
        elif value == self.fail_code:
            return self.fail_description
    
class ResponseDefinitionInt(ResponseDefinition):
    def __init__(self, index: int, description: str, unit : str):
        self.description = description
        self.unit = unit
    
    def is_valid_response(self, value) -> bool:
        #Do we need to check if it's negative? Should we have max and min bounds?
        return isinstance(value, int)
    
    def get_description(self, value) -> str:
        #Option to make the description include the value, for example "Inverter temperature 34C"
        return self.description + " " + str(value) + self.unit
    
class ResponseDefinitionOption(ResponseDefinition):
    def __init__(self, index: int, description: str, options : list[str]):
        self.index = index
        self.description = description
        self.options = options
    
    def is_valid_response(self, value) -> bool:
        return value in self.options
    
    def get_description(self, value) -> str:
        return self.description + " - " + str(value)
    
class ResponseDefinitionBytes(ResponseDefinition):
    #Seems to be a catch-all for responses that are not properly implemented
    def __init__(self, index: int, description: str, unit : str):
        self.index = index
        self.description = description
        self.unit = unit
    
    def is_valid_response(self, value) -> bool:
        return True
    
    def get_description(self, value) -> str:
        #Option to make the description include the value, for example "Inverter temperature 34C"
        return self.description + " - " + str(value) + self.unit
    
class ResponseDefinitionFloat(ResponseDefinition):
    def __init__(self, index: int, description: str, unit : str):
        self.index = index
        self.description = description
        self.unit = unit
    
    def is_valid_response(self, value) -> bool:
        #Do we need to check if it's negative? Should we have max and min bounds?
        return isinstance(value, float)
    
    def get_description(self, value) -> str:
        #Option to make the description include the value, for example "Inverter temperature 34C"
        return self.description + " " + str(value) + self.unit
    
class ResponseDefinitionStrKeyed(ResponseDefinition):
    def __init__(self, index: int, description: str, options : dict[str, str]):
        self.index = index
        self.description = description
        self.options = options
            
    def is_valid_response(self, value) -> bool:
        return value in self.options
    
    def get_description(self, value) -> str:
        #Option to make the description include the value, for example "Inverter temperature 34C"
        return self.description + " - " + self.options[value]