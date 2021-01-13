import logging
import paho.mqtt.publish as publish

from .mqtt import mqtt

log = logging.getLogger("MPP-Solar")


class influx2_mqtt(mqtt):
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.influx2_mqtt __init__ kwargs {kwargs}")

    def build_msgs(self, data, tag):
        # Build array of Influx Line Protocol II messages
        # Message format is: mpp-solar,command=QPGS0 max_charger_range=120.0
        #                    mpp-solar,command=inverter2 parallel_instance_number="valid"
        #                    measurement,tag_set field_set
        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        if tag is None:
            tag = cmd
        # Loop through responses
        for key in data:
            value = data[key][0]
            if isinstance(value, int) or isinstance(value, float):
                msg = {
                    "topic": "mpp-solar",
                    "payload": f"mpp-solar,command={tag} {key}={value}",
                }
            else:
                msg = {
                    "topic": "mpp-solar",
                    "payload": f'mpp-solar,command={tag} {key}="{value}"',
                }
            msgs.append(msg)
        return msgs
