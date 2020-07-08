# !/usr/bin/python3
from argparse import ArgumentParser
import logging
import sys

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
    parser.add_argument('-n', '--name', type=str, help='Specifies the device name - used to differentiate different devices', default='mppsolarname')
    parser.add_argument('-t', '--type', type=str, help='Specifies the device type (mppsolar [default], jkbms)', default='mppsolar')
    parser.add_argument('-d', '--device', type=str, help='Specifies the device to communicate with (/dev/ttyUSB0 [default], /dev/hidraw, test, ...)', default='/dev/ttyUSB0')
    # parser.add_argument('-p', '--port', type=str, help='Specifies the device communication port, (/dev/ttyUSB0 [default], /dev/hidraw0, test ...)', default='/dev/ttyUSB0')
    parser.add_argument('-P', '--protocol', type=str, help='Specifies the device command and response protocol, (default: PI30)', default='PI30', choices=['PI18', 'PI30', 'PI41'])
    parser.add_argument('-T', '--tag', type=str, help='Override the command name and use this instead (for mqtt and influx type output processors)')
    parser.add_argument('-b', '--baud', type=int, help='Baud rate for serial communications, defaults to 2400', default=2400)
    parser.add_argument('-M', '--model', type=str, help='Specifies the inverter model to select commands for, defaults to "standard", currently supports LV5048', default='standard')

    parser.add_argument('-c', '--command', help='Command to run', default='QID')
    # parser.add_argument('-c', '--command', help='Raw command to run')

    parser.add_argument('-o', '--output', type=str, help='Specifies the output processor(s) to use [comma separated if multiple] (screen [default], influx_mqtt, mqtt, hass_config, hass_mqtt)', default='screen')
    parser.add_argument('-q', '--mqtt_broker', type=str, help='Specifies the mqtt broker to publish to if using a mqtt output (localhost [default], hostname, ip.add.re.ss ...)', default='localhost')

    parser.add_argument('-l', '--listknown', action='store_true', help='List known commands')
    parser.add_argument('-s', '--getStatus', action='store_true', help='Get Inverter Status')
    # '-t' now changed from getSettings to type
    parser.add_argument('--getSettings', action='store_true', help='Get Inverter Settings')

    parser.add_argument('-R', '--showraw', action='store_true', help='Display the raw results')
    parser.add_argument('-D', '--enableDebug', action='store_true', help='Enable Debug and above (i.e. all) messages')
    parser.add_argument('-I', '--enableInfo', action='store_true', help='Enable Info and above level messages')
    parser.add_argument('-p', '--printcrc', action='store_true', help='Display the command and crc and nothing else')
    args = parser.parse_args()

    # Turn on debug if needed
    if(args.enableDebug):
        log.setLevel(logging.DEBUG)
        # ch.setLevel(logging.DEBUG)
    elif(args.enableInfo):
        log.setLevel(logging.INFO)
        # ch.setLevel(logging.INFO)

    log.info(f'mpp-solar version {__version__}')

    # process some arguments
    if args.tag:
        tag = args.tag
    else:
        tag = args.command
    if args.mqtt_broker:
        mqtt_broker = args.mqtt_broker
    else:
        mqtt_broker = 'localhost'
    if args.baud:
        log.error('ERROR: baud option is deprecated please update your scripts')
    if(args.listknown):
        log.error('-l --listknown option is deprecated, please update your scripts')
        sys.exit(1)

    log.debug(f'communications device used: {args.device}, tag: {tag}, mqtt_broker: {mqtt_broker}')

    # create instance of device (supplying port + protocol types)
    # log.info(f'Creating device "{args.name}" (type: "{args.type}") on port "{args.port}" using protocol "{args.protocol}"')
    # device_type = args.type.lower()
    # try:
    #     device_module = importlib.import_module('powermon.devices.' + device_type, '.')
    # except ModuleNotFoundError:
    #     # perhaps raise a Powermon exception here??
    #     log.critical(f'No module found for device {device_type}')
    #     exit(1)
    # device_class = getattr(device_module, device_type)
    # log.debug(f'device_class {device_class}')
    # # The device class __init__ will instantiate the port communications and protocol classes
    # device = device_class(name=args.name, port=args.port, protocol=args.protocol)
    log.debug(f'command {args.command}')
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

    #
    #
    # # run command or called helper function
    # results = device.run_command(command=args.command, show_raw=args.show_raw)
    #

    # # send to output processor(s)
    # outputs = args.output.split(',')
    # for output in outputs:
    #     log.info(f'attempting to create output processor: {output}')
    #     try:
    #         output_module = importlib.import_module('powermon.outputs.' + output, '.')
    #     except ModuleNotFoundError:
    #         # perhaps raise a Powermon exception here??
    #         log.critical(f'No module found for output processor {output}')
    #     output_class = getattr(output_module, output)
    #
    #     # init function will do the processing
    #     output_class(results=results, tag=tag, mqtt_broker=mqtt_broker)
