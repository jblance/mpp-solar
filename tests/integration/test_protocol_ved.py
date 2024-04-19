import unittest
from mppsolar.protocols.ved import ved as pi


class test_daly_decode(unittest.TestCase):
    maxDiff = 9999

    def test_vedtext(self):
        """test the decode of a VEDTEXT response"""
        protocol = pi()
        response = b"\x00L\r\nH1\t-32914\r\nH2\t0\r\nH3\t0\r\nH4\t0\r\nH5\t0\r\nH6\t-35652\r\nH7\t12041\r\nH8\t14282\r\nH9\t0\r\nH10\t0\r\nH11\t0\r\nH12\t0\r\nH15\t-22\r\nH16\t0\r\nH17\t46\r\nH18\t48\r\nChecksum\t\x1a\r\nPID\t0xA389\r\nV\t12868\r\nVS\t-12\r\nI\t0\r\nP\t0\r\nCE\t0\r\nSOC\t1000\r\nTTG\t-1\r\nAlarm\tOFF\r\nAR\t0\r\nBMV\tSmartShunt 500A/50mV\r\nFW\t0405\r\nChecksum\tK\r"
        command = "vedtext"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": [
                "\x00L\r\nH1\t-32914\r\nH2\t0\r\nH3\t0\r\nH4\t0\r\nH5\t0\r\nH6\t-35652\r\nH7\t12041\r\nH8\t14282\r\nH9\t0\r\nH10\t0\r\nH11\t0\r\nH12\t0\r\nH15\t-22\r\nH16\t0\r\nH17\t46\r\nH18\t48\r\nChecksum\t\x1a\r\nPID\t0xA389\r\nV\t12868\r\nVS\t-12\r\nI\t0\r\nP\t0\r\nCE\t0\r\nSOC\t1000\r\nTTG\t-1\r\nAlarm\tOFF\r\nAR\t0\r\nBMV\tSmartShunt 500A/50mV\r\nFW\t0405\r\nChecksum\tK\r",
                "",
            ],
            "_command": "vedtext",
            "_command_description": "VE Direct Text",
            "Depth of the deepest discharge": [-32.914, "Ah"],
            "Depth of the last discharge": [0.0, "Ah"],
            "Depth of the average discharge": [0.0, "Ah"],
            "Number of charge cycles": ["0", ""],
            "Number of full discharges": ["0", ""],
            "Cumulative Amp Hours drawn": [-35.652, "Ah"],
            "Minimum main battery voltage": [12.041, "V"],
            "Maximum main battery voltage": [14.282, "V"],
            "Number of seconds since last full charge": [0.0, "Seconds"],
            "Number of automatic synchronizations": ["0", ""],
            "Number of low main voltage alarms": ["0", ""],
            "Number of high main voltage alarms": ["0", ""],
            "Minimum auxiliary battery voltage": [-0.022, "V"],
            "Maximum auxiliary battery voltage": [0.0, "V"],
            "Amount of discharged energy": [0.46, "kWh"],
            "Amount of charged energy": [0.48, "kWh"],
            "Product ID": ["0xA389", ""],
            "Main or channel 1 battery voltage": [12.868, "V"],
            "Auxiliary starter voltage": [-0.012, "V"],
            "Main or channel 1 battery current": [0.0, "A"],
            "Instantaneous power": [0.0, "W"],
            "Consumed Amp Hours": [0.0, "Ah"],
            "State-of-charge": [100.0, "%"],
            "Time-to-go": [-1.0, "Minutes"],
            "Alarm condition active": ["OFF", ""],
            "Alarm reason": ["0", ""],
            "Model description": ["SmartShunt 500A/50mV", ""],
            "Firmware version 16 bit": ["0405", ""],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)

    def test_batteryCapacity(self):
        """test the decode of a batteryCapacity response"""
        protocol = pi()
        response = b"\x00\x1a:70010007800C6\n"
        command = "batteryCapacity"
        # needed to initialise variables
        protocol.get_full_command(command)
        expected = {
            "raw_response": ["\x00\x1a:70010007800C6\n", ""],
            "_command": "batteryCapacity",
            "_command_description": "battery capacity",
            "Command response flag": ["OK", ""],
            "Battery Capacity": [120, "Ah"],
        }
        result = protocol.decode(response, command)
        # print(result)
        self.assertEqual(result, expected)
