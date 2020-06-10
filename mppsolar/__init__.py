# !/usr/bin/python3
import logging
from argparse import ArgumentParser

from .version import __version__  # noqa: F401
# import mppcommands
from .mpputils import mppUtils

log = logging.getLogger('MPP-Solar')
# setup logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# ch = logging.StreamHandler()
# create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# add the handlers to logger
# log.addHandler(ch)
# set default log levels
log.setLevel(logging.WARNING)
# ch.setLevel(logging.WARNING)
logging.basicConfig()


def main():
    parser = ArgumentParser(description='MPP Solar Command Utility, version: {}'.format(__version__))
    parser.add_argument('-c', '--command', help='Command to run', default='QID')
    parser.add_argument('-D', '--enableDebug', action='store_true', help='Enable Debug and above (i.e. all) messages')
    parser.add_argument('-I', '--enableInfo', action='store_true', help='Enable Info and above level messages')
    parser.add_argument('-d', '--device', type=str, help='Serial (or USB) device to communicate with, defaults to /dev/ttyUSB0', default='/dev/ttyUSB0')
    parser.add_argument('-b', '--baud', type=int, help='Baud rate for serial communications, defaults to 2400', default=2400)
    parser.add_argument('-M', '--model', type=str, help='Specifies the inverter model to select commands for, defaults to "standard", currently supports LV5048', default='standard')
    parser.add_argument('-l', '--listknown', action='store_true', help='List known commands')
    parser.add_argument('-s', '--getStatus', action='store_true', help='Get Inverter Status')
    parser.add_argument('-t', '--getSettings', action='store_true', help='Get Inverter Settings')
    parser.add_argument('-R', '--showraw', action='store_true', help='Display the raw results')
    parser.add_argument('-p', '--printcrc', action='store_true', help='Display the command and crc and nothing else')
    args = parser.parse_args()

    # Turn on debug if needed
    if(args.enableDebug):
        log.setLevel(logging.DEBUG)
        # ch.setLevel(logging.DEBUG)
    elif(args.enableInfo):
        log.setLevel(logging.INFO)
        # ch.setLevel(logging.INFO)

    log.info('command %s', args.command)
    log.info('Serial device used: %s, baud rate: %d', args.device, args.baud)

    # mp = mppcommands.mppCommands(args.device, args.baud)
    mp = mppUtils(args.device, args.baud, args.model)

    if(args.printcrc):
        # print("{0:#x}".format(100))
        _command = mp.getFullCommand(args.command)
        if _command:
            print('{}'.format(_command.byte_command))
        else:
            [crca, crcb] = mppcommand.crc(args.command)  # noqa: F821
            print("{0} {1:#x} {2:#x}".format(args.command, crca, crcb))
    elif(args.listknown):
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
