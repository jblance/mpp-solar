import subprocess
import unittest

from mppsolar.protocols.pi16 import pi16 as pi


class test_pi16_decode(unittest.TestCase):
    maxDiff = None

    def test_pi16_QPI(self):
        """test the decode of a QPI response"""
        protocol = pi()
        response = b"(PI16\x9c\xaf\r"
        command = "QPI"
        expected = {
            "raw_response": ["(PI16\x9c¯\r", ""],
            "_command": "QPI",
            "_command_description": "Device Protocol Version inquiry",
            "Protocol Version": ["PI16", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi16_QED(self):
        """test the decode of a QED response"""
        protocol = pi()
        response = b"(012345\x9c\xaf\r"
        command = "QED12345678"
        expected = {
            "raw_response": ["(012345\x9c¯\r", ""],
            "_command": "QED12345678",
            "_command_description": "Query energy produced for a specific day",
            "Energy produced": [12345, "Wh"],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi16_QPIBI(self):
        """test the decode of a QPIBI response"""
        protocol = pi()
        response = b"(0 6 1234 12 43\xb7\x6c\r"
        command = "QPIBI"
        expected = {
            "raw_response": ["(0 6 1234 12 43·l\r", ""],
            "_command": "QPIBI",
            "_command_description": "Battery information query",
            "unknown": [0, ""],
            "Number of batteries": [6, "#"],
            "Battery total capacity": [1234, "Ah"],
            "unknown_2": [12, ""],
            "Battery remaining time": [43, "min"],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi16_QMOD_badkey(self):
        """test the decode of a QMOD response - with a bad key"""
        protocol = pi()
        response = b"(012345\x9c\xaf\r"
        command = "QMOD"
        expected = {
            "raw_response": ["(012345\x9c¯\r", ""],
            "_command": "QMOD",
            "_command_description": "Operational mode query",
            "Device Mode": ["Invalid key: 012345", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi16_QMOD(self):
        """test the decode of a QMOD response"""
        protocol = pi()
        response = b"(B\x9c\xaf\r"
        command = "QMOD"
        expected = {
            "raw_response": ["(B\x9c¯\r", ""],
            "_command": "QMOD",
            "_command_description": "Operational mode query",
            "Device Mode": ["Inverter (Battery) Mode", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi16_QPIGS(self):
        """test the decode of a QPIGS response"""
        protocol = pi()
        response = b"(224.6 000000 49.9 0006.8 232.4 01594 49.9 006.8 029 415.0 415.0 057.9 ---.- 100 00000 00000 ----- 000.0 000.0 ---.- 035.0 D---110001k\xdb\r"
        command = "QPIGS"
        expected = {
            "raw_response": [
                "(224.6 000000 49.9 0006.8 232.4 01594 49.9 006.8 029 415.0 415.0 057.9 ---.- 100 00000 00000 ----- 000.0 000.0 ---.- 035.0 D---110001kÛ\r",
                "",
            ],
            "_command": "QPIGS",
            "_command_description": "General status query",
            "Grid voltage": [224.6, "V"],
            "Output power": [0, "W"],
            "Grid frequency": [49.9, "Hz"],
            "Output current": [6.8, "A"],
            "AC output voltage R": [232.4, "V"],
            "AC output power R": [1594, "W"],
            "AC output frequency": [49.9, "Hz"],
            "AC output current R": [6.8, "A"],
            "Output load percent": [29, "%"],
            "PBUS voltage": [415.0, "V"],
            "SBUS voltage": [415.0, "V"],
            "Positive battery voltage": [57.9, "V"],
            "Negative battery voltage": [0, "V"],
            "Battery capacity": [100, "%"],
            "PV1 input power": [0, "W"],
            "PV2 input power": [0, "W"],
            "PV3 input power": [0, "W"],
            "PV1 input voltage": [0.0, "V"],
            "PV2 input voltage": [0.0, "V"],
            "PV3 input voltage": [0, "V"],
            "Max temperature": [35.0, "°C"],
            "status TODO": ["D---110001", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi16_QPIRI(self):
        """test the decode of a QPIRI response"""
        protocol = pi()
        response = b"(230.0 50.0 013.0 230.0 013.0 18.0 048.0 1 10 0\x86\x42\r"
        command = "QPIRI"
        expected = {
            "raw_response": ["(230.0 50.0 013.0 230.0 013.0 18.0 048.0 1 10 0\x86B\r", ""],
            "_command": "QPIRI",
            "_command_description": "Device rating inquiry",
            "Grid Input Voltage Rating": [230.0, "V"],
            "Grid Input Frequency Rating": [50.0, "Hz"],
            "Grid Input Current Rating": [13.0, "A"],
            "AC Output Voltage Rating": [230.0, "V"],
            "AC Output Current Rating": [13.0, "A"],
            "Maximum input current per PV": [18.0, "A"],
            "Battery Voltage Rating": [48.0, "V"],
            "Number of MPP trackers": [1, ""],
            "Machine Type": ["Hybrid", ""],
            "Topology": ["transformerless", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi16_getdevice_id(self):
        try:
            expected = "PI16:000:00000.27\n"
            result = subprocess.run(
                ["mpp-solar", "-p", "test", "-P", "pi16", "--getDeviceId", "-o", "value"],
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
