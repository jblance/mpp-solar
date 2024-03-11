""" powermon / outputformats / hass.py """
import json as js
import logging
from datetime import datetime

from powermon.commands.command import Command
from powermon.commands.reading import Reading
from powermon.commands.result import Result
from powermon.outputformats.abstractformat import AbstractFormat

log = logging.getLogger("hass")


class Hass(AbstractFormat):
    """ formatter to generate home assistant auto config mqtt messages """
    def __init__(self, config):
        super().__init__(config)
        self.name = "hass"
        self.discovery_prefix = config.get("discovery_prefix", "homeassistant")
        self.entity_id_prefix = config.get("entity_id_prefix", None)

    def format(self, command: Command, result: Result, device_info) -> list:
        log.info("Using output formatter: %s", self.name)

        config_msgs = []
        value_msgs = []

        _result = []
        if result.readings is None:
            return _result
        display_data : list[Reading] = self.format_and_filter_data(result)
        log.debug("displayData: %s", display_data)

        # build data to display
        for response in display_data:
            # Get key data
            data_name = self.format_key(response.data_name)
            value = response.data_value
            unit = response.data_unit
            icon = response.icon
            device_class = response.device_class
            state_class = response.state_class

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

            # Object ID
            if self.entity_id_prefix is None:
                object_id = f"{data_name}".lower().replace(" ", "_")
                name = f"{data_name}"
            else:
                object_id = f"{self.entity_id_prefix}_{data_name}".lower().replace(" ", "_")
                name = f"{self.entity_id_prefix} {data_name}"

            # Home Assistant MQTT Auto Discovery Message
            #
            # Topic
            # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config, eg homeassistant/binary_sensor/garden/config
            topic_base = f"{self.discovery_prefix}/{component}/{object_id}".replace(" ", "_")
            topic = f"{topic_base}/config"
            state_topic = f"{topic_base}/state"

            # Payload
            # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C", "icon": "power-plug"}'
            payload = {
                "name": f"{name}",
                "state_topic": f"{state_topic}",
                "unique_id": f"{object_id}_{device_info.device_id}",
                "force_update": "true",
                "last_reset": str(datetime.now()),
            }

            # Add device info
            # payload["device"] = {"name": f"{device_name}", "identifiers": ["mppsolar"], "model": "PIP6048MAX", "manufacturer": "MPP-Solar"}
            payload["device"] = {
                "name": device_info.name,
                "identifiers": [device_info.device_id],
                "model": device_info.model,
                "manufacturer": device_info.manufacturer,
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

            payloads = js.dumps(payload)
            # print(payloads)
            msg = {"topic": topic, "payload": payloads}
            config_msgs.append(msg)

            # VALUE SETTING
            msg = {"topic": state_topic, "payload": value}
            value_msgs.append(msg)

        # order value msgs after config to allow HA time to build entity before state data arrives
        return config_msgs + value_msgs
