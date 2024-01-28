""" tests / pmon / unit / test_protocol_ved.py """
import unittest

from powermon.commands.reading_definition import ReadingType, ResponseType
from powermon.commands.result import ResultType
from powermon.errors import CommandError, InvalidResponse, InvalidCRC
from powermon.protocols.ved import VictronCommandType, VictronEnergyDirect


class TestProtocolVed(unittest.TestCase):
    """ exercise different functions in ved protocol """

    def test_check_crc(self):
        """ test a for correct CRC validation """
        ved = VictronEnergyDirect()
        _result = ved.check_crc(response=b"\x00\x1a:70010007800C6\n")
        # print(_result)
        self.assertTrue(_result)

    def test_check_crc_incorrect(self):
        """ test an exception is raised if CRC validation fails """
        ved = VictronEnergyDirect()
        self.assertRaises(InvalidCRC, ved.check_crc, response=b":70010007800C7\n")

    def test_full_command_battery_capacity(self):
        """ test a for correct build of full command - batteryCapacity """
        ved = VictronEnergyDirect()
        _result = ved.get_full_command(command="batteryCapacity")
        expected = ':70010003E\n'

        # print(_result)
        self.assertEqual(_result, expected)

    def test_full_command_vedtext(self):
        """ test a for correct build of full command - vedtext """
        ved = VictronEnergyDirect()
        _result = ved.get_full_command(command="vedtext")
        expected = VictronCommandType.LISTEN

        # print(_result)
        self.assertEqual(_result, expected)

    def test_trim(self):
        """ test ved protocol does a correct trim operation """
        ved = VictronEnergyDirect()
        _result = ved.trim_response(response=b":70010007800C6\n")
        expected = b'70010007800'

        # print(_result)
        self.assertEqual(_result, expected)

    def test_check_valid_ok(self):
        """ test ved protocol returns true for a correct response validation check """
        ved = VictronEnergyDirect()
        _result = ved.check_valid(response=b":70010007800C6\n")
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
        self.assertRaises(InvalidResponse, ved.check_valid, response="12")

    def test_full_command_missing_device_command_code(self):
        """ ensure an exception is raised if the device_command_code is missing in the protocol definition """
        command_definitions_config = {"batCap": {"name": "batCap",
                                                 "description": "Battery Capacity",
                                                 "help": " -- display the Battery Capacity",
                                                 "device_command_type": VictronCommandType.GET,
                                                 "result_type": ResultType.SINGLE,
                                                 "reading_definitions": [{"description": "Command type", "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.INT}]}}

        ved = VictronEnergyDirect()
        ved.add_command_definitions(command_definitions_config=command_definitions_config)
        self.assertRaises(CommandError, ved.get_full_command, command="batCap")
