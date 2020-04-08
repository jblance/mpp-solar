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

    print('MPP-Solar-Service initializing ...')
    print('MPP-Solar-Service config file: {}'.format(args.configfile))
    #config = configparser.ConfigParser()
    #config.read('example.ini')
    #time.sleep(10)
    print('Startup complete')
    # Tell systemd that our service is ready
    systemd.daemon.notify('READY=1')

    while True:
        print('MPP-Solar-Service: while loop')
        time.sleep(5)
