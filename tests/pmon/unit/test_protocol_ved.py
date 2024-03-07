""" tests / pmon / unit / test_protocol_ved.py """
import unittest

import construct as cs

from powermon.commands.command import Command, CommandType
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import ReadingType, ResponseType
from powermon.commands.result import ResultType
from powermon.device import DeviceInfo
from powermon.errors import CommandError, InvalidCRC, InvalidResponse
from powermon.outputformats.simple import SimpleFormat
from powermon.protocols.ved import VictronEnergyDirect

battery_capacity_defn = cs.Struct(
    "command_type" / cs.Byte,
    "command" / cs.Int16ul,
    "command_response_flag" / cs.Int8ul,
    "battery_capacity" / cs.Int16ul,
    "rest" / cs.GreedyBytes,
)

command_definitions_config = {
    "name": "battery_capacity",
    "description": "Battery Capacity",
    "help": " -- display the Battery Capacity",
    "command_type": CommandType.VICTRON_GET,
    "command_code": "1000",
    "result_type": ResultType.CONSTRUCT,
    "construct": battery_capacity_defn,
    "construct_min_response": 6,
    "reading_definitions": [
        {"index": "command_type", "description": "command type", "reading_type": ReadingType.IGNORE},
        {"index": "command", "description": "command", "reading_type": ReadingType.IGNORE},
        {"index": "command_response_flag", "description": "command response flag",
            "reading_type": ReadingType.IGNORE,
            "response_type": ResponseType.OPTION,
            "options": {0: "OK",
                        1: "Unknown ID",
                        2: "Not supported",
                        4: "Parameter Error"}},
        {"index": "battery_capacity", "description": "Battery Capacity", "reading_type": ReadingType.ENERGY}]}
cd = CommandDefinition.from_config(command_definitions_config)


class TestProtocolVed(unittest.TestCase):
    """ exercise different functions in ved protocol """

    def test_check_crc(self):
        """ test a for correct CRC validation """
        ved = VictronEnergyDirect()
        _result = ved.check_crc(response=b"\x00\x1a:70010007800C6\n", command_definition=cd)
        # print(_result)
        self.assertTrue(_result)

    def test_check_crc_incorrect(self):
        """ test an exception is raised if CRC validation fails """
        ved = VictronEnergyDirect()
        self.assertRaises(InvalidCRC, ved.check_crc, response=b":70010007800C7\n", command_definition=cd)

    def test_full_command_battery_capacity(self):
        """ test a for correct build of full command - battery_capacity """
        ved = VictronEnergyDirect()
        _result = ved.get_full_command(command="battery_capacity")
        expected = b':70010003E\n'

        # print(_result)
        self.assertEqual(_result, expected)

    def test_full_command_serial_number(self):
        """ test a for correct build of full command - serial_number """
        ved = VictronEnergyDirect()
        _result = ved.get_full_command(command="serial_number")
        expected = b':70A010043\n'

        # print(_result)
        self.assertEqual(_result, expected)

    def test_full_command_vedtext(self):
        """ test a for correct build of full command - vedtext """
        ved = VictronEnergyDirect()
        _result = ved.get_full_command(command="vedtext")
        expected = CommandType.VICTRON_LISTEN

        # print(_result)
        self.assertEqual(_result, expected)

    def test_trim(self):
        """ test ved protocol does a correct trim operation """
        ved = VictronEnergyDirect()
        _result = ved.trim_response(response=b":70010007800C6\n", command_definition=cd)
        expected = b'\x07\x00\x10\x00x\x00'

        # print(_result)
        self.assertEqual(_result, expected)

    def test_check_valid_ok(self):
        """ test ved protocol returns true for a correct response validation check """
        ved = VictronEnergyDirect()
        _result = ved.check_valid(response=b":70010007800C6\n", command_definition=cd)
        expected = True

        # print(_result)
        self.assertEqual(_result, expected)

    def test_check_valid_none(self):
        """ test ved protocol returns false for a None response validation check """
        ved = VictronEnergyDirect()

        # print(_result)
        self.assertRaises(InvalidResponse, ved.check_valid, response=None)

    def test_check_valid_short(self):
        """ test ved protocol returns false for a short response validation check """
        ved = VictronEnergyDirect()

        # print(_result)
        self.assertRaises(InvalidResponse, ved.check_valid, response=b"12")

    def test_check_valid_missing(self):
        """ test ved protocol returns false for a short response validation check """
        ved = VictronEnergyDirect()
        # _result = ved.check_valid(response=b"70010007800C6\n", command_definition=cd)

        # print(_result)
        self.assertRaises(InvalidResponse, ved.check_valid, response=b"70010007800C6\n", command_definition=cd)

    def test_build_result_battery_capacity(self):
        """ test result build for battery capacity"""
        expected = ['battery_capacity=120Ah']
        simple_formatter = SimpleFormat({"extra_info": True})

        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        command = Command.from_config({"command": "battery_capacity"})
        command.command_definition = cd
        ved = VictronEnergyDirect()
        raw_response = b":70010007800C6\n"

        _result = command.build_result(raw_response=raw_response, protocol=ved)

        formatted_data = simple_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_build_result_missing(self):
        """ test result build with invalid response"""
        expected = ['Error Count: 1', "Error #0: Response incomplete - missing ':'"]
        simple_formatter = SimpleFormat({"extra_info": True})

        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        command = Command.from_config({"command": "battery_capacity"})
        command.command_definition = cd
        ved = VictronEnergyDirect()
        raw_response = b"70010007800C6\n"

        _result = command.build_result(raw_response=raw_response, protocol=ved)
        # print(_result)

        formatted_data = simple_formatter.format(command, _result, device_info)
        # print(formatted_data)
        self.assertEqual(formatted_data, expected)

    def test_full_command_missing_command_code(self):
        """ ensure an exception is raised if the command_code is missing in the protocol definition """
        command_definition_config = {"batCap": {"name": "batCap",
                                                "description": "Battery Capacity",
                                                "help": " -- display the Battery Capacity",
                                                "command_type": CommandType.VICTRON_GET,
                                                "result_type": ResultType.SINGLE,
                                                "reading_definitions": [{"description": "Command type", "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.INT}]}}
        ved = VictronEnergyDirect()
        ved.add_command_definitions(command_definitions_config=command_definition_config)
        self.assertRaises(CommandError, ved.get_full_command, command="batCap")
