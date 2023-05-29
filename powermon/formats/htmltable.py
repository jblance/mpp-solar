import logging
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("htmltable")


class htmltable(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "htmltable"

    def format(self, result):
        log.info("Using output formatter: %s" % self.name)

        _result = []
        data = result.decoded_responses
        if data is None:
            return _result
        log.debug(f"data: {data}")
        displayData = self.formatAndFilterData(data)
        log.debug(f"displayData: {displayData}")

        _result.append("<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>")
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            _result.append(f"<tr><td>{key}</td><td>{value}</td><td>{unit}</td></tr>")
        _result.append("</table>")
        return _result
