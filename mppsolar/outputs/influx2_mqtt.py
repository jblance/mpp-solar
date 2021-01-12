import logging
import paho.mqtt.publish as publish

log = logging.getLogger("MPP-Solar")


class influx2_mqtt:
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.influx2_mqtt __init__ kwargs {kwargs}")

    def output(self, data=None, tag=None, mqtt_broker="localhost", mqtt_user=None, mqtt_pass=None):
        log.info("Using output processor: influx2_mqtt")

        if data is None:
            return

        if tag is None:
            tag = "mpp-solar"

        if mqtt_user is not None and mqtt_pass is not None:
            auth = {"username": mqtt_user, "password": mqtt_pass}
            log.info(f"Using mqtt authentication, username: {mqtt_user}, password: [supplied]")
        else:
            log.debug("No mqtt authentication used")
            auth = None

        # Build array of Influx Line Protocol II messages
        msgs = []
        # Remove command and _command_description
        data.pop("_command", None)
        data.pop("_command_description", None)
        # Loop through responses
        for key in data:
            value = data[key][0]
            # unit = _data[key][1]
            # Message format is: mpp-solar,command=QPGS0 max_charger_range=120.0
            if isinstance(value, int) or isinstance(value, float):
                msg = {
                    "topic": "mpp-solar",
                    "payload": f"mpp-solar,command={tag} {key}={value}",
                }
            else:
                msg = {
                    "topic": "mpp-solar",
                    "payload": f'mpp-solar,command={tag} {key}="{value}"',
                }
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker, auth=auth)
