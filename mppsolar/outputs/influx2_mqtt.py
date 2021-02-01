import logging

from .mqtt import mqtt

log = logging.getLogger("MPP-Solar")


class influx2_mqtt(mqtt):
    def __str__(self):
        return "outputs the to the supplied mqtt broker: eg mpp-solar,command=QPGS0 max_charger_range=120.0"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.influx2_mqtt __init__ kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = self.get_kwargs(kwargs, "data")
        tag = self.get_kwargs(kwargs, "tag")
        topic = self.get_kwargs(kwargs, "topic", default="mpp-solar")
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
        # Loop through responses
        for key in data:
            value = data[key][0]
            # remove spaces
            key = key.lower().replace(" ", "_")
            if isinstance(value, int) or isinstance(value, float):
                msg = {
                    "topic": topic,
                    "payload": f"{topic},command={tag} {key}={value}",
                }
            else:
                msg = {
                    "topic": topic,
                    "payload": f'{topic},command={tag} {key}="{value}"',
                }
            msgs.append(msg)
        return msgs
