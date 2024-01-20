import unittest

from powermon.device import DeviceInfo
from powermon.formats.htmltable import htmltable
from powermon.commands.result import Result, ResultType
from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType
from powermon.commands.command_definition import CommandDefinition

class test_format_htmltable(unittest.TestCase):
    def test_format_htmltable(self):
        expected = ["<table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>",
                    "<tr><td>test</td><td>300</td><td>Wh</td></tr>",
                    "</table>"]
        table_formatter = htmltable({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        _result = Result(result_type=ResultType.SINGLE, raw_response=b"(300\xcd\xcd\r", command_definition=command_definition, trimmed_response=b"300")

        #print(_result.readings[0].data_value)
        # print(expected)
        formatted_data = table_formatter.format(_result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
        