import unittest
from mppsolar.protocols.jk485 import jk485 as pi


class test_jk04_decode(unittest.TestCase):
    maxDiff = None

    def test_getBalancerData(self):
        """ test the decode of a getBalancerData response"""
        protocol = pi()
        response = bytes.fromhex(
            "EB 90 01 FF 1E D3 0F 69 14 13 02 00 00 00 07 00 00 00 05 03 E8 01 14 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 0F 69 00 16 6F"
        )
        command = "getBalancerData"
        expected = {
            "raw_response": [
                "ë\x90\x01ÿ\x1eÓ\x0fi\x14\x13\x02\x00\x00\x00\x07\x00\x00\x00\x05\x03è\x01\x14\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x0fi\x00\x16o",
                "",
            ],
            "_command": "getBalancerData",
            "_command_description": "Get Balancer Data",
            "Header": ["eb90", ""],
            "Slave Address": ["01", ""],
            "Command Code": ["ff", ""],
            "Total Battery Voltage": [78.91, "V"],
            "Average Cell Voltage": [3.945, "V"],
            "Number of Cells": [20, ""],
            "Highest Cell": [19, ""],
            "Lowest Cell": [2, ""],
            "Charging / Discharging": ["00", ""],
            "Alarm - todo": ["00", ""],
            "Voltage Difference": [0.007, "V"],
            "Balance Current": [0.0, "A"],
            "Balance Trigger Voltage": [0.005, "V"],
            "Max Balance Current": [1.0, "A"],
            "Balance On / Off": ["01", ""],
            "Set Number of Cells": [20, ""],
            "Voltage Cell01": [3.945, "V"],
            "Voltage Cell02": [3.945, "V"],
            "Voltage Cell03": [3.945, "V"],
            "Voltage Cell04": [3.945, "V"],
            "Voltage Cell05": [3.945, "V"],
            "Voltage Cell06": [3.945, "V"],
            "Voltage Cell07": [3.945, "V"],
            "Voltage Cell08": [3.945, "V"],
            "Voltage Cell09": [3.945, "V"],
            "Voltage Cell10": [3.945, "V"],
            "Voltage Cell11": [3.945, "V"],
            "Voltage Cell12": [3.945, "V"],
            "Voltage Cell13": [3.945, "V"],
            "Voltage Cell14": [3.945, "V"],
            "Voltage Cell15": [3.945, "V"],
            "Voltage Cell16": [3.945, "V"],
            "Voltage Cell17": [3.945, "V"],
            "Voltage Cell18": [3.945, "V"],
            "Voltage Cell19": [3.945, "V"],
            "Voltage Cell20": [3.945, "V"],
            "Voltage Cell21": [3.945, "V"],
            "Voltage Cell22": [3.945, "V"],
            "Voltage Cell23": [3.945, "V"],
            "Voltage Cell24": [3.945, "V"],
            "Temperature": [22, "°C"],
            "Checksum": ["6f", ""],
        }
        protocol.get_full_command(command)
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
