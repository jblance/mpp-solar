""" reading_definition.py """
import calendar  # pylint: disable=w0611 # needed for INFO type evaluating templates
import logging
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
    FLOAT = auto()
    STRING = auto()
    BYTES = auto()
    OPTION = auto()  # response identifies which option from a list is the info
    # BYTES = "bytes.decode"  # can't use auto() for this value
    ENABLE_DISABLE_FLAGS = auto()
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
    TIME_SECONDS = auto()
    MESSAGE = auto()
    FLAGS = auto()
    MULTI_ENABLE_DISABLE = auto()
    AMPERAGE = auto()
    TEMPERATURE = auto()
    PERCENTAGE = auto()
    FREQUENCY = auto()
    AMPS = auto()


class ReadingDefinition():
    """
    Default / base ReadingDefinition
    It doesn't contain the response value, just the definition of what is valid.
    """
    def __str__(self):
        return f"{self.index=}, {self.description=}, {self.response_type=}, {self.unit=}, instance={type(self)}"

    def __init__(self, index, response_type, description, device_class, state_class, icon, unit=""):
        # {"index": 13, "reading_type": ReadingType.WATTS, "response_type": ResponseType.INT,
        #  "description": "SCC charge power", "icon": "mdi:solar-power", "device-class": "power"}
        self.description = description
        self.response_type = response_type
        self.unit = unit
        self.index = index

        self.device_class = device_class
        self.state_class = state_class
        self.icon = icon

    @property
    def description(self) -> str:
        """ text description of this reading """
        return self._description

    @description.setter
    def description(self, value):
        """ set the description """
        # log.debug("Setting description to '%s'", value)
        self._description = value

    @property
    def response_type(self) -> ResponseType:
        """ response_type of this reading """
        return self._response_type

    @response_type.setter
    def response_type(self, value):
        # log.debug("Setting response_type to '%s'", value)
        self._response_type = value

    @property
    def options(self) -> dict:
        """ options dict for decoding """
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    def translate_raw_response(self, raw_value):
        """ interpret the raw response into a python basic type """
        log.debug("translate_raw_response: %s from type: %s", raw_value, self.response_type)
        match self.response_type:
            case ResponseType.INT:
                return int(raw_value.decode('utf-8'))
            case ResponseType.FLOAT:
                return float(raw_value.decode('utf-8'))
            case ResponseType.OPTION:
                if not isinstance(self.options, dict):
                    raise TypeError(f"For Reading Defininition {self.description}, options must be a dict if response_type is OPTION")
                value = str(raw_value.decode('utf-8'))
                return self.options[value]
            case _:
                return raw_value.decode('utf-8')

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        """ generate a reading object from a raw value """
        log.debug("raw_value: %s", raw_value)
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

    def get_invalid_message(self, raw_value) -> str:
        """ message for invalid state """
        return f"Invalid response for {self.description}: {raw_value}"

    def is_info(self) -> bool:
        """ is this reading definition an info definition """
        return False

    @classmethod
    def multiple_from_config(cls, reading_definitions_config: list[dict]) -> dict[int, "ReadingDefinition"]:
        """ build list of reading definitions from config """
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
        """ build a reading definition object from a config dict """
        index = i
        description = reading_definition_config.get("description")
        response_type = reading_definition_config.get("response_type")
        reading_type = reading_definition_config.get("reading_type")
        device_class = reading_definition_config.get("device-class", None)
        state_class = reading_definition_config.get("state-class", None)
        icon = reading_definition_config.get("icon", None)

        match reading_type:
            case ReadingType.ACK:
                reading = ReadingDefinitionACK(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.WATT_HOURS:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "Wh"
            case ReadingType.MESSAGE:
                reading = ReadingDefinitionMessage(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.TEMPERATURE:
                reading = ReadingDefinitionTemperature(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.MULTI_ENABLE_DISABLE:
                reading =  ReadingDefinitionENFlags(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.TIME_SECONDS:
                reading =  ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "s"
            case ReadingType.FLAGS:
                flags = reading_definition_config.get("flags")
                reading =  ReadingDefinitionFlags(
                    index=index, response_type=response_type, description=description, flags=flags,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.AMPERAGE:
                reading =  ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "A"
            case ReadingType.PERCENTAGE:
                reading =  ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "%"
            case ReadingType.FREQUENCY:
                reading =  ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "Hz"
            case ReadingType.WATTS:
                reading =  ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "W"
            case _:
                log.error("Reading description: %s has unknown reading_type definition type: %s", description, reading_type)
                raise ValueError(
                    f"Reading description: {description} has unknown reading_type definition type: {reading_type}"
                )
        # Use options dict to supply additional decode data
        # currently in use for ResponseType.OPTIONS and ENABLE_DISABLE_FLAGS
        options: dict[str, str] = reading_definition_config.get("options")
        if options is not None:
            reading.options = options
        return reading


class ReadingDefinitionNumeric(ReadingDefinition):
    """ A ReadingDefinition for readings that must be numeric """
    def __init__(self, index: int, response_type: str, description: str,
        device_class: str = None, state_class: str = None, icon: str = None):
        super().__init__(index, response_type, description, device_class, state_class, icon)
        if response_type not in [ResponseType.INT, ResponseType.FLOAT]:
            raise TypeError(f"{type(self)} response must be of type int or float, ResponseType {response_type} is not valid")

class ReadingDefinitionACK(ReadingDefinition):
    """ ReadingDefinition for ACK type readings """
    def __init__(self, index: int, response_type: str, description: str,
        device_class: str = None, state_class: str = None, icon: str = None, ):
        super().__init__(index, response_type, description, device_class, state_class, icon)

        self.fail_code = "NAK"
        self.fail_description = "Failed"
        self.success_code = "ACK"
        self.success_description = "Succeeded"

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        value = raw_value.decode()
        if value == self.success_code:
            return [
                Reading(data_name=self.description, data_value=self.success_description, data_unit=None,
                    device_class=self.device_class, state_class=self.state_class, icon=self.icon)
            ]
        elif value == self.fail_code:
            return [
                Reading(data_name=self.description, data_value=self.fail_description, data_unit=None,
                    device_class=self.device_class, state_class=self.state_class, icon=self.icon)
            ]


class ReadingDefinitionMessage(ReadingDefinition):
    """ ReadingDefinition for message (ie wordy) type readings """
    def __init__(self, index: int, response_type: str, description: str,
                device_class: str = None, state_class: str = None, icon: str = None):
        super().__init__(index, response_type, description, device_class, state_class, icon)


class ReadingDefinitionTemperature(ReadingDefinitionNumeric):
    """ ReadingDefinition for temperature readings - will include translation eg celcius to fahrenheit """
    def __init__(self, index: int, description: str, response_type: ResponseType,
                device_class: str = None, state_class: str = None, icon: str = None):
        # TODO: find a way to make the unit configurable
        super().__init__(index, response_type, description, device_class, state_class, icon)
        self.unit="°C"


class ReadingDefinitionENFlags(ReadingDefinition):
    """ ReadingDefinition for specific Enable/Disable flag (eg: EakxyDbjuvz) type readings """
    def __init__(self, index: int, description: str, response_type: ResponseType,
                device_class: str = None, state_class: str = None, icon: str = None):
        super().__init__(index, response_type, description, device_class, state_class, icon)

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
                _key = self.options.get(item, {}) or f"unknown_{i}"
                return_values[_key] = status
        return return_values

    def reading_from_raw_response(self, raw_value) -> list[Reading]:
        values: dict[str, str] = self.translate_raw_response(raw_value)
        responses = []
        for name, value in values.items():
            responses.append(
                Reading(data_name=name, data_value=value, data_unit="",
                    device_class=self.device_class, state_class=self.state_class, icon=self.icon)
            )

        return responses


class ReadingDefinitionFlags(ReadingDefinition):
    """ ReadingDefinition for flags (eg: 10100110) type readings """
    def __init__(self, index: int, description: str, response_type: ResponseType, flags: list[str],
                device_class: str = None, state_class: str = None, icon: str = None):
        super().__init__(index, response_type, description, device_class, state_class, icon)
        self.flags = flags

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
