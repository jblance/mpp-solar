""" formats / simple.py """
import logging
from powermon.formats.abstractformat import AbstractFormat
from powermon.dto.formatDTO import FormatDTO
from powermon.commands.result import Result
from powermon.commands.reading import Reading

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
        #if result.error:
        #    data = {}
        #    data["Error"] = [f"Command: {result.command_code} incurred an error or errors during execution or processing", ""]
        #    data["Error Count"] = [len(result.error_messages), ""]
        #    for i, message in enumerate(result.error_messages):
        #        data[f"Error #{i}"] = [message, ""]


        if len(result.get_responses()) == 0:
            return _result

        display_data : list[Reading] = self.format_and_filter_data(result)

        # build data to display
        for response in display_data:
            name = response.get_data_name()
            value = response.get_data_value()
            unit = response.get_data_unit()
            if self.extra_info:
                extra = ""
                if response.get_device_class() is not None:
                    extra = " " + response.get_device_class()
                if response.get_icon() is not None:
                    extra += " " + response.get_icon()
                if response.get_state_class() is not None:
                    extra += " " + response.get_state_class()
                
                
                _result.append(f"{name}={value}{unit}{extra}")
            else:
                _result.append(f"{name}={value}{unit}")
        return _result

    @classmethod
    def from_DTO(cls, dto: FormatDTO):
        return cls(formatConfig={})