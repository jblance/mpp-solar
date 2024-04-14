import unittest
from mppsolar.protocols.jk232 import jk232 as pi


class test_jk232_decode(unittest.TestCase):
    maxDiff = None

    def test_getBalancerData(self):
        """test the decode of a getBalancerData response"""
        protocol = pi()
        response = bytes.fromhex(
            "DD 03 00 1B 17 00 00 00 02 D0 03 E8 00 00 20 78 00 00 00 00 00 00 10 48 03 0F 02 0B 76 0B 82 FB FF 77"
        )
        command = "getBalancerData"
        expected = {
            "raw_response": [
                "Ý\x03\x00\x1b\x17\x00\x00\x00\x02Ð\x03è\x00\x00 x\x00\x00\x00\x00\x00\x00\x10H\x03\x0f\x02\x0bv\x0b\x82ûÿw",
                "",
            ],
            "_command": "getBalancerData",
            "_command_description": "Get Balancer Data",
            "Start Byte": ["dd", ""],
            "Command Code": ["03", ""],
            "Status": ["00", ""],
            "Data Length": [27, ""],
            "Total Battery Voltage": [58.88, "V"],
            "Total Current": [0.0, "A"],
            "Remaining Capacity": [7.2, "Ah"],
            "Nominal Capacity": [10.0, "Ah"],
            "Cycles": [0, "cycles"],
            "Production Date": ["2078", ""],
            "Equilibrium State (TODO)": ["0000", ""],
            "Equilibrium State 2 (TODO)": ["0000", ""],
            "Protection State (TODO)": ["0000", ""],
            "Keep": ["10", ""],
            "Remaining Battery": [72, "%"],
            "FET Control Status": ["03", ""],
            "Number of Battery Strings": [15, ""],
            "Number of NTC": [2, ""],
            "NTC 1": [20.3, "°C"],
            "NTC 2": [21.5, "°C"],
            "Checksum": ["fbff", ""],
            "End Byte": ["77", ""],
        }
        protocol.get_full_command(command)
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
