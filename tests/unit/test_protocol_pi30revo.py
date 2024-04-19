""" tests / mpp / unit / test_protocol_pi30revo.py """
import unittest

from mppsolar.protocols.pi30revo import pi30revo as pi

protocol = pi()


class test_pi30revo(unittest.TestCase):
    """ unit tests of pi30revo protocol """
    maxDiff = None

    def test_get_full_command_pset(self):
        """ test for full command generation for pset with no new line"""
        result = protocol.get_full_command("PSET120103 56.3 54.6 43.8 42.6 040 020 2020 02 18 17 06 00")
        expected = b"PSET120103 56.3 54.6 43.8 42.6 040 020 2020 02 18 17 06 00\xf7"
        # print(result)
        # print(expected)
        self.assertEqual(expected, result)

    def test_checksum_pqse(self):
        """ test for correct checksum for PQSE command """
        command = 'PQSE'
        byte_cmd = bytes(command, "utf-8")
        result = protocol.get_chk(byte_cmd)
        expected = 0x3a
        # print(hex(result))
        # print(expected)
        self.assertEqual(expected, result)

    def test_checksum_pset(self):
        """ test for correct checksum for PSET command """
        command = 'PSET120103 56.3 54.6 43.8 42.6 040 020 2020 02 18 17 06 00'
        byte_cmd = bytes(command, "utf-8")
        result = protocol.get_chk(byte_cmd)
        expected = 0xf7  # note documentation has f6 but tests have shown this is incorrect
        # print(hex(result))
        # print(expected)
        self.assertEqual(expected, result)

    def test_check_response_valid_qlith0(self):
        """ test for correctly validating valid qlith0 response """
        response = b'(052.5 000.0 000.0 032 036 000 070.0 007.0 057.0 004.6 0 5\x82\xe0\r'
        result = protocol.check_response_valid(response)[0]
        # print(result)
        self.assertTrue(result)

    def test_decode_qlith0(self):
        """ test successful decode of QLITH0 response """
        expected = {'_command': 'QLITH0', '_command_description': 'Read lithium battery information', 'raw_response': ['(052.5 000.0 000.0 032 036 000 070.0 007.0 057.0 004.6 0 5\x82à\r', ''], 'Battery voltage from BMS': [52.5, 'V'], 'Battery charging current from BMS': [0.0, 'A'], 'Battery discharge current from BMS': [0.0, 'A'], 'Battery temperature': [32, '0.1°C'], 'Battery capacity from BMS': [36, '%'], 'Battery wearout': [0, '%'], 'Battery max charging current': [70.0, 'A'], 'Battery max discharge current': [7.0, 'A'], 'Battery max charge voltage': [57.0, 'V'], 'Battery min discharge voltage': [4.6, 'V'], 'Fault Code from BMS': ['No warning', ''], 'Warning Code fom BMS': ['Battery overcurrent', '']}
        response = b'(052.5 000.0 000.0 032 036 000 070.0 007.0 057.0 004.6 0 5\x82\xe0\r'
        result = protocol.decode(response, "QLITH0")
        # print(result)
        self.assertEqual(expected, result)
