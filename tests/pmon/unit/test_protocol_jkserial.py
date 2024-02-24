""" tests / pmon / unit / test_protocol_jkserial.py """
import unittest

from powermon.commands.command_definition import CommandDefinition
from powermon.commands.result import ResultType
from powermon.errors import InvalidResponse, PowermonProtocolError
from powermon.ports.abstractport import AbstractPort
from powermon.ports.serialport import SerialPort
from powermon.ports.testport import TestPort
from powermon.ports.usbport import USBPort
from powermon.protocols import get_protocol_definition

command_definitions_config = {"name": "batteryCapacity",
                              "description": "Battery Capacity",
                              "help": " -- display the Battery Capacity",
                              "result_type": ResultType.CONSTRUCT,
                              "reading_definitions": [{"index": "cell_count", "description": "Cell Count"}]}
cd = CommandDefinition.from_config(command_definitions_config)
protocol = get_protocol_definition(protocol="jkserial")


class TestProtocolJKSerial(unittest.TestCase):
    """ exercise different functions in jkserial protocol """

    def test_check_crc(self):
        """ test a for correct CRC validation """
        result = protocol.check_crc(response=b"\x00\x1a:70010007800C6\n", command_definition=cd)
        self.assertTrue(result)

    def test_check_valid(self):
        """ test for True response to a valid response """
        response = b'NW\x01\x1b\x00\x00\x00\x00\x03\x00\x01y*\x01\x0f\x90\x02\x0f\x91\x03\x0f\x94\x04\x0f\x8e\x05\x0f\x92\x06\x0f\x91\x07\x0f\x91\x08\x0f\x91\t\x0f\x93\n\x0f\x8e\x0b\x0f\x91\x0c\x0f\x90\r\x0f\x90\x0e\x0f\x8d\x80\x00!\x81\x00\x1c\x82\x00\x1e\x83\x15\xca\x84\x81\xc5\x85d\x86\x02\x87\x00\x19\x89\x00\x00\x16\xda\x8a\x00\x0e\x8b\x00\x00\x8c\x00\x03\x8e\x16\xb2\x8f\x10\xf4\x90\x106\x91\x10\x04\x92\x00\x05\x93\x0c\x1c\x94\x0c\x80\x95\x00\x05\x96\x01,\x97\x00n\x98\x01,\x99\x00U\x9a\x00\x1e\x9b\x0b\xb8\x9c\x002\x9d\x01\x9e\x00Z\x9f\x00F\xa0\x00d\xa1\x00d\xa2\x00\x14\xa3\x00<\xa4\x00<\xa5\x00\x01\xa6\x00\x03\xa7\xff\xec\xa8\xff\xf6\xa9\x0e\xaa\x00\x00\x00\xea\xab\x01\xac\x01\xad\x047\xae\x01\xaf\x01\xb0\x00\n\xb1\x14\xb2123456\x00\x00\x00\x00\xb3\x00\xb4Input Us\xb52306\xb6\x00\x01\x82\xe3\xb711.XW_S11.261__\xb8\x00\xb9\x00\x00\x00\xea\xbaInput UserdaJK_B1A20S15P\xc0\x01\x00\x00\x00\x00h\x00\x00Q\xd6'
        result = protocol.check_valid(response=response, command_definition=cd)
        # print(result)
        self.assertTrue(result)

    def test_check_valid_short(self):
        """ test for exception response to a short response """
        response = b'NW'
        self.assertRaises(InvalidResponse, protocol.check_valid, response=response, command_definition=cd)

    def test_check_valid_none(self):
        """ test for exception response to a None response """
        response = None
        self.assertRaises(InvalidResponse, protocol.check_valid, response=response, command_definition=cd)

    def test_check_valid_incorrect_start(self):
        """ test for exception response to a response that doesnt have correct start """
        response = b'NY\x01\x1b'
        self.assertRaises(InvalidResponse, protocol.check_valid, response=response, command_definition=cd)

    def test_port_supported_serial(self):
        """ test that jkserial protocol is supported on SerialPort"""
        _port = SerialPort("/dev/tty0", 9600, protocol, "id")
        self.assertIsInstance(_port, AbstractPort)

    def test_port_notsupported_usb(self):
        """ test that jkserial protocol is not supported on UsbPort"""
        self.assertRaises(PowermonProtocolError, USBPort, "path", protocol, "id")
        # self.assertIsInstance(sp, AbstractPort)

    def test_port_supported_test(self):
        """ test that jkserial protocol is supported on TestPort"""
        _port = TestPort("path", protocol)
        self.assertIsInstance(_port, AbstractPort)

    def test_full_command_all_data(self):
        """ test for full command generation for all data"""
        result = protocol.get_full_command(command="all_data")
        expected = bytearray(b'NW\x00\x13\x00\x00\x00\x00\x06\x03\x00\x00\x00\x00\x00\x00h\x00\x00\x01)')
        # print(result)
        # print(expected)
        self.assertEqual(expected, result)

    def test_get_full_command_battery_voltage(self):
        """ test full command generation for battery voltage command """
        result = protocol.get_full_command(command="battery_voltage")
        expected = bytearray(b'NW\x00\x13\x00\x00\x00\x00\x03\x03\x00\x83\x00\x00\x00\x00h\x00\x00\x01\xa9')
        # print(result)
        # print(expected)
        self.assertEqual(expected, result)
