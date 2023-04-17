import logging

from mppsolar.helpers import get_kwargs


log = logging.getLogger("screen")


class Screen:
    def __init__(self, formatter):
        self.formatter = formatter

    def __str__(self):
        return "the screen transport just prints the results to standard out"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"transport.screen __init__ args: {args}, kwargs: {kwargs}")

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
