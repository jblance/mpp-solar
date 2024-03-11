""" tests / pmon / unit / test_format_table.py """
import unittest

from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
# from powermon.commands.reading import Reading
from powermon.commands.reading_definition import (ReadingDefinition,
                                                  ReadingType, ResponseType)
from powermon.commands.result import Result, ResultType
from powermon.device import DeviceInfo
from powermon.outputformats.table import Table


class TestFormatTable(unittest.TestCase):
    """ test tge table output formatter """
    def test_format_table_draw_lines_true(self):
        """ test table with lines """
        expected = ['╔═════════════════════════════════╗',
                    '║ Command: None - unknown command ║',
                    '╠═══════════╤═══════╤═════════════╣',
                    '║ Parameter │ Value │ Unit        ║',
                    '╟───────────┼───────┼─────────────╢',
                    '║ test      │ 0.0   │             ║',
                    '╚═══════════╧═══════╧═════════════╝']
        table_formatter = Table({'draw_lines': True})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "test", "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.FLOAT, "icon": "mdi:solar-power"})
        command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "None"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"0.0")
        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_format_table_draw_lines_false(self):
        """ test table without lines """
        expected = ['--------------------------------',
                    'Command: None - unknown command',
                    '--------------------------------',
                    'Parameter     Value  Unit ',
                    'test_message  0.0         ',]
        table_formatter = Table({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "Test Message", "response_type": ResponseType.FLOAT})
        command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "None"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"0.0")
        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_format_table_large_value(self):
        """ test table with a large value """
        expected = ['-----------------------------------------------',
                    'Command: None - unknown command',
                    '-----------------------------------------------',
                    'Parameter  Value                           Unit ',
                    'test       123456789012345678901234567890  Wh   ']
        table_formatter = Table({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "test", "reading_type": ReadingType.WATT_HOURS})
        command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "None"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"123456789012345678901234567890")
        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_table_error(self):
        """ test table format with an error state reading """
        expected = ['----------------------------------------',
                    'Command: None - unknown command',
                    '----------------------------------------',
                    'Parameter    Value                  Unit ',
                    'error_count  2                           ',
                    'error_#0     error message 1             ',
                    'error_#1     another error message       ',
                    'test         238800                 Wh   ']
        table_formatter = Table({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "test", "reading_type": ReadingType.WATT_HOURS})
        command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "None"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"238800")
        _result.error = True
        _result.error_messages = ["error message 1", "another error message"]
        _result.is_valid = False
        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_format_table_extra_info(self):
        """ test table with extra info """
        expected = ['---------------------------',
                    'Command: QT - Test Command',
                    '---------------------------',
                    'Parameter     Value  Unit  Extra Info',
                    'test_message  0.0          icon:mdi:current-ac, device_class:frequency']
        table_formatter = Table({'extra_info': True})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "Test Message", "response_type": ResponseType.FLOAT, "icon": "mdi:current-ac", "device_class": "frequency"})
        command_definition = CommandDefinition(code="QT", description="Test Command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "QT"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"0.0")
        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
