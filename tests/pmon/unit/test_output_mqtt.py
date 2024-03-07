""" tests / pmon / unit / test_output_mqtt.py """
import unittest
import unittest.mock as mock

from powermon.commands.command import Command
from powermon.commands.command_definition import CommandDefinition
from powermon.commands.reading_definition import (ReadingDefinition,
                                                  ReadingType, ResponseType)
from powermon.commands.result import Result, ResultType
from powermon.device import DeviceInfo
from powermon.outputs.mqtt import MQTT

reading_definition = ReadingDefinition.from_config({"index": 0, "description": "test", "reading_type": ReadingType.MESSAGE, "response_type": ResponseType.FLOAT, "icon": "mdi:solar-power"}, 0)
command_definition = CommandDefinition(code="None", description="unknown command", help_text="", result_type=ResultType.SINGLE, reading_definitions=[reading_definition])
device_info = DeviceInfo(name="name", device_id="device_id", model="model", manufacturer="manufacturer")
command = Command.from_config({"command": "None"})
command.command_definition = command_definition
_result = Result(command=command, raw_response=b"(238800\xcd\xcd\r", responses=b"0.0")
test_topic = "test/topic"
output_mqtt = MQTT(topic=test_topic)


class TestOutputMqtt(unittest.TestCase):
    """ test the mqtt output processor """
    def test_output_mqtt_topic(self):
        """ test topic setting as part of init """
        self.assertEqual(output_mqtt.topic, test_topic)

    def test_output_mqtt_no_formatter(self):
        """ test process raises error with no formatter set """
        self.assertRaises(RuntimeError, output_mqtt.process, command=command, result=_result, mqtt_broker=None, device_info=device_info)

    @mock.patch('powermon.outputformats.AbstractFormat')
    def test_output_mqtt_no_broker(self, mock_formatter):
        """ test process raises error with no mqtt_broker set """
        output_mqtt.formatter = mock_formatter
        mock_formatter.format.return_value = "mocked_formated_data"
        self.assertRaises(RuntimeError, output_mqtt.process, command=command, result=_result, mqtt_broker=None, device_info=device_info)

    @mock.patch('powermon.libs.mqttbroker.MqttBroker')
    @mock.patch('powermon.outputformats.AbstractFormat')
    def test_output_mqtt_calls_formatter(self, mock_mqtt_broker, mock_formatter):
        """ test process calls the formatter """
        output_mqtt.formatter = mock_formatter
        mock_formatter.format.return_value = "mocked_formated_data"
        output_mqtt.process(command=command, result=_result, mqtt_broker=mock_mqtt_broker, device_info=device_info)
        mock_formatter.format.assert_called_once_with(command=command, result=_result, device_info=device_info)

    @mock.patch('powermon.libs.mqttbroker.MqttBroker')
    @mock.patch('powermon.outputformats.AbstractFormat')
    def test_output_mqtt_calls_publish_str(self, mock_mqtt_broker, mock_formatter):
        """ test process calls the publish once for a str format response """
        output_mqtt.formatter = mock_formatter
        mock_formatter.format.return_value = "mocked_formated_data"
        output_mqtt.process(command=command, result=_result, mqtt_broker=mock_mqtt_broker, device_info=device_info)
        mock_mqtt_broker.publish.assert_called_once_with(topic=test_topic, payload=mock_formatter.format.return_value)

    @mock.patch('powermon.libs.mqttbroker.MqttBroker')
    @mock.patch('powermon.outputformats.AbstractFormat')
    def test_output_mqtt_calls_publish_bytes(self, mock_mqtt_broker, mock_formatter):
        """ test process calls the publish once for a bytes format response """
        output_mqtt.formatter = mock_formatter
        mock_formatter.format.return_value = b"mocked_formated_data"
        output_mqtt.process(command=command, result=_result, mqtt_broker=mock_mqtt_broker, device_info=device_info)
        mock_mqtt_broker.publish.assert_called_once_with(topic=test_topic, payload=mock_formatter.format.return_value)

    @mock.patch('powermon.libs.mqttbroker.MqttBroker')
    @mock.patch('powermon.outputformats.AbstractFormat')
    def test_output_mqtt_calls_publish_list_of_str(self, mock_mqtt_broker, mock_formatter):
        """ test process calls the publish once for each of a list of str format responses """
        output_mqtt.formatter = mock_formatter
        mock_formatter.format.return_value = ["mocked_formatted_data", "more_mocked_formatted_data"]
        output_mqtt.process(command=command, result=_result, mqtt_broker=mock_mqtt_broker, device_info=device_info)
        mock_mqtt_broker.publish.assert_has_calls([mock.call(topic=test_topic, payload='mocked_formatted_data'), mock.call(topic=test_topic, payload='more_mocked_formatted_data')])

    @mock.patch('powermon.libs.mqttbroker.MqttBroker')
    @mock.patch('powermon.outputformats.AbstractFormat')
    def test_output_mqtt_calls_publish_list_of_dict(self, mock_mqtt_broker, mock_formatter):
        """ test process calls the publish once for each of a list of dict (topic/payload) format responses """
        output_mqtt.formatter = mock_formatter
        mock_formatter.format.return_value = [{"topic": "test/topic1", "payload": "mocked_formatted_data"}, {"topic": "test/topic2", "payload": "more_mocked_formatted_data"}]
        output_mqtt.process(command=command, result=_result, mqtt_broker=mock_mqtt_broker, device_info=device_info)
        mock_mqtt_broker.publish.assert_has_calls([mock.call(topic='test/topic1', payload='mocked_formatted_data'), mock.call(topic='test/topic2', payload='more_mocked_formatted_data')])

    @mock.patch('powermon.libs.mqttbroker.MqttBroker')
    @mock.patch('powermon.outputformats.AbstractFormat')
    def test_output_mqtt_calls_publish_dict_missing_topic(self, mock_mqtt_broker, mock_formatter):
        """ test process calls the publish correct for a dict with payload only format responses """
        output_mqtt.formatter = mock_formatter
        mock_formatter.format.return_value = [{"payload": "mocked_formatted_data"}]
        output_mqtt.process(command=command, result=_result, mqtt_broker=mock_mqtt_broker, device_info=device_info)
        mock_mqtt_broker.publish.assert_has_calls([mock.call(topic=test_topic, payload='mocked_formatted_data')])
