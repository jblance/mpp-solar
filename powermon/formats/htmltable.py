import logging
from powermon.formats.abstractformat import AbstractFormat
from powermon.commands.result import Result
from powermon.commands.reading import Reading

log = logging.getLogger("htmltable")


class htmltable(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "htmltable"
        
    # def set_command_description(self, command_description):
    #     pass

    def format(self, result: Result, device_info):
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
            return _result

        displayData : list[Reading] = self.format_and_filter_data(result)
        log.debug(f"displayData: {displayData}")

        _result.append("<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>")
        for response in displayData:
            key = response.get_data_name()
            value = response.get_data_value()
            unit = response.get_data_unit()
            _result.append(f"<tr><td>{key}</td><td>{value}</td><td>{unit}</td></tr>")
        _result.append("</table>")
        return _result
