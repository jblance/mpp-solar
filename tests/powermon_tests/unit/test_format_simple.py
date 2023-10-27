import unittest

from powermon.formats.simple import SimpleFormat
from powermon.commands.result import Result
from powermon.commands.reading import Reading

class test_formats_simple(unittest.TestCase):
    
    def test_simple_format_no_extra(self):
        expected = ["test=0.0Check"]
        simple_formatter = SimpleFormat({})
        
        _result = Result(command_code=None)
        _response = Reading(data_name="test", data_value="0.0", data_unit="Check")
        _result.add_responses([_response])
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)

    
    def test_simple_format_with_device_class(self):
        expected = ["test=0.0Check Extra"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        _result = Result(command_code=None)
        _response = Reading(data_name="test", data_value="0.0", data_unit="Check", device_class="Extra")
        _result.add_responses([_response])
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_with_icon(self):
        expected = ["test=0.0Check Extra"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        _result = Result(command_code=None)
        _response = Reading(data_name="test", data_value="0.0", data_unit="Check", icon="Extra")
        _result.add_responses([_response])
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_with_all_extra(self):
        expected = ["test=0.0Check test-device icon state"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        _result = Result(command_code=None)
        _response = Reading(data_name="test", data_value="0.0", data_unit="Check", device_class="test-device", icon="icon", state_class="state")
        _result.add_responses([_response])
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_multiple(self):
        expected = ["test=0.0Check",
                    "test2=2.0Check"]
        simple_formatter = SimpleFormat({})
        
        _result = Result(command_code=None)
        _response = Reading(data_name="test", data_value="0.0", data_unit="Check")
        _response2 = Reading(data_name="test2", data_value="2.0", data_unit="Check")
        _result.add_responses([_response, _response2])
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
    
    