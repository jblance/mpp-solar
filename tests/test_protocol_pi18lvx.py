import subprocess
import unittest

from mppsolar.protocols.pi18lvx import pi18lvx as pi


class test_pi18_decode(unittest.TestCase):
    maxDiff = None

    def test_pi18lvx_PI(self):
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


class test_pi18lvx_fullcommands(unittest.TestCase):
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
        expected = b"^P013ED20231217\r"
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
        expected = b"^P006VFW\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MCHGCR(self):
        """test the build of full command MCHGCR"""
        protocol = pi()
        result = protocol.get_full_command("MCHGCR")
        expected = b'^P009MCHGCR\r'
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MUCHGCR(self):
        """test the build of full command MUCHGCR"""
        protocol = pi()
        result = protocol.get_full_command("MUCHGCR")
        expected = b"^P010MUCHGCR\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PRI(self):
        """test the build of full command PRI"""
        protocol = pi()
        result = protocol.get_full_command("PRI0")
        expected = b"^P007PRI0\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PGS(self):
        """test the build of full command PGS"""
        protocol = pi()
        result = protocol.get_full_command("PGS0")
        expected = b"^P007PGS0\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_FWS(self):
        """test the build of full command FWS"""
        protocol = pi()
        result = protocol.get_full_command("FWS")
        expected = b"^P005FWS\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_DI(self):
        """test the build of full command DI"""
        protocol = pi()
        result = protocol.get_full_command("DI")
        expected = b"^P005DI\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PIRI(self):
        """test the build of full command PIRI"""
        protocol = pi()
        result = protocol.get_full_command("PIRI")
        expected = b"^P007PIRI\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_GS(self):
        """test the build of full command GS"""
        protocol = pi()
        result = protocol.get_full_command("GS")
        expected = b"^P005GS\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MOD(self):
        """test the build of full command MOD"""
        protocol = pi()
        result = protocol.get_full_command("MOD")
        expected = b"^P006MOD\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_FLAG(self):
        """test the build of full command FLAG"""
        protocol = pi()
        result = protocol.get_full_command("FLAG")
        expected = b"^P007FLAG\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_ACCT(self):
        """test the build of full command ACCT"""
        protocol = pi()
        result = protocol.get_full_command("ACCT")
        expected = b"^P005ACCT\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_ACLT(self):
        """test the build of full command ACLT"""
        protocol = pi()
        result = protocol.get_full_command("ACLT")
        expected = b"^P005ACLT\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_LON(self):
        """test the build of full command LON"""
        protocol = pi()
        result = protocol.get_full_command("LON0")
        expected = b"^S007LON0\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEA(self):
        """test the build of full command PEA"""
        protocol = pi()
        result = protocol.get_full_command("PEA")
        expected = b"^S006PEA\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDA(self):
        """test the build of full command PDA"""
        protocol = pi()
        result = protocol.get_full_command("PDA")
        expected = b"^S006PDA\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEB(self):
        """test the build of full command PEB"""
        protocol = pi()
        result = protocol.get_full_command("PEB")
        expected = b"^S006PEB\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDB(self):
        """test the build of full command PDB"""
        protocol = pi()
        result = protocol.get_full_command("PDB")
        expected = b"^S006PDB\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEC(self):
        """test the build of full command PEC"""
        protocol = pi()
        result = protocol.get_full_command("PEC")
        expected = b'^S006PEC\r'
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDC(self):
        """test the build of full command PDC"""
        protocol = pi()
        result = protocol.get_full_command("PDC")
        expected = b"^S006PDC\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PED(self):
        """test the build of full command PED"""
        protocol = pi()
        result = protocol.get_full_command("PED")
        expected = b"^S006PED\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDD(self):
        """test the build of full command PDD"""
        protocol = pi()
        result = protocol.get_full_command("PDD")
        expected = b"^S006PDD\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEE(self):
        """test the build of full command PEE"""
        protocol = pi()
        result = protocol.get_full_command("PEE")
        expected = b"^S006PEE\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDE(self):
        """test the build of full command PDE"""
        protocol = pi()
        result = protocol.get_full_command("PDE")
        expected = b"^S006PDE\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEF(self):
        """test the build of full command PEF"""
        protocol = pi()
        result = protocol.get_full_command("PEF")
        expected = b"^S006PEF\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDF(self):
        """test the build of full command PDF"""
        protocol = pi()
        result = protocol.get_full_command("PDF")
        expected = b"^S006PDF\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEG(self):
        """test the build of full command PEG"""
        protocol = pi()
        result = protocol.get_full_command("PEG")
        expected = b"^S006PEG\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDG(self):
        """test the build of full command PDG"""
        protocol = pi()
        result = protocol.get_full_command("PDG")
        expected = b"^S006PDG\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEH(self):
        """test the build of full command PEH"""
        protocol = pi()
        result = protocol.get_full_command("PEH")
        expected = b"^S006PEH\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDH(self):
        """test the build of full command PDH"""
        protocol = pi()
        result = protocol.get_full_command("PDH")
        expected = b"^S006PDH\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PEI(self):
        """test the build of full command PEI"""
        protocol = pi()
        result = protocol.get_full_command("PEI")
        expected = b"^S006PEI\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PDI(self):
        """test the build of full command PDI"""
        protocol = pi()
        result = protocol.get_full_command("PDI")
        expected = b"^S006PDI\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_PF(self):
        """test the build of full command PF"""
        protocol = pi()
        result = protocol.get_full_command("PF")
        expected = b"^S005PF\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MCHGC(self):
        """test the build of full command MCHGC"""
        protocol = pi()
        result = protocol.get_full_command("MCHGC0,050")
        expected = b"^S013MCHGC0,050\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MUCHGC(self):
        """test the build of full command MUCHGC"""
        protocol = pi()
        result = protocol.get_full_command("MUCHGC0,050")
        expected = b"^S014MUCHGC0,050\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_MCHGV(self):
        """test the build of full command MCHGV"""
        protocol = pi()
        result = protocol.get_full_command("MCHGV564,540")
        expected = b"^S015MCHGV564,540\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_DAT(self):
        """test the build of full command DAT"""
        protocol = pi()
        result = protocol.get_full_command("DAT190518224530")
        expected = b"^S018DAT190518224530\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_POP(self):
        """test the build of full command POP"""
        protocol = pi()
        result = protocol.get_full_command("POP0")
        expected = b"^S007POP0\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18_fullcommand_BUCD(self):
        """test the build of full command BUCD"""
        protocol = pi()
        result = protocol.get_full_command("BUCD440,480")
        expected = b"^S014BUCD440,480\r"
        # print(result)
        self.assertEqual(result, expected)

    def test_pi18lvx_getdevice_id(self):
        try:
            expected = "18:5402\n"
            result = subprocess.run(
                ["mpp-solar", "-p", "test", "-P", "pi18lvx", "--getDeviceId", "-o", "value"],
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
