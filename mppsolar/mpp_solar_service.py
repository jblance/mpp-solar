#!/usr/bin/python
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
    # Tell systemd that our service is ready
    systemd.daemon.notify('READY=1')

    while True:
        #print('MPP-Solar-Service: while loop')
        for section in sections:
            print('MPP-Solar-Service: Execute - {}'.format(config[section]))
            tag=section
            model=config[section].get('model')
            port=config[section].get('port')
            baud=config[section].get('baud', fallback=2400)
            command=config[section].get('command')
            format=config[section].get('format')
            print('MPP-Solar-Service: Section: {} Setting - model: {}'.format(section, model))
            print('MPP-Solar-Service: Section: {} Setting - port: {}'.format(section, port))
            print('MPP-Solar-Service: Section: {} Setting - baud: {}'.format(section, baud))
            print('MPP-Solar-Service: Section: {} Setting - command: {}'.format(section, command))
            print('MPP-Solar-Service: Section: {} Setting - format: {}'.format(section, format))
            # [Inverter_1]
            # model=standard
            # port=/dev/ttyUSB0
            # baud=2400
            # command=QPGS0
            # format=influx2
            #mp = mppUtils(usb_port, args.baud, args.model)
            #    serial_number = mp.getSerialNumber()
        time.sleep(pause)
