""" formats / table.py """
import logging

from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition
from powermon.commands.result import Result
from powermon.errors import ConfigError
from powermon.outputformats.abstractformat import AbstractFormat

log = logging.getLogger("Table")


class Table(AbstractFormat):
    """ table formatter - formats results in a table suitable for std out """

    def __str__(self):
        return "outputs the results to standard out in a table (optionally formatted with line art boxes)"

    def __init__(self, config):
        super().__init__(config)
        self.name = "table"
        self.draw_lines = config.get("draw_lines", False)
        # self.command_description = "unknown command"

    # def set_command_description(self, command_description):
    #     self.command_description = command_description

    def format(self, command, result: Result, device_info) -> list[str]:
        log.info("Using output formatter: %s", self.name)

        _result = []
        filtered_responses: list[Reading] = []

        # check for error in result
        if result.error:
            filtered_responses.append(Reading(raw_value=None, processed_value=len(result.error_messages), definition=ReadingDefinition.from_config({"description": "Error Count"})))
            for i, message in enumerate(result.error_messages):
                reading_definition = ReadingDefinition.from_config({"description": f"Error #{i}"})
                filtered_responses.append(Reading(raw_value=None, processed_value=f"{message}", definition=reading_definition))

        if len(result.readings) == 0:
            filtered_responses.append(Reading(raw_value=None, processed_value="No readings in result", definition=ReadingDefinition.from_config({"description": "Error"})))

        filtered_responses.extend(self.format_and_filter_data(result))
        log.debug("displayData: %s", "\n".join((str(a) for a in filtered_responses)))

        # Determine column widths
        _pad = 1

        # data_name column
        max_data_name_length = max(len(reading.data_name) + _pad for reading in filtered_responses)
        max_data_name_length = max(max_data_name_length, 9 + _pad)
        # data_valuye column
        max_data_value_length = max(len(str(reading.data_value)) + _pad for reading in filtered_responses)
        max_data_value_length = max(max_data_value_length, 5 + _pad)
        # data_unit column
        max_data_unit_length = max(len(reading.data_unit) + _pad for reading in filtered_responses)
        max_data_unit_length = max(max_data_unit_length, 4 + _pad)

        # Total line length - of data
        line_length = max_data_name_length + max_data_value_length + max_data_unit_length + _pad

        cmd_str = f"Command: {command.code} - {command.command_definition.description}"

        if not self.extra_info:
            if self.draw_lines:
                # draw lines
                line_length += 3
                # Make line length longer if cmd_str exceeds data size
                line_length = max(line_length, len(cmd_str) + 4)
                # Check if columns too short and expand units if needed
                if (max_data_name_length + max_data_value_length + max_data_unit_length + 7) <= line_length:
                    max_data_unit_length = line_length - (max_data_name_length + max_data_value_length + 7)
                # Check if data and parameter are larger than line_length
                column_label_line_length = max(max_data_name_length, 9) + max(max_data_value_length, 5) + max(max_data_unit_length, 4) + 7
                line_length = max(column_label_line_length, line_length)
                # Command head / description
                _result.append(f"{'╔':═<{line_length - 1}}╗")
                _result.append(f"║ {cmd_str: <{line_length - 3}}║")
                _result.append(f"{'╠':═<{max_data_name_length + 2}}{'╤':═<{max_data_value_length + 2}}{'╤':═<{max_data_unit_length + 2}}╣")
                # Column titles
                _result.append(f"║ {'Parameter': <{max_data_name_length}}│ {'Value': <{max_data_value_length}}│ {'Unit': <{max_data_unit_length}}║")
                _result.append(f"{'╟':─<{max_data_name_length + 2}}{'┼':─<{max_data_value_length + 2}}{'┼':─<{max_data_unit_length + 2}}╢")
                # Data
                for reading in filtered_responses:
                    name = self.format_key(reading.data_name)
                    value = reading.data_value
                    unit = reading.data_unit
                    _result.append(f"║ {name: <{max_data_name_length}}│ {value: <{max_data_value_length}}│ {unit: <{max_data_unit_length}}║")
                # Footer
                _result.append(f"{'╚':═<{max_data_name_length + 2}}{'╧':═<{max_data_value_length + 2}}{'╧':═<{max_data_unit_length + 2}}╝")
            else:  # no lines
                # Make line length longer if cmd_str exceeds data size
                line_length = max(line_length, len(cmd_str) + _pad)
                # Command head / description
                _result.append(f"{'':-<{line_length}}")
                _result.append(f"{cmd_str}")
                _result.append(f"{'':-<{line_length}}")
                # Column titles
                _result.append(f"{'Parameter': <{max_data_name_length}} {'Value': <{max_data_value_length}} {'Unit': <{max_data_unit_length}}")
                # Data
                for reading in filtered_responses:
                    name = self.format_key(reading.data_name)
                    value = reading.data_value
                    unit = reading.data_unit
                    _result.append(f"{name: <{max_data_name_length}} {value: <{max_data_value_length}} {unit: <{max_data_unit_length}}")
        else:  # extra_info
            if self.draw_lines:
                raise ConfigError('drawlines with extra info is not supported')
            else:  # no lines
                # max_data_unit_length = max(len(reading.data_unit) + _pad for reading in filtered_responses)
                # Make line length longer if cmd_str exceeds data size
                line_length = max(line_length, len(cmd_str) + _pad)
                # Command head / description
                _result.append(f"{'':-<{line_length}}")
                _result.append(f"{cmd_str}")
                _result.append(f"{'':-<{line_length}}")
                # Column titles
                _result.append(f"{'Parameter': <{max_data_name_length}} {'Value': <{max_data_value_length}} {'Unit': <{max_data_unit_length}} Extra Info")
                # Data
                for reading in filtered_responses:
                    name = self.format_key(reading.data_name)
                    value = reading.data_value
                    unit = reading.data_unit
                    icon = reading.icon
                    state_class = reading.state_class
                    device_class = reading.device_class
                    extra_info = ''
                    if icon:
                        extra_info += f"icon:{icon}, "
                    if state_class:
                        extra_info += f"state_class:{state_class}, "
                    if device_class:
                        extra_info += f"device_class:{device_class}"
                    _result.append(f"{name: <{max_data_name_length}} {value: <{max_data_value_length}} {unit: <{max_data_unit_length}} {extra_info}")

        return _result
