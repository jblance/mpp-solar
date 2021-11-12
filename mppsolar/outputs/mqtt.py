import logging
import re
import paho.mqtt.publish as publish

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
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")
        # Build array of mqtt messages
        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)
        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)
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
                log.debug(f"build_msgs: tag {tag}, key {key}, value {value}, unit {unit}")
                # 'tag'/status/total_output_active_power/value 1250
                # 'tag'/status/total_output_active_power/unit W
                msg = {"topic": f"{tag}/status/{key}/value", "payload": value}
                msgs.append(msg)
                if unit:
                    msg = {"topic": f"{tag}/status/{key}/unit", "payload": unit}
                    msgs.append(msg)
        log.debug(f"build_msgs: {msgs}")
        return msgs

    def output(self, *args, **kwargs):
        log.info("Using output processor: mqtt")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        if data is None:
            return
        mqtt_broker = get_kwargs(kwargs, "mqtt_broker")
        if mqtt_broker is None or not mqtt_broker.name:
            return
        mqtt_port = mqtt_broker.port
        mqtt_user = mqtt_broker.username
        mqtt_pass = mqtt_broker.password

        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        if mqtt_user and mqtt_pass:
            auth = {"username": mqtt_user, "password": mqtt_pass}
            log.info(f"Using mqtt authentication, username: {mqtt_user}, password: [supplied]")
        else:
            log.debug("No mqtt authentication used")
            auth = None

        msgs = self.build_msgs(**kwargs)
        log.debug(f"mqtt.output msgs {msgs}")
        if msgs:
            if mqtt_broker.name == "screen":
                for msg in msgs:
                    print(msg)
            else:
                try:
                    publish.multiple(msgs, hostname=mqtt_broker.name, port=mqtt_port, auth=auth)
                except Exception as e:
                    log.warning(
                        f"Error publishing MQTT messages to broker '{mqtt_broker.name}' on port '{mqtt_port}' with auth '{auth}'"
                    )
                    log.warning(e)
        else:
            if mqtt_broker == "screen":
                print("MQTT build_msgs returned no messages")
            else:
                log.warning("MQTT build_msgs returned no messages")
