import logging
import paho.mqtt.publish as publish

log = logging.getLogger("MPP-Solar")


class mqtt:
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.mqtt __init__ kwargs {kwargs}")

    def output(self, data=None, tag=None, mqtt_broker="localhost", mqtt_user=None, mqtt_pass=None):
        log.info("Using output processor: mqtt")

        if data is None:
            return

        if mqtt_user is not None and mqtt_pass is not None:
            auth = {"username": mqtt_user, "password": mqtt_pass}
            log.info(f"Using mqtt authentication, username: {mqtt_user}, password: [supplied]")
        else:
            log.debug("No mqtt authentication used")
            auth = None

        # Build array of mqtt messages
        msgs = []
        # Remove command and _command_description
        data.pop("_command", None)
        data.pop("_command_description", None)
        # Loop through responses
        for key in data:
            value = data[key][0]
            unit = data[key][1]
            # 'tag'/status/total_output_active_power/value 1250
            # 'tag'/status/total_output_active_power/unit W
            msg = {"topic": f"{tag}/status/{key}/value", "payload": value}
            msg = {"topic": f"{tag}/status/{key}/unit", "payload": unit}
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker, auth=auth)
