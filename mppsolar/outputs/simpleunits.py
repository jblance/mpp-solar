import logging
import re

from .baseoutput import baseoutput
from ..helpers import get_kwargs, key_wanted

log = logging.getLogger("simpleunits")


class simpleunits(baseoutput):
    def __str__(self):
        return "outputs 'param=value(unit)' only to standard out"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.value __init__ kwargs {kwargs}")

    def printHeader(command, description):
        pass

    def output(self, *args, **kwargs):
        log.info("Using output processor: value")
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
            filter = config.get("filter", None)
            excl_filter = config.get("excl_filter", None)
        else:
            # get formatting info
            remove_spaces = True
            keep_case = get_kwargs(kwargs, "keep_case")
            filter = get_kwargs(kwargs, "filter")
            excl_filter = get_kwargs(kwargs, "excl_filter")

        if filter is not None:
            filter = re.compile(filter)
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        # remove raw response
        if "raw_response" in data:
            data.pop("raw_response")

        # build header
        if "_command" in data:
            data.pop("_command")

        if "_command_description" in data:
            data.pop("_command_description")

        # build data to display
        displayData = {}
        for key in data:
            _values = data[key]
            # remove spaces
            if remove_spaces:
                key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                displayData[key] = _values
        log.debug(f"displayData: {displayData}")

        # print data
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            if unit:
                print(f"{key}={value}({unit})")
            else:
                print(f"{key}={value}")
