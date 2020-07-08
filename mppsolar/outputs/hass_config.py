import logging
import paho.mqtt.publish as publish

log = logging.getLogger('powermon')


class hass_config():
    def __init__(self, *args, **kwargs) -> None:
        log.info('Using output processor: hass_config')
        log.debug(f'processor.hass_config __init__ kwargs {kwargs}')
        data = kwargs['results']
        tag = kwargs['tag']
        mqtt_broker = kwargs['mqtt_broker']
        if data is None:
            return

        # Build array of mqtt messages with hass autoconfig format
        msgs = []
        # Loop through responses
        for key in data:
            # value = data[key][0]
            unit = data[key][1]
            # <discovery_prefix>/<component>/[<node_id>/]<object_id>/config
            # topic "homeassistant/binary_sensor/garden/config"
            # msg '{"name": "garden", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state", "unit_of_measurement": "°C"}'
            topic = f'homeassistant/sensor/pm_{tag}_{key}/config'
            payload = f'{{"name": "pm_{tag}_{key}", "state_topic": "homeassistant/sensor/pm_{tag}_{key}/state", "unit_of_measurement": "{unit}"}}'
            msg = {'topic': topic, 'payload': payload, 'retain': True}
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker)
