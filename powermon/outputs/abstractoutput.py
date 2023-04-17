from abc import ABC, abstractmethod
import logging
from powermon.outputs.screen import Screen
from powermon.outputs.mqtt import MQTT
from enum import StrEnum, auto


log = logging.getLogger("Output")

class OutputType(StrEnum):
    SCREEN = auto()
    MQTT = auto()

class AbstractOutput(ABC):
    def __init__(self, formatter):
        self.formatter = formatter

    def filter(self, data):
        pass
