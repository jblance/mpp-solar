import json as js
import logging
import re
from datetime import datetime

from mppsolar.helpers import key_wanted

log = logging.getLogger("hass")


class hass:
    def __init__(self, remove_spaces=True, keep_case=False, filter=None, excl_filter=None, 
                 discovery_prefix="homeassistant", entity_id_prefix="mpp", device_name="MPP Solar", 
                 device_id="mpp-solar", device_model="MPP Solar", device_manufacturer="MPP Solar"):
        self.remove_spaces = remove_spaces
        self.keep_case = keep_case
        self.filter = filter
        self.excl_filter = excl_filter

        self.discovery_prefix = discovery_prefix
        self.entity_id_prefix = entity_id_prefix
        self.device_name = device_name
        self.device_id = device_id
        self.device_model = device_model
        self.device_manufacturer = device_manufacturer

    def output(*args, **kwargs):
        log.info("Using output formatter: hass")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")

        config_msgs = []
        value_msgs = []
        if data is None:
            return []

        # check if config supplied
        config = get_kwargs(kwargs, "config")
        fullconfig = get_kwargs(kwargs, "fullconfig")
        # print(fullconfig)
        if config is not None:
            log.debug(f"config: {config}")
            # get formatting info
            remove_spaces = config.get("remove_spaces", True)
            keep_case = config.get("keep_case", False)
            # extra_info = config.get("extra_info", False)
            filter = config.get("filter", None)
            excl_filter = config.get("excl_filter", None)
            # formatter specific
            

        _filter = None
        _excl_filter = None

        if filter is not None:
            _filter = re.compile(filter)

        if excl_filter is not None:
            _excl_filter = re.compile(excl_filter)

        # remove raw response
        if "raw_response" in data:
            data.pop("raw_response")

        # remove command info
        if "_command" in data:
            data.pop("_command")
        if "_command_description" in data:
            data.pop("_command_description")

        # build data to display
        for key in data:
            f_key = key

            # remove spaces
            if remove_spaces:
                f_key = f_key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                f_key = f_key.lower()

            if key_wanted(f_key, _filter, _excl_filter):
                # Get key data
                value = data[key][0]
                unit = data[key][1]

                # Set component type
                if unit == "bool" or value == "enabled" or value == "disabled":
                    component = "binary_sensor"
                else:
                    component = "sensor"

                # Make value adjustments
                if component == "binary_sensor":
                    if value == 0 or value == "0" or value == "disabled":
                        value = "OFF"
                    elif value == 1 or value == "1" or value == "enabled":
                        value = "ON"

                # Get icon if present
                icon = None
                if len(data[key]) > 2 and data[key][2] and "icon" in data[key][2]:
                    icon = data[key][2]["icon"]

                # Get device_class if present
                device_class = None
                if len(data[key]) > 2 and data[key][2] and "device-class" in data[key][2]:
                    device_class = data[key][2]["device-class"]

                # Get state_class if present
                state_class = None
                if len(data[key]) > 2 and data[key][2] and "state_class" in data[key][2]:
                    state_class = data[key][2]["state_class"]

                # Object ID
                object_id = f"{entity_id_prefix}_{f_key}".lower()

                name = f"{entity_id_prefix} {key}"

                # Home Assistant MQTT Auto Discovery Message
                #
                # Topic
                # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config, eg homeassistant/binary_sensor/garden/config
                topic_base = f"{discovery_prefix}/{component}/{object_id}".replace(" ", "_")
                topic = f"{topic_base}/config"
                state_topic = f"{topic_base}/state"

                # Payload
                # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C", "icon": "power-plug"}'
                payload = {
                    "name": f"{name}",
                    "state_topic": f"{state_topic}",
                    "unique_id": f"{object_id}",
                    "force_update": "true",
                    "last_reset": str(datetime.now()),
                }

                # Add device info
                # payload["device"] = {"name": f"{device_name}", "identifiers": ["mppsolar"], "model": "PIP6048MAX", "manufacturer": "MPP-Solar"}
                payload["device"] = {
                    "name": device_name,
                    "identifiers": [device_id],
                    "model": device_model,
                    "manufacturer": device_manufacturer,
                }

                # Add unit of measurement
                if unit and unit != "bool":
                    payload["unit_of_measurement"] = f"{unit}"

                # Add icon
                if icon:
                    payload.update({"icon": icon})

                # Add device class
                if device_class:
                    payload["device_class"] = device_class

                # Add state_class
                if state_class:
                    payload["state_class"] = state_class

                # TODO move to protocol defs
                # if unit == "W":
                #    payload.update({"state_class": "measurement", "device_class": "power"})
                # TODO move to protocol defs
                # if unit == "Wh" or unit == "kWh":
                #     payload.update(
                #         {
                #             "icon": "mdi:counter",
                #             "device_class": "energy",
                #             "state_class": "total",
                #         }
                #     )

                payloads = js.dumps(payload)
                # print(payloads)
                msg = {"topic": topic, "payload": payloads}
                config_msgs.append(msg)

                # VALUE SETTING
                msg = {"topic": state_topic, "payload": value}
                value_msgs.append(msg)

        # order value msgs after config to allow HA time to build entity before state data arrives
        return config_msgs + value_msgs
