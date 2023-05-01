from abc import ABC, abstractmethod
import logging
from enum import StrEnum, auto


log = logging.getLogger("Output")

class OutputType(StrEnum):
    SCREEN = auto()
    MQTT = auto()
    API_MQTT = auto()

class AbstractOutput(ABC):


    def __init__(self, formatter):
        self.formatter = formatter


    @abstractmethod
    def output(self, data):
        pass

    
