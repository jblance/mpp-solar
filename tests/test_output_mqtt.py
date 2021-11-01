import unittest

import paho.mqtt.client as mqttclient

from mppsolar.outputs import get_outputs
from mppsolar.libs.mqttbroker import MqttBroker
from mppsolar.outputs.mqtt import mqtt as mqtt


class test_mqtt_output(unittest.TestCase):
    maxDiff = 9999

    def test_mqtt_out(self):
        """test the mqtt output"""
        global run, result, count
        result = []
        # Get a mqtt output processor
        op = get_outputs("mqtt")[0]
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
        mqtt_broker = MqttBroker(name="localhost", port=1883, username=None, password=None)

        msgs = mqtt().build_msgs(
            data=data, tag=tag, keep_case=False, filter=None, excl_filter=None
        )
        msg_count = len(msgs)
        count = 0

        # needed to initialise variables
        expected = [
            {f"{tag}/status/battery_voltage/value": b"51.4"},
            {f"{tag}/status/battery_voltage/unit": b"V"},
        ]

        topic = f"{tag}/#"

        # define the callback for mqtt subscription
        def on_message(mqttc, userdata, message):
            global run, result, count
            result.append({message.topic: message.payload})
            count += 1
            if count >= msg_count:
                run = False

        # subscribe to the mqtt topic
        mqttc = mqttclient.Client()
        mqttc.on_message = on_message
        mqttc.connect(mqtt_broker.name, mqtt_broker.port, 60)
        mqttc.subscribe(topic, qos=0)

        # process the output
        op.output(
            data=data,
            tag=tag,
            mqtt_broker=mqtt_broker,
            filter=None,
            excl_filter=None,
            keep_case=False,
        )

        # wait for mqtt messages
        run = True
        while run:
            mqttc.loop()

        # print(result)
        self.assertEqual(result, expected)
