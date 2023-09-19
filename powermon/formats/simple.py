import logging
from powermon.formats.abstractformat import AbstractFormat
from powermon.dto.formatDTO import FormatDTO
from powermon.commands.result import Result

log = logging.getLogger("simple")


class SimpleFormat(AbstractFormat):
    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "simple"
        self.extra_info = formatConfig.get("extra_info", False)
   
    def set_command_description(self, command_description):
        pass

    def format(self, result: Result) -> list:

        _result = []

        # check for error in result
        if result.error:
            data = {}
            data["Error"] = [f"Command: {result.command_code} incurred an error or errors during execution or processing", ""]
            data["Error Count"] = [len(result.error_messages), ""]
            for i, message in enumerate(result.error_messages):
                data[f"Error #{i}"] = [message, ""]
        else:
            data = result.decoded_responses

        if data is None:
            return _result

        displayData = self.formatAndFilterData(data)

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

    @classmethod
    def from_DTO(cls, dto: FormatDTO):
        return cls(formatConfig={})