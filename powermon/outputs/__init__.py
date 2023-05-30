import logging
from enum import auto

from strenum import LowercaseStrEnum

from powermon.formats import getFormatfromConfig, DEFAULT_FORMAT

# Set-up logger
log = logging.getLogger("outputs")

DEFAULT_OUTPUT = "screen"


class OutputType(LowercaseStrEnum):
    SCREEN = auto()
    MQTT = auto()
    API_MQTT = auto()


def getOutputClass(outputType, _format, outputConfig=None, mqtt_broker=None, topic=None, schedule_name=None):
    output_class = None
    # Only import the required class
    log.debug("outputType %s" % outputType)
    if outputType == OutputType.MQTT:
        from powermon.outputs.mqtt import MQTT

        output_class = MQTT(outputConfig, topic, mqtt_broker, _format)
    elif outputType == OutputType.API_MQTT:
        from powermon.outputs.api_mqtt import API_MQTT

        output_class = API_MQTT(outputConfig, topic, schedule_name, mqtt_broker, _format)
    else:
        from powermon.outputs.screen import Screen

        output_class = Screen(outputConfig, _format)
    return output_class


def getOutputs(outputsConfig, topic=None, schedule_name=None, device=None, mqtt_broker=None):
    # outputs can be None,
    # str (eg screen),
    # list (eg [{'type': 'screen', 'format': 'simple'}, {'type': 'screen', 'format': {'type': 'htmltable'}}])
    # dict (eg {'format': 'table'})
    # print("outputs %s, type: %s" % (outputs, type(outputs)))
    _outputs = []
    log.debug("processing outputsConfig: %s" % outputsConfig)
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


def parseOutputConfig(outputConfig, topic=None, schedule_name=None, device=None, mqtt_broker=None):
    log.debug("parseOutputConfig, config: %s, topic: %s" % (outputConfig, topic))
    topic_override = None
    # outputConfig can be None, a str (eg 'screen') a dict (eg {'format': 'table'}) or a list (eg [{'type': 'screen', 'format': 'simple'}])
    if outputConfig is None:
        log.debug("got blank outputConfig")
        outputType = DEFAULT_OUTPUT
        _format = getFormatfromConfig(DEFAULT_FORMAT, device, topic)
        log.debug("got format: %s" % (_format))
        _output = getOutputClass(outputType, _format)
        log.debug("got output: %s" % (_output))
        return _output
    elif isinstance(outputConfig, str):
        # eg 'screen'
        log.debug("got str type outputConfig: %s" % (outputConfig))
        outputType = outputConfig
        _format = getFormatfromConfig(DEFAULT_FORMAT, device, topic)
        log.debug("got format: %s" % (_format))
        _output = getOutputClass(outputType, _format)
        log.debug("got output: %s" % (_output))
        return _output
    elif isinstance(outputConfig, dict):
        # eg {'format': 'table'}
        log.debug("got dict type outputConfig: %s" % (outputConfig))
        outputType = outputConfig.get("type", DEFAULT_OUTPUT)
        formatConfig = outputConfig.get("format", DEFAULT_FORMAT)
        topic_override = outputConfig.get("topic_override")
        # use topic override from the config
        if topic_override is not None:
            topic = topic_override
        _format = getFormatfromConfig(formatConfig, device, topic)
        log.debug("got format: %s" % (_format))
        _output = getOutputClass(outputType, _format)
        log.debug("got output: %s" % (_output))
        return _output
    elif isinstance(outputConfig, list):
        # eg [{'type': 'screen', 'format': 'simple'}], possibly multiple outputs
        # loop through outputs
        log.debug("got list type outputConfig: %s" % (outputConfig))
        raise Exception("Problem in outputs init - list type for outputConfig")

        # for item in outputConfig:
        #     _out = parseOutputConfig(item, topic, schedule_name, device, mqtt_broker)
        #     if _out is not None:
        #         outputs.append(_out)
        # return outputs
    else:
        # miss configured output?
        log.warn("outputConfig (%s) doesnt match expectations, defaulting" % outputConfig)
        outputType = DEFAULT_OUTPUT
        formatConfig = DEFAULT_FORMAT

    _format = getFormatfromConfig(formatConfig, device, topic)
    log.debug("got format: %s" % (_format))
