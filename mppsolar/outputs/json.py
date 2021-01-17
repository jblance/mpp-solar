import json as js
import logging

from .baseoutput import baseoutput

log = logging.getLogger("MPP-Solar")


class json(baseoutput):
    def __str__(self):
        return "json - outputs the results to standard out in json format"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.json __init__ kwargs {kwargs}")

    def output(self, *args, **kwargs):
        log.info("Using output processor: json")
        log.debug(f"processor.json.output kwargs {kwargs}")
        data = self.get_kwargs(kwargs, "data")

        output = {}
        for key in data:
            value = data[key]
            if isinstance(value, list):
                value = data[key][0]
            # unit = data[key][1]
            output[key] = value

        print(js.dumps(output))
