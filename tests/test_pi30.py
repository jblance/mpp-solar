import unittest
from mppsolar.protocols.pi30 import pi30 as pi

# Examples
# self.assertRaises(mppinverter.NoDeviceError, mppinverter.mppInverter)
# self.assertEqual(inverter._baud_rate, 2400)
# self.assertIsNone(inverter._serial_number)
# self.assertFalse(inverter._direct_usb)
# self.assertIsInstance(inverter.getAllCommands(), list)
# self.assertTrue(inverter._direct_usb)
# self.assertListEqual(mppcommand.crc(bytes('196', 'utf-8')), [27, 14])


class test_pi30_decode(unittest.TestCase):
    def test_pi30_QPI(self):
        """ test the decode of a QPI response"""
        protocol = pi()
        response = b"(PI30\x9a\x0b\r"
        command = "QPI"
        expected = {
            "raw_response": ["(PI30\x9a\x0b\r", ""],
            "_command": "QPI",
            "_command_description": "Protocol ID inquiry",
            "Protocol ID": ["PI30", ""],
        }
        result = protocol.decode(response, command)
        self.assertEqual(result, expected)

    def test_pi30_QPIGS(self):
        """ test the decode of a QPIGS response"""
        protocol = pi()
        response = b"(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010\x24\x8c\r"

        command = "QPIGS"
        expected = {
            "raw_response": [
                "(000.0 00.0 230.0 49.9 0161 0119 003 460 57.50 012 100 0069 0014 103.8 57.45 00000 00110110 00 00 00856 010$\x8c\r",
                "",
            ],
            "_command": "QPIGS",
            "_command_description": "General Status Parameters inquiry",
            "AC Input Voltage": [0.0, "V"],
            "AC Input Frequency": [0.0, "Hz"],
            "AC Output Voltage": [230.0, "V"],
            "AC Output Frequency": [49.9, "Hz"],
            "AC Output Apparent Power": [161, "VA"],
            "AC Output Active Power": [119, "W"],
            "AC Output Load": [3, "%"],
            "BUS Voltage": [460, "V"],
            "Battery Voltage": [57.5, "V"],
            "Battery Charging Current": [12, "A"],
            "Battery Capacity": [100, "%"],
            "Inverter Heat Sink Temperature": [69, "°C"],
            "PV Input Current for Battery": [14.0, "A"],
            "PV Input Voltage": [103.8, "V"],
            "Battery Voltage from SCC": [57.45, "V"],
            "Battery Discharge Current": [0, "A"],
            "Is SBU Priority Version Added": [0, "bool"],
            "Is Configuration Changed": [0, "bool"],
            "Is SCC Firmware Updated": [1, "bool"],
            "Is Load On": [1, "bool"],
            "Is Battery Voltage to Steady While Charging": [0, "bool"],
            "Is Charging On": [1, "bool"],
            "Is SCC Charging On": [1, "bool"],
            "Is AC Charging On": [0, "bool"],
            "RSV1": [0, "A"],
            "RSV2": [0, "A"],
            "PV Input Power": [856, "W"],
            "Is Charging to Float": [0, "bool"],
            "Is Switched On": [1, "bool"],
            "Is Reserved": [0, "bool"],
        }
        result = protocol.decode(response, command)
        self.assertEqual(result, expected)

    def test_pi30_QPIRI(self):
        """ test the decode of a QPIRI response"""
        protocol = pi()
        response = b"(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1\x6F\x7E\r"
        command = "QPIRI"
        expected = {
            "raw_response": [
                "(230.0 21.7 230.0 50.0 21.7 5000 4000 48.0 46.0 42.0 56.4 54.0 0 10 010 1 0 0 6 01 0 0 54.0 0 1o~\r",
                "",
            ],
            "_command": "QPIRI",
            "_command_description": "Current Settings inquiry",
            "AC Input Voltage": [230.0, "V"],
            "AC Input Current": [21.7, "A"],
            "AC Output Voltage": [230.0, "V"],
            "AC Output Frequency": [50.0, "Hz"],
            "AC Output Current": [21.7, "A"],
            "AC Output Apparent Power": [5000, "VA"],
            "AC Output Active Power": [4000, "W"],
            "Battery Voltage": [48.0, "V"],
            "Battery Recharge Voltage": [46.0, "V"],
            "Battery Under Voltage": [42.0, "V"],
            "Battery Bulk Charge Voltage": [56.4, "V"],
            "Battery Float Charge Voltage": [54.0, "V"],
            "Battery Type": ["AGM", ""],
            "Max AC Charging Current": [10, "A"],
            "Max Charging Current": [10, "A"],
            "Input Voltage Range": ["UPS", ""],
            "Output Source Priority": ["Utility first", ""],
            "Charger Source Priority": ["Utility first", ""],
            "Max Parallel Units": [6, "units"],
            "Machine Type": ["Off Grid", ""],
            "Topology": ["transformerless", ""],
            "Output Mode": ["single machine output", ""],
            "Battery Redischarge Voltage": [54.0, "V"],
            "PV OK Condition": [
                "As long as one unit of inverters has connect PV, parallel system will consider PV OK",
                "",
            ],
            "PV Power Balance": [
                "PV input max power will be the sum of the max charged power and loads power",
                "",
            ],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_pi30_QFLAG(self):
        """ test the decode of a QFLAG response"""
        protocol = pi()
        response = b"(EakxyDbjuvz\x2F\x29\r"
        command = "QFLAG"
        expected = {
            "raw_response": ["(EakxyDbjuvz/)\r", ""],
            "_command_description": "Flag Status inquiry",
            "_command": "QFLAG",
            "Buzzer": ["enabled", ""],
            "LCD Reset to Default": ["enabled", ""],
            "LCD Backlight": ["enabled", ""],
            "Primary Source Interrupt Alarm": ["enabled", ""],
            "Overload Bypass": ["disabled", ""],
            "Power Saving": ["disabled", ""],
            "Overload Restart": ["disabled", ""],
            "Over Temperature Restart": ["disabled", ""],
            "Record Fault Code": ["disabled", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
