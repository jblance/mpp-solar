import logging

from mppsolar.helpers import getMaxLen, pad
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("table")


class table(AbstractFormat):
    def __str__(self):
        return "outputs the results to standard out in a table (optionally formatted with line art boxes)"

    def __init__(self, formatConfig):
        super().__init__(formatConfig)
        self.name = "table"
        self.extra_info = formatConfig.get("extra_info", False)
        self.drawlines = formatConfig.get("draw_lines", False)

    def format(self, result):
        log.info("Using output formatter: %s" % self.name)

        _result = []

        # check for error in result
        if result.error:
            data = {}
            data["Error"] = [f"Command: {result.command.name} incurred an error or errors during execution or processing", ""]
            data["Error Count"] = [len(result.error_messages), ""]
            for i, message in enumerate(result.error_messages):
                data[f"Error #{i}"] = [message, ""]
        else:
            data = result.decoded_responses

        if data is None:
            return _result

        displayData = self.formatAndFilterData(data)
        log.debug(f"displayData: {displayData}")

        # build header
        command = result.command.name
        if result.command.command_defn and "description" in result.command.command_defn:
            description = result.command.command_defn['description']
        else:
            description = "unknown command"

        # Determine column widths
        _pad = 1
        # Width of parameter column
        width_p = getMaxLen(displayData) + _pad
        if width_p < 9 + _pad:
            width_p = 9 + _pad
        # Width of value column
        width_v = getMaxLen(data.values()) + _pad
        if width_v < 6 + _pad:
            width_v = 6 + _pad
        # Width of units column
        width_u = getMaxLen(data.values(), 1) + _pad
        if width_u < 5 + _pad:
            width_u = 5 + _pad
        # Total line length
        line_length = width_p + width_v + width_u + 7
        # Check if command / description line is longer and extend line if needed
        cmd_str = f"Command: {command} - {description}"
        width_c = len(cmd_str)
        log.debug(f"{width_c=}, {line_length=}, {width_p=}, {width_v=}, {width_u=}")
        if line_length < (width_c + 7):
            line_length = width_c + 7
        # Check if columns too short and expand units if needed
        if (width_p + width_v + width_u + 7) <= line_length:
            width_u = line_length - (width_p + width_v + 7) 
        log.debug(f"{width_c=}, {line_length=}, {width_p=}, {width_v=}, {width_u=}")

        # print header
        if self.drawlines:
            _result.append("\u2554" + ("\u2550" * (line_length - 2)) + "\u2557")
            _result.append(f"\u2551 {cmd_str}" + (" " * (line_length - len(cmd_str) - 3)) + "\u2551")
        else:
            _result.append("-" * (line_length))
            _result.append(f"{cmd_str}" + (" " * (line_length - len(cmd_str) - 2)))
            _result.append("-" * (line_length))

        # print separator
        if self.drawlines:
            _result.append("\u2560" + ("\u2550" * (width_p + 1)) + "\u2564" + ("\u2550" * (width_v + 1)) + "\u2564" + ("\u2550" * (width_u + 1)) + "\u2563")
        # print column headings
        if self.drawlines:
            _result.append(f"\u2551 {pad('Parameter', width_p)}\u2502 {pad('Value', width_v)}\u2502 {pad('Unit', width_u)}\u2551")
        else:
            _result.append(f"{pad('Parameter', width_p)} {pad('Value', width_v)} {pad('Unit', width_u)}")
        # print separator
        if self.drawlines:
            _result.append("\u255f" + ("\u2500" * (width_p + 1)) + "\u253c" + ("\u2500" * (width_v + 1)) + "\u253c" + ("\u2500" * (width_u + 1)) + "\u2562")

        # print data
        for key in displayData:
            value = displayData[key][0]
            unit = displayData[key][1]
            if self.drawlines:
                _result.append(f"\u2551 {pad(key, width_p)}\u2502 {pad(value, width_v)}\u2502 {pad(unit, width_u)}\u2551")
            else:
                _result.append(f"{pad(key, width_p)} {pad(value, width_v)} {pad(unit, width_u)}")

        # print footer
        if self.drawlines:
            _result.append("\u255a" + ("\u2550" * (width_p + 1)) + "\u2567" + ("\u2550" * (width_v + 1)) + "\u2567" + ("\u2550" * (width_u + 1)) + "\u255d")
        # _result.append("\n")
        return _result
