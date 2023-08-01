import logging

from powermon.outputs.abstractoutput import AbstractOutput
from powermon.dto.resultDTO import ResultDTO
from powermon.libs.result import Result
from powermon.libs.mqttbroker import MqttBroker

log = logging.getLogger("API_MQTT")


class API_MQTT(AbstractOutput):
    def __init__(self, mqtt_broker: MqttBroker, command_name: str, formatter) -> None:
        super().__init__(formatter)
        self.mqtt_broker: MqttBroker = mqtt_broker

        self.topic_base = "powermon/results/"
        self.command_name = command_name

    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg powermon/status/total_output_active_power/value 1250"
    
    def get_topic(self):
        return self.topic_base + self.command_name

    def output(self, result: Result):
        log.info("Using output processor: api_mqtt")
        # exit if no data
        if result.raw_response is None:
            return

        # exit if no broker
        if self.mqtt_broker is None:
            log.error("No mqtt broker supplied")
            return

        # build the messages...
        formatted_data = self.formatter.format(result)
        log.debug("mqtt.output msgs %s",formatted_data)

        result_dto = ResultDTO(device_identifier=result.get_device_id(), command=result.command.name, data=result.get_decoded_responses())

        log.debug("Topic: %s", self.get_topic())
        self.mqtt_broker.publish(self.get_topic(), result_dto.json())

    def process(self, result: Result):
        self.output(result)
