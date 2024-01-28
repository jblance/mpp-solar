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

    def test_kilowatt_hours(self):
        """ test ReadingType.KILOWATT_HOURS """
        reading_definition_config = {"description": "Todays Power", "reading_type": ReadingType.KILOWATT_HOURS, "response_type": ResponseType.INT}
        expected = ["todays_power=123kWh"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(123\xcd\xcd\r", responses=b"123")

        formatted_data = simple_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_hex_str(self):
        """ test ReadingType.KILOWATT_HOURS """
        reading_definition_config = {"description": "Checksum", "reading_type": ReadingType.HEX_STR, "response_type": ResponseType.HEX_CHAR}
        expected = ["checksum=0x1a"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(\x1a\xcd\xcd\r", responses=b"\x1a")

        formatted_data = simple_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)
