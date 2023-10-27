from strenum import LowercaseStrEnum
from enum import auto
import datetime

class ParameterType(LowercaseStrEnum):
    DATE = auto()
    
class ParameterFormat(LowercaseStrEnum):
    YYYYMMDD = auto()
    
class Parameter:
    def __init__(self, name, description, parameter_type: ParameterType, parameter_format: ParameterFormat):
        self.name = name
        self.description = description
        self.parameter_type = parameter_type
        self.parameter_format = parameter_format
        self.value = None
        
    def set_value(self, value):
        if self.parameter_type == ParameterType.DATE:
            if self.parameter_format == ParameterFormat.YYYYMMDD:
                self.value = datetime.date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
        
        
    @classmethod
    def multiple_from_config(cls, parameters_config: list) -> dict[str, "Parameter"]:
        parameters: dict[str, Parameter] = {}
        if parameters_config is None:
            return parameters
        for parameter_config in parameters_config:
            parameter = Parameter.from_config(parameter_config)
            parameters[parameter.name] = parameter
        return parameters
        
    @classmethod
    def from_config(cls, parameter_config: dict) -> "Parameter":
        name = parameter_config.get("name")
        description = parameter_config.get("description")
        parameter_type = ParameterType(parameter_config.get("parameter_type"))
        parameter_format = ParameterFormat(parameter_config.get("parameter_format"))
        return Parameter(name, description, parameter_type, parameter_format)
        
    def __str__(self):
        return f"Parameter: {self.name} {self.description} {self.parameter_type} {self.parameter_format}"
        
    def __repr__(self):
        return self.__str__()
        