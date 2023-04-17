from .htmltable import htmltable
from .hass import hass
from .abstractformat import FormatterType


def getFormatfromConfig(formatConfig, device):
    #Get values from config
    #Type is required
    formatType = formatConfig["type"]

    if formatType == FormatterType.HTMLTABLE:
        formatter = htmltable(formatConfig)
    elif formatType == FormatterType.HASS:
        formatter = hass(formatConfig, device)
    #elif formatType == FormatterType.SIMPLE:
        #formatter = simple(mqtt_broker, topic, tag)

    return formatter