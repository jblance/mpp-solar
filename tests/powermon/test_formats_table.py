import unittest

from powermon.formats.table import table
from powermon.commands.result import Result
from powermon.commands.response import Response

class test_formats_table(unittest.TestCase):
    def test_format_table_draw_lines_true(self):
        expected = ['╔════════════════════════════════════╗',
                    '║ Command: None - unknown command    ║',
                    '╠═══════════╤════════╤═══════════════╣',
                    '║ Parameter │ Value  │ Unit          ║',
                    '╟───────────┼────────┼───────────────╢',
                    '║ Test      │ 0.0    │ Check         ║',
                    '╚═══════════╧════════╧═══════════════╝']
        table_formatter = table({})
        table_formatter.draw_lines = True
        
        _result = Result(command_code=None)
        response = Response(name="Test", data_value="0.0", data_unit="Check")
        _result.add_response(response)
        
        formatted_data = table_formatter.format(_result)
        print(formatted_data)
        self.assertEqual(formatted_data, expected)
        
    def test_format_table_draw_lines_false(self):
        expected = ['--------------------------------------',
                    'Command: None - unknown command     ',
                    '--------------------------------------',
                    'Parameter  Value   Unit          ',
                    'Test       0.0     Check         ',]
        table_formatter = table({})
        table_formatter.draw_lines = False
        
        _result = Result(command_code=None)
        response = Response(name="Test", data_value="0.0", data_unit="Check")
        _result.add_response(response)
        
        formatted_data = table_formatter.format(_result)
        print(formatted_data)
        self.assertEqual(formatted_data, expected)
        
    def test_format_table_large_value(self):
        expected = ['----------------------------------------------------------------------------------------------------',
                    'Command: None - unknown command                                                                   ',
                    '----------------------------------------------------------------------------------------------------',
                    'Parameter                       Value                           Unit                           ',
                    'Test                            123456789012345678901234567890  Check                          ',]
        table_formatter = table({})
        table_formatter.draw_lines = False
        
        _result = Result(command_code=None)
        response = Response(name="Test", data_value="123456789012345678901234567890", data_unit="Check")
        _result.add_response(response)
        
        formatted_data = table_formatter.format(_result)
        print(formatted_data)
        self.assertEqual(formatted_data, expected)
        
    def test_format_table_no_responses(self):
        expected = []
        table_formatter = table({})
        table_formatter.draw_lines = False
        
        _result = Result(command_code=None)
        
        formatted_data = table_formatter.format(_result)
        print(formatted_data)
        self.assertEqual(formatted_data, expected)