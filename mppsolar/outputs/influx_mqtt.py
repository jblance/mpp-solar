import logging
import paho.mqtt.publish as publish

log = logging.getLogger('powermon')


class influx_mqtt():
    def __init__(self, *args, **kwargs) -> None:
        log.info('Using output processor: influx_mqtt')
        log.debug(f'processor.influx_mqtt __init__ kwargs {kwargs}')
        data = kwargs['results']
        tag = kwargs['tag']
        mqtt_broker = kwargs['mqtt_broker']
        if data is None:
            return

        # Build array of Influx Line Protocol messages
        msgs = []
        # Loop through responses
        for key in data:
            value = data[key][0]
            # unit = _data[key][1]
            # Message format is: mpp-solar,command=QPGS0 max_charger_range=120.0
            msg = {'topic': 'powermon', 'payload': f'powermon,command={tag} {key}={value}'}
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker)
