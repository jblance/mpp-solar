import logging

from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("screen")


class Screen(AbstractOutput):
    def __init__(self, outputConfig, formatter):
        log.debug("outputConfig: %s, formatter: %s" % (outputConfig, formatter))
        super().__init__(formatter)
        self.name = "Screen"
        # self.formatter = formatter

    def output(self, data):
        log.info("Using output sender: screen")
        log.debug("formatter: %s" % self.formatter)
        if data is None:
            print("No data supplied")
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
