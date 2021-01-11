import logging
import paho.mqtt.publish as publish

log = logging.getLogger("MPP-Solar")


class hass_config:
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.hass_config __init__ kwargs {kwargs}")

    def output(self, data=None, tag=None, mqtt_broker="localhost", mqtt_user=None, mqtt_pass=None):
        log.info("Using output processor: hass_config")
        if data is None:
            return

        if mqtt_user is not None and mqtt_pass is not None:
            auth = {"username": mqtt_user, "password": mqtt_pass}
            log.info(f"Using mqtt authentication, username: {mqtt_user}, password: [supplied]")
        else:
            log.debug("No mqtt authentication used")
            auth = None

        # Build array of mqtt messages with hass autoconfig format
        msgs = []
        # Remove command and _command_description
        data.pop("_command", None)
        data.pop("_command_description", None)
        # Loop through responses
        for key in data:
            # value = data[key][0]
            unit = data[key][1]
            # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
            # topic "homeassistant/binary_sensor/garden/config"
            # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C"}'
            topic = f"homeassistant/sensor/pm_{tag}_{key}/config"
            payload = f'{{"name": "pm_{tag}_{key}", "state_topic": "homeassistant/sensor/pm_{tag}_{key}/state", "unit_of_measurement": "{unit}"}}'
            msg = {"topic": topic, "payload": payload, "retain": True}
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker, auth=auth)
