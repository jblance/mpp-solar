import subprocess
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


class test_pi18_fullcommands(unittest.TestCase):
    maxDiff = None

    def test_pi18_fullcommand_et(self):
        """test the build of full command et"""
        protocol = pi()
        result = protocol.get_full_command("ET")
        expected = b"^P005ETN\x91\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_ey(self):
        """test the build of full command ey"""
        protocol = pi()
        result = protocol.get_full_command("EY2022")
        expected = b"^P009EY2022\x81\x1c\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_id(self):
        """test the build of full command id"""
        protocol = pi()
        result = protocol.get_full_command("ID")
        expected = b"^P005ID\x19\xcd\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_vfw(self):
        """test the build of full command vfw"""
        protocol = pi()
        result = protocol.get_full_command("VFW")
        expected = b"^P006VFW\xf6\xe6\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_piri(self):
        """test the build of full command piri"""
        protocol = pi()
        result = protocol.get_full_command("PIRI")
        expected = b"^P007PIRI\xee8\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_gs(self):
        """test the build of full command gs"""
        protocol = pi()
        result = protocol.get_full_command("GS")
        expected = b"^P005GSX\x14\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_mod(self):
        """test the build of full command mod"""
        protocol = pi()
        result = protocol.get_full_command("MOD")
        expected = b"^P006MOD\xdd\xbe\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_flag(self):
        """test the build of full command flag"""
        protocol = pi()
        result = protocol.get_full_command("FLAG")
        expected = b"^P007FLAG\x8e\x18\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_mchgcr(self):
        """test the build of full command mchgcr"""
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

    def test_pi18_fullcommand_PI(self):
        """test the build of full command PI"""
        protocol = pi()
        result = protocol.get_full_command("PI")
        expected = b"^P005PIq\x8b\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_POP(self):
        """test the build of full command POP"""
        protocol = pi()
        result = protocol.get_full_command("POP0")
        expected = b"^S007POP0\x1d1\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PSP(self):
        """test the build of full command PSP"""
        protocol = pi()
        result = protocol.get_full_command("PSP1")
        expected = b"^S007PSP1;\x12\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEI(self):
        """test the build of full command PEI"""
        protocol = pi()
        result = protocol.get_full_command("PEI")
        expected = b"^S006PEI:h\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDI(self):
        """test the build of full command PDI"""
        protocol = pi()
        result = protocol.get_full_command("PDI")
        expected = b"^S006PDI\tY\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PCP(self):
        """test the build of full command PCP"""
        protocol = pi()
        result = protocol.get_full_command("PCP0,1")
        expected = b"^S009PCP0,1\x8f\x07\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MCHGC(self):
        """test the build of full command MCHGC"""
        protocol = pi()
        result = protocol.get_full_command("MCHGC0,030")
        expected = b"^S013MCHGC0,030\xc4\xee\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MUCHGC(self):
        """test the build of full command MUCHGC"""
        protocol = pi()
        result = protocol.get_full_command("MUCHGC0,030")
        expected = b"^S014MUCHGC0,030\xee\xdd\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PBT(self):
        """test the build of full command PBT"""
        protocol = pi()
        result = protocol.get_full_command("PBT0")
        expected = b"^S007PBT0\x93\xa4\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MCHGV(self):
        """test the build of full command MCHGV"""
        protocol = pi()
        result = protocol.get_full_command("MCHGV552,540")
        expected = b"^S015MCHGV552,540\x88\xe8\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PSDV(self):
        """test the build of full command PSDV"""
        protocol = pi()
        result = protocol.get_full_command("PSDV450")
        expected = b"^S010PSDV450,\x8b\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_BUCD(self):
        """test the build of full command BUCD"""
        protocol = pi()
        result = protocol.get_full_command("BUCD440,480")
        expected = b"^S014BUCD440,480\xa5]\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_getdevice_id(self):
        try:
            expected = "18:5220\n"
            result = subprocess.run(
                ["mpp-solar", "-p", "test", "-P", "pi18", "--getDeviceId", "-o", "value"],
                check=True,
                capture_output=True,
                text=True,
            )
            # print(result.stdout)
            self.assertEqual(result.stdout, expected)
            self.assertEqual(result.returncode, 0)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error
