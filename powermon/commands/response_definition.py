from strenum import LowercaseStrEnum
from enum import auto
from abc import ABC, abstractmethod
from powermon.commands.response import Response
import calendar #needed for INFO type evaluating templates


class ResponseType(LowercaseStrEnum):
    ACK = auto()
    INT = auto()
    TEN_INT = auto()
    OPTION = auto()
    BYTES = "bytes.decode" #can't use auto() for this value
    FLOAT = auto()
    STR_KEYED = auto()
    ENFLAGS = auto()
    STRING = auto()
    FLAGS = auto()
    INFO = auto()
    

class ResponseDefinition(ABC):
    """Create a flat representation to check if a response is valid for the command. It doesn't contain the response value, just the definition of what is valid."""
    
    def is_valid_response(self, value) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_description(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def response_from_raw_values(self, raw_value) -> list[Response]:
        raise NotImplementedError
    
    def get_invalid_message(self, raw_value) -> str:
        return f"Invalid response for {self.get_description()}: {raw_value}"
    
    def is_info(self) -> bool:
        return False
    
    @classmethod
    def multiple_from_config(cls, response_definitions_config : list[list]) -> dict[int,"ResponseDefinition"]:
        if response_definitions_config is None:
            return {}
        else:
            response_definitions : dict[int,"ResponseDefinition"] = {}
            for response_definition_config in response_definitions_config:
                response_definition = cls.from_config(response_definition_config)
                response_definitions[response_definition.index] = response_definition
            return response_definitions
        
    @classmethod
    def from_config(cls, response_definition_config : list) -> "ResponseDefinition":
        response_definition_index = response_definition_config[0]
        response_definition_description = response_definition_config[1]
        response_definition_type = response_definition_config[2]
        
        response_definition_extra = None
        device_class = None
        state_class = None
        icon = None
        
        #parse out the extra values
        if len(response_definition_config) > 4:
            response_definition_extra = response_definition_config[4]
            device_class = response_definition_extra.get("device-class", None)
            state_class = response_definition_extra.get("state-class", None)
            icon = response_definition_extra.get("icon", None)
        
        if response_definition_type == ResponseType.ACK:
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
                                         fail_description=fail_description,
                                         device_class=device_class,
                                         state_class=state_class,
                                         icon=icon)
        
        elif response_definition_type == ResponseType.INT:
            unit = response_definition_config[3]
            return ResponseDefinitionInt(index=response_definition_index,
                                         description=response_definition_description,
                                         unit=unit,
                                         device_class=device_class,
                                         state_class=state_class,
                                         icon=icon)
        
        elif response_definition_type == ResponseType.TEN_INT:
            unit = response_definition_config[3]
            return ResponseDefinitionTenInt(index=response_definition_index,
                                         description=response_definition_description,
                                         unit=unit,
                                         device_class=device_class,
                                         state_class=state_class,
                                         icon=icon)
        
        elif response_definition_type == ResponseType.OPTION:
            options : list[str] = response_definition_config[3]
            return ResponseDefinitionOption(index=response_definition_index,
                                            description=response_definition_description,
                                            options=options,
                                            device_class=device_class,
                                            state_class=state_class,
                                            icon=icon)
        
        elif response_definition_type == ResponseType.BYTES:
            unit = response_definition_config[3]
            return ResponseDefinitionBytes(index=response_definition_index,
                                            description=response_definition_description,
                                            unit=unit,
                                            device_class=device_class,
                                            state_class=state_class,
                                            icon=icon)
        
        elif response_definition_type == ResponseType.FLOAT:
            unit = response_definition_config[3]
            return ResponseDefinitionFloat(index=response_definition_index,
                                            description=response_definition_description,
                                            unit=unit,
                                            device_class=device_class,
                                            state_class=state_class,
                                            icon=icon)
            
        elif response_definition_type == ResponseType.STR_KEYED:
            options : dict[str, str] = response_definition_config[3]
            return ResponseDefinitionStrKeyed(index=response_definition_index,
                                            description=response_definition_description,
                                            options=options,
                                            device_class=device_class,
                                            state_class=state_class,
                                            icon=icon)
            
        elif response_definition_type == ResponseType.ENFLAGS:
            flags : dict[str, dict[str, str]] = response_definition_config[3]
            return ResponseDefinitionENFlags(index=response_definition_index,
                                            description=response_definition_description,
                                            enflags=flags,
                                            device_class=device_class,
                                            state_class=state_class,
                                            icon=icon)
            
        elif response_definition_type == ResponseType.STRING:
            unit = response_definition_config[3]
            return ResponseDefinitionString(index=response_definition_index,
                                            description=response_definition_description,
                                            unit=unit,
                                            device_class=device_class,
                                            state_class=state_class,
                                            icon=icon)
            
        elif response_definition_type == ResponseType.FLAGS:
            flags : list[str] = response_definition_config[3]
            return ResponseDefinitionFlags(index=response_definition_index,
                                            description=response_definition_description,
                                            flags=flags,
                                            device_class=device_class,
                                            state_class=state_class,
                                            icon=icon)
            
        elif ResponseType.INFO in response_definition_type:
            template = response_definition_type.split(":",1)[1]
            return ResponseDefinitionInfo(index=response_definition_index,
                                            description=response_definition_description,
                                            template=template,
                                            device_class=device_class,
                                            state_class=state_class,
                                            icon=icon)
            
            
        else:
            raise ValueError(f"Response description: {response_definition_description} has unknown response definition type: {response_definition_type}")
    
        
    
