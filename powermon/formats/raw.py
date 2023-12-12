import logging
from powermon.formats.abstractformat import AbstractFormat
from powermon.commands.result import Result

log = logging.getLogger("raw")


class raw(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "raw"
        self.extra_info = formatConfig.get("extra_info", False)
        
    # def set_command_description(self, command_description):
    #     pass

    def format(self, result: Result, device_info):
        log.info("Using output formatter: %s", self.name)

        data = result.raw_response
        log.debug(f"data: {data}")
        return [data]
