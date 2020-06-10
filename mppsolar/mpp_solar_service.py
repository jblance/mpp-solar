#!/usr/bin/python3
#
#
# MPP-Solar-Service
#
import configparser
import time
import systemd.daemon
from argparse import ArgumentParser

import paho.mqtt.publish as publish
from .mpputils import mppUtils


def main():
    # Some default defaults
    pause = 60
    mqtt_broker = 'localhost'

    # Process arguments
    parser = ArgumentParser(description='MPP Solar Inverter Helper Service')
    parser.add_argument('-c', '--configfile', type=str, help='Full location of config file', default='/etc/mpp-solar/mpp-solar.conf')
    args = parser.parse_args()

    print('MPP-Solar-Service: Initializing ...')
    print('MPP-Solar-Service: Config file: {}'.format(args.configfile))
    config = configparser.ConfigParser()
    config.read(args.configfile)
    sections = config.sections()

    if 'SETUP' in config:
        pause = config['SETUP'].getint('pause', fallback=60)
        mqtt_broker = config['SETUP'].get('mqtt_broker', fallback='localhost')
        sections.remove('SETUP')
    print('MPP-Solar-Service: Config setting - pause: {}'.format(pause))
    print('MPP-Solar-Service: Config setting - mqtt_broker: {}'.format(mqtt_broker))
    print('MPP-Solar-Service: Config setting - command sections found: {}'.format(len(sections)))
    # Build array of commands to run
    mppUtilArray = []
    for section in sections:
        # print('MPP-Solar-Service: Execute - {}'.format(config[section]))
        model = config[section].get('model')
        port = config[section].get('port')
        baud = config[section].get('baud', fallback=2400)
        command = config[section].get('command')
        tag = config[section].get('tag')
        format = config[section].get('format')
        mp = mppUtils(port, baud, model)
        mppUtilArray.append({'mp': mp, 'command': command, 'format': format, 'tag': tag})

    # Tell systemd that our service is ready
    systemd.daemon.notify('READY=1')

    while True:
        # Loop through the configured commands
        for item in mppUtilArray:
            # Tell systemd watchdog we are still alive
            systemd.daemon.notify('WATCHDOG=1')
            print('MPP-Solar-Service: item {}'.format(item))
            if item['format'] == 'influx':
                print('MPP-Solar-Service: format influx not supported')
            elif item['format'] == 'influx2':
                # print('MPP-Solar-Service: format influx2 yet to be supported')
                msgs = []
                _data = item['mp'].getInfluxLineProtocol2(item['command'])
                for _item in _data:
                    payload = 'mpp-solar,command={} {}'.format(item['tag'], _item)
                    msg = {'topic': 'mpp-solar', 'payload': payload}
                    msgs.append(msg)
                publish.multiple(msgs, hostname=mqtt_broker)
            elif item['format'] == 'mqtt1':
                # print('MPP-Solar-Service: format mqtt1 yet to be supported')
                msgs = []
                _data = item['mp'].getResponseDict(item['command'])
                for _item in _data:
                    # Value
                    topic = 'mpp-solar/{}/{}/value'.format(item['tag'], _item)
                    payload = _data[_item][0]
                    msg = {'topic': topic, 'payload': payload}
                    msgs.append(msg)
                    # print (msg)
                    # Unit
                    topic = 'mpp-solar/{}/{}/unit'.format(item['tag'], _item)
                    payload = '{}'.format(_data[_item][1])
                    msg = {'topic': topic, 'payload': payload}
                    msgs.append(msg)
                    # print (msg)
                publish.multiple(msgs, hostname=mqtt_broker)
            else:
                print('MPP-Solar-Service: format {} not supported'.format(item['format']))
        print('MPP-Solar-Service: sleeping for {}sec'.format(pause))
        # Tell systemd watchdog we are still alive
        systemd.daemon.notify('WATCHDOG=1')
        time.sleep(pause)
