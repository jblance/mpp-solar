import unittest

from powermon.formats.htmltable import htmltable
from powermon.commands.result import Result
from powermon.commands.response import Response

class test_format_htmltable(unittest.TestCase):
    def test_format_htmltable(self):
        expected = ["<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>",
                    "<tr><td>test</td><td>0.0</td><td>Check</td></tr>",
                    "</table>"]
        table_formatter = htmltable({})
        
        _result = Result(command_code=None)
        response = Response(data_name="Test", data_value="0.0", data_unit="Check")
        _result.add_responses([response])
        
        formatted_data = table_formatter.format(_result)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
        