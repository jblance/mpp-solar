import logging
import paho.mqtt.publish as publish

log = logging.getLogger("MPP-Solar")


class influx_mqtt:
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"processor.influx_mqtt __init__ kwargs {kwargs}")

    def output(self, data=None, tag=None, mqtt_broker="localhost", mqtt_user=None, mqtt_pass=None):
        log.info("Using output processor: influx_mqtt")

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

        # Build array of Influx Line Protocol messages
        msgs = []
        # Remove command and _command_description
        data.pop("_command", None)
        data.pop("_command_description", None)
        # Loop through responses
        for key in data:
            value = data[key][0]
            unit = data[key][1]
            # Message format is: tag, tag,setting=total_ac_output_apparent_power value=1577.0,unit="VA"
            msg = {
                "topic": tag,
                "payload": f"{tag},setting={key} value={value},unit={unit}",
            }
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker, auth=auth)
