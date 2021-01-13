import logging
import paho.mqtt.publish as publish

from .baseoutput import BaseOutput

log = logging.getLogger("MPP-Solar")


class mqtt(BaseOutput):
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.mqtt __init__ kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = self.get_kwargs(kwargs, "data")
        tag = self.get_kwargs(kwargs, "tag")
        # Build array of mqtt messages
        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        if tag is None:
            tag = cmd
        # Loop through responses
        for key in data:
            value = data[key][0]
            unit = data[key][1]
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
        data = self.get_kwargs(kwargs, "data")
        if data is None:
            return
        tag = self.get_kwargs(kwargs, "tag")
        topic = self.get_kwargs(kwargs, "topic")
        mqtt_broker = self.get_kwargs(kwargs, "mqtt_broker", "localhost")
        mqtt_user = self.get_kwargs(kwargs, "mqtt_user")
        mqtt_pass = self.get_kwargs(kwargs, "mqtt_pass")

        if mqtt_user is not None and mqtt_pass is not None:
            auth = {"username": mqtt_user, "password": mqtt_pass}
            log.info(f"Using mqtt authentication, username: {mqtt_user}, password: [supplied]")
        else:
            log.debug("No mqtt authentication used")
            auth = None

        msgs = self.build_msgs(data=data, tag=tag, topic=topic)
        publish.multiple(msgs, hostname=mqtt_broker, auth=auth)
