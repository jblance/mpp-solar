"""
mqtt output module
outputs messages to mqtt broker
"""
import logging

from powermon.commands.result import Result
from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("MQTT")


class MQTT(AbstractOutput):
    """ mqtt output class"""
    def __init__(self, topic: str):
        super().__init__(name="Mqtt")
        self.topic = topic

    def __str__(self):
        return f"outputs.MQTT: {self.topic=}"

    @property
    def topic(self):
        """ the topic to send the output to """
        return getattr(self, "_topic", None)

    @topic.setter
    def topic(self, value):
        self._topic = value

    # def get_topic(self) -> str:
    #     return self.topic

    def process(self, command=None, result: Result = None, mqtt_broker=None, device_info=None):
        log.info("Using output processor: MQTT, topic: %s", self.topic)
        log.debug("formatter: %s, result: %s, mqtt_broker: %s, device_info: %s", self.formatter, result, mqtt_broker, device_info)

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
        formatted_data = self.formatter.format(command=command, result=result, device_info=device_info)
        log.debug("mqtt.output msgs %s", formatted_data)

        # publish
        if isinstance(formatted_data, (str, bytes)):
            # simple payload, so publish as payload
            mqtt_broker.publish(topic=self.topic, payload=formatted_data)
        elif isinstance(formatted_data, list):
            # iterate list
            for item in formatted_data:
                if isinstance(item, (str, bytes)):
                    mqtt_broker.publish(topic=self.topic, payload=item)
                elif isinstance(item, dict) and 'topic' in item and 'payload' in item:
                    mqtt_broker.publish(topic=item['topic'], payload=item['payload'])
                elif isinstance(item, dict) and 'payload' in item:
                    mqtt_broker.publish(topic=self.topic, payload=item['payload'])
                else:
                    log.warning('Unknown mqtt data to publish, type: %s, data: %s', type(item), item)
        else:
            log.warning('Unknown mqtt data to publish, type: %s, data: %s', type(formatted_data), formatted_data)

    @classmethod
    def from_config(cls, output_config) -> "MQTT":
        """build object from config dict"""
        topic = output_config.get("topic", None)
        return cls(topic=topic)
