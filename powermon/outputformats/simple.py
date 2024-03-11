""" formats / simple.py """
import logging
from powermon.outputformats.abstractformat import AbstractFormat
from powermon.dto.formatDTO import FormatDTO
from powermon.commands.result import Result
from powermon.commands.reading import Reading

log = logging.getLogger("simple")


class SimpleFormat(AbstractFormat):
    """ simple format - {name}={value}{unit} format """
    def __init__(self, config):
        super().__init__(config)
        self.name = "simple"

    # def set_command_description(self, command_description):
    #     pass

    def format(self, command, result: Result, device_info) -> list:

        _result = []

        # check for error in result
        if result.error:
            _result.append(f"Error Count: {len(result.error_messages)}")
            for i, message in enumerate(result.error_messages):
                _result.append(f"Error #{i}: {message}")
            # return _result

        if len(result.readings) == 0:
            return _result

        display_data : list[Reading] = self.format_and_filter_data(result)

        # build data to display
        for reading in display_data:
            name = self.format_key(reading.data_name)
            value = reading.data_value
            unit = reading.data_unit
            if self.extra_info:
                extra = ""
                if reading.device_class is not None:
                    extra = " " + reading.device_class
                if reading.icon is not None:
                    extra += " " + reading.icon
                if reading.state_class is not None:
                    extra += " " + reading.state_class
                _result.append(f"{name}={value}{unit}{extra}")
            else:
                _result.append(f"{name}={value}{unit}")
        return _result

    @classmethod
    def from_dto(cls, dto: FormatDTO):
        """ build class object from dto """
        return cls(config=dto)
