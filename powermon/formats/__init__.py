from .abstractformat import FormatterType


def getFormatfromConfig(formatConfig, device, topic, tag):
    #Get values from config
    #Type is required
    formatType = formatConfig["type"]

    if formatType == FormatterType.HTMLTABLE:
        from .htmltable import htmltable
        formatter = htmltable(formatConfig)
    elif formatType == FormatterType.HASS:
        from .hass import hass
        formatter = hass(formatConfig, device)
    elif formatType == FormatterType.TOPICS:
        from .topics import Topics
        formatter = Topics(formatConfig, topic, tag)
    elif formatType == FormatterType.SIMPLE:
        from .simple import simple
        formatter = simple(formatConfig)

    return formatter