import unittest
from mppsolar.protocols.protocol_helpers import Hex2Int, Hex2Str
from mppsolar.protocols.protocol_helpers import BigHex2Float


class test_protocol_helpers(unittest.TestCase):
    def test_Hex2Int(self):
        """ test the Hex2Int"""
        result = Hex2Int(bytes.fromhex("64"))
        expected = 100
        # print(result)
        self.assertEqual(result, expected)

    def test_Hex2Str(self):
        """ test the Hex2Str"""
        result = Hex2Str(bytes.fromhex("AE0212"))
        expected = "ae0212"
        # print(result)
        self.assertEqual(result, expected)

    def test_BigHex2Float(self):
        """ test BigHex2Float """
        hexString = b"\x00\x03\xcb@"
        result = BigHex2Float(hexString)
        expected = 248640
        # print(result)
        self.assertEqual(result, expected)
