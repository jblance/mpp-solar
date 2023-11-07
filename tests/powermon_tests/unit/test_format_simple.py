import unittest

from powermon.formats.simple import SimpleFormat
from powermon.commands.result import Result, ResultType
from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType

class test_formats_simple(unittest.TestCase):
    
    def test_simple_format_no_extra(self):
        expected = ["test=238800Wh"]
        simple_formatter = SimpleFormat({})
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"238800", reading_definitions=[reading_definition], parameters=None)
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)

    
    def test_simple_format_with_device_class(self):
        expected = ["test=238800Wh energy"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "device-class": "energy"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"238800", reading_definitions=[reading_definition], parameters=None)
        
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_with_icon(self):
        expected = ["test=238800Wh mdi:solar-power"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"238800", reading_definitions=[reading_definition], parameters=None)
        
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_with_all_extra(self):
        expected = ["test=238800Wh energy mdi:solar-power total"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},0)
        _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"238800", reading_definitions=[reading_definition], parameters=None)

        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_multiple(self):
        expected = ["test=2Wh",
                    "test2=8C"]
        simple_formatter = SimpleFormat({})
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.WATT_HOURS, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},0)
        reading_definition2 = ReadingDefinition.from_config({"index":1, "description":"test", "reading_type":ReadingType.TEMP, "response_type":ResponseType.INT, "icon": "mdi:solar-power", "device-class": "energy", "state_class": "total"},1)
        
        _result = Result(command_code=None, result_type=ResultType.INDEXED, raw_response=b"28", reading_definitions=[reading_definition, reading_definition2], parameters=None)

        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
    
    