import unittest

from powermon.formats.hass import hass
from powermon.commands.result import Result
from powermon.commands.reading import Reading

class test_format_hass(unittest.TestCase):
    def test_format_htmltable(self):
        
        self.maxDiff = None
        hass_formatter = hass({}, device=None)
        
        _result = Result(command_code=None)
        response = Reading(data_name="Test", data_value="0.0", data_unit="Check")
        _result.add_responses([response])
        
        formatted_data = hass_formatter.format(_result)
        # print(formatted_data)
        self.assertEqual(formatted_data[0]["topic"], "homeassistant/sensor/mpp_test/config") #TODO: add some more asserts. Lots of info in the hass format
        