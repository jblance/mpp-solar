import unittest

from powermon.formats.table import Table
from powermon.commands.result import Result, ResultType
from powermon.commands.reading import Reading
from powermon.device import DeviceInfo
from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType

class test_format_table(unittest.TestCase):
    def test_format_table_draw_lines_true(self):
        expected = ['╔════════════════════════════════════╗',
                    '║ Command: None - unknown command    ║',
                    '╠═══════════╤════════╤═══════════════╣',
                    '║ Parameter │ Value  │ Unit          ║',
                    '╟───────────┼────────┼───────────────╢',
                    '║ test      │ 0.0    │               ║',
                    '╚═══════════╧════════╧═══════════════╝']
        table_formatter = Table({})
        table_formatter.draw_lines = True
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.MESSAGE, "response_type":ResponseType.FLOAT, "icon": "mdi:solar-power"},0)
        command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command":"None"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"0.0")
        # _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"0.0", reading_definitions=[reading_definition], parameters=None)
        
        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
        
    def test_format_table_draw_lines_false(self):
        expected = ['--------------------------------------',
                    'Command: None - unknown command     ',
                    '--------------------------------------',
                    'Parameter  Value   Unit          ',
                    'test       0.0                   ',]
        table_formatter = Table({})
        table_formatter.draw_lines = False
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.MESSAGE, "response_type":ResponseType.FLOAT, "icon": "mdi:solar-power"},0)
        command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command":"None"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"0.0")
        # _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"0.0", reading_definitions=[reading_definition], parameters=None)
        
        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
        
    def test_format_table_large_value(self):
        self.maxDiff = 2000
        expected = ['------------------------------------------------------',
                    'Command: None - unknown command                     ',
                    '------------------------------------------------------',
                    'Parameter  Value                           Unit  ',
                    'test       123456789012345678901234567890  Wh    ',]
        table_formatter = Table({})
        table_formatter.draw_lines = False
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power"},0)
        command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command":"None"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"123456789012345678901234567890")
        # _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"123456789012345678901234567890", reading_definitions=[reading_definition], parameters=None)

        formatted_data = table_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
        