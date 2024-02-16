""" tests / pmon / unit / test_protocol_jkserial.py """
import unittest

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.result import ResultType
# from powermon.errors import InvalidResponse, PowermonProtocolError
# from powermon.ports.abstractport import AbstractPort
# from powermon.ports.serialport import SerialPort
# from powermon.ports.testport import TestPort
# from powermon.ports.usbport import USBPort
from powermon.protocols import get_protocol_definition

command_definitions_config = {"name": "batteryCapacity",
                              "description": "Battery Capacity",
                              "help": " -- display the Battery Capacity",
                              "result_type": ResultType.CONSTRUCT,
                              "reading_definitions": [{"index": "cell_count", "description": "Cell Count"}]}
cd = CommandDefinition.from_config(command_definitions_config)
protocol = get_protocol_definition(protocol="pi18")


class TestProtocolPI18(unittest.TestCase):
    """ exercise different functions in jkserial protocol """

    def test_check_crc_good(self):
        """ test a for correct CRC validation """
        response = b"^D0882300,217,2300,500,217,5000,5000,480,480,530,440,570,570,2,10,070,1,1,1,9,0,0,0,0,1,00\xe1k\r"
        result = protocol.check_crc(response=response, command_definition=cd)
        self.assertTrue(result)

    def test_check_crc_incorrect(self):
        """ test a for failing CRC validation (crc is wrong) """
        response = b"^D0882300,217,2300,500,217,5000,5000,480,480,530,440,570,570,2,10,070,1,1,1,9,0,0,0,0,1,00\xe2k\r"
        result = protocol.check_crc(response=response, command_definition=cd)
        self.assertFalse(result)

    def test_check_crc_wrong_response_start(self):
        """ test a for failing CRC validation (not a response that starts with ^D) """
        response = b"0882300,217,2300,500,217,5000,5000,480,480,530,440,570,570,2,10,070,1,1,1,9,0,0,0,0,1,00\xe1k\r"
        result = protocol.check_crc(response=response, command_definition=cd)
        self.assertFalse(result)

    def test_get_full_command_piri(self):
        """ test full command generation for PIRI command """
        fc = protocol.get_full_command('PIRI')
        # print(fc)
        expected = b'^P007PIRI\xee8\r'
        self.assertEqual(expected, fc)

    def test_get_full_command_pi(self):
        """ test full command generation for PI command """
        fc = protocol.get_full_command('PI')
        # print(fc)
        expected = b'^P005PIq\x8b\r'
        self.assertEqual(expected, fc)
