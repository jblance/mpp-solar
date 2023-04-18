from .mqtt import MQTT
from .screen import Screen
from powermon.formats.abstractformat import AbstractFormat, FormatterType
from powermon.formats import getFormatfromConfig
from .abstractoutput import OutputType



def getOutputFromConfig(outputConfig, device, mqtt_broker):
    outputType = outputConfig["type"]

    formatConfig = outputConfig["format"]
    format = getFormatfromConfig(formatConfig, device)

    output_class = None
    if outputType == OutputType.SCREEN:
        output_class = Screen(outputConfig, format)
    elif outputType == OutputType.MQTT:
        output_class = MQTT(outputConfig, mqtt_broker, format)
        

    return output_class