class ResponseDefinitionACK(ResponseDefinition):
    def __init__(self, index: int, description: str, success_code: str, success_description: str, fail_code: str, fail_description: str, 
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.success_code = success_code
        self.success_description = success_description
        self.fail_code = fail_code
        self.fail_description = fail_description
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
    
    def is_valid_response(self, value) -> bool:
        return value == self.success_code or value == self.fail_code
        
    def response_from_raw_values(self, raw_value) -> list[Response]:
        value = raw_value.decode()
        if value == self.success_code:
            return [Response(data_name=self.description,
                            data_value=self.success_description,
                            data_unit=None,
                            device_class=self.device_class,
                            state_class=self.state_class,
                            icon=self.icon)]
        elif value == self.fail_code:
            return [Response(data_name=self.description,
                            data_value=self.fail_description,
                            data_unit=None,
                            device_class=self.device_class,
                            state_class=self.state_class,
                            icon=self.icon)]
        
    def get_description(self) -> str:
        return self.description
    
class ResponseDefinitionInt(ResponseDefinition):
    def __init__(self, index: int, description: str, unit : str,
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.unit = unit
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
    
    def is_valid_response(self, value) -> bool:
        #Do we need to check if it's negative? Should we have max and min bounds?
        return isinstance(value, int)
    
    def translate_raw_response(self, raw_value) -> str:
        return int(raw_value.decode())
    
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        value = self.translate_raw_response(raw_value)
        return [Response(data_name=self.description,
                        data_value=str(value),
                        data_unit=self.unit,
                        device_class=self.device_class,
                        state_class=self.state_class,
                        icon=self.icon)]
    
    def get_description(self) -> str:
        return self.description
      
# Same INT but base 10
class ResponseDefinitionTenInt(ResponseDefinition):
    def __init__(self, index: int, description: str, unit : str,
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.unit = unit
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
    
    def is_valid_response(self, value) -> bool:
        #Do we need to check if it's negative? Should we have max and min bounds?
        return isinstance(value, int) / 10
    
    def translate_raw_response(self, raw_value) -> str:
        return int(raw_value.decode()) / 10
    
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        value = self.translate_raw_response(raw_value)
        return [Response(data_name=self.description,
                        data_value=str(value),
                        data_unit=self.unit,
                        device_class=self.device_class,
                        state_class=self.state_class,
                        icon=self.icon)]
    
    def get_description(self) -> str:
        return self.description
    
class ResponseDefinitionOption(ResponseDefinition):
    def __init__(self, index: int, description: str, options : list[str],
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.options = options
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
    
    def is_valid_response(self, value) -> bool:
        return value in self.options
    
    def translate_raw_response(self, raw_value) -> str:
        value = int(raw_value.decode())
        return self.options[value]
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        value = self.translate_raw_response(raw_value)
        return [Response(data_name=self.description,
                        data_value=value,
                        data_unit="",
                        device_class=self.device_class,
                        state_class=self.state_class,
                        icon=self.icon)]
    
    def get_description(self) -> str:
        return self.description
    
class ResponseDefinitionBytes(ResponseDefinition):
    #Seems to be a catch-all for responses that are not properly implemented
    def __init__(self, index: int, description: str, unit : str,
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.unit = unit
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
    
    def is_valid_response(self, value) -> bool:
        return True
    
    def translate_raw_response(self, raw_value) -> str:
        return raw_value.decode()
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        value = self.translate_raw_response(raw_value)
        return [Response(data_name=self.description,
                        data_value=value,
                        data_unit="",
                        device_class=self.device_class,
                        state_class=self.state_class,
                        icon=self.icon)]
    
    def get_description(self) -> str:
        return self.description
    
class ResponseDefinitionString(ResponseDefinition):
    #Seems to be a catch-all for responses that are not properly implemented
    def __init__(self, index: int, description: str, unit : str,
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.unit = unit
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
    
    def is_valid_response(self, value) -> bool:
        return isinstance(value, str)
    
    def translate_raw_response(self, raw_value) -> str:
        if isinstance(raw_value, str):
            return raw_value
        return str(raw_value.decode())
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        return [Response(data_name=self.description,
                        data_value=self.translate_raw_response(raw_value),
                        data_unit=self.unit,
                        device_class=self.device_class,
                        state_class=self.state_class,
                        icon=self.icon)]
    
    def get_description(self) -> str:
        return self.description
    
class ResponseDefinitionFloat(ResponseDefinition):
    def __init__(self, index: int, description: str, unit : str,
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.unit = unit
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
    
    def is_valid_response(self, value) -> bool:
        #Do we need to check if it's negative? Should we have max and min bounds?
        return isinstance(value, float)
    
    def translate_raw_response(self, raw_value) -> float:
        return float(raw_value.decode())
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        value = self.translate_raw_response(raw_value)
        return [Response(data_name=self.description,
                        data_value=str(value),
                        data_unit=self.unit,
                        device_class=self.device_class,
                        state_class=self.state_class,
                        icon=self.icon)]
    
    def get_description(self) -> str:
        return self.description
    
class ResponseDefinitionStrKeyed(ResponseDefinition):
    def __init__(self, index: int, description: str, options : dict[str, str],
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.options = options
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
            
    def is_valid_response(self, value) -> bool:
        return value in self.options
    
    def translate_raw_response(self, raw_value) -> str:
        value = raw_value.decode()
        return self.options[value]
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        value = self.translate_raw_response(raw_value)
        return [Response(data_name=self.description,
                        data_value=value,
                        data_unit="",
                        device_class=self.device_class,
                        state_class=self.state_class,
                        icon=self.icon)]
    
    def get_description(self) -> str:
        return self.description
    
class ResponseDefinitionENFlags(ResponseDefinition):
    def __init__(self, index: int, description: str, enflags : dict[str, dict[str, str]],
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.enflags = enflags #what does enflags mean?
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
            
    def is_valid_response(self, value) -> bool:
        return True
    
    def translate_raw_response(self, raw_value) -> dict[str, str]:
        return_values = {}
        status = "unknown"
        for i, item in enumerate(raw_value):
            item = chr(item)
            if item == "E":
                status = "enabled"
            elif item == "D":
                status = "disabled"
            else:
                if item in self.enflags:
                    _key = self.enflags[item]["name"]
                else:
                    _key = f"unknown_{i}"
                return_values[_key] = status
        return return_values
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        values : dict[str, str] = self.translate_raw_response(raw_value)
        responses = []
        for name, value in values.items():
            responses.append(Response(data_name=name,
                                      data_value=value,
                                      data_unit="",
                                      device_class=self.device_class,
                                      state_class=self.state_class,
                                      icon=self.icon))
        
        return responses
    
    def get_description(self) -> str:
        return self.description

class ResponseDefinitionFlags(ResponseDefinition):
    def __init__(self, index: int, description: str, flags : list[str],
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.flags = flags
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
        
    def is_valid_response(self, value) -> bool:
        return value in self.flags
    
    def translate_raw_response(self, raw_value) -> dict[str, int]:
        return_value = {}
        for i, flag in enumerate(raw_value):
            if self.flags[i]:  # only append value if flag name is present
                return_value[self.flags[i]] = int(chr(flag))
        return return_value
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        values : dict[str, int] = self.translate_raw_response(raw_value)
        responses = []
        for name, value in values.items():
            responses.append(Response(data_name=name,
                                      data_value=value,
                                      data_unit="bool",
                                      device_class=self.device_class,
                                      state_class=self.state_class,
                                      icon=self.icon))
        return responses
    
    def get_description(self) -> str:
        return self.description
    
class ResponseDefinitionInfo(ResponseDefinition):
    def __init__(self, index: int, description: str, template : str,
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None):
        self.index = index
        self.description = description
        self.template = template
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon
    
    def translate_raw_response(self, cn) -> str:
        return eval(self.template)
    
    def is_info(self) -> bool:
        return True
    
    def response_from_raw_values(self, raw_value) -> list[Response]:
        value = self.translate_raw_response(raw_value)
        return [Response(data_name=self.description,
                data_value=value,
                data_unit="",
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon)]
    
    def get_description(self) -> str:
        return self.description
