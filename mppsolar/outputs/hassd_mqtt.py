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
        log.debug(f"kwargs {kwargs}")

        data = get_kwargs(kwargs, "data")
        # Clean data
        if "_command" in data:
            command = data.pop("_command")
        if "_command_description" in data:
            data.pop("_command_description")
        if "raw_response" in data:
            data.pop("raw_response")

        # check if config supplied
        config = get_kwargs(kwargs, "config")
        if config is not None:
            log.debug(f"config: {config}")
            # get results topic
            # results_topic = config.get("results_topic", None)
            # get formatting info
            remove_spaces = config.get("remove_spaces", True)
            keep_case = config.get("keep_case", False)
            filter = config.get("filter", None)
            excl_filter = config.get("excl_filter", None)
            tag = config.get("tag", None)
            # device_name =
        else:
            # results_topic = None
            # get formatting info
            remove_spaces = True
            keep_case = get_kwargs(kwargs, "keep_case")
            filter = get_kwargs(kwargs, "filter")
            excl_filter = get_kwargs(kwargs, "excl_filter")
            tag = get_kwargs(kwargs, "tag")
        device_name = get_kwargs(kwargs, "name", "mppsolar")

        if filter is not None:
            filter = re.compile(filter)
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)
        if tag is None:
            tag = command

        # build topic prefix
        # if results_topic is not None:
        #     topic_prefix = results_topic
        # else:
        #     topic_prefix = f"{tag}/status"

        # build data to output
        _data = {}
        for key in data:
            _values = data[key]
            # remove spaces
            if remove_spaces:
                key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                _data[key] = _values
        log.debug(f"output data: {_data}")

        # Build array of mqtt messages with hass update format
        # assumes hass_config has been run
        # or hass updated manually
        msgs = []

        # Loop through responses
        for _key in _data:
            value = _data[_key][0]
            unit = _data[_key][1]

            #
            # CONFIG / AUTODISCOVER
            #
            # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
            # topic "homeassistant/binary_sensor/garden/config"
            # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C"}'

            # For binary sensors
            if unit == "bool":
                sensor = "binary_sensor"
            else:
                sensor = "sensor"
            topic = f"homeassistant/{sensor}/mpp_{tag}_{_key}/config"
            topic = topic.replace(" ", "_")
            name = f"{tag} {_key}"
            payload = {
                "name": f"{name}",
                "state_topic": f"homeassistant/{sensor}/mpp_{tag}_{_key}/state",
                "unique_id": f"mpp_{tag}_{_key}",
                "force_update": "true",
            }
            if unit and unit != "bool":
                payload["unit_of_measurement"] = f"{unit}"

            # payload["device"] = {"name": f"{device_name}", "identifiers": ["mppsolar"], "model": "PIP6048MAX", "manufacturer": "MPP-Solar"}
            payload["device"] = {
                "name": f"{device_name}",
                "identifiers": [f"{device_name}"],
                "model": f"{device_name}",
                "manufacturer": "MPP-Solar",
            }
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
            topic = f"homeassistant/{sensor}/mpp_{tag}_{_key}/state"
            msg = {"topic": topic, "payload": value}
            msgs.append(msg)
        return msgs
