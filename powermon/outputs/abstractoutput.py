from abc import ABC, abstractmethod
import logging
from enum import auto
from strenum import LowercaseStrEnum


log = logging.getLogger("Output")


class OutputType(LowercaseStrEnum):
    SCREEN = auto()
    MQTT = auto()
    API_MQTT = auto()


class AbstractOutput(ABC):
    def __init__(self, formatter):
        self.formatter = formatter

    @abstractmethod
    def output(self, data):
        pass
