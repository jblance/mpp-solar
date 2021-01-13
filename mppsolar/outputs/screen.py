import logging

from .baseoutput import BaseOutput

log = logging.getLogger("MPP-Solar")


class screen(BaseOutput):
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.screen __init__ kwargs {kwargs}")

    def output(self, *args, **kwargs):
        log.info("Using output processor: screen")
        log.debug(f"processor.screen.output kwargs {kwargs}")
        data = self.get_kwargs(kwargs, "data")
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

        print(f"{'Parameter':<30}\t{'Value':<15} Unit")
        for key in data:
            value = data[key][0]
            unit = data[key][1]
            print(f"{key:<30}\t{value:<15}\t{unit:<4}")
