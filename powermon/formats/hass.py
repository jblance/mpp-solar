import json as js
import logging
from datetime import datetime
from powermon.formats.abstractformat import AbstractFormat

log = logging.getLogger("hass")


class hass(AbstractFormat):
    def __init__(self, formatConfig, device):
        super().__init__(formatConfig)
        self.name = "hass"
        self.extra_info = formatConfig.get("extra_info", False)
        self.discovery_prefix = formatConfig.get("discovery_prefix", "homeassistant")
        self.entity_id_prefix = formatConfig.get("entity_id_prefix", "mpp")
        if device is None:
            self.device_name = "MPP Solar"
            self.device_id = "mpp-solar"
            self.device_model = "MPP Solar"
            self.device_manufacturer = "MPP Solar"
        else:
            self.device_name = device.name
            self.device_id = device.identifier
            self.device_model = device.model
            self.device_manufacturer = device.manufacturer

    def sendsMultipleMessages(self) -> bool:
        return True

    def format(self, result) -> list:
        log.info("Using output formatter: %s" % self.name)

        config_msgs = []
        value_msgs = []

        _result = []
        data = result.decoded_responses
        if data is None:
            return _result
        log.debug(f"data: {data}")
        displayData = self.formatAndFilterData(data)
        log.debug(f"displayData: {displayData}")

        # build data to display
        for key in displayData:
            # Get key data
            value = displayData[key][0]
            unit = displayData[key][1]

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
            if len(displayData[key]) > 2 and displayData[key][2] and "icon" in displayData[key][2]:
                icon = displayData[key][2]["icon"]

            # Get device_class if present
            device_class = None
            if len(displayData[key]) > 2 and displayData[key][2] and "device-class" in displayData[key][2]:
                device_class = displayData[key][2]["device-class"]

            # Get state_class if present
            state_class = None
            if len(displayData[key]) > 2 and displayData[key][2] and "state_class" in displayData[key][2]:
                state_class = displayData[key][2]["state_class"]

            # Object ID
            object_id = f"{self.entity_id_prefix}_{key}".lower()

            name = f"{self.entity_id_prefix} {key}"

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
                "unique_id": f"{object_id}",
                "force_update": "true",
                "last_reset": str(datetime.now()),
            }

            # Add device info
            # payload["device"] = {"name": f"{device_name}", "identifiers": ["mppsolar"], "model": "PIP6048MAX", "manufacturer": "MPP-Solar"}
            payload["device"] = {
                "name": self.device_name,
                "identifiers": [self.device_id],
                "model": self.device_model,
                "manufacturer": self.device_manufacturer,
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
