# !/usr/bin/python
import logging
from argparse import ArgumentParser

# import mppcommands
from .mpputils import mppUtils

log = logging.getLogger('MPP-Solar')


def main():
    parser = ArgumentParser(description='MPP Solar Command Utility')
    parser.add_argument('-c', '--command', help='Command to run', default='QID')
    parser.add_argument('-D', '--enableDebug', action='store_true', help='Enable Debug')
    parser.add_argument('-d', '--device', type=str, help='Serial device to communicate with', default='/dev/ttyUSB0')
    parser.add_argument('-b', '--baud', type=int, help='Baud rate for serial communications', default=2400)
    parser.add_argument('-l', '--listknown', action='store_true', help='List known commands')
    parser.add_argument('-s', '--getStatus', action='store_true', help='Get Inverter Status')
    parser.add_argument('-t', '--getSettings', action='store_true', help='Get Inverter Settings')
    parser.add_argument('-R', '--showraw', action='store_true', help='Display the raw results')
    args = parser.parse_args()

    ch = logging.StreamHandler()
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # Turn on debug if needed
    if(args.enableDebug):
        log.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARNING)
        ch.setLevel(logging.WARNING)
    # add the handlers to logger
    log.addHandler(ch)

    log.debug('command %s', args.command)
    log.debug('Serial device used: %s, baud rate: %d', args.device, args.baud)

    # mp = mppcommands.mppCommands(args.device, args.baud)
    mp = mppUtils(args.device, args.baud)

    if(args.listknown):
        for line in mp.getKnownCommands():
            print(line)
    elif(args.getStatus):
        fullStatus = mp.getFullStatus()
        print("================ Status ==================")
        print("{:<30}\t{:<15} {}".format('Parameter', 'Value', 'Unit'))
        for key in sorted(fullStatus):
            print("{:<30}\t{:<15} {}".format(key, fullStatus[key]['value'], fullStatus[key]['unit']))
    elif(args.getSettings):
        settings = mp.getSettings()
        print("================ Settings ==================")
        print("{:<30}\t{:<10}\t{:<10} {}".format('Parameter', 'Default', 'Current', 'Unit'))
        for key in sorted(settings):
            print("{:<30}\t{:<10}\t{:<10} {}".format(key, settings[key]['default'],
                                                     settings[key]['value'],
                                                     settings[key]['unit']))
    else:
        # TODO: check if command is valid
        # maybe check if query or setter and ...
        if(args.showraw):
            print(mp.getResponse(args.command))
        else:
            results = mp.getResponseDict(args.command)
            for key in sorted(results):
                print("{:<30}\t{:<15} {}".format(key, results[key][0], results[key][1]))
