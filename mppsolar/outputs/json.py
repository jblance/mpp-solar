import json as js
import logging
import re

from ..helpers import get_kwargs
from . import to_json
from .baseoutput import baseoutput

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

        output = to_json(data, keep_case, excl_filter, filter)
        print(js.dumps(output))
