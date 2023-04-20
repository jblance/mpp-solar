import logging

from mppsolar.helpers import get_kwargs
from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("screen")


class Screen(AbstractOutput):
    def __init__(self, outputConfig, formatter):
        super().__init__(formatter)
        self.formatter = formatter

    def output(self, data):
        log.info("Using output sender: screen")
        if data is None:
            return

        formatted_data = self.formatter.format(data)
        if formatted_data is None:
            print("Nothing returned from data formatting")
            return

        if isinstance(formatted_data, list):
            for line in formatted_data:
                print(line)
        else:
            print(formatted_data)
