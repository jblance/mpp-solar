import logging
from enum import auto

from strenum import LowercaseStrEnum

from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("formats")


class FormatterType(LowercaseStrEnum):
    HASS = auto()
    HTMLTABLE = auto()
    RAW = auto()
    SIMPLE = auto()
    TABLE = auto()
    TOPICS = auto()


DEFAULT_FORMAT = FormatterType.SIMPLE


def getFormatfromConfig(formatConfig, device, topic) -> AbstractFormat:
    # Get values from config
    log.debug("getFormatfromConfig, formatConfig: %s, device: %s, topic: %s" % (formatConfig, device, topic))

    # formatConfig can be None, a str (eg 'simple') or a dict
    if formatConfig is None:
        formatType = DEFAULT_FORMAT
        formatConfig = {}
    elif isinstance(formatConfig, str):
        formatType = formatConfig
        formatConfig = {}
        formatConfig["type"] = formatType
    else:
        formatType = formatConfig.get("type")
    log.debug("getFormatfromConfig, formatType: %s" % (formatType))

    formatter = None
    match formatType:
        case FormatterType.HTMLTABLE:
            from powermon.formats.htmltable import htmltable
            formatter = htmltable(formatConfig)
        case FormatterType.HASS:
            from powermon.formats.hass import hass
            formatter = hass(formatConfig, device)
        case FormatterType.TOPICS:
            from powermon.formats.topics import Topics
            formatter = Topics(formatConfig, topic)
        case FormatterType.SIMPLE:
            from powermon.formats.simple import simple
            formatter = simple(formatConfig)
        case FormatterType.TABLE:
            from powermon.formats.table import table
            formatter = table(formatConfig)
        case FormatterType.RAW:
            from powermon.formats.raw import raw
            formatter = raw(formatConfig)
        case _:
            log.warning("No formatter found for: %s" % formatType)
            formatter = None

    return formatter
