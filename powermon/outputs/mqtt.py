import logging
import re

from mppsolar.helpers import get_kwargs

log = logging.getLogger("MQTT")


class MQTT:

    @classmethod
    def buildFromConfig(cls, output_config, mqtt_broker, formatter):
        log.debug(f"processor.MQTT buildFromConfig {output_config}")
        results_topic = output_config.get("results_topic", None)
        tag = output_config.get("tag", None)
        return cls(mqtt_broker, results_topic, tag, formatter)
    
    def __init__(self, mqtt_broker, results_topic, tag, formatter) -> None:
        self.mqtt_broker = mqtt_broker
        self.results_topic = results_topic
        self.tag = tag
        self.formatter = formatter
        log.debug(f"processor.MQTT __init__ ")
    
    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg {tag}/status/total_output_active_power/value 1250"

    #TODO: use proper parameters to make the code more readable
    def build_msgs(self, *args, **kwargs):

        data = get_kwargs(kwargs, "data")
        # Clean data
        if "_command" in data:
            command = data.pop("_command")
        if "_command_description" in data:
            data.pop("_command_description")
        if "raw_response" in data:
            data.pop("raw_response")

        # check if config supplied
#        config = get_kwargs(kwargs, "config")
#        if config is not None:
#            log.debug(f"config: {config}")
#            # get results topic
#            results_topic = config.get("results_topic", None)
#            # get formatting info
#            remove_spaces = config.get("remove_spaces", True)
#            keep_case = config.get("keep_case", False)
#            filter = config.get("filter", None)
#            excl_filter = config.get("excl_filter", None)
#            tag = config.get("tag", None)
#        else:
#            results_topic = None
#            # get formatting info
#            remove_spaces = True
#            keep_case = get_kwargs(kwargs, "keep_case")
#            filter = get_kwargs(kwargs, "filter")
#            excl_filter = get_kwargs(kwargs, "excl_filter")
#            tag = get_kwargs(kwargs, "tag")

#        if filter is not None:
#            filter = re.compile(filter)
#        if excl_filter is not None:
#            excl_filter = re.compile(excl_filter)

        if self.tag is None:
            self.tag = command

        # build topic prefix
        if self.results_topic is not None:
            topic_prefix = self.results_topic + "/" + self.tag
        else:
            topic_prefix = f"{self.tag}/status"

        # build data to output
        _data = {}
        for key in data:
            _values = data[key]
            # remove spaces
            #if not keep_case:
                # make lowercase
            #    key = key.lower()
            #if key_wanted(key, filter, excl_filter):
            _data[key] = _values
        log.debug(f"output data: {_data}")

        # Build array of mqtt messages
        msgs = []
        # Loop through responses build topics and messages
        for key in _data:
            value = _data[key][0]
            unit = _data[key][1]
            log.debug(
                f"build_msgs: prefix {topic_prefix}, key {key}, value {value}, unit {unit}"
            )
            msg = {"topic": f"{topic_prefix}/{key}/value", "payload": value}
            msgs.append(msg)
            if unit:
                msg = {"topic": f"{topic_prefix}/{key}/unit", "payload": unit}
                msgs.append(msg)
        log.debug(f"build_msgs: {msgs}")
        return msgs

    def output(self, *args, **kwargs):
        log.info("Using output processor: mqtt")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        # exit if no data
        if data is None:
            return

        # exit if no broker
        if self.mqtt_broker is None:
            return

        # build the messages...
        msgs = self.build_msgs(**kwargs)
        log.debug(f"mqtt.output msgs {msgs}")

        # publish
        self.mqtt_broker.publishMultiple(msgs)