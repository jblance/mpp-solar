import unittest
from powermon.outputs.mqtt import MQTT

class test_powermon_output_mqtt(unittest.TestCase):
    
    def test_output_mqtt_get_topic(self):
        test_topic = "test/topic"
        output_mqtt = MQTT(results_topic=test_topic)
        self.assertEqual(output_mqtt.get_topic(), test_topic)
        