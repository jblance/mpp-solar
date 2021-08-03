import unittest
from mppsolar.protocols.pi17 import pi17 as pi


class test_pi17_decode(unittest.TestCase):
    maxDiff = None

    def test_pi17_PI(self):
        """test the decode of a PI response"""
        protocol = pi()
        response = b"^D00517\xca\xec\r"
        command = "PI"
        expected = {
            "raw_response": ["^D00517Êì\r", ""],
            "_command": "PI",
            "_command_description": "Device Protocol Version inquiry",
            "Protocol Version": ["17", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
