""" reading_definition.py """
import calendar  # needed for INFO type evaluating templates
import logging
from abc import ABC, abstractmethod
from enum import auto

from strenum import LowercaseStrEnum

from powermon.commands.reading import Reading

log = logging.getLogger("ReadingDefinition")


class ResponseType(LowercaseStrEnum):
    """
    the type of the response
    - determines how to read and translate to useful info
    """
    ACK = auto()
    INT = auto()
    OPTION = auto()
    BYTES = "bytes.decode"  # can't use auto() for this value
    FLOAT = auto()
    ENFLAGS = auto()
    STRING = auto()
    FLAGS = auto()
    INFO = auto()


class ReadingType(LowercaseStrEnum):
    """
    the type of the reading
    - higher level type, like Wh etc
    - allows translations
    """
    ACK = auto()
    WATT_HOURS = auto()
    WATTS = auto()
    TIME = auto()
    MESSAGE = auto()
    FLAG = auto()
    AMPERAGE = auto()
    TEMPERATURE = auto()
    PERCENTAGE = auto()
    FREQUENCY = auto()
    AMPS = auto()


class ReadingDefinition(ABC):
    """
    Create a flat representation to check if a response is valid for the command.
    It doesn't contain the response value, just the definition of what is valid.
    """
    def __str__(self):
        return f"{self.index=}, {self.name=}, {self.description=}, {self.response_type=}, {self.unit=}, instance={type(self)}"

    def __init__(self, index, name, response_type, description, device_class, state_class, icon, unit=""):
        self.index = index
        self.name = name
        self.response_type = response_type
        self.unit = unit
        self.description = description
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon

    def get_description(self) -> str:
        return self.description

    @abstractmethod
    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        raise NotImplementedError

    def get_invalid_message(self, raw_value) -> str:
        return f"Invalid response for {self.get_description()}: {raw_value}"

    def is_info(self) -> bool:
        return False

    @classmethod
    def multiple_from_config(cls, reading_definitions_config: list[dict]) -> dict[int, "ReadingDefinition"]:
        if reading_definitions_config is None:
            return {}
        else:
            reading_definitions: dict[int, "ReadingDefinition"] = {}
            for i, reading_definition_config in enumerate(reading_definitions_config):
                reading_definition = cls.from_config(reading_definition_config, i)
                log.debug("reading definition: %s", reading_definition)
                reading_definitions[reading_definition.index] = reading_definition
            return reading_definitions

    @classmethod
    def from_config(cls, reading_definition_config: dict, i) -> "ReadingDefinition":
        index = i
        name = reading_definition_config.get("name")
        description = reading_definition_config.get("description")
        response_type = reading_definition_config.get("response_type")
        reading_type = reading_definition_config.get("reading_type")
        device_class = reading_definition_config.get("device-class", None)
        state_class = reading_definition_config.get("state-class", None)
        icon = reading_definition_config.get("icon", None)

        match reading_type:
            case ReadingType.ACK:
                return ReadingDefinitionACK(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )
            case ReadingType.WATT_HOURS:
                return ReadingDefinitionWattHours(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )
            case ReadingType.MESSAGE:
                options = None
                if response_type == ResponseType.OPTION:
                    options: dict[str, str] = reading_definition_config.get("options")
                return ReadingDefinitionMessage(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    options=options,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )
            case ReadingType.TEMPERATURE:
                return ReadingDefinitionTemperature(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon
                )
            case ReadingType.TIME:
                return ReadingDefinitionDefault(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                    unit="s"
                )
            case ReadingType.FLAG:
                return ReadingDefinitionDefault(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon
                )
            case ReadingType.AMPERAGE:
                return ReadingDefinitionDefault(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                    unit="A"
                )
            case ReadingType.PERCENTAGE:
                return ReadingDefinitionDefault(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                    unit="%"
                )
            case ReadingType.FREQUENCY:
                return ReadingDefinitionDefault(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                    unit="Hz"
                )
            case ReadingType.WATTS:
                return ReadingDefinitionDefault(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                    unit="W"
                )

            case _:
                raise ValueError(
                    f"Reading description: {description} has unknown reading_type definition type: {reading_type}"
                )


class ReadingDefinitionDefault(ReadingDefinition):
    def __init__(
        self,
        index: int,
        name: str,
        response_type: str,
        description: str,
        device_class: str = None,
        state_class: str = None,
        icon: str = None,
        unit: str = ""
    ):
        super().__init__(index, name, response_type, description, device_class, state_class, icon, unit=unit)

    def translate_raw_response(self, raw_value) -> str:
        return raw_value.decode()

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = self.translate_raw_response(raw_value)
        return [
            Reading(
                data_name=self.description,
                data_value=value,
                data_unit=self.unit,
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon,
            )
        ]


