""" mppsolar / outputs / screen.py """
import logging
import re

from .baseoutput import baseoutput
from ..helpers import get_kwargs, key_wanted, pad, get_max_response_length

log = logging.getLogger("screen")


class screen(baseoutput):
    """ the default output model, outputs to standard out in a table format """
    def __str__(self):
        return "[the default output module] outputs the results to standard out in a slightly formatted way"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.screen __init__ args: {args}, kwargs: {kwargs}")

    def printHeader(self, command, description):
        pass

    def output(self, *args, **kwargs):
        log.info("Using output processor: screen")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        if data is None:
            return

        # check if config supplied
        config = get_kwargs(kwargs, "config")
        if config is not None:
            log.debug(f"config: {config}")
            # get formatting info
            remove_spaces = config.get("remove_spaces", True)
            keep_case = config.get("keep_case", False)
            _filter = config.get("filter", None)
            excl_filter = config.get("excl_filter", None)
        else:
            # get formatting info
            remove_spaces = True
            keep_case = get_kwargs(kwargs, "keep_case")
            _filter = get_kwargs(kwargs, "filter")
            excl_filter = get_kwargs(kwargs, "excl_filter")

        if _filter is not None:
            _filter = re.compile(_filter)
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        # remove raw response
        data.pop("raw_response", None)

        # build header
        command = data.pop("_command", "Unknown command")
        description = data.pop("_command_description", "No description found")

        # build data to display
        displayData = {}
        for key, _values in data.items():
            # remove spaces
            if remove_spaces:
                key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, _filter, excl_filter):
                displayData[key] = _values
        log.debug(f"displayData: {displayData}")

        # print header
        print(f"Command: {command} - {description}")
        print("-" * 80)

        # print data
        maxP = get_max_response_length(displayData)
        if maxP < 9:
            maxP = 9
        # maxV = getMaxLen(data.values())
        print(f"{pad('Parameter', maxP+1)}{'Value':<15}Unit")
        for key, values in displayData.items():
            try:
                value = values[0]
                unit = values[1]
                if len(values) > 2 and values[2]:
                    extra = values[2]
                    print(f"{pad(key,maxP+1)}{value:<15}{unit:<6}{extra}")
                else:
                    print(f"{pad(key,maxP+1)}{value:<15}{unit}")
            except TypeError:
                log.info("unable to format for %s, %s, %s", key, value, unit)

        # print footer
        print("-" * 80)
        print("\n")
