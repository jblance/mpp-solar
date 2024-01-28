""" tests / pmon / unit / test_responsetype.py """
import struct
import unittest

from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import (ReadingDefinition,
                                                  ReadingType, ResponseType)
from powermon.commands.result import Result, ResultType
from powermon.device import DeviceInfo
from powermon.formats.simple import SimpleFormat


class TestResponseTypes(unittest.TestCase):
    """ exercise different response types """

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

    def test_le_2b_s(self):
        """ test ResponseType.LE_2B_s """
        reading_definition_config = {"description": "Battery Capacity", "reading_type": ReadingType.ENERGY, "response_type": ResponseType.LE_2B_S}
        expected = ["battery_capacity=120Ah"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(7800\xcd\xcd\r", responses=b"7800")

        formatted_data = simple_formatter.format(command, _result, device_info)
        print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_le_2b_s_not_2b_short(self):
        """ test ResponseType.LE_2B_S when response is not 2B (only 1B) """
        reading_definition_config = {"description": "Battery Capacity", "reading_type": ReadingType.ENERGY, "response_type": ResponseType.LE_2B_S}

        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        self.assertRaises(struct.error, Result, command, b"(78\xcd\xcd\r", b"78")

    def test_template_bytes(self):
        """ test ResponseType.TEMPLATE_BYTES """
        reading_definition_config = {"description": "Serial Number", "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.TEMPLATE_BYTES, "format_template" : "r[2:int(r[0:2])+2]"}
        expected = ["serial_number=92932105105335"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(1492932105105335005535\x94\x0e\r", responses=b"1492932105105335005535")

        formatted_data = simple_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_template_int(self):
        """ test ResponseType.TEMPLATE_INT """
        reading_definition_config = {"description": "Energy Last Hour", "reading_type": ReadingType.ENERGY, "response_type": ResponseType.TEMPLATE_INT, "format_template": "r/1000"}
        expected = ["energy_last_hour=12.345Ah"]

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(12345\x94\x0e\r", responses=b"12345")

        formatted_data = simple_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_bit_encoded(self):
        """ test ResponseType.BIT_ENCODED """
        reading_definition_config = {"index": "AR", "description": "Alarm reason", "reading_type": ReadingType.MESSAGE,
                                     "response_type": ResponseType.BIT_ENCODED,
                                     "options": {0: "No alarm",
                                                 1: "Low Voltage",
                                                 2: "High Voltage",
                                                 4: "Low SOC",
                                                 8: "Low Starter Voltage",
                                                 16: "High Starter Voltage",
                                                 32: "Low Temperature",
                                                 64: "High Temperature",
                                                 128: "Mid Voltage",
                                                 256: "Overload",
                                                 512: "DC-ripple",
                                                 1024: "Low V AC out",
                                                 2048: "High V AC out",
                                                 4096: "Short Circuit",
                                                 8192: "BMS Lockout"}}
        expected = ['alarm_reason=High Voltage,Low Starter Voltage,High Starter Voltage,Low Temperature,High Temperature,Mid Voltage']

        simple_formatter = SimpleFormat({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config(reading_definition_config, 0)
        command_definition = CommandDefinition(code="CODE", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "CODE"})
        command.command_definition = command_definition

        _result = Result(command=command, raw_response=b"(12345\x94\x0e\r", responses=b"250")

        formatted_data = simple_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)