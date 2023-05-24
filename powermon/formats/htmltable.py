import logging
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("htmltable")


class htmltable(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "htmltable"

    def format(self, data):
        log.info("Using output formatter: htmltable")

        _result = ""
        if data is None:
            return _result

        displayData = self.formatAndFilterData(data)

        _result += "<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>"
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            _result += f"<tr><td>{key}</td><td>{value}</td><td>{unit}</td></tr>"
        _result += "</table>"
        return _result
