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
    parser = ArgumentParser(description='MPP Solar Inverter Helper Service')
    parser.add_argument('-c', '--configfile', type=str, help='Full location of config file', default='/etc/mpp-solar/mpp-solar.conf')
    args = parser.parse_args()

    print('MPP-Solar-Service: Initializing ...')
    print('MPP-Solar-Service: Config file: {}'.format(args.configfile))
    config = configparser.ConfigParser()
    config.read(args.configfile)
    pause = config[setup].getint('pause', fallback=60)
    print('MPP-Solar-Service: Config setting - pause: {}'.format(pause))


    # Tell systemd that our service is ready
    systemd.daemon.notify('READY=1')

    while True:
        print('MPP-Solar-Service: while loop')
        time.sleep(5)
