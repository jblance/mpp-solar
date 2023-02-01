import logging

# import json

# import re

# from .baseoutput import baseoutput
from ..helpers import get_kwargs  # , key_wanted, pad, getMaxLen
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
        formatter = config.get("format", "table")

        formatted_data = format_data(formatter=formatter, config=config, data=data)
        if formatted_data is None:
            print("Nothing returned from data formatting")
            return

        # dd = json.dumps(config, indent=2)

        # print("header")
        if isinstance(formatted_data, list):
            for line in formatted_data:
                print(line)
        else:
            print(formatted_data)
        # print(dd)
        # print(f"config {config}")
        # #
        # # print(f"kwargs {kwargs}")
        # print("-" * 80)
        # print(data)

        # # check if config supplied
        # config = get_kwargs(kwargs, "config")
        # if config is not None:
        #     log.debug(f"config: {config}")
        #     # get formatting info
        #     remove_spaces = config.get("remove_spaces", True)
        #     keep_case = config.get("keep_case", False)
        #     filter = config.get("filter", None)
        #     excl_filter = config.get("excl_filter", None)
        # else:
        #     # get formatting info
        #     remove_spaces = True
        #     keep_case = get_kwargs(kwargs, "keep_case")
        #     filter = get_kwargs(kwargs, "filter")
        #     excl_filter = get_kwargs(kwargs, "excl_filter")

        # if filter is not None:
        #     filter = re.compile(filter)
        # if excl_filter is not None:
        #     excl_filter = re.compile(excl_filter)

        # # remove raw response
        # if "raw_response" in data:
        #     data.pop("raw_response")

        # # build header
        # if "_command" in data:
        #     command = data.pop("_command")
        # else:
        #     command = "Unknown command"
        # if "_command_description" in data:
        #     description = data.pop("_command_description")
        # else:
        #     description = "No description found"

        # # build data to display
        # displayData = {}
        # for key in data:
        #     _values = data[key]
        #     # remove spaces
        #     if remove_spaces:
        #         key = key.replace(" ", "_")
        #     if not keep_case:
        #         # make lowercase
        #         key = key.lower()
        #     if key_wanted(key, filter, excl_filter):
        #         displayData[key] = _values
        # log.debug(f"displayData: {displayData}")

        # # print header
        # print(f"Command: {command} - {description}")
        # print("-" * 80)

        # # print data
        # maxP = getMaxLen(displayData)
        # if maxP < 9:
        #     maxP = 9
        # # maxV = getMaxLen(data.values())
        # print(f"{pad('Parameter', maxP+1)}{'Value':<15}\tUnit")
        # for key in displayData:
        #     value = displayData[key][0]
        #     unit = displayData[key][1]
        #     if len(displayData[key]) > 2 and displayData[key][2]:
        #         extra = displayData[key][2]
        #         print(f"{pad(key,maxP+1)}{value:<15}\t{unit:<4}\t{extra}")
        #     else:
        #         print(f"{pad(key,maxP+1)}{value:<15}\t{unit:<4}")
