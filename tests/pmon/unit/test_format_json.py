""" tests / pmon / unit / test_format_json.py """
import unittest

from powermon.device import DeviceInfo
from powermon.outputformats.json_fmt import Json as fmt
from powermon.commands.command import Command
from powermon.commands.result import Result, ResultType
# from powermon.commands.reading import Reading
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType
from powermon.commands.command_definition import CommandDefinition


class TestFormatJson(unittest.TestCase):
    """ test the json formatter """
    def test_json_format_no_extra(self):
        """ test json format with no config """
        expected = ['{"data_name": "test_energy_total", "data_value": 238, "data_unit": "Wh"}']
        formatter = fmt({})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "Test Energy Total", "reading_type": ReadingType.WATT_HOURS, "icon": "mdi:solar-power", "device_class": "energy", "state_class": "total"})
        command_definition = CommandDefinition(code="TEST", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "TEST"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b'(238', responses=b"238")
        formatted_data = formatter.format(command, _result, device_info)

        self.assertEqual(formatted_data, expected)

    def test_json_format_extra_info(self):
        """ test json format with extra_info requested """
        expected = ['{"data_name": "test_energy_total", "data_value": 238, "data_unit": "Wh", "icon": "mdi:solar-power", "state_class": "total", "device_class": "energy"}']
        formatter = fmt({'extra_info': True})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "Test Energy Total", "reading_type": ReadingType.WATT_HOURS, "icon": "mdi:solar-power", "device_class": "energy", "state_class": "total"})
        command_definition = CommandDefinition(code="TEST", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "TEST"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b'(238', responses=b"238")
        formatted_data = formatter.format(command, _result, device_info)

        self.assertEqual(formatted_data, expected)

    def test_json_format_extra_info_with_nulls(self):
        """ test json format with extra_info and include missing requested """
        expected = ['{"data_name": "test_energy_total", "data_value": 238, "data_unit": "Wh", "icon": null, "state_class": "total", "device_class": "energy"}']
        formatter = fmt({'extra_info': True, 'include_missing': True})
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        reading_definition = ReadingDefinition.from_config({"description": "Test Energy Total", "reading_type": ReadingType.WATT_HOURS, "device_class": "energy", "state_class": "total"})
        command_definition = CommandDefinition(code="TEST", description="description", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        command = Command.from_config({"command": "TEST"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b'(238', responses=b"238")
        formatted_data = formatter.format(command, _result, device_info)

        self.assertEqual(formatted_data, expected)

    def test_json_format_multiple(self):
        """ test json format with multiple readings """
        expected = ['{"data_name": "test_energy_total", "data_value": 230, "data_unit": "Wh"}',
                    '{"data_name": "test_temperature", "data_value": 28.0, "data_unit": "\\u00b0C"}']
        formatter = fmt({})
        reading_definition = ReadingDefinition.from_config({"description": "Test Energy Total", "reading_type": ReadingType.WATT_HOURS, "icon": "mdi:solar-power", "device_class": "energy", "state-class": "total"})
        reading_definition2 = ReadingDefinition.from_config({"description": "Test Temperature", "reading_type": ReadingType.TEMPERATURE, "response_type": ResponseType.FLOAT, "icon": "mdi:solar-power", "device_class": "energy", "state-class": "total"}, 1)
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        command_definition = CommandDefinition(code="TEST", description="description", help_text="", result_type=ResultType.ORDERED, reading_definitions=[reading_definition, reading_definition2])
        command = Command.from_config({"command": "TEST"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=[b'230', b'28'])
        formatted_data = formatter.format(command, _result, device_info)

        self.assertEqual(formatted_data, expected)
