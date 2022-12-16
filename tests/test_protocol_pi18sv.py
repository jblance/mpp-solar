import unittest
from mppsolar.protocols.pi18sv import pi18sv as pi


class test_pi18_decode(unittest.TestCase):
    maxDiff = None

    def test_pi18sv_PI(self):
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


class test_pi18sv_fullcommands(unittest.TestCase):
    maxDiff = None

    def test_pi18_fullcommand_PI(self):
        """test the build of full command PI"""
        protocol = pi()
        result = protocol.get_full_command("PI")
        expected = b"^P005PI\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_T(self):
        """test the build of full command T"""
        protocol = pi()
        result = protocol.get_full_command("T")
        expected = b"^P004T\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_ET(self):
        """test the build of full command ET"""
        protocol = pi()
        result = protocol.get_full_command("ET")
        expected = b"^P005ET\r"
        # print(result)
        self.assertEqual(result, expected)
