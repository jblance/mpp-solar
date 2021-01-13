import logging

from .mqtt import mqtt

log = logging.getLogger("MPP-Solar")


class hass_mqtt(mqtt):
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.hass_mqtt __init__ kwargs {kwargs}")

    def build_msgs(self, data, tag):
        # Build array of mqtt messages with hass update format
        # assumes hass_config has been run
        # or hass updated manually
        msgs = []
        # Remove command and _command_description
        data.pop("_command", None)
        data.pop("_command_description", None)
        # Loop through responses
        for key in data:
            value = data[key][0]
            # unit = data[key][1]
            # 'tag'/status/total_output_active_power/value 1250
            # 'tag'/status/total_output_active_power/unit W
            topic = f"homeassistant/sensor/pm_{tag}_{key}/state"
            msg = {"topic": topic, "payload": value}
            msgs.append(msg)
        return msgs
