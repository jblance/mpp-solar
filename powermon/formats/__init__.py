from .htmltable import htmltable
from .hass import hass
from .topics import Topics
from .simple import simple
from .abstractformat import FormatterType


def getFormatfromConfig(formatConfig, device):
    #Get values from config
    #Type is required
    formatType = formatConfig["type"]

    if formatType == FormatterType.HTMLTABLE:
        formatter = htmltable(formatConfig)
    elif formatType == FormatterType.HASS:
        formatter = hass(formatConfig, device)
    elif formatType == FormatterType.TOPICS:
        formatter = Topics(formatConfig)
    elif formatType == FormatterType.SIMPLE:
        formatter = simple(formatConfig)

    return formatter