import logging
import re

from .baseoutput import baseoutput
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("screen")


class screen(baseoutput):
    def __str__(self):
        return "[the default output module] outputs the results to standard out in a slightly formatted way"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.screen __init__ kwargs {kwargs}")

    def output(self, *args, **kwargs):
        log.info("Using output processor: screen")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        if data is None:
            return

        keep_case = get_kwargs(kwargs, "keep_case")
        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        _desc = "No description found"
        if "_command_description" in data:
            _desc = data["_command_description"]
            del data["_command_description"]
        if "_command" in data:
            print(f"Command: {data['_command']} - {_desc}")
            print("-" * 60)
            del data["_command"]
        if "raw_response" in data:
            del data["raw_response"]

        print(f"{'Parameter':<30}\t{'Value':<15} Unit")
        for key in data:
            value = data[key][0]
            unit = data[key][1]
            # remove spaces
            key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                try:
                    print(f"{key:<30}\t{value:<15}\t{unit:<4}")
                except TypeError:
                    print(key, value, unit)
