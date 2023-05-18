import logging
from enum import auto

from strenum import LowercaseStrEnum

from powermon.formats.abstractformat import AbstractFormat
from powermon.device import Device

log = logging.getLogger("formats")

DEFAULT_FORMAT = "simple"


class FormatterType(LowercaseStrEnum):
    HASS = auto()
    HTMLTABLE = auto()
    RAW = auto()
    SIMPLE = auto()
    TABLE = auto()
    TOPICS = auto()


def getFormatfromConfig(formatConfig: dict, device: Device, topic: str) -> AbstractFormat:
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
    if formatType == FormatterType.HTMLTABLE:
        from powermon.formats.htmltable import htmltable

        formatter = htmltable(formatConfig)
    elif formatType == FormatterType.HASS:
        from powermon.formats.hass import hass

        formatter = hass(formatConfig, device)
    elif formatType == FormatterType.TOPICS:
        from powermon.formats.topics import Topics

        formatter = Topics(formatConfig, topic)
    elif formatType == FormatterType.SIMPLE:
        from powermon.formats.simple import simple

        formatter = simple(formatConfig)
    elif formatType == FormatterType.TABLE:
        from powermon.formats.table import table

        formatter = table(formatConfig)

    else:
        log.warning("No formatter found for: %s" % formatType)
        formatter = None

    return formatter
