import unittest
from mppsolar.protocols.daly import daly as pi


class test_daly_decode(unittest.TestCase):
    def test_daly_SOC(self):
        """ test the decode of a SOC response"""
        protocol = pi()

        response = b"\xa5\x01\x90\x08\x02\x14\x00\x00uE\x03x\x89"
        command = "SOC"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": ["¥\x01\x90\x08\x02\x14\x00\x00uE\x03x\x89", ""],
            "_command": "SOC",
            "_command_description": "State of Charge",
            "Battery Bank Voltage": [53.2, "V"],
            "acquistion": [0.0, "V"],
            "Current": [2.1, "A"],
            "SOC": [88.8, "%"],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_daly_cellMinMax(self):
        """ test the decode of a cellMinMax response"""
        protocol = pi()
        response = b"\xa5\x01\x91\x08\r\x00\x0f\x0c\xfe\x01\x03x\xe1"
        command = "cellMinMax"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": ["¥\x01\x91\x08\r\x00\x0f\x0cþ\x01\x03xá", ""],
            "_command": "cellMinMax",
            "_command_description": "Cell Minimum and Maximum Voltages",
            "Maximum Cell Voltage": [3.328, "V"],
            "Maximum Cell Number": [15, ""],
            "Minimum Cell Voltage": [3.326, "V"],
            "Minimum Cell Number": [1, ""],
            "SOC": [88.8, "%"],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_daly_status(self):
        """ test the decode of a cellMinMax response"""
        protocol = pi()
        response = b"\xa5\x01\x94\x08\x10\x01\x00\x00\x00\x00\x03@\x96"
        command = "status"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": ["¥\x01\x94\x08\x10\x01\x00\x00\x00\x00\x03@\x96", ""],
            "_command": "status",
            "_command_description": "Status Information",
            "Battery String": ["10", ""],
            "Temperature": ["01", ""],
            "Charger Status": ["disconnected", ""],
            "Load Status": ["disconnected", ""],
            "Flags (TODO)": ["00", ""],
            "Charge/Discharge Cycles": [3, "cycles"],
            "Reserved": ["40", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
