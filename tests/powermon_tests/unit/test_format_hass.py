import unittest

from powermon.formats.hass import hass
from powermon.commands.result import Result, ResultType
from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType

class test_format_hass(unittest.TestCase):
    def test_format_htmltable(self):
        
        self.maxDiff = None
        hass_formatter = hass({}, device=None)
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"238800", reading_definitions=[reading_definition], parameters=None)
        
        formatted_data = hass_formatter.format(_result)
        # print(formatted_data)
        self.assertEqual(formatted_data[0]["topic"], "homeassistant/sensor/mpp_test/config") #TODO: add some more asserts. Lots of info in the hass format
        