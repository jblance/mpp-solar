import unittest

from powermon.device import DeviceInfo
from powermon.outputformats.simple import SimpleFormat
from powermon.commands.command import Command
from powermon.commands.result import Result, ResultType
# from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType
from powermon.commands.command_definition import CommandDefinition


class test_formats_simple(unittest.TestCase):
    
    def test_simple_format_no_extra(self):
        expected = ["test=238800Wh"]
        simple_formatter = SimpleFormat({})
        
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device_class": "energy", "state_class": "total"},0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command":"CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"238800")
        # _result = Result(result_type=ResultType.SINGLE, raw_response=b"(238800\xcd\xcd\r", command_definition=command_definition, trimmed_response=b"238800")
        
        formatted_data = simple_formatter.format(command, _result, device_info)
        
        self.assertEqual(formatted_data, expected)

    
    def test_simple_format_with_device_class(self):
        expected = ["test=238800Wh energy"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "device_class": "energy"},0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command":"CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"238800")
        # _result = Result(result_type=ResultType.SINGLE, raw_response=b"(238800\xcd\xcd\r", command_definition=command_definition, trimmed_response=b"238800")
        
        formatted_data = simple_formatter.format(command, _result, device_info)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_with_icon(self):
        expected = ["test=238800Wh mdi:solar-power"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power"},0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command":"CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"238800")
        # _result = Result(result_type=ResultType.SINGLE, raw_response=b"(238800\xcd\xcd\r", command_definition=command_definition, trimmed_response=b"238800")
        
        formatted_data = simple_formatter.format(command, _result, device_info)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_with_all_extra(self):
        expected = ["test=238800Wh energy mdi:solar-power total"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device_class": "energy", "state_class": "total"},0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command":"CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"238800")
        # _result = Result(result_type=ResultType.SINGLE, raw_response=b"(238800\xcd\xcd\r", command_definition=command_definition, trimmed_response=b"238800")
        
        formatted_data = simple_formatter.format(command, _result, device_info)
        # print(formatted_data)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_multiple(self):
        expected = ["test=230Wh",
                    "test2=28.0°C"]
        simple_formatter = SimpleFormat({})
        
        reading_definition = ReadingDefinition.from_config({"description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device_class": "energy", "state-class": "total"},0)
        reading_definition2 = ReadingDefinition.from_config({"description":"test2", "reading_type":ReadingType.TEMPERATURE, "response_type":ResponseType.FLOAT, "icon": "mdi:solar-power", "device_class": "energy", "state-class": "total"},1)
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.ORDERED, reading_definitions=[reading_definition, reading_definition2])
        command = Command.from_config({"command":"CODE"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=[b'230', b'28'])
        # _result = Result(result_type=ResultType.ORDERED, raw_response=b"(238800\xcd\xcd\r", command_definition=command_definition, trimmed_response=b"230 28")
        
        formatted_data = simple_formatter.format(command, _result, device_info)
        
        self.assertEqual(formatted_data, expected)
    
    