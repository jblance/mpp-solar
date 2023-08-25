import logging

from powermon.outputs.abstractoutput import AbstractOutput
from powermon.dto.resultDTO import ResultDTO
from powermon.libs.result import Result
from powermon.libs.mqttbroker import MqttBroker

log = logging.getLogger("API_MQTT")


class API_MQTT(AbstractOutput):
    def __init__(self, formatter) -> None:
        self.set_formatter(formatter)
        self.command_name : str = "not_set"
        self.device_id : str = "not_set"

        self.topic_base : str = "powermon/"
        self.topic_type : str = "results/"

    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg powermon/status/total_output_active_power/value 1250"
    
    def set_formatter(self, formatter):
        self.formatter = formatter

    def set_command(self, command_name):
        self.command_name = command_name

    def set_mqtt_broker(self, mqtt_broker: MqttBroker):
        self.mqtt_broker = mqtt_broker

    def set_device_id(self, device_id):
        self.device_id = device_id
    
    def get_topic(self):
        #TODO: is there a more readable approach? like a format string?
        return self.topic_base + str(self.device_id) + "/" + self.topic_type + self.command_name
    
    

    def output(self, result: Result):
        log.info("Using output processor: api_mqtt")
        # exit if no data
        if result.raw_response is None:
            return

        # exit if no broker
        if self.mqtt_broker is None:
            log.error("No mqtt broker supplied")
            raise RuntimeError("No mqtt broker supplied")

        # build the messages...
        formatted_data = self.formatter.format(result)
        log.debug("mqtt.output msgs %s",formatted_data)

        result_dto = ResultDTO(device_identifier=result.get_device_id(), command=result.command.name, data=result.get_decoded_responses())

        log.debug("Topic: %s", self.get_topic())
        self.mqtt_broker.publish(self.get_topic(), result_dto.json())

    def process(self, result: Result):
        self.output(result)
