from abc import ABC, abstractmethod
import logging


log = logging.getLogger("Output")


class AbstractOutput(ABC):
    def __str__(self):
        return f"Output: {self.name}, {self.formatter}"

    def __init__(self, formatter):
        self.name = "AbstractOutput"
        self.formatter = formatter

    @abstractmethod
    def process(self, result):
        pass
