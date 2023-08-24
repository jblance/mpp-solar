import logging

from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("MQTT")


class MQTT(AbstractOutput):
    def __init__(self, results_topic) -> None:
        self.results_topic = results_topic

    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg powermon/status/total_output_active_power/value 1250"
    
    def set_mqtt_broker(self, mqtt_broker):
        self.mqtt_broker = mqtt_broker

    def set_formatter(self, formatter):
        self.formatter = formatter

    def output(self, data):
        #Not sure that formatter and mqtt_broker are set, could use builder pattern to ensure they are set
        if(self.formatter is None):
            log.error("No formatter supplied")
            raise RuntimeError("No formatter supplied")
        
        if(self.mqtt_broker is None):
            log.error("No mqtt broker supplied")
            raise RuntimeError("No mqtt broker supplied")
        
        log.info("Using output processor: mqtt")
        # exit if no data
        if data is None:
            return

        # exit if no broker
        if self.mqtt_broker is None:
            log.error("No mqtt broker supplied")
            return

        # build the messages...
        formatted_data = self.formatter.format(data)
        log.debug(f"mqtt.output msgs {formatted_data}")

        # publish
        if (self.formatter.sendsMultipleMessages()):
            self.mqtt_broker.publishMultiple(formatted_data)
        else:
            self.mqtt_broker.publish(self.results_topic, formatted_data)

    def process(self, result):
        self.output(result)

    @classmethod
    def from_config(cls, output_config) -> "MQTT":
        results_topic = output_config.get("topic_override", None)
        return cls(results_topic)
