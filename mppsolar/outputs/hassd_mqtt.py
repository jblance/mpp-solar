import json as js
import logging
import re

from ..helpers import get_kwargs, key_wanted
from .mqtt import mqtt

log = logging.getLogger("hassd_mqtt")


class hassd_mqtt(mqtt):
    def __str__(self):
        return """outputs the to the supplied mqtt broker in hass format: eg "homeassistant/sensor/mpp_{tag}_{key}/state" """

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def build_msgs(self, *args, **kwargs):
        data = get_kwargs(kwargs, "data")
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")
        device_name = get_kwargs(kwargs, "name", "mppsolar")

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
                topic = f"homeassistant/sensor/mpp_{tag}_{key}/config"
                topic = topic.replace(" ", "_")
                name = f"{tag} {_key}"
                payload = {"name": f"{name}", "state_topic": f"homeassistant/sensor/mpp_{tag}_{key}/state", "unit_of_measurement": f"{unit}", "unique_id": f"mpp_{tag}_{key}", "force_update": "true"}
                # payload["device"] = {"name": f"{device_name}", "identifiers": ["mppsolar"], "model": "PIP6048MAX", "manufacturer": "MPP-Solar"}
                payload["device"] = {"name": f"{device_name}", "identifiers": [f"{device_name}"], "model": f"{device_name}", "manufacturer": "MPP-Solar"}
                if unit == "W":
                    payload.update({"state_class": "measurement", "device_class": "power"})
                # msg = {"topic": topic, "payload": payload, "retain": True}
                payloads = js.dumps(payload)
                # print(payloads)
                msg = {"topic": topic, "payload": payloads}
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
