import logging
import re

from .mqtt import mqtt
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("hass_mqtt")


class hass_mqtt(mqtt):
    def __str__(self):
        return """outputs the to the supplied mqtt broker in hass format: eg "homeassistant/sensor/mpp_{tag}_{key}/state" """

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = get_kwargs(kwargs, "data")
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")

        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        # Build array of mqtt messages with hass update format
        # assumes hass_config has been run
        # or hass updated manually
        msgs = []
        # Remove command and _command_description
        data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)

        # Loop through responses
        for _key in data:
            value = data[_key][0]
            unit = data[_key][1]
            # remove spaces
            key = _key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                #
                # CONFIG / AUTODISCOVER
                #
                # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
                # topic "homeassistant/binary_sensor/garden/config"
                # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C"}'
                if unit == "bool" or value == "enabled" or value == "disabled":
                    topic = f"homeassistant/binary_sensor/mpp_{tag}_{key}/config"
                    topic = topic.replace(" ", "_")
                    name = f"{tag} {_key}"
                    payload = f'{{"name": "{name}", "state_topic": "homeassistant/binary_sensor/mpp_{tag}_{key}/state", "unique_id": "mpp_{tag}_{key}", "force_update": "true" }}'
                    msg = {"topic": topic, "payload": payload}
                    msgs.append(msg)
                    topic = f"homeassistant/binary_sensor/mpp_{tag}_{key}/state"
                    if value == 0 or value == "0" or value == "disabled":
                        # for QPIWS one can add [or tag == "myQPIWStag"], if there's a QPIWS section in mpp-solar.conf
                        value = "OFF"
                    elif value == 1 or value == "1" or value == "enabled":
                        value = "ON"
                    msg = {"topic": topic, "payload": value}
                    msgs.append(msg)
                else:
                    topic = f"homeassistant/sensor/mpp_{tag}_{key}/config"
                    topic = topic.replace(" ", "_")
                    name = f"{tag} {_key}"
                    if unit == "W":
                        payload = f'{{"name": "{name}", "state_topic": "homeassistant/sensor/mpp_{tag}_{key}/state", "unit_of_measurement": "{unit}", "unique_id": "mpp_{tag}_{key}", "state_class": "measurement", "device_class": "power", "force_update": "true" }}'
                    elif unit == "":
                        payload = f'{{"name": "{name}", "state_topic": "homeassistant/sensor/mpp_{tag}_{key}/state", "unique_id": "mpp_{tag}_{key}", "force_update": "true" }}'
                    else:
                        payload = f'{{"name": "{name}", "state_topic": "homeassistant/sensor/mpp_{tag}_{key}/state", "unit_of_measurement": "{unit}", "unique_id": "mpp_{tag}_{key}", "force_update": "true" }}'
                    # msg = {"topic": topic, "payload": payload, "retain": True}
                    msg = {"topic": topic, "payload": payload}
                    msgs.append(msg)
                    #
                    # VALUE SETTING
                    #
                    # unit = data[key][1]
                    # 'tag'/status/total_output_active_power/value 1250
                    # 'tag'/status/total_output_active_power/unit W
                    topic = f"homeassistant/sensor/mpp_{tag}_{key}/state"
                    msg = {"topic": topic, "payload": value}
                    msgs.append(msg)
        return msgs
