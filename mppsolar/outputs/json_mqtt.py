import json as js
import logging
import re

from .mqtt import mqtt
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("json_mqtt")


class json_mqtt(mqtt):
    def __str__(self):
        return "outputs all the results to the supplied mqtt broker in a single message formated as json: eg "

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = get_kwargs(kwargs, "data")
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")

        topic = get_kwargs(kwargs, "mqtt_topic", default="mpp-solar/")
        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        # Build array of Influx Line Protocol II messages
        # Message format is: mpp-solar,command=QPGS0 max_charger_range=120.0
        #                    mpp-solar,command=inverter2 parallel_instance_number="valid"
        #                    measurement,tag_set field_set
        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)
        if tag is None:
            tag = cmd
        topic = topic + tag

        output = {}
        # Loop through responses
        for key in data:
            value = data[key]
            if isinstance(value, list):
                value = data[key][0]
            # unit = data[key][1]
            # remove spaces
            key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                output[key] = value

        payload = js.dumps(output)
        msg = {
            "topic": topic,
            "payload": payload,
        }
        msgs.append(msg)
        return msgs
