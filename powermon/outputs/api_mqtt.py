import logging

from powermon.outputs.abstractoutput import AbstractOutput
from powermon.dto.resultDTO import ResultDTO
from powermon.libs.result import Result
from powermon.libs.mqttbroker import MqttBroker

log = logging.getLogger("API_MQTT")


class API_MQTT(AbstractOutput):
    def __init__(self, output_config, topic, mqtt_broker: MqttBroker, formatter) -> None:
        super().__init__(formatter)
        self.mqtt_broker: MqttBroker = mqtt_broker
        self.results_topic = output_config.get("topic_override", None)

        if self.results_topic is None:
            self.results_topic = topic

    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg powermon/status/total_output_active_power/value 1250"

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

        result_DTO = ResultDTO(device_identifier=result.get_device_id(), command=result.command.name, formatted_data=formatted_data)

        log.debug("Topic: %s", self.results_topic)
        self.mqtt_broker.publish(self.results_topic, result_DTO.json())

    def process(self, result: Result):
        self.output(result)
