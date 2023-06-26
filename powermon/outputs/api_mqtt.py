import logging

from powermon.outputs.abstractoutput import AbstractOutput
from powermon.dto.resultDTO import ResultDTO

log = logging.getLogger("API_MQTT")


class API_MQTT(AbstractOutput):
    def __init__(self, output_config, topic, schedule_name: str, mqtt_broker, formatter) -> None:
        super().__init__(formatter)
        self.mqtt_broker = mqtt_broker
        self.schedule_name = schedule_name
        self.results_topic = output_config.get("topic_override", None)

        if self.results_topic is None:
            self.results_topic = topic

    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg powermon/status/total_output_active_power/value 1250"

    def output(self, data):
        log.info("Using output processor: api_mqtt")
        # exit if no data
        if data is None:
            return

        # exit if no broker
        if self.mqtt_broker is None:
            log.error("No mqtt broker supplied")
            return

        # build the messages...
        formatted_data = self.formatter.format(data)
        log.debug("mqtt.output msgs %s",formatted_data)

        result = ResultDTO(result=formatted_data)

        log.debug("Topic: %s", self.results_topic)
        self.mqtt_broker.publish(self.results_topic, result.json())

    def process(self, result):
        self.output(result)