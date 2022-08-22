import unittest
from mppsolar.protocols.jk02 import jk02 as pi


class test_jk02_decode(unittest.TestCase):
    maxDiff = None

    def test_getInfo(self):
        """test the decode of a getInfo response"""
        protocol = pi()
        response = bytes.fromhex(
            "55aaeb9003f14a4b2d42324132345300000000000000332e300000000000332e322e330000000876450004000000506f7765722057616c6c203100000000313233340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c2"
        )
        command = "getInfo"
        expected = {
            "raw_response": [
                "Uªë\x90\x03ñJK-B2A24S\x00\x00\x00\x00\x00\x00\x003.0\x00\x00\x00\x00\x003.2.3\x00\x00\x00\x08vE\x00\x04\x00\x00\x00Power Wall 1\x00\x00\x00\x001234\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Â",
                "",
            ],
            "_command": "getInfo",
            "_command_description": "BLE Device Information inquiry",
            "Header": ["55aaeb90", ""],
            "Record Type": ["03", ""],
            "Record Counter": [241, ""],
            "Device Model": ["JK-B2A24S", ""],
            "Hardware Version": ["3.0", ""],
            "Software Version": ["3.2.3", ""],
            "Device Name": ["Power Wall 1", ""],
            "Device Passcode": ["1234", ""],
            "Manufacturing Date": ["", ""],
            "Passcode": ["", ""],
            "Power-on Times": [4, ""],
            "Serial Number": ["", ""],
            "Up Time": ["52D16H30M0S", ""],
            "User Data": ["", ""],
            "Setup Passcode": ["", ""],
        }
        protocol.get_full_command(command)
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_getCellData(self):
        """test the decode of a getCellData response"""
        protocol = pi()
        response = bytes.fromhex(
            "55aaeb9002b52e0d280dfa0c2e0d2f0d220d220d130d190d1d0d1d0d170d1f0d160dfb0c1f0d00000000000000000000000000000000ffff00001c0d350004029b00c600a000b300bc00cc00be00b100b4002d013d01b000a100ab00b200ad0000000000000000000000000000000000000000000000bcd1000000000000000000001e0116013c010000000000636b0c0300400d030000000000dc4d010064000000781e16000101480a000000000000000000000000070101000000980400000000260141400000000037feffff00000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080"
        )
        command = "getCellData"
        expected = {
            "raw_response": [
                'Uªë\x90\x02µ.\r(\rú\x0c.\r/\r"\r"\r\x13\r\x19\r\x1d\r\x1d\r\x17\r\x1f\r\x16\rû\x0c\x1f\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ÿÿ\x00\x00\x1c\r5\x00\x04\x02\x9b\x00Æ\x00\xa0\x00³\x00¼\x00Ì\x00¾\x00±\x00´\x00-\x01=\x01°\x00¡\x00«\x00²\x00\xad\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00¼Ñ\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x01\x16\x01<\x01\x00\x00\x00\x00\x00ck\x0c\x03\x00@\r\x03\x00\x00\x00\x00\x00ÜM\x01\x00d\x00\x00\x00x\x1e\x16\x00\x01\x01H\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x01\x01\x00\x00\x00\x98\x04\x00\x00\x00\x00&\x01A@\x00\x00\x00\x007þÿÿ\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80',
                "",
            ],
            "_command": "getCellData",
            "_command_description": "BLE Cell Data inquiry",
            "Header": ["55aaeb90", ""],
            "Record_Type": ["02", ""],
            "Record_Counter": [181, ""],
            "Voltage_Cell01": [3.374, "V"],
            "Voltage_Cell02": [3.368, "V"],
            "Voltage_Cell03": [3.322, "V"],
            "Voltage_Cell04": [3.374, "V"],
            "Voltage_Cell05": [3.375, "V"],
            "Voltage_Cell06": [3.362, "V"],
            "Voltage_Cell07": [3.362, "V"],
            "Voltage_Cell08": [3.347, "V"],
            "Voltage_Cell09": [3.353, "V"],
            "Voltage_Cell10": [3.357, "V"],
            "Voltage_Cell11": [3.357, "V"],
            "Voltage_Cell12": [3.351, "V"],
            "Voltage_Cell13": [3.359, "V"],
            "Voltage_Cell14": [3.35, "V"],
            "Voltage_Cell15": [3.323, "V"],
            "Voltage_Cell16": [3.359, "V"],
            "Voltage_Cell17": [0.0, "V"],
            "Voltage_Cell18": [0.0, "V"],
            "Voltage_Cell19": [0.0, "V"],
            "Voltage_Cell20": [0.0, "V"],
            "Voltage_Cell21": [0.0, "V"],
            "Voltage_Cell22": [0.0, "V"],
            "Voltage_Cell23": [0.0, "V"],
            "Voltage_Cell24": [0.0, "V"],
            "Average_Cell_Voltage": [3.356, "V"],
            "Delta_Cell_Voltage": [0.053, "V"],
            "Current_Balancer": [0.516, ""],
            "Resistance_Cell01": [0.155, "Ohm"],
            "Resistance_Cell02": [0.198, "Ohm"],
            "Resistance_Cell03": [0.16, "Ohm"],
            "Resistance_Cell04": [0.179, "Ohm"],
            "Resistance_Cell05": [0.188, "Ohm"],
            "Resistance_Cell06": [0.204, "Ohm"],
            "Resistance_Cell07": [0.19, "Ohm"],
            "Resistance_Cell08": [0.177, "Ohm"],
            "Resistance_Cell09": [0.18, "Ohm"],
            "Resistance_Cell10": [0.301, "Ohm"],
            "Resistance_Cell11": [0.317, "Ohm"],
            "Resistance_Cell12": [0.176, "Ohm"],
            "Resistance_Cell13": [0.161, "Ohm"],
            "Resistance_Cell14": [0.171, "Ohm"],
            "Resistance_Cell15": [0.178, "Ohm"],
            "Resistance_Cell16": [0.173, "Ohm"],
            "Resistance_Cell17": [0.0, "Ohm"],
            "Resistance_Cell18": [0.0, "Ohm"],
            "Resistance_Cell19": [0.0, "Ohm"],
            "Resistance_Cell20": [0.0, "Ohm"],
            "Resistance_Cell21": [0.0, "Ohm"],
            "Resistance_Cell22": [0.0, "Ohm"],
            "Resistance_Cell23": [0.0, "Ohm"],
            "Resistance_Cell24": [0.0, "Ohm"],
            "Battery_Voltage": [53.692, "V"],
            "Battery_Power": [0, "W"],
            "Balance_Current": [0.0, "A"],
            "Battery_T1": [28.6, "°C"],
            "Battery_T2": [27.8, "°C"],
            "MOS_Temp": [31.6, "°C"],
            "Percent_Remain": [99, "%"],
            "Capacity_Remain": [199.787, "Ah"],
            "Nominal_Capacity": [200.0, "Ah"],
            "Cycle_Count": [0, ""],
            "Cycle_Capacity": [85.468, "Ah"],
            "Time": ["16D18H39M52S", ""],
            "Current_Charge": [0.004, ""],
            "Current_Discharge": [0.0, ""],
        }
        protocol.get_full_command(command)
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
