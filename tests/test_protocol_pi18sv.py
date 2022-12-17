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

    def test_pi18_fullcommand_EY(self):
        """test the build of full command EY"""
        protocol = pi()
        result = protocol.get_full_command("EY2023")
        expected = b"^P009EY2023\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_EM(self):
        """test the build of full command EM"""
        protocol = pi()
        result = protocol.get_full_command("EM202312")
        expected = b"^P011EM202312\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_ED(self):
        """test the build of full command ED"""
        protocol = pi()
        result = protocol.get_full_command("ED20231217")
        expected = b"^P013ED20231217\xba\xd2\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_ID(self):
        """test the build of full command ID"""
        protocol = pi()
        result = protocol.get_full_command("ID")
        expected = b"^P005ID\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_VFW(self):
        """test the build of full command VFW"""
        protocol = pi()
        result = protocol.get_full_command("VFW")
        expected = b"^P006VFW\xf6\xe6\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MCHGCR(self):
        """test the build of full command MCHGCR"""
        protocol = pi()
        result = protocol.get_full_command("MCHGCR")
        expected = b'^P009MCHGCR\xee"\r'
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MUCHGCR(self):
        """test the build of full command MUCHGCR"""
        protocol = pi()
        result = protocol.get_full_command("MUCHGCR")
        expected = b"^P010MUCHGCR\xb5\x8b\r"
        # print(result)
        self.assertEqual(result, expected)
