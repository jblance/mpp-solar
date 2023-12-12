""" formats / __init__.py """
import logging
from enum import auto

from strenum import LowercaseStrEnum

from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("formats")


class FormatterType(LowercaseStrEnum):
    """ enumeration of valid formatter types """
    HASS = auto()
    HTMLTABLE = auto()
    RAW = auto()
    SIMPLE = auto()
    JSON = auto()
    TABLE = auto()
    TOPICS = auto()


DEFAULT_FORMAT = FormatterType.SIMPLE


def getFormatfromConfig(formatConfig) -> AbstractFormat:
    # Get values from config
    log.debug("getFormatfromConfig, formatConfig: %s", formatConfig)

    # formatConfig can be None, a str (eg 'simple') or a dict
    if formatConfig is None:
        formatType = FormatterType.SIMPLE
        formatConfig = {}
    elif isinstance(formatConfig, str):
        formatType = formatConfig
        formatConfig = {}
        formatConfig["type"] = formatType
    else:
        formatType = formatConfig.get("type")
    log.debug("getFormatfromConfig, formatType: %s", formatType)

    formatter = None
    # TODO: should we replace this config processing with from_config methods on each type to remain consistent?
    match formatType:
        case FormatterType.HTMLTABLE:
            from powermon.formats.htmltable import htmltable
            formatter = htmltable(formatConfig)
        case FormatterType.HASS:
            from powermon.formats.hass import Hass
            formatter = Hass(formatConfig)
        # case FormatterType.TOPICS:
        #     from powermon.formats.topics import Topics
        #     formatter = Topics(formatConfig)
        case FormatterType.SIMPLE:
            from powermon.formats.simple import SimpleFormat
            formatter = SimpleFormat(formatConfig)
        case FormatterType.TABLE:
            from powermon.formats.table import Table
            formatter = Table(formatConfig)
        case FormatterType.RAW:
            from powermon.formats.raw import raw
            formatter = raw(formatConfig)
        case _:
            log.warning("No formatter found for: %s", formatType)
            formatter = None

    return formatter
