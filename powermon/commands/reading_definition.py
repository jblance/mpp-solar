""" reading_definition.py """
import calendar  # needed for INFO type evaluating templates
from abc import ABC, abstractmethod
from enum import auto

from strenum import LowercaseStrEnum

from powermon.commands.reading import Reading


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
    STR_KEYED = auto()
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
    AMPS = auto()
    WATTS = auto()
    STRING = auto()
    TEMP = auto()
    OPTION = auto()
    BYTES = auto()
    FLOAT = auto()


class ReadingDefinition(ABC):
    """
    Create a flat representation to check if a response is valid for the command.
    It doesn't contain the response value, just the definition of what is valid.
    """
    def __str__(self):
        return f"{self.index=}, {self.name=}, {self.description=}, {self.response_type=}, {self.unit=}, instance={type(self)}"

    def __init__(self, index, name, response_type, unit, description, device_class, state_class, icon):
        self.index = index
        self.name = name
        self.response_type = response_type
        self.unit = unit
        self.description = description
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon

    def is_valid_response(self, value) -> bool:
        raise NotImplementedError


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
                print(reading_definition)
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
            case ReadingType.STRING:
                return ReadingDefinitionString(
                    index=index,
                    name=name,
                    response_type=response_type,
                    description=description,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )
            case ReadingType.OPTION:
                options: list[str] = reading_definition_config.get("options")
                return ReadingDefinitionOption(
                    index=index,
                    description=description,
                    options=options,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )
            case ReadingType.BYTES:
                unit = reading_definition_config[3]
                return ReadingDefinitionBytes(
                    index=index,
                    description=description,
                    unit=unit,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )
            case ReadingType.FLOAT:
                unit = reading_definition_config[3]
                return ReadingDefinitionFloat(
                    index=index,
                    description=description,
                    unit=unit,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )

            case ReadingType.STR_KEYED:
                options: dict[str, str] = reading_definition_config[3]
                return ReadingDefinitionStrKeyed(
                    index=index,
                    description=description,
                    options=options,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )

            case ReadingType.ENFLAGS:
                flags: dict[str, dict[str, str]] = reading_definition_config[3]
                return ReadingDefinitionENFlags(
                    index=index,
                    description=description,
                    enflags=flags,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )

            case ReadingType.FLAGS:
                flags: list[str] = reading_definition_config[3]
                return ReadingDefinitionFlags(
                    index=index,
                    description=description,
                    flags=flags,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )

            case ResponseType.INFO:
                template = reading_type.split(":", 1)[1]
                return ReadingDefinitionInfo(
                    index=index,
                    description=description,
                    template=template,
                    device_class=device_class,
                    state_class=state_class,
                    icon=icon,
                )

            case _:
                raise ValueError(
                    f"Reading description: {description} has unknown reading_type definition type: {reading_type}"
                )


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
        super().__init__(index, name, response_type, "", description, device_class, state_class, icon)
 
        self.fail_code = "NAK"
        self.fail_description = "Failed"
        self.success_code = "ACK"
        self.success_description = "Successful"

    def is_valid_response(self, value) -> bool:
        return value == self.success_code or value == self.fail_code

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
        super().__init__(index, name, response_type, "Wh", description, device_class, state_class, icon)
        
    def is_valid_response(self, value) -> bool:
        # Do we need to check if it's negative? Should we have max and min bounds?
        return isinstance(value, int)

    def translate_raw_response(self, raw_value) -> str:
        return int(raw_value.decode())

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

class ReadingDefinitionString(ReadingDefinition):
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
        super().__init__(index, name, response_type, "", description, device_class, state_class, icon)
        
    def is_valid_response(self, value) -> bool:
        return True

    def translate_raw_response(self, raw_value) -> str:
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

class ReadingDefinitionInt(ReadingDefinition):
    def __init__(self, index: int, description: str, unit: str, device_class: str = None, state_class: str = None, icon: str = None):
        self.index = index
        self.description = description
        self.unit = unit
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon

    def is_valid_response(self, value) -> bool:
        # Do we need to check if it's negative? Should we have max and min bounds?
        return isinstance(value, int)

    def translate_raw_response(self, raw_value) -> str:
        return int(raw_value.decode())

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

class ReadingDefinitionOption(ReadingDefinition):
    def __init__(self, index: int, description: str, options: list[str], device_class: str = None, state_class: str = None, icon: str = None):
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

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = self.translate_raw_response(raw_value)
        return [
            Reading(
                data_name=self.description,
                data_value=value,
                data_unit="",
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon,
            )
        ]

    def get_description(self) -> str:
        return self.description

class ReadingDefinitionBytes(ReadingDefinition):
    # Seems to be a catch-all for responses that are not properly implemented
    def __init__(self, index: int, description: str, unit: str, device_class: str = None, state_class: str = None, icon: str = None):
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

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = self.translate_raw_response(raw_value)
        return [
            Reading(
                data_name=self.description,
                data_value=value,
                data_unit="",
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon,
            )
        ]

    def get_description(self) -> str:
        return self.description

class ReadingDefinitionFloat(ReadingDefinition):
    def __init__(self, index: int, description: str, unit: str, device_class: str = None, state_class: str = None, icon: str = None):
        self.index = index
        self.description = description
        self.unit = unit
        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon

    def is_valid_response(self, value) -> bool:
        # Do we need to check if it's negative? Should we have max and min bounds?
        return isinstance(value, float)

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

class ReadingDefinitionStrKeyed(ReadingDefinition):
    def __init__(self, index: int, description: str, options: dict[str, str], device_class: str = None, state_class: str = None, icon: str = None):
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

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = self.translate_raw_response(raw_value)
        return [
            Reading(
                data_name=self.description,
                data_value=value,
                data_unit="",
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

    def is_valid_response(self, value) -> bool:
        return value in self.flags

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

class ReadingDefinitionInfo(ReadingDefinition):
    def __init__(self, index: int, description: str, template: str, device_class: str = None, state_class: str = None, icon: str = None):
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

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = self.translate_raw_response(raw_value)
        return [
            Reading(
                data_name=self.description,
                data_value=value,
                data_unit="",
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon,
            )
        ]

    def get_description(self) -> str:
        return self.description
