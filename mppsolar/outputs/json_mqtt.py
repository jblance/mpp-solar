import json as js
import logging
import re

from . import to_json
from .mqtt import mqtt
from ..helpers import get_kwargs

# from ..helpers import key_wanted

log = logging.getLogger("json_mqtt")


class json_mqtt(mqtt):
    def __str__(self):
        return "outputs all the results to the supplied mqtt broker in a single message formatted as json: eg "

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = get_kwargs(kwargs, "data")
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")
        mqtt_broker = get_kwargs(kwargs, "mqtt_broker")
        if mqtt_broker is not None:
            topic = mqtt_broker.results_topic
        else:
            topic = get_kwargs(kwargs, "mqtt_topic", default="mpp-solar")
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
        output = to_json(data, keep_case, excl_filter, filter)
        payload = js.dumps(output)
        msg = {
             "topic": f"{tag}/{topic}",
            "payload": payload,
        }
        msgs.append(msg)
        return msgs
