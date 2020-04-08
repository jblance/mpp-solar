#!/usr/bin/python
#
#
# MPP-Solar-Service
#
import configparser
import time
import systemd.daemon
from argparse import ArgumentParser

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
    # Tell systemd that our service is ready
    systemd.daemon.notify('READY=1')

    while True:
        #print('MPP-Solar-Service: while loop')
        for section in sections:
            print('MPP-Solar-Service: Execute - {}'.format(config[section]))
        time.sleep(pause)