class ReadingDefinitionACK(ReadingDefinition):
    def __init__(
        self,
        index: int,
        name: str,
        response_type: str,
        description: str,
        device_class: str = None,
        state_class: str = None,
        icon: str = None,
    ):
        super().__init__(index, name, response_type, description, device_class, state_class, icon)

        self.fail_code = "NAK"
        self.fail_description = "Failed"
        self.success_code = "ACK"
        self.success_description = "Successful"

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = raw_value.decode()
        if value == self.success_code:
            return [
                Reading(
                    data_name=self.description,
                    data_value=self.success_description,
                    data_unit=None,
                    device_class=self.device_class,
                    state_class=self.state_class,
                    icon=self.icon,
                )
            ]
        elif value == self.fail_code:
            return [
                Reading(
                    data_name=self.description,
                    data_value=self.fail_description,
                    data_unit=None,
                    device_class=self.device_class,
                    state_class=self.state_class,
                    icon=self.icon,
                )
            ]

    def get_description(self) -> str:
        return self.description

class ReadingDefinitionWattHours(ReadingDefinition):
    def __init__(
        self,
        index: int,
        name: str,
        response_type: str,
        description: str,
        device_class: str = None,
        state_class: str = None,
        icon: str = None
    ):
        super().__init__(index, name, response_type, description, device_class, state_class, icon, unit="Wh")
        if response_type not in [ResponseType.INT]:
            raise TypeError(f"Wh response must be of type int, ResponseType {response_type} is not valid")

    def translate_raw_response(self, raw_value) -> str:
        return int(raw_value.decode())

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = self.translate_raw_response(raw_value)
        return [
            Reading(
                data_name=self.description,
                data_value=value,
                data_unit=self.unit,
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon,
            )
        ]


class ReadingDefinitionMessage(ReadingDefinition):
    def __init__(
        self,
        index: int,
        name: str,
        response_type: str,
        description: str,
        options: dict[str, str] = None,
        device_class: str = None,
        state_class: str = None,
        icon: str = None
    ):
        super().__init__(index, name, response_type, description, device_class, state_class, icon, unit="")
        if response_type == ResponseType.OPTION and not isinstance(options, dict):
            raise TypeError(f"For Reading Defininition {self.name}, options must be a dict if response_type is OPTION")
        
        self.options = options

    def translate_raw_response(self, raw_value) -> str:
        if self.response_type == ResponseType.OPTION:
            value = str(raw_value.decode())
            print(f"Reading:{self.description} Value:{value}")
            
            return self.options[value]
        return raw_value.decode('utf-8')

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = self.translate_raw_response(raw_value)
        return [
            Reading(
                data_name=self.description,
                data_value=str(value),
                data_unit=self.unit,
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon,
            )
        ]

class ReadingDefinitionTemperature(ReadingDefinition):
    def __init__(self, index: int, name: str, description: str,  response_type: ResponseType, device_class: str = None, state_class: str = None, icon: str = None):
        #TODO: find a way to make the unit configurable
        super().__init__(index, name, response_type, description, device_class, state_class, icon, unit="°C")
        if response_type not in [ResponseType.INT, ResponseType.FLOAT]:
            raise TypeError(f"Temperature response must be of type int or float, ResponseType {response_type} is not valid")

    def translate_raw_response(self, raw_value) -> float:
        return float(raw_value.decode())

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = self.translate_raw_response(raw_value)
        return [
            Reading(
                data_name=self.description,
                data_value=str(value),
                data_unit=self.unit,
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon,
            )
        ]

    def get_description(self) -> str:
        return self.description

class ReadingDefinitionENFlags(ReadingDefinition):
    def __init__(
        self, index: int, description: str, enflags: dict[str, dict[str, str]], device_class: str = None, state_class: str = None, icon: str = None
    ):
        self.index = index
        self.description = description
        self.enflags = enflags  # what does enflags mean?
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon

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

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        values: dict[str, str] = self.translate_raw_response(raw_value)
        responses = []
        for name, value in values.items():
            responses.append(
                Reading(
                    data_name=name, data_value=value, data_unit="", device_class=self.device_class, state_class=self.state_class, icon=self.icon
                )
            )

        return responses

    def get_description(self) -> str:
        return self.description

class ReadingDefinitionFlags(ReadingDefinition):
    def __init__(self, index: int, description: str, flags: list[str], device_class: str = None, state_class: str = None, icon: str = None):
        self.index = index
        self.description = description
        self.flags = flags
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon

    def translate_raw_response(self, raw_value) -> dict[str, int]:
        return_value = {}
        for i, flag in enumerate(raw_value):
            if self.flags[i]:  # only append value if flag name is present
                return_value[self.flags[i]] = int(chr(flag))
        return return_value

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        values: dict[str, int] = self.translate_raw_response(raw_value)
        responses = []
        for name, value in values.items():
            responses.append(
                Reading(
                    data_name=name, data_value=value, data_unit="bool", device_class=self.device_class, state_class=self.state_class, icon=self.icon
                )
            )
        return responses

    def get_description(self) -> str:
        return self.description


