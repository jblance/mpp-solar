import unittest
from mppsolar.protocols.daly import daly as pi


class test_daly_decode(unittest.TestCase):
    maxDiff = 9999

    def test_daly_SOC(self):
        """test the decode of a SOC response"""
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

    def test_daly_cellMinMaxVoltages(self):
        """test the decode of a cellMinMaxVoltages response"""
        protocol = pi()
        response = b"\xa5\x01\x91\x08\r\x00\x0f\x0c\xfe\x01\x03x\xe1"
        command = "cellMinMaxVoltages"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": ["¥\x01\x91\x08\r\x00\x0f\x0cþ\x01\x03xá", ""],
            "_command": "cellMinMaxVoltages",
            "_command_description": "Cell Minimum and Maximum Voltages",
            "Maximum Cell Voltage": [3.328, "V"],
            "Maximum Cell Number": [15, ""],
            "Minimum Cell Voltage": [3.326, "V"],
            "Minimum Cell Number": [1, ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_daly_status(self):
        """test the decode of a status response"""
        protocol = pi()
        response = b"\xa5\x01\x94\x08\x10\x01\x00\x00\x00\x00\x03@\x96"
        command = "status"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": ["¥\x01\x94\x08\x10\x01\x00\x00\x00\x00\x03@\x96", ""],
            "_command": "status",
            "_command_description": "Status Information",
            "Number of Cells": [16, ""],
            "Number of Temperature Sensors": [1, ""],
            "Charger Status": ["disconnected", ""],
            "Load Status": ["disconnected", ""],
            "Flags (TODO)": ["00", ""],
            "Charge/Discharge Cycles": [3, "cycles"],
            "Reserved": ["40", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_daly_mosStatus(self):
        """test the decode of a mosStatus response"""
        protocol = pi()
        response = b"\xa5\x01\x93\x08\x00\x01\x01\x9a\x00\x02\xa2\xd8Y"
        command = "mosStatus"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": ["¥\x01\x93\x08\x00\x01\x01\x9a\x00\x02¢ØY", ""],
            "_command": "mosStatus",
            "_command_description": "mosStatus",
            "Charge Status": ["stationary", ""],
            "Charging MOS Tube Status": ["01", ""],
            "Discharging MOS Tube Status": ["01", ""],
            "BMS Life": [154, "cycles"],
            "Residual Capacity": [172.76, "AH"],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_daly_cellVoltages(self):
        """test the decode of a cellVoltages response"""
        protocol = pi()
        response = b"\xa5\x01\x95\x08\x01\x0c\xfd\x0c\xfe\x0c\xfe@\xa1\xa5\x01\x95\x08\x02\x0c\xfe\x0c\xfe\x0c\xfe@\xa3\xa5\x01\x95\x08\x03\x0c\xfe\x0c\xfe\x0c\xfe@\xa4\xa5\x01\x95\x08\x04\x0c\xfe\x0c\xfc\x0c\xfe@\xa3\xa5\x01\x95\x08\x05\x0c\xfe\x0c\xff\x0c\xfe@\xa7\xa5\x01\x95\x08\x06\x0c\xfc\x00\x00\x00\x00@\x91\xa5\x01\x95\x08\x07\x00\x00\x00\x00\x00\x00@\x8a\xa5\x01\x95\x08\x08\x00\x00\x00\x00\x00\x00@\x8b\xa5\x01\x95\x08\t\x00\x00\x00\x00\x00\x00@\x8c\xa5\x01\x95\x08\n\x00\x00\x00\x00\x00\x00@\x8d\xa5\x01\x95\x08\x0b\x00\x00\x00\x00\x00\x00@\x8e\xa5\x01\x95\x08\x0c\x00\x00\x00\x00\x00\x00@\x8f\xa5\x01\x95\x08\r\x00\x00\x00\x00\x00\x00@\x90\xa5\x01\x95\x08\x0e\x00\x00\x00\x00\x00\x00@\x91\xa5\x01\x95\x08\x0f\x00\x00\x00\x00\x00\x00@\x92\xa5\x01\x95\x08\x10\x00\x00\x00\x00\x00\x00@\x93"
        command = "cellVoltages"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": [
                "¥\x01\x95\x08\x01\x0cý\x0cþ\x0cþ@¡¥\x01\x95\x08\x02\x0cþ\x0cþ\x0cþ@£¥\x01\x95\x08\x03\x0cþ\x0cþ\x0cþ@¤¥\x01\x95\x08\x04\x0cþ\x0cü\x0cþ@£¥\x01\x95\x08\x05\x0cþ\x0cÿ\x0cþ@§¥\x01\x95\x08\x06\x0cü\x00\x00\x00\x00@\x91¥\x01\x95\x08\x07\x00\x00\x00\x00\x00\x00@\x8a¥\x01\x95\x08\x08\x00\x00\x00\x00\x00\x00@\x8b¥\x01\x95\x08\t\x00\x00\x00\x00\x00\x00@\x8c¥\x01\x95\x08\n\x00\x00\x00\x00\x00\x00@\x8d¥\x01\x95\x08\x0b\x00\x00\x00\x00\x00\x00@\x8e¥\x01\x95\x08\x0c\x00\x00\x00\x00\x00\x00@\x8f¥\x01\x95\x08\r\x00\x00\x00\x00\x00\x00@\x90¥\x01\x95\x08\x0e\x00\x00\x00\x00\x00\x00@\x91¥\x01\x95\x08\x0f\x00\x00\x00\x00\x00\x00@\x92¥\x01\x95\x08\x10\x00\x00\x00\x00\x00\x00@\x93",
                "",
            ],
            "_command": "cellVoltages",
            "_command_description": "Cell Voltages Information",
            "Cell 01 Voltage": [3.325, "V"],
            "Cell 02 Voltage": [3.326, "V"],
            "Cell 03 Voltage": [3.326, "V"],
            "Cell 04 Voltage": [3.326, "V"],
            "Cell 05 Voltage": [3.326, "V"],
            "Cell 06 Voltage": [3.326, "V"],
            "Cell 07 Voltage": [3.326, "V"],
            "Cell 08 Voltage": [3.326, "V"],
            "Cell 09 Voltage": [3.326, "V"],
            "Cell 10 Voltage": [3.326, "V"],
            "Cell 11 Voltage": [3.324, "V"],
            "Cell 12 Voltage": [3.326, "V"],
            "Cell 13 Voltage": [3.326, "V"],
            "Cell 14 Voltage": [3.327, "V"],
            "Cell 15 Voltage": [3.326, "V"],
            "Cell 16 Voltage": [3.324, "V"],
            "Cell 17 Voltage": [0.0, "V"],
            "Cell 18 Voltage": [0.0, "V"],
            "Cell 19 Voltage": [0.0, "V"],
            "Cell 20 Voltage": [0.0, "V"],
            "Cell 21 Voltage": [0.0, "V"],
            "Cell 22 Voltage": [0.0, "V"],
            "Cell 23 Voltage": [0.0, "V"],
            "Cell 24 Voltage": [0.0, "V"],
            "Cell 25 Voltage": [0.0, "V"],
            "Cell 26 Voltage": [0.0, "V"],
            "Cell 27 Voltage": [0.0, "V"],
            "Cell 28 Voltage": [0.0, "V"],
            "Cell 29 Voltage": [0.0, "V"],
            "Cell 30 Voltage": [0.0, "V"],
            "Cell 31 Voltage": [0.0, "V"],
            "Cell 32 Voltage": [0.0, "V"],
            "Cell 33 Voltage": [0.0, "V"],
            "Cell 34 Voltage": [0.0, "V"],
            "Cell 35 Voltage": [0.0, "V"],
            "Cell 36 Voltage": [0.0, "V"],
            "Cell 37 Voltage": [0.0, "V"],
            "Cell 38 Voltage": [0.0, "V"],
            "Cell 39 Voltage": [0.0, "V"],
            "Cell 40 Voltage": [0.0, "V"],
            "Cell 41 Voltage": [0.0, "V"],
            "Cell 42 Voltage": [0.0, "V"],
            "Cell 43 Voltage": [0.0, "V"],
            "Cell 44 Voltage": [0.0, "V"],
            "Cell 45 Voltage": [0.0, "V"],
            "Cell 46 Voltage": [0.0, "V"],
            "Cell 47 Voltage": [0.0, "V"],
            "Cell 48 Voltage": [0.0, "V"],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
