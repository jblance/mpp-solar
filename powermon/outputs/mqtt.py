"""
mqtt output module
outputs messages to mqtt broker
"""
import logging

from powermon.commands.result import Result
# from powermon.device import Device
# from powermon.formats.abstractformat import AbstractFormat
# from powermon.dto.outputDTO import OutputDTO
from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("MQTT")


class MQTT(AbstractOutput):
    """ mqtt output class"""
    def __init__(self, results_topic: str):
        super().__init__(name="Mqtt")
        self.results_topic = results_topic

    def __str__(self):
        return f"outputs.MQTT: {self.results_topic=}"

    def get_topic(self) -> str:
        return self.results_topic

    def process(self, command=None, result: Result=None, mqtt_broker=None, device_info=None):
        log.info("Using output processor: MQTT")
        # exit if no data
        if result is None:
            log.debug("No result to output")
            return

        # Not sure that formatter and mqtt_broker are set, could use builder pattern to ensure they are set
        if self.formatter is None:
            log.error("No formatter supplied")
            raise RuntimeError("No formatter supplied")

        if mqtt_broker is None:
            log.error("No mqtt broker supplied")
            raise RuntimeError("No mqtt broker supplied")

        # build the messages...
        formatted_data = self.formatter.format(result)
        log.debug("mqtt.output msgs %s", formatted_data)

        # publish
        # TODO: check this approach (single vs multiple and tidy/consolidate)
        if self.formatter.sendsMultipleMessages():
            mqtt_broker.publishMultiple(formatted_data)
        else:
            mqtt_broker.publish(self.results_topic, formatted_data)

    @classmethod
    def from_config(cls, output_config) -> "MQTT":
        """build object from config dict"""
        results_topic = output_config.get("topic_override", None)
        return cls(results_topic=results_topic)
