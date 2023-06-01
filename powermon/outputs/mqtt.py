import logging

from powermon.outputs.abstractoutput import AbstractOutput

log = logging.getLogger("MQTT")


class MQTT(AbstractOutput):
    def __init__(self, output_config, topic, mqtt_broker, formatter) -> None:
        super().__init__(formatter)
        self.mqtt_broker = mqtt_broker
        self.results_topic = output_config.get("topic_override", None)

        if self.results_topic is None:
            self.results_topic = topic

    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg powermon/status/total_output_active_power/value 1250"

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
        formattedData = self.formatter.format(data)
        log.debug(f"mqtt.output msgs {formattedData}")

        # publish
        if (self.formatter.sendsMultipleMessages()):
            self.mqtt_broker.publishMultiple(formattedData)
        else:
            self.mqtt_broker.publish(self.topic_prefix, formattedData)
