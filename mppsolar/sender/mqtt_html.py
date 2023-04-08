import logging

log = logging.getLogger("MQTT_HTML")


class MQTT_HTML:
    
    def __init__(self, mqtt_broker, results_topic, tag) -> None:
        self.mqtt_broker = mqtt_broker
        self.results_topic = results_topic
        self.tag = tag
        log.debug(f"processor.MQTT_HTML __init__ ")
    
    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg {tag}/status/total_output_active_power/value 1250"

    def build_msgs(self, data):

        # Clean data
        if "_command" in data:
            command = data.pop("_command")
        if "_command_description" in data:
            data.pop("_command_description")
        if "raw_response" in data:
            data.pop("raw_response")

        if self.tag is None:
            self.tag = command

        topic_prefix = f"{self.tag}/status"

        # build data to output
        _data = {}
        for key in data:
            _values = data[key]
            _data[key] = _values
        log.debug(f"output data: {_data}")

        # Build array of mqtt messages
        html = "<table>"
        # Loop through responses
        for key in _data:
            value = _data[key][0]
            unit = _data[key][1]
            row = "<tr><td>" + key + "</td><td>" + str(value) + "</td><td>" + str(unit) + "</td></tr>"
            html += row
        html += "</table>"
        return html

    def output(self, data):
        log.info("Using output processor: mqtt")
        # exit if no data
        if data is None:
            return

        # exit if no broker
        if self.mqtt_broker is None:
            return

        # build the messages...
        msgs = self.build_msgs(data)

        topic = self.results_topic +"/" + self.tag
        log.debug(f"topic: {topic}\nmqtt_html.output msgs {msgs}")
        # publish
        self.mqtt_broker.publish(topic,str(msgs))