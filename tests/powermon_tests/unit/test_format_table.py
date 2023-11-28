import unittest

from powermon.formats.table import table
from powermon.commands.result import Result, ResultType
from powermon.commands.reading import Reading
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
        table_formatter = table({})
        table_formatter.draw_lines = True
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.MESSAGE, "response_type":ResponseType.FLOAT, "icon": "mdi:solar-power"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"0.0", reading_definitions=[reading_definition], parameters=None)
        
        
        formatted_data = table_formatter.format(_result)
        print(formatted_data)
        self.assertEqual(formatted_data, expected)
        
    def test_format_table_draw_lines_false(self):
        expected = ['--------------------------------------',
                    'Command: None - unknown command     ',
                    '--------------------------------------',
                    'Parameter  Value   Unit          ',
                    'test       0.0                   ',]
        table_formatter = table({})
        table_formatter.draw_lines = False
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.MESSAGE, "response_type":ResponseType.FLOAT, "icon": "mdi:solar-power"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"0.0", reading_definitions=[reading_definition], parameters=None)
        
        
        formatted_data = table_formatter.format(_result)
        print(formatted_data)
        self.assertEqual(formatted_data, expected)
        
    def test_format_table_large_value(self):
        self.maxDiff = 2000
        expected = ['------------------------------------------------------',
                    'Command: None - unknown command                     ',
                    '------------------------------------------------------',
                    'Parameter  Value                           Unit  ',
                    'test       123456789012345678901234567890  Wh    ',]
        table_formatter = table({})
        table_formatter.draw_lines = False
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"123456789012345678901234567890", reading_definitions=[reading_definition], parameters=None)
        
        
        formatted_data = table_formatter.format(_result)
        print(formatted_data)
        self.assertEqual(formatted_data, expected)
        