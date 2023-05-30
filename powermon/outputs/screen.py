import logging

from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("screen")


class Screen(AbstractOutput):
    def __init__(self, outputConfig, formatter):
        log.debug("outputConfig: %s, formatter: %s" % (outputConfig, formatter))
        super().__init__(formatter)
        self.name = "Screen"
        # self.formatter = formatter

    def process(self, result):
        log.info("Using output sender: screen")
        log.debug("formatter: %s" % self.formatter)

        # check for error in result and display error if exists
        if result.error:
            print(f"Command: {result.command.name} incurred an error or errors during execution or processing")
            print(f"Error message count: {len(result.error_messages)}")
            for message in result.error_messages:
                print(f"{message}")
            return

        formatted_data = self.formatter.format(result)
        if formatted_data is None:
            print("Nothing returned from data formatting")
            return

        for line in formatted_data:
            print(line)
