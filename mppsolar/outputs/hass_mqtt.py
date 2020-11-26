import logging
import paho.mqtt.publish as publish

log = logging.getLogger('MPP-Solar')


class hass_mqtt():
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f'processor.hass_mqtt __init__ kwargs {kwargs}')

    def output(self, data=None, tag=None, mqtt_broker='localhost'):
        log.info('Using output processor: hass_mqtt')
        if data is None:
            return

        # Build array of mqtt messages with hass update format
        # assumes hass_config has been run
        # or hass updated manually
        msgs = []
        # Loop through responses
        for key in data:
            value = data[key][0]
            # unit = data[key][1]
            # 'tag'/status/total_output_active_power/value 1250
            # 'tag'/status/total_output_active_power/unit W
            topic = f"homeassistant/sensor/pm_{tag}_{key}/state"
            msg = {'topic': topic, 'payload': value}
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker)
