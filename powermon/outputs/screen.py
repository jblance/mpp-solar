import logging
from powermon.formats.abstractformat import AbstractFormat

from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("screen")


class Screen(AbstractOutput):
    def __init__(self, formatter):
        self.name = "Screen"
        self.set_formatter(formatter)
        

    def set_formatter(self, formatter: AbstractFormat):
        self.formatter = formatter

    def process(self, result):
        log.info("Using output sender: screen")
        log.debug("formatter: %s" % self.formatter)

        formatted_data = self.formatter.format(result)
        if formatted_data is None:
            print("Nothing returned from data formatting")
            return

        for line in formatted_data:
            print(line)
