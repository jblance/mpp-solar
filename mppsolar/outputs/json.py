import logging

from .baseoutput import BaseOutput

log = logging.getLogger("MPP-Solar")


class json(BaseOutput):
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.json __init__ kwargs {kwargs}")

    def output(self, *args, **kwargs):
        log.info("Using output processor: json")
        log.debug(f"processor.json.output kwargs {kwargs}")
        output = {}
        data = self.get_kwargs(kwargs, "data")
        for key in data:
            value = data[key]
            if isinstance(value, list):
                value = data[key][0]
            # unit = data[key][1]
            output[key] = value
        print(output)
