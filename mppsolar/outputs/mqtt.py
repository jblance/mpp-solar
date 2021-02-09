import logging
import re
import paho.mqtt.publish as publish

from .baseoutput import baseoutput
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("MPP-Solar")


class mqtt(baseoutput):
    def __str__(self):
        return "outputs the to the supplied mqtt broker: eg 'tag'/status/total_output_active_power/value 1250"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.mqtt __init__ kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = get_kwargs(kwargs, "data")
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")
        # Build array of mqtt messages
        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)
        if tag is None:
            tag = cmd
        # Loop through responses
        for key in data:
            value = data[key][0]
            unit = data[key][1]
            # remove spaces
            key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                log.debug(f"tag {tag}, key {key}, value {value}, unit {unit}")
                # 'tag'/status/total_output_active_power/value 1250
                # 'tag'/status/total_output_active_power/unit W
                msg = {"topic": f"{tag}/status/{key}/value", "payload": value}
                msgs.append(msg)
                if unit:
                    msg = {"topic": f"{tag}/status/{key}/unit", "payload": unit}
                    msgs.append(msg)
        log.debug(msgs)
        return msgs

    def output(self, *args, **kwargs):
        log.info("Using output processor: mqtt")
        log.debug(f"processor.mqtt.output kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        if data is None:
            return
        mqtt_broker = get_kwargs(kwargs, "mqtt_broker", "localhost")
        mqtt_port = get_kwargs(kwargs, "mqtt_port", 1883)
        mqtt_user = get_kwargs(kwargs, "mqtt_user")
        mqtt_pass = get_kwargs(kwargs, "mqtt_pass")

        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        if mqtt_user is not None and mqtt_pass is not None:
            auth = {"username": mqtt_user, "password": mqtt_pass}
            log.info(f"Using mqtt authentication, username: {mqtt_user}, password: [supplied]")
        else:
            log.debug("No mqtt authentication used")
            auth = None

        msgs = self.build_msgs(**kwargs)
        log.debug(f"mqtt.output msgs {msgs}")
        if msgs:
            publish.multiple(msgs, hostname=mqtt_broker, port=mqtt_port, auth=auth)
        else:
            log.warn("MQTT build_msgs returned no messages")
