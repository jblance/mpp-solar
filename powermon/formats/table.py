import logging
from mppsolar.helpers import getMaxLen, pad
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("table")


class table(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.extra_info = formatConfig.get("extra_info", False)

    def format(self, data):
        log.info("Using output formatter: table")

        _result = []
        if data is None:
            return _result

        if "_command" in data:
            command = data.pop("_command")
        else:
            command = "Unknown command"
        if "_command_description" in data:
            description = data.pop("_command_description")
        else:
            description = "No description found"

        displayData = self.formatAndFilterData(data)
        log.debug(f"displayData: {displayData}")

        # build data to display

        # build header
        _result.append(f"Command: {command} - {description}")
        # if filter or excl_filter:
        #     _result.append(
        #         f"Using filter: '{filter}' and excl_filter: '{excl_filter}'. {len(displayData)} results retained from {len(data)} in total"
        #     )
        _result.append("-" * 80)

        # build data
        maxP = getMaxLen(displayData)
        if maxP < 9:
            maxP = 9
        # maxV = getMaxLen(data.values())
        _result.append(f"{pad('Parameter', maxP+1)}{'Value':<15}\tUnit")
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            if len(displayData[key]) > 2 and displayData[key][2] and self.extra_info:
                extra = displayData[key][2]
                _result.append(f"{pad(key,maxP+1)}{value:<15}\t{unit:<4}\t{extra}")
            else:
                _result.append(f"{pad(key,maxP+1)}{value:<15}\t{unit:<4}")
        return _result
