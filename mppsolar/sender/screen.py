import logging

from ..helpers import get_kwargs
from .formats import format_data

log = logging.getLogger("screen")


class screen:
    def __str__(self):
        return "the screen sender just prints the results to standard out"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.screen __init__ args: {args}, kwargs: {kwargs}")

    def output(self, *args, **kwargs):
        log.info("Using output sender: screen")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        if data is None:
            return

        config = get_kwargs(kwargs, "config")
        fullconfig = get_kwargs(kwargs, "fullconfig")
        formatter = config.get("format", "table")

        formatted_data = format_data(formatter=formatter, config=config, data=data, fullconfig=fullconfig)
        if formatted_data is None:
            print("Nothing returned from data formatting")
            return

        if isinstance(formatted_data, list):
            for line in formatted_data:
                print(line)
        else:
            print(formatted_data)
