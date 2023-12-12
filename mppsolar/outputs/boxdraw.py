import logging
import re

from .baseoutput import baseoutput
from ..helpers import get_kwargs, key_wanted, pad, get_max_response_length

log = logging.getLogger("boxdraw")


class boxdraw(baseoutput):
    def __str__(self):
        return "outputs the results to standard out in a table formatted with line art boxes"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.boxdraw __init__ kwargs {kwargs}")

    def printHeader(command, description):
        pass

    def output(self, *args, **kwargs):
        log.info("Using output processor: boxdraw")
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
            if key_wanted(key, filter, excl_filter):
                displayData[key] = _values
        log.debug(f"displayData: {displayData}")

        # Determine column widths
        _pad = 1
        # Width of parameter column
        width_p = get_max_response_length(displayData) + _pad
        if width_p < 9 + _pad:
            width_p = 9 + _pad
        # Width of value column
        width_v = get_max_response_length(data.values()) + _pad
        if width_v < 6 + _pad:
            width_v = 6 + _pad
        # Width of units column
        width_u = get_max_response_length(data.values(), 1) + _pad
        if width_u < 5 + _pad:
            width_u = 5 + _pad
        # Total line length
        line_length = width_p + width_v + width_u + 7
        # Check if command / description line is longer and extend line if needed
        cmd_str = f" Command: {command} - {description}"
        if line_length < (len(cmd_str) + 7):
            line_length = len(cmd_str) + 7
        # Check if columns too short and expand units if needed
        if (width_p + width_v + width_u + 7) < line_length:
            width_u = line_length - (width_p + width_u + 7) - 1

        # print header
        print("\u2554" + ("\u2550" * (line_length - 2)) + "\u2557")
        print(f"\u2551{cmd_str}" + (" " * (line_length - len(cmd_str) - 2)) + "\u2551")

        # print separator
        print("\u2560" + ("\u2550" * (width_p + 1)) + "\u2564" + ("\u2550" * (width_v + 1)) + "\u2564" + ("\u2550" * (width_u + 1)) + "\u2563")
        # print column headings
        print(f"\u2551 {pad('Parameter', width_p)}\u2502 {pad('Value', width_v)}\u2502 {pad('Unit', width_u)}\u2551")
        # print separator
        print("\u255f" + ("\u2500" * (width_p + 1)) + "\u253c" + ("\u2500" * (width_v + 1)) + "\u253c" + ("\u2500" * (width_u + 1)) + "\u2562")

        # print data
        for key, values in displayData.items():
            value = values[0]
            unit = values[1]
            print(f"\u2551 {pad(key, width_p)}\u2502 {pad(value, width_v)}\u2502 {pad(unit, width_u)}\u2551")

        # print footer
        print("\u255a" + ("\u2550" * (width_p + 1)) + "\u2567" + ("\u2550" * (width_v + 1)) + "\u2567" + ("\u2550" * (width_u + 1)) + "\u255d")
        print("\n")
