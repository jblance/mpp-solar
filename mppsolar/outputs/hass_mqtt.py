import logging

from .mqtt import mqtt

log = logging.getLogger("MPP-Solar")


class hass_mqtt(mqtt):
    def __str__(self):
        return """hass_mqtt - outputs the to the supplied mqtt broker in hass format: eg "homeassistant/sensor/pm_{tag}_{key}/state" """

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.hass_mqtt __init__ kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = self.get_kwargs(kwargs, "data")
        tag = self.get_kwargs(kwargs, "tag")
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
            # remove spaces
            key = key.replace(" ", "_")
            #
            # CONFIG / AUTODISCOVER
            #
            # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
            # topic "homeassistant/binary_sensor/garden/config"
            # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C"}'
            topic = f"homeassistant/sensor/pm_{tag}_{key}/config"
            payload = f'{{"name": "pm_{tag}_{key}", "state_topic": "homeassistant/sensor/pm_{tag}_{key}/state", "unit_of_measurement": "{unit}"}}'
            msg = {"topic": topic, "payload": payload, "retain": True}
            #
            # VALUE SETTING
            #
            # unit = data[key][1]
            # 'tag'/status/total_output_active_power/value 1250
            # 'tag'/status/total_output_active_power/unit W
            topic = f"homeassistant/sensor/pm_{tag}_{key}/state"
            msg = {"topic": topic, "payload": value}
            msgs.append(msg)
        return msgs
