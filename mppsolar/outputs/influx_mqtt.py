import logging
import re

from .mqtt import mqtt
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("influx_mqtt")


class influx_mqtt(mqtt):
    def __str__(self):
        return """outputs the to the supplied mqtt broker: eg {tag}, {tag},setting=total_ac_output_apparent_power value=1577.0,unit="VA" """

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = get_kwargs(kwargs, "data")
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")
        topic = get_kwargs(kwargs, "mqtt_topic", default="mpp-solar")

        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        # Build array of Influx Line Protocol messages
        msgs = []
        # Remove command and _command_description
        cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)

        if tag is None:
            tag = cmd
        # Loop through responses
        for key, values in data.items():
            value = values[0]
            unit = values[1]
            # remove spaces
            key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            # Message format is: tag, tag,setting=total_ac_output_apparent_power value=1577.0,unit="VA"
            if key_wanted(key, filter, excl_filter):
                if not unit:
                    msg = {
                        "topic": topic,
                        "payload": f"{tag},setting={key} value={value}",
                    }
                else:
                    msg = {
                        "topic": topic,
                        "payload": f"{tag},setting={key} value={value},unit={unit}",
                    }
                msgs.append(msg)
        return msgs
