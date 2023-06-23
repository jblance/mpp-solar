import logging
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("simple")


class simple(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "simple"
        self.extra_info = formatConfig.get("extra_info", False)

    def format(self, result):
        log.info("Using output formatter: %s" % self.name)

        _result = []

        # check for error in result
        if result.error:
            data = {}
            data["Error"] = [f"Command: {result.command.name} incurred an error or errors during execution or processing", ""]
            data["Error Count"] = [len(result.error_messages), ""]
            for i, message in enumerate(result.error_messages):
                data[f"Error #{i}"] = [message, ""]
        else:
            data = result.decoded_responses

        if data is None:
            return _result

        log.debug(f"data: {data}")
        displayData = self.formatAndFilterData(data)
        log.debug(f"displayData: {displayData}")

        # build data to display
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            if len(displayData[key]) > 2 and displayData[key][2] and self.extra_info:
                extra = displayData[key][2]
                _result.append(f"{key}={value}{unit} {extra}")
            else:
                _result.append(f"{key}={value}{unit}")
        return _result
