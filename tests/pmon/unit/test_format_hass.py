import unittest

from powermon.device import DeviceInfo
from powermon.outputformats.hass import Hass
from powermon.commands.command import Command
from powermon.commands.result import Result, ResultType
from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType
from powermon.commands.command_definition import CommandDefinition


class test_format_hass(unittest.TestCase):
    def test_format_htmltable(self):
        
        self.maxDiff = None
        hass_formatter = Hass({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command":"CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"238800")
        
        formatted_data = hass_formatter.format(_result, device_info=device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data[0]["topic"], "homeassistant/sensor/mpp_test/config") #TODO: add some more asserts. Lots of info in the hass format
        