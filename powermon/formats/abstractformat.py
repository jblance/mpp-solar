from abc import ABC, abstractmethod
import logging
from enum import StrEnum, auto

# from time import sleep
log = logging.getLogger("Formatter")

class FormatterType(StrEnum):
    HASS = auto()
    HTMLTABLE = auto()
    RAW = auto()
    SIMPLE = auto()
    TABLE = auto()

class AbstractFormat(ABC):

    def __init__(self, formatConfig):
        self.remove_spaces = formatConfig.get("remove_spaces", True)
        self.keep_case = formatConfig.get("keep_case", False)
        self.filter = formatConfig.get("filter", None)
        self.excl_filter = formatConfig.get("excl_filter", None)

   
    @abstractmethod
    def output(*args, **kwargs):
        pass