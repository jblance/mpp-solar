import logging
import paho.mqtt.publish as publish

log = logging.getLogger('powermon')


class mqtt():
    def __init__(self, *args, **kwargs) -> None:
        log.info('Using output processor: mqtt')
        log.debug(f'processor.mqtt __init__ kwargs {kwargs}')
        data = kwargs['results']
        tag = kwargs['tag']
        mqtt_broker = kwargs['mqtt_broker']
        if data is None:
            return

        # Build array of mqtt messages
        msgs = []
        # Loop through responses
        for key in data:
            value = data[key][0]
            unit = data[key][1]
            # 'tag'/status/total_output_active_power/value 1250
            # 'tag'/status/total_output_active_power/unit W
            msg = {'topic': f'{tag}/status/{key}/value', 'payload': value}
            msg = {'topic': f'{tag}/status/{key}/unit', 'payload': unit}
            msgs.append(msg)
        publish.multiple(msgs, hostname=mqtt_broker)
