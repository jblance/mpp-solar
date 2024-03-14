import unittest

# from mppsolar.outputs import get_outputs
from mppsolar.outputs.mqtt import mqtt as mqtt


class test_mqtt_output(unittest.TestCase):
    maxDiff = 9999

    def test_mqtt_out(self):
        """test the mqtt output"""
        global run, result, count
        result = []
        # Get a mqtt output processor
        # op = get_outputs("mqtt")[0]
        tag = "test"
        data = {
            "raw_response": [
                "(1 92931701100510 B  0141 005 51.4 Ì#\r",
                "",
            ],
            "_command": "QPGS0",
            "_command_description": "Parallel Information inquiry",
            "Battery voltage": [51.4, "V"],
        }

        msgs = mqtt().build_msgs(
            data=data, tag=tag, keep_case=False, filter=None, excl_filter=None
        )

        # needed to initialise variables
        expected = [
            {"topic": f"{tag}/status/battery_voltage/value", "payload": 51.4},
            {"topic": f"{tag}/status/battery_voltage/unit", "payload": "V"},
        ]

        # topic = f"{tag}/#"

        # print(result)
        self.assertEqual(msgs, expected)
