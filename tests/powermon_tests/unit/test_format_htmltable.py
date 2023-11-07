import unittest

from powermon.formats.htmltable import htmltable
from powermon.commands.result import Result, ResultType
from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType

class test_format_htmltable(unittest.TestCase):
    def test_format_htmltable(self):
        expected = ["<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>",
                    "<tr><td>test</td><td>300</td><td>Wh</td></tr>",
                    "</table>"]
        table_formatter = htmltable({})
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"00300", reading_definitions=[reading_definition], parameters=None)
        print(_result.readings[0].data_value)
        
        formatted_data = table_formatter.format(_result)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
        