""" tests / pmon / unit / test_reading_definition.py """
import unittest

from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import (ReadingDefinition,
                                                  ReadingType, ResponseType)
from powermon.commands.result import Result, ResultType
from powermon.device import DeviceInfo
from powermon.formats.simple import SimpleFormat


class TestReadingDefinitions(unittest.TestCase):
    """ exercise different reading definition functionality """

    def test_option_invalid_key(self):
        """ test that when supplying an invalid key to a ResponseType.OPTION raises a KeyError exception """
        reading_definition_config = {"reading_type": ReadingType.MESSAGE, "response_type": ResponseType.OPTION, "description": "Parallel Mode", "options": {"00": "New", "01": "Slave", "02": "Master"}}

        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition
        self.assertRaises(KeyError, Result, command=command, raw_response=b"(03\xcd\xcd\r", responses=b"03")

    def test_option_valid_key(self):
        """ test ResponseType.OPTION returns value associated with key """
        reading_definition_config = {"reading_type": ReadingType.MESSAGE, "response_type": ResponseType.OPTION, "description": "Parallel Mode", "options": {"00": "New", "01": "Slave", "02": "Master"}}
        expected = ["parallel_mode=Master"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(03\xcd\xcd\r", responses=b"02")

        formatted_data = simple_formatter.format(command, _result, device_info)
        self.assertEqual(formatted_data, expected)

    def test_list_invalid_index(self):
        """ test that when supplying an invalid index to a ResponseType.LIST raises a IndexError exception """
        reading_definition_config = {"description": "Output Source Priority", "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.LIST, "options": ["Utility first", "Solar first", "SBU first"]}

        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition
        self.assertRaises(IndexError, Result, command=command, raw_response=b"(03\xcd\xcd\r", responses=b"03")

    def test_list_valid_index(self):
        """ test ResponseType.OPTION returns value associated with key """
        reading_definition_config = {"description": "Output Source Priority", "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.LIST, "options": ["Utility first", "Solar first", "SBU first"]}
        expected = ["output_source_priority=SBU first"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(03\xcd\xcd\r", responses=b"02")

        formatted_data = simple_formatter.format(command, _result, device_info)
        self.assertEqual(formatted_data, expected)

    def test_temperature_reading(self):
        """ test a correct temperature is returned in celcius """
        reading_definition_config = {"description": "Inverter Heat Sink Temperature", "reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.INT, "icon": "mdi:details", "device_class": "temperature"}
        expected = ["inverter_heat_sink_temperature=27°C"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(03\xcd\xcd\r", responses=b"27")

        formatted_data = simple_formatter.format(command, _result, device_info)
        self.assertEqual(formatted_data, expected)

    def test_temperature_reading_override(self):
        """ test a correct temperature is returned in farenheit when overriden """
        reading_definition_config = {"description": "Inverter Heat Sink Temperature", "reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.INT, "icon": "mdi:details", "device_class": "temperature"}
        expected = ["inverter_heat_sink_temperature=80.6°F"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE", "override": {"temperature": "F"}})
        command.command_definition = command_definition
        # print(command)

        _result = Result(command=command, raw_response=b"(03\xcd\xcd\r", responses=b"27")

        formatted_data = simple_formatter.format(command, _result, device_info)
        self.assertEqual(formatted_data, expected)
