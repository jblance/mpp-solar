""" outputformats / __init__.py """
import logging
from enum import auto

from strenum import LowercaseStrEnum

from powermon.outputformats.abstractformat import AbstractFormat

log = logging.getLogger("formats")


class FormatterType(LowercaseStrEnum):
    """ enumeration of valid formatter types """
    HASS = auto()
    HTMLTABLE = auto()
    JSON = auto()
    RAW = auto()
    SIMPLE = auto()
    TABLE = auto()
    TOPICS = auto()


DEFAULT_FORMAT = FormatterType.SIMPLE


def from_config(format_config) -> AbstractFormat:
    """ use a config dict to build and return a format class """
    # Get values from config
    log.debug("Format from_config, format_config: %s", format_config)

    # formatConfig can be None, a str (eg 'simple') or a dict
    if format_config is None:
        format_type = FormatterType.SIMPLE
        format_config = {}
    elif isinstance(format_config, str):
        format_type = format_config
        format_config = {}
        format_config["type"] = format_type
    else:
        format_type = format_config.get("type")
    log.debug("getFormatfromConfig, formatType: %s", format_type)

    match format_type:
        case FormatterType.HTMLTABLE:
            from powermon.outputformats.htmltable import HtmlTable as fmt
        case FormatterType.HASS:
            from powermon.outputformats.hass import Hass as fmt
        case FormatterType.JSON:
            from powermon.outputformats.json_fmt import Json as fmt
        # case FormatterType.TOPICS:
        #     from powermon.outputformats.topics import Topics as fmt
        case FormatterType.SIMPLE:
            from powermon.outputformats.simple import SimpleFormat as fmt
        case FormatterType.TABLE:
            from powermon.outputformats.table import Table as fmt
        case FormatterType.RAW:
            from powermon.outputformats.raw import raw as fmt
        case _:
            log.warning("No formatter found for: %s", format_type)
            return None
    return fmt(format_config)
