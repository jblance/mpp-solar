""" reading_definition.py """
import calendar  # pylint: disable=w0611 # needed for INFO type evaluating templates
import logging
from enum import auto
from struct import unpack

from strenum import LowercaseStrEnum

from powermon.commands.reading import Reading

log = logging.getLogger("ReadingDefinition")


class ResponseType(LowercaseStrEnum):
    """
    the type of the response
    - determines how to read and translate to useful info
    """
    ACK = auto()
    BOOL = auto()      # 0 is false, 1 is true
    INT = auto()
    HEX_CHAR = auto()
    FLOAT = auto()
    STRING = auto()
    BYTES = auto()
    LE_2B_S = auto()  # little endian 2 byte value (as string, eg 7800 = 0x0078 = 120)
    OPTION = auto()  # response identifies which option from a dict (called 'options') is the info
    LIST = auto()  # response identifies which option from a list (called 'options') is the info
    BIT_ENCODED = auto()
    ENABLE_DISABLE_FLAGS = auto()
    FLAGS = auto()
    INFO = auto()
    INFO_FROM_COMMAND = auto()  # process the supplied command using a template
    TEMPLATE_BYTES = auto()  # process the response value using a template
    TEMPLATE_INT = auto()  # process the response int value using a template


class ReadingType(LowercaseStrEnum):
    """
    the type of the reading
    - higher level type, like Wh etc
    - allows translations
    """
    ACK = auto()
    CURRENT = auto()
    APPARENT_POWER = auto()
    ENERGY = auto()
    WATTS = auto()
    WATT_HOURS = auto()
    KILOWATT_HOURS = auto()
    VOLTS = auto()
    DATE_TIME = auto()
    YEAR = auto()
    MONTH = auto()
    DAY = auto()
    TIME = auto()
    TIME_SECONDS = auto()
    TIME_MINUTES = auto()
    TIME_HOURS = auto()
    TIME_DAYS = auto()
    MESSAGE = auto()
    MESSAGE_AMPS = auto()
    FLAGS = auto()
    MULTI_ENABLE_DISABLE = auto()
    TEMPERATURE = auto()
    PERCENTAGE = auto()
    FREQUENCY = auto()
    HEX_STR = auto()


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

    @property
    def slice_array(self) -> str:
        """ slice array for decoding """
        return self._slice_array

    @slice_array.setter
    def slice_array(self, value):
        self._slice_array = value

    @property
    def default(self):
        """ default value for error situations """
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    @property
    def format_template(self):
        """ a template that allows re-formating of value """
        return self._format_template

    @format_template.setter
    def format_template(self, value):
        if value is not None:
            log.debug("format templater for '%s': %s", self.description, value)
        self._format_template = value

    def translate_raw_response(self, raw_value):
        """ interpret the raw response into a python basic type """
        log.debug("translate_raw_response: %s from type: %s", raw_value, self.response_type)
        match self.response_type:
            case ResponseType.BOOL:
                return bool(int(raw_value.decode('utf-8')))
            case ResponseType.HEX_CHAR:
                return raw_value[0]
                # return ord(raw_value.decode('utf-8')[0])
            case ResponseType.INT:
                try:
                    result = int(raw_value.decode('utf-8'))
                    return result
                except ValueError as e:
                    if self.default:
                        return self.default
                    raise ValueError(f"For Reading Defininition '{self.description}', expected an INT, got {raw_value}") from e
            case ResponseType.TEMPLATE_INT:
                try:
                    r = int(raw_value.decode('utf-8'))
                    if self.format_template:
                        r = eval(self.format_template)  # pylint: disable=W0123
                    return r
                except ValueError as e:
                    if self.default:
                        return self.default
                    raise ValueError(f"For Reading Defininition '{self.description}', expected an INT, got {raw_value}") from e
            case ResponseType.FLOAT:
                return float(raw_value.decode('utf-8'))
            case ResponseType.LE_2B_S:
                result = raw_value.decode('utf-8')
                result = unpack('<h', bytes.fromhex(result))[0]
                return result
            case ResponseType.BIT_ENCODED:
                if not isinstance(self.options, dict):
                    raise TypeError(f"For Reading Defininition '{self.description}', options must be a dict if response_type is BIT_ENCODED")
                value = int(raw_value.decode('utf-8'))
                if value == 0:
                    return self.options[0]
                # loop through options and check if applicable
                results = []
                for key in self.options.keys():
                    if value & key:
                        results.append(self.options[key])
                return ",".join(results)
            case ResponseType.OPTION:
                if not isinstance(self.options, dict):
                    raise TypeError(f"For Reading Defininition '{self.description}', options must be a dict if response_type is OPTION")
                value = str(raw_value.decode('utf-8'))
                try:
                    return self.options[value]
                except KeyError as e:
                    raise KeyError(f"For Reading Defininition '{self.description}', keys: {self.options.keys()}, requested key: {value}") from e
            case ResponseType.LIST:
                if not isinstance(self.options, list):
                    raise TypeError(f"For Reading Defininition '{self.description}', options must be a list if response_type is LIST")
                value = int(raw_value.decode('utf-8'))
                try:
                    return self.options[value]
                except IndexError as e:
                    raise IndexError(f"For Reading Defininition '{self.description}', len: {len(self.options)}, got index: {value}") from e
            case ResponseType.TEMPLATE_BYTES:
                r = raw_value.decode('utf-8')
                if self.format_template:
                    r = eval(self.format_template)  # pylint: disable=W0123
                return r
            case ResponseType.INFO_FROM_COMMAND:
                cn = raw_value
                if self.format_template:
                    # print(self.format_template)
                    res = eval(self.format_template)  # pylint: disable=W0123
                    return res
                return cn
            case _:
                return raw_value.decode('utf-8')

    def reading_from_raw_response(self, raw_value, override=None) -> list[Reading]:
        """ generate a reading object from a raw value """
        log.debug("raw_value: %s, override: %s", raw_value, override)
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
    def multiple_from_config(cls, reading_definition_configs: list[dict]) -> dict[int | str, "ReadingDefinition"]:
        """ build list of reading definitions from config """
        if reading_definition_configs is None:
            return {}
        else:
            reading_definitions: dict[int, "ReadingDefinition"] = {}
            for i, reading_definition_config in enumerate(reading_definition_configs):
                if "index" in reading_definition_config:
                    i = reading_definition_config.get("index")
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
        device_class = reading_definition_config.get("device_class", None)
        state_class = reading_definition_config.get("state_class", None)
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
            case ReadingType.KILOWATT_HOURS:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "kWh"
            case ReadingType.APPARENT_POWER:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "VA"
            case ReadingType.ENERGY:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "Ah"
            case ReadingType.MESSAGE:
                reading = ReadingDefinitionMessage(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.MESSAGE_AMPS:
                reading = ReadingDefinitionMessage(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "A"
            case ReadingType.TEMPERATURE:
                reading = ReadingDefinitionTemperature(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.MULTI_ENABLE_DISABLE:
                reading = ReadingDefinitionENFlags(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.DATE_TIME:
                reading = ReadingDefinitionMessage(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.YEAR:
                reading = ReadingDefinitionMessage(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.MONTH:
                reading = ReadingDefinitionMessage(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.DAY:
                reading = ReadingDefinitionMessage(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.TIME_SECONDS:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "sec"
            case ReadingType.TIME_MINUTES:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "min"
            case ReadingType.TIME_HOURS:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "hours"
            case ReadingType.TIME_DAYS:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "days"
            case ReadingType.FLAGS:
                flags = reading_definition_config.get("flags")
                reading = ReadingDefinitionFlags(
                    index=index, response_type=response_type, description=description, flags=flags,
                    device_class=device_class, state_class=state_class, icon=icon)
            case ReadingType.CURRENT:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "A"
            case ReadingType.VOLTS:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "V"
            case ReadingType.PERCENTAGE:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "%"
            case ReadingType.FREQUENCY:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "Hz"
            case ReadingType.WATTS:
                reading = ReadingDefinitionNumeric(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
                reading.unit = "W"
            case ReadingType.HEX_STR:
                reading = ReadingDefinitionHexStr(
                    index=index, response_type=response_type, description=description,
                    device_class=device_class, state_class=state_class, icon=icon)
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
        # check for a default setting
        reading.default = reading_definition_config.get("default")
        # check for a format template
        reading.format_template = reading_definition_config.get("format_template")
        # check for a slice value
        reading.slice_array = reading_definition_config.get("slice")
        return reading


class ReadingDefinitionNumeric(ReadingDefinition):
    """ A ReadingDefinition for readings that must be numeric """
    def __init__(self, index: int, response_type: str, description: str, device_class: str = None, state_class: str = None, icon: str = None):
        super().__init__(index, response_type, description, device_class, state_class, icon)
        if response_type not in [ResponseType.INT, ResponseType.TEMPLATE_INT, ResponseType.FLOAT, ResponseType.LE_2B_S, ResponseType.HEX_CHAR]:
            raise TypeError(f"{type(self)} response must be of type int or float, ResponseType {response_type} is not valid")


class ReadingDefinitionACK(ReadingDefinition):
    """ ReadingDefinition for ACK type readings """
    def __init__(self, index: int, response_type: str, description: str, device_class: str = None, state_class: str = None, icon: str = None, ):
        super().__init__(index, response_type, description, device_class, state_class, icon)

        self.fail_code = "NAK"
        self.fail_description = "Failed"
        self.success_code = "ACK"
        self.success_description = "Succeeded"

    def reading_from_raw_response(self, raw_value, override=None) -> list[Reading]:
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
    def __init__(self, index: int, response_type: str, description: str, device_class: str = None, state_class: str = None, icon: str = None):
        super().__init__(index, response_type, description, device_class, state_class, icon)


class ReadingDefinitionHexStr(ReadingDefinitionNumeric):
    """ ReadingDefinition for hex (displayed as a string) type readings """
    def reading_from_raw_response(self, raw_value, override=None) -> list[Reading]:
        """ generate a reading object from a raw value """
        log.debug("raw_value: %s, override: %s", raw_value, override)
        value = self.translate_raw_response(raw_value)
        value = hex(value)
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


class ReadingDefinitionTemperature(ReadingDefinitionNumeric):
    """ ReadingDefinition for temperature readings that are stored in celcius - can be overriden to translate to fahrenheit """
    def __init__(self, index: int, description: str, response_type: ResponseType, device_class: str = None, state_class: str = None, icon: str = None):
        super().__init__(index, response_type, description, device_class, state_class, icon)
        self.unit = "°C"

    def reading_from_raw_response(self, raw_value, override=None) -> list[Reading]:
        """ generate a reading object from a raw value """
        log.debug("raw_value: %s, override: %s", raw_value, override)
        value = self.translate_raw_response(raw_value)
        _unit = self.unit
        if override is not None and "temperature" in override:
            temp_override = override.get('temperature')
            if temp_override.startswith("F"):
                value = (1.8 * value) + 32
                _unit = "°F"
        return [
            Reading(
                data_name=self.description,
                data_value=value,
                data_unit=_unit,
                device_class=self.device_class,
                state_class=self.state_class,
                icon=self.icon,
            )
        ]


class ReadingDefinitionENFlags(ReadingDefinition):
    """ ReadingDefinition for specific Enable/Disable flag (eg: EakxyDbjuvz) type readings """
    def __init__(self, index: int, description: str, response_type: ResponseType, device_class: str = None, state_class: str = None, icon: str = None):
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

    def reading_from_raw_response(self, raw_value, override=None) -> list[Reading]:
        values: dict[str, str] = self.translate_raw_response(raw_value)
        responses = []
        for name, value in values.items():
            responses.append(
                Reading(data_name=name, data_value=value, data_unit="", device_class=self.device_class, state_class=self.state_class, icon=self.icon)
            )

        return responses


class ReadingDefinitionFlags(ReadingDefinition):
    """ ReadingDefinition for flags (eg: 10100110) type readings """
    def __init__(self, index: int, description: str, response_type: ResponseType, flags: list[str], device_class: str = None, state_class: str = None, icon: str = None):
        super().__init__(index, response_type, description, device_class, state_class, icon)
        self.flags = flags

    def translate_raw_response(self, raw_value) -> dict[str, int]:
        return_value = {}
        for i, flag in enumerate(raw_value):
            if self.flags[i]:  # only append value if flag name is present
                return_value[self.flags[i]] = int(chr(flag))
        return return_value

    def reading_from_raw_response(self, raw_value, override=None) -> list[Reading]:
        values: dict[str, int] = self.translate_raw_response(raw_value)
        responses = []
        for name, value in values.items():
            responses.append(
                Reading(
                    data_name=name, data_value=value, data_unit="bool", device_class=self.device_class, state_class=self.state_class, icon=self.icon
                )
            )
        return responses
