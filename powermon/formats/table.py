import logging
from mppsolar.helpers import getMaxLen, pad
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("table")


class table(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "table"
        self.extra_info = formatConfig.get("extra_info", False)

    def format(self, result):
        log.info("Using output formatter: %s" % self.name)

        _result = []
        data = result.decoded_responses
        if data is None:
            return _result

        displayData = self.formatAndFilterData(data)
        log.debug(f"displayData: {displayData}")

        # get sizes data to display
        maxP = getMaxLen(displayData)
        if maxP < 9:
            maxP = 9
        maxV = getMaxLen(data.values())
        if maxV > 50:
            maxV = 50
        width = maxP + maxV + 8

        # build header
        _result.append(f"Command: {result.command.name} - {result.command.command_defn['description']}")
        # if filter or excl_filter:
        #     _result.append(
        #         f"Using filter: '{filter}' and excl_filter: '{excl_filter}'. {len(displayData)} results retained from {len(data)} in total"
        #     )
        _result.append("-" * width)

        # build data
        _result.append(f"{pad('Parameter', maxP+2)}{pad('Value', maxV+2)}Unit")
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            if len(displayData[key]) > 2 and displayData[key][2] and self.extra_info:
                extra = displayData[key][2]
                _result.append(f"{pad(key,maxP+1)}{value:<15}\t{unit:<4}\t{extra}")
            else:
                _result.append(f"{pad(key,maxP+1)}{value:<15}\t{unit:<4}")
        return _result
