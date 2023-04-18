import logging
import re

from mppsolar.helpers import get_kwargs
from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("MQTT")


class MQTT(AbstractOutput):
    
    def __init__(self, output_config, mqtt_broker, formatter) -> None:
        super().__init__(formatter)
        self.mqtt_broker = mqtt_broker
        self.results_topic = output_config.get("results_topic", None)
        self.tag = output_config.get("tag", None)
    
    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg {tag}/status/total_output_active_power/value 1250"

    

    def output(self, data):
        log.info("Using output processor: mqtt")
        # exit if no data
        if data is None:
            return

        # exit if no broker
        if self.mqtt_broker is None:
            log.error("No mqtt broker supplied")
            return

        # build the messages...
        msgs = self.formatter.format(data)
        log.debug(f"mqtt.output msgs {msgs}")

        # publish
        self.mqtt_broker.publishMultiple(msgs)