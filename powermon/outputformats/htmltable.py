""" powermon / outputformats / htmltable.py """
import logging
from powermon.outputformats.abstractformat import AbstractFormat
from powermon.commands.result import Result
from powermon.commands.reading import Reading

log = logging.getLogger("htmltable")


class HtmlTable(AbstractFormat):
    def __init__(self, config):
        super().__init__(config)
        self.name = "htmltable"

    def format(self, command, result: Result, device_info):
        log.info("Using output formatter: %s", self.name)

        _result = []

        # check for error in result
        # TODO: have the result output the error
        if result.error:
            data = {}
            data["Error"] = [f"Command: {result.command_code} incurred an error or errors during execution or processing", ""]
            data["Error Count"] = [len(result.error_messages), ""]
            for i, message in enumerate(result.error_messages):
                data[f"Error #{i}"] = [message, ""]

        if len(result.readings) == 0:
            _result.append("<b>No readings in result</b>")
            return _result

        display_data : list[Reading] = self.format_and_filter_data(result)
        log.debug("display_data: %s", display_data)

        _result.append("<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>")
        for reading in display_data:
            key = self.format_key(reading.data_name)
            value = reading.data_value
            unit = reading.data_unit
            _result.append(f"<tr><td>{key}</td><td>{value}</td><td>{unit}</td></tr>")
        _result.append("</table>")
        return _result
