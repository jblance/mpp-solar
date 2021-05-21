import json as js
import logging
import re

from .baseoutput import baseoutput
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("json")


class json(baseoutput):
    def __str__(self):
        return "outputs the results to standard out in json format"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def output(self, *args, **kwargs):
        log.info("Using output processor: json")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        keep_case = get_kwargs(kwargs, "keep_case")
        data.pop("raw_response", None)

        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        output = {}
        for key in data:
            value = data[key]
            if isinstance(value, list):
                value = data[key][0]
            # unit = data[key][1]
            # remove spaces
            key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                output[key] = value

        print(js.dumps(output))
