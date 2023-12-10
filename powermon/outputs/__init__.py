""" outputs / __init__.py """
import logging
from enum import auto

from strenum import LowercaseStrEnum

from powermon.errors import ConfigError
from powermon.formats import DEFAULT_FORMAT, getFormatfromConfig

# Set-up logger
log = logging.getLogger("outputs")

DEFAULT_OUTPUT = "screen"


class OutputType(LowercaseStrEnum):
    SCREEN = auto()
    MQTT = auto()
    API_MQTT = auto()


def getOutputClass(output_type, formatter, output_config={}):
    output_class = None
    # Only import the required class
    log.debug("outputType %s", output_type)
    if output_type == OutputType.MQTT:
        from powermon.outputs.mqtt import MQTT
        output_class = MQTT.from_config(output_config)
        output_class.set_formatter(formatter)
    elif output_type == OutputType.API_MQTT:
        from powermon.outputs.api_mqtt import ApiMqtt
        output_class = ApiMqtt.from_config(output_config)
        output_class.set_formatter(formatter)
    else:
        from powermon.outputs.screen import Screen
        output_class = Screen.from_config(output_config)
        output_class.set_formatter(formatter)
    return output_class


def getOutputs(outputsConfig):
    # outputs can be None,
    # str (eg screen),
    # list (eg [{'type': 'screen', 'format': 'simple'}, {'type': 'screen', 'format': {'type': 'htmltable'}}])
    # dict (eg {'format': 'table'})
    # print("outputs %s, type: %s" % (outputs, type(outputs)))
    _outputs = []
    log.debug("processing outputsConfig: %s", outputsConfig)
    if outputsConfig is None:
        _outputs.append(parseOutputConfig({"type": "screen", "format": "simple"}))
    elif isinstance(outputsConfig, str):
        # eg 'screen'
        _outputs.append(parseOutputConfig(outputsConfig))
    elif isinstance(outputsConfig, list):
        # eg [{'type': 'screen', 'format': 'simple'}, {'type': 'screen', 'format': {'type': 'htmltable'}}]
        for outputConfig in outputsConfig:
            _outputs.append(parseOutputConfig(outputConfig))
    elif isinstance(outputsConfig, dict):
        # eg {'format': 'table'}
        _outputs.append(parseOutputConfig(outputsConfig))
    else:
        pass
    return _outputs


# TODO: clean up the multiple types of outputconfig, there should only be one type
def parseOutputConfig(outputConfig):
    log.debug("parseOutputConfig, config: %s", outputConfig)
    # outputConfig can be None, a str (eg 'screen') a dict (eg {'format': 'table'})
    if outputConfig is None:
        log.debug("got blank outputConfig")
        output_type = DEFAULT_OUTPUT
        format_config = DEFAULT_FORMAT
    elif isinstance(outputConfig, str):
        # eg 'screen'
        log.debug("got str type outputConfig: %s", outputConfig)
        output_type = outputConfig
        format_config = DEFAULT_FORMAT
    elif isinstance(outputConfig, dict):
        # eg {'format': 'table'}
        log.debug("got dict type outputConfig: %s", outputConfig)
        output_type = outputConfig.get("type", DEFAULT_OUTPUT)
        format_config = outputConfig.get("format", DEFAULT_FORMAT)
    else:
        # incorrect output config
        log.debug("got problematic (type: %s) outputConfig: %s", type(outputConfig), outputConfig)
        raise ConfigError(f"Problem in outputs init, type: '{type(outputConfig)}', config: '{outputConfig}'")


    _format = getFormatfromConfig(format_config)
    log.debug("got format: %s", (_format))
    _output = getOutputClass(output_type, formatter=_format)
    log.debug("got output: %s", _output)
    return _output
