import unittest
from mppsolar.protocols.pi18 import pi18 as pi


class test_pi18_decode(unittest.TestCase):
    maxDiff = None

    def test_pi18_PI(self):
        """test the decode of a PI response"""
        protocol = pi()
        response = b"^D00518\xca\xed\r"
        command = "PI"
        expected = {
            "raw_response": ["^D00518Êí\r", ""],
            "_command": "PI",
            "_command_description": "Device Protocol Version inquiry",
            "Protocol Version": ["18", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
