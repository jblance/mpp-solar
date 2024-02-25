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
