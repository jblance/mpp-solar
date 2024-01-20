import unittest
import unittest.mock as mock

from powermon.outputs.mqtt import MQTT
from powermon.commands.result import Result, ResultType
from powermon.commands.reading_definition import ReadingDefinition, ReadingType, ResponseType
from powermon.device import DeviceInfo
from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition

class test_powermon_output_mqtt(unittest.TestCase):
    
    def test_output_mqtt_get_topic(self):
        test_topic = "test/topic"
        output_mqtt = MQTT(results_topic=test_topic)
        self.assertEqual(output_mqtt.get_topic(), test_topic)
        
    @mock.patch('powermon.libs.mqttbroker.MqttBroker')
    @mock.patch('powermon.formats.AbstractFormat')

    def test_output_mqtt_process(self, mock_mqtt_broker, mock_formatter):
        
        test_topic = "test/topic"
        output_mqtt = MQTT(results_topic=test_topic)
        
        mock_formatter.format.return_value = "mocked_formated_data"
        mock_formatter.sendsMultipleMessages.return_value = False
        output_mqtt.formatter = mock_formatter
        
        reading_definition = ReadingDefinition.from_config({"index":0, "description":"test", "reading_type":ReadingType.MESSAGE, "response_type":ResponseType.FLOAT, "icon": "mdi:solar-power"},0)
        command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
        device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
        command = Command.from_config({"command":"None"})
        command.command_definition = command_definition
        _result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"0.0")
        # _result = Result(command_code=None, result_type=ResultType.SINGLE, raw_response=b"0.0", reading_definitions=[reading_definition], parameters=None)
        # Raises error as no mqttbroker set
        self.assertRaises(RuntimeError, output_mqtt.process, _result, mock_mqtt_broker)
        
        # mock_formatter.format.assert_called_once_with(command, _result, device_info)
        # mock_mqtt_broker.publish.assert_called_once_with(test_topic, mock_formatter.format.return_value)
        