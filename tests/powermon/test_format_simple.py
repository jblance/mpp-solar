import unittest

from powermon.formats.simple import SimpleFormat
from powermon.commands.result import Result
from powermon.commands.response import Response

class test_formats_simple(unittest.TestCase):
    
    def test_simple_format_no_extra(self):
        expected = ["Test=0.0Check"]
        simple_formatter = SimpleFormat({})
        
        _result = Result(command_code=None)
        _response = Response(data_name="Test", data_value="0.0", data_unit="Check")
        _result.add_responses(_response)
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)

    
    def test_simple_format_with_extra(self):
        expected = ["Test=0.0Check Extra"]
        simple_formatter = SimpleFormat({"extra_info": True})
        
        _result = Result(command_code=None)
        _response = Response(data_name="Test", data_value="0.0", data_unit="Check", extra_info="Extra")
        _result.add_responses(_response)
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
        
    def test_simple_format_multiple(self):
        expected = ["Test=0.0Check",
                    "Test2=2.0Check"]
        simple_formatter = SimpleFormat({})
        
        _result = Result(command_code=None)
        _response = Response(data_name="Test", data_value="0.0", data_unit="Check")
        _response2 = Response(data_name="Test2", data_value="2.0", data_unit="Check")
        _result.add_responses(_response)
        _result.add_responses(_response2)
        
        formatted_data = simple_formatter.format(_result)
        
        self.assertEqual(formatted_data, expected)
    
    