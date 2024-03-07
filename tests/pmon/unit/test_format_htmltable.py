""" tests / pmon / unit / test_format_htmltable.py """
import unittest

from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
# from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ReadingType
from powermon.commands.result import Result, ResultType
from powermon.device import DeviceInfo
from powermon.outputformats.htmltable import HtmlTable


class TestFormatHtmltable(unittest.TestCase):
    """ test the htmltable formatter """
    def test_format_htmltable(self):
        """ test generation of normal html table with single reading """
        expected = ["<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>",
                    "<tr><td>energy_today</td><td>300</td><td>Wh</td></tr>",
                    "</table>"]
        config = {}
        table_formatter = HtmlTable(config)
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "Energy Today", "reading_type": ReadingType.WATT_HOURS, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"})
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(300\xcd\xcd\r", responses=b"300")

        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_format_htmltable_multiline(self):
        """ test generation of normal html table with two readings """
        expected = ["<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>",
                    "<tr><td>energy_today</td><td>300</td><td>Wh</td></tr>",
                    '<tr><td>energy_this_week</td><td>23400</td><td>Wh</td></tr>',
                    "</table>"]
        config = {}
        table_formatter = HtmlTable(config)
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition1 = ReadingDefinition.from_config({"description": "Energy Today", "reading_type": ReadingType.WATT_HOURS, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"})
        reading_definition2 = ReadingDefinition.from_config({"description": "Energy This Week", "reading_type": ReadingType.WATT_HOURS, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"})
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.COMMA_DELIMITED, reading_definitions=[reading_definition1, reading_definition2])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(300\xcd\xcd\r", responses=[300, 23400])

        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertListEqual(formatted_data, expected)

    def test_format_htmltable_no_readings(self):
        """ test generation of normal html table with no readings """
        expected = ["<b>No readings in result</b>"]
        config = {}
        table_formatter = HtmlTable(config)
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "Energy Today", "reading_type": ReadingType.WATT_HOURS, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"})
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(300\xcd\xcd\r", responses=None)

        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
