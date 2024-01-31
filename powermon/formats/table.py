""" formats / table.py """
import logging

from powermon.commands.reading import Reading
from powermon.commands.result import Result
from powermon.formats.abstractformat import (AbstractFormat,
                                             get_max_response_lengths, pad)

log = logging.getLogger("Table")


class Table(AbstractFormat):
    """ table formatter - formats results in a table suitable for std out """

    def __str__(self):
        return "outputs the results to standard out in a table (optionally formatted with line art boxes)"

    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "table"
        self.extra_info = formatConfig.get("extra_info", False)
        self.draw_lines = formatConfig.get("draw_lines", False)
        # self.command_description = "unknown command"

    # def set_command_description(self, command_description):
    #     self.command_description = command_description

    def format(self, command, result: Result, device_info) -> list[str]:
        log.info("Using output formatter: %s", self.name)

        _result = []
        filtered_responses: list[Reading] = []

        # check for error in result
        if result.error:
            filtered_responses.append(Reading(data_name="Error Count", data_value=len(result.error_messages), data_unit=""))
            for i, message in enumerate(result.error_messages):
                filtered_responses.append(Reading(data_name=f"Error #{i}", data_value=f"{message}", data_unit=""))

        if len(result.readings) == 0:
            filtered_responses.append(Reading(data_name="Error", data_value="No readings in result", data_unit=""))

        filtered_responses.extend(self.format_and_filter_data(result))
        log.debug("displayData: %s", "\n".join((str(a) for a in filtered_responses)))

        # build header
        # command_code = result.command_definition.code

        # Determine column widths
        _pad = 1

        width_p, width_v, width_u = get_max_response_lengths(filtered_responses)
        # Width of parameter column
        width_p += _pad
        if width_p < 9 + _pad:
            width_p = 9 + _pad
        # Width of value column
        width_v += _pad
        if width_v < 6 + _pad:
            width_v = 6 + _pad
        # Width of units column
        width_u += _pad
        if width_u < 5 + _pad:
            width_u = 5 + _pad
        # Total line length
        line_length = width_p + width_v + width_u + 7
        # Check if command / description line is longer and extend line if needed
        cmd_str = f"Command: {command.code} - {command.command_definition.description}"
        width_c = len(cmd_str)
        # log.debug(f"{width_c=}, {line_length=}, {width_p=}, {width_v=}, {width_u=}")
        if line_length < (width_c + 7):
            line_length = width_c + 7
        # Check if columns too short and expand units if needed
        if (width_p + width_v + width_u + 7) <= line_length:
            width_u = line_length - (width_p + width_v + 7)
        # log.debug(f"{width_c=}, {line_length=}, {width_p=}, {width_v=}, {width_u=}")

        # print header
        if self.draw_lines:
            _result.append("\u2554" + ("\u2550" * (line_length - 2)) + "\u2557")
            _result.append(f"\u2551 {cmd_str}" + (" " * (line_length - len(cmd_str) - 3)) + "\u2551")
        else:
            _result.append("-" * (line_length))
            _result.append(f"{cmd_str}" + (" " * (line_length - len(cmd_str) - 2)))
            _result.append("-" * (line_length))

        # print separator
        if self.draw_lines:
            _result.append("\u2560" + ("\u2550" * (width_p + 1)) + "\u2564" + ("\u2550" * (width_v + 1)) + "\u2564" + ("\u2550" * (width_u + 1)) + "\u2563")
        # print column headings
        if self.draw_lines:
            _result.append(f"\u2551 {pad('Parameter', width_p)}\u2502 {pad('Value', width_v)}\u2502 {pad('Unit', width_u)}\u2551")
        else:
            _result.append(f"{pad('Parameter', width_p)} {pad('Value', width_v)} {pad('Unit', width_u)}")
        # print separator
        if self.draw_lines:
            _result.append("\u255f" + ("\u2500" * (width_p + 1)) + "\u253c" + ("\u2500" * (width_v + 1)) + "\u253c" + ("\u2500" * (width_u + 1)) + "\u2562")

        # print data
        for response in filtered_responses:
            name = response.get_data_name()
            value = response.get_data_value()
            unit = response.get_data_unit()
            if self.draw_lines:
                _result.append(f"\u2551 {pad(name, width_p)}\u2502 {pad(value, width_v)}\u2502 {pad(unit, width_u)}\u2551")
            else:
                _result.append(f"{pad(name, width_p)} {pad(value, width_v)} {pad(unit, width_u)}")

        # print footer
        if self.draw_lines:
            _result.append("\u255a" + ("\u2550" * (width_p + 1)) + "\u2567" + ("\u2550" * (width_v + 1)) + "\u2567" + ("\u2550" * (width_u + 1)) + "\u255d")
        # _result.append("\n")
        return _result
