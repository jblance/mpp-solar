import logging
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("raw")


class raw(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "raw"
        self.extra_info = formatConfig.get("extra_info", False)

    def format(self, result):
        log.info("Using output formatter: %s" % self.name)

        data = result.raw_response
        log.debug(f"data: {data}")
        return [data]
