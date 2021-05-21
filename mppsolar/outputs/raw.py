import logging

from .baseoutput import baseoutput
from ..helpers import get_kwargs

log = logging.getLogger("raw")


class raw(baseoutput):
    def __str__(self):
        return "outputs the raw results to standard out"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def output(self, *args, **kwargs):
        log.info("Using output processor: raw")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        if data is None:
            return
        _desc = "No description found"
        if "_command_description" in data:
            _desc = data["_command_description"]
            del data["_command_description"]
        if "_command" in data:
            print(f"Command: {data['_command']} - {_desc}")
            print("-" * 60)
            del data["_command"]
        if "raw_response" in data:
            key = "raw_response"
            value = data[key][0]
            print(f"{key:<30}\t{value!a:<15}")
        return
