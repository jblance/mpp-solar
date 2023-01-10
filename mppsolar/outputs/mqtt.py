import logging
import re

from .baseoutput import baseoutput
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("mqtt")


class mqtt(baseoutput):
    def __str__(self):
        return "outputs the results to the supplied mqtt broker: eg {tag}/status/total_output_active_power/value 1250"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

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
        config = get_kwargs(kwargs, "config")
        if config is not None:
            log.debug(f"config: {config}")
            # get results topic
            results_topic = config.get("results_topic", None)
            # get formatting info
            remove_spaces = config.get("remove_spaces", True)
            keep_case = config.get("keep_case", False)
            filter = config.get("filter", None)
            excl_filter = config.get("excl_filter", None)
            tag = config.get("tag", None)
        else:
            results_topic = None
            # get formatting info
            remove_spaces = True
            keep_case = get_kwargs(kwargs, "keep_case")
            filter = get_kwargs(kwargs, "filter")
            excl_filter = get_kwargs(kwargs, "excl_filter")
            tag = get_kwargs(kwargs, "tag")

        if filter is not None:
            filter = re.compile(filter)
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)
        if tag is None:
            tag = command

        # build topic prefix
        if results_topic is not None:
            topic_prefix = results_topic
        else:
            topic_prefix = f"{tag}/status"

        # build data to output
        _data = {}
        for key in data:
            _values = data[key]
            # remove spaces
            if remove_spaces:
                key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                _data[key] = _values
        log.debug(f"output data: {_data}")

        # Build array of mqtt messages
        msgs = []
        # Loop through responses
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

        # get the broker instance
        mqtt_broker = get_kwargs(kwargs, "mqtt_broker")
        # exit if no broker
        if mqtt_broker is None:
            return

        # build the messages...
        msgs = self.build_msgs(**kwargs)
        log.debug(f"mqtt.output msgs {msgs}")

        # publish
        mqtt_broker.publishMultiple(msgs)
