import json as js
import logging
import re
from datetime import datetime
from time import sleep

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
        command = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)

        # check if config supplied
        config = get_kwargs(kwargs, "config")
        if config is not None:
            log.debug(f"config: {config}")
            # try for fullconfig
            fullconfig = get_kwargs(kwargs, "fullconfig")
            # get results topic
            # results_topic = config.get("results_topic", None)
            # get formatting info
            remove_spaces = config.get("remove_spaces", True)
            keep_case = config.get("keep_case", False)
            filter = config.get("filter", None)
            excl_filter = config.get("excl_filter", None)
            tag = config.get("tag", None)
            device = fullconfig.get("device", {})
            device_name = device.get("name", "mppsolar")
            device_id = device.get("id", "mppsolar")
            device_model = device.get("model", "mppsolar")
            device_manufacturer = device.get("manufacturer", "mppsolar")
        else:
            # results_topic = None
            # get formatting info
            remove_spaces = True
            keep_case = get_kwargs(kwargs, "keep_case")
            filter = get_kwargs(kwargs, "filter")
            excl_filter = get_kwargs(kwargs, "excl_filter")
            tag = get_kwargs(kwargs, "tag")
            device_name = get_kwargs(kwargs, "name", "mppsolar")
            device_id = device_name
            device_model = device_name
            device_manufacturer = "MPP-Solar"

        if filter is not None:
            filter = re.compile(filter)
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)
        if tag is None:
            if command:
                tag = command
            else:
                tag = "mppsolar"

        # Build array of mqtt messages with hass update format
        config_msgs = []
        value_msgs = []

        # Loop through responses
        for key, values in data.items():
            orig_key = key
            value = values[0]
            unit = values[1]
            if len(values) > 2 and values[2] and "unit" in values[2]:
                unit = values[2]["unit"]
                
            icon = None
            if len(values) > 2 and values[2] and "icon" in values[2]:
                icon = values[2]["icon"]
            device_class = None

            if len(values) > 2 and values[2] and "device-class" in values[2]:
                device_class = values[2]["device-class"]
            state_class = None
            if len(values) > 2 and values[2] and "state_class" in values[2]:
                state_class = values[2]["state_class"]

            # remove spaces
            if remove_spaces:
                key = key.replace(" ", "_")
            if not keep_case:
                # make lowercase
                key = key.lower()
            if key_wanted(key, filter, excl_filter):
                #
                # CONFIG / AUTODISCOVER
                #
                # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
                # topic "homeassistant/binary_sensor/garden/config"
                # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C", "icon": "power-plug"}'

                # For binary sensors
                if unit == "bool" or value == "enabled" or value == "disabled":
                    sensor = "binary_sensor"
                    if value == 0 or value == "0" or value == "disabled":
                        # for QPIWS one can add [or tag == "myQPIWStag"], if there's a QPIWS section in mpp-solar.conf
                        value = "OFF"
                    elif value == 1 or value == "1" or value == "enabled":
                        value = "ON"
                else:
                    sensor = "sensor"
                topic = f"homeassistant/{sensor}/mpp_{tag}_{key}/config"
                topic = topic.replace(" ", "_")
                name = f"{tag} {orig_key}"
                payload = {
                    "name": f"{name}",
                    "state_topic": f"homeassistant/{sensor}/mpp_{tag}_{key}/state",
                    "unique_id": f"mpp_{tag}_{key}",
                    "force_update": "true",
                }
                if unit and unit != "bool":
                    payload["unit_of_measurement"] = f"{unit}"

                # payload["device"] = {"name": f"{device_name}", "identifiers": ["mppsolar"], "model": "PIP6048MAX", "manufacturer": "MPP-Solar"}
                payload["device"] = {
                    "name": device_name,
                    "identifiers": [device_id],
                    "model": device_model,
                    "manufacturer": device_manufacturer,
                }

                if device_class:
                    payload["device_class"] = device_class
                if state_class:
                    payload["state_class"] = state_class
                if icon:
                    payload.update({"icon": icon})
                if unit == "Hz":
                    payload.update({"device_class": "frequency"})
                if unit in ["A", "mA"]:
                    payload.update({"device_class": "current"})
                if unit in ["V", "mV"]:
                    payload.update({"device_class": "voltage"})
                if unit in ["W", "kW"]:
                    payload.update({"device_class": "power"})
                if unit == "Wh" or unit == "kWh":
                    payload.update(
                        {
                            "icon": "mdi:counter",
                            "device_class": "energy",
                            "state_class": "total_increasing",
                            "last_reset": str(datetime.now()),
                        }
                    )

                # msg = {"topic": topic, "payload": payload, "retain": True}
                payloads = js.dumps(payload)
                # print(payloads)
                msg = {"topic": topic, "payload": payloads}
                config_msgs.append(msg)
                #
                # VALUE SETTING
                #
                # 'tag'/status/total_output_active_power/value 1250
                # 'tag'/status/total_output_active_power/unit W
                topic = f"homeassistant/{sensor}/mpp_{tag}_{key}/state"
                msg = {"topic": topic, "payload": value}
                value_msgs.append(msg)
        return config_msgs, value_msgs

    def output(self, *args, **kwargs):
        """Over write mqtt output as we want to send config msgs first...."""
        log.info("Using output processor: hassd_mqtt")
        log.debug(f"kwargs {kwargs}")
        data = get_kwargs(kwargs, "data")
        # exit if no data
        if data is None:
            return

        # get the broker instance
        mqtt_broker = get_kwargs(kwargs, "mqtt_broker")
        # exit if no broker
        if mqtt_broker is None:
            return

        # build the messages...
        config_msgs, value_msgs = self.build_msgs(**kwargs)
        log.debug(f"hassd_mqtt.output config_msgs {config_msgs}")
        log.debug(f"hassd_mqtt.output value_msgs {value_msgs}")

        # publish
        mqtt_broker.publishMultiple(config_msgs)
        sleep(0.5)
        mqtt_broker.publishMultiple(value_msgs)
