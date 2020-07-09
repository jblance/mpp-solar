import logging
import paho.mqtt.publish as publish

log = logging.getLogger('MPP-Solar')


class influx2_mqtt():
    def __init__(self, *args, **kwargs) -> None:
        log.debug(f'processor.influx2_mqtt __init__ kwargs {kwargs}')

    def output(data=None, tag=None, mqtt_broker='localhost'):
        log.info('Using output processor: influx2_mqtt')
        if data is None:
            return

        # Build array of Influx Line Protocol II messages
        msgs = []
        # Loop through responses
        for key in data:
            value = data[key][0]
            # unit = _data[key][1]
            # Message format is: mpp-solar,command=QPGS0 max_charger_range=120.0
            msg = {'topic': 'mppsolar', 'payload': f'mppsolar,command={tag} {key}={value}'}
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker)
