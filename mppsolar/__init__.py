# !/usr/bin/python3
from argparse import ArgumentParser
import importlib
import logging
from sys import exit

from .version import __version__  # noqa: F401
# import mppcommands
# from .mpputils import mppUtils

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
    parser.add_argument('-n', '--name', type=str, help='Specifies the device name - used to differentiate different devices', default='unnamed')
    parser.add_argument('-t', '--type', type=str, help='Specifies the device type (default: mppsolar)', default='mppsolar')
    parser.add_argument('-p', '--port', type=str, help='Specifies the device communications port (/dev/ttyUSB0 [default], /dev/hidraw, test, ...)', default='/dev/ttyUSB0')
    parser.add_argument('-d', '--device', type=str, help='DEPRECATED, use -p')
    parser.add_argument('-P', '--protocol', type=str, help='Specifies the device command and response protocol, (default: PI30)', default='PI30', choices=['PI18', 'PI30', 'PI41'])
    parser.add_argument('-T', '--tag', type=str, help='Override the command name and use this instead (for mqtt and influx type output processors)')
    parser.add_argument('-b', '--baud', type=int, help='Baud rate for serial communications (default: 2400)', default=2400)
    parser.add_argument('-M', '--model', type=str, help='Specifies the inverter model to select commands for, defaults to "standard", currently supports LV5048', default='standard')

    parser.add_argument('-c', '--command', help='Command to run', default='QID')
    # parser.add_argument('-c', '--command', help='Raw command to run')

    parser.add_argument('-o', '--output', type=str, help='Specifies the output processor(s) to use [comma separated if multiple] (screen [default], influx_mqtt, mqtt, hass_config, hass_mqtt)', default='screen')
    parser.add_argument('-q', '--mqttbroker', type=str, help='Specifies the mqtt broker to publish to if using a mqtt output (localhost [default], hostname, ip.add.re.ss ...)', default='localhost')

    parser.add_argument('--listknown', action='store_true', help='List known commands')
    parser.add_argument('--getStatus', action='store_true', help='Get Inverter Status')
    parser.add_argument('--getSettings', action='store_true', help='Get Inverter Settings')

    parser.add_argument('-R', '--showraw', action='store_true', help='Display the raw results')
    parser.add_argument('-D', '--debug', action='store_true', help='Enable Debug and above (i.e. all) messages')
    parser.add_argument('-I', '--info', action='store_true', help='Enable Info and above level messages')
    parser.add_argument('--printcrc', action='store_true', help='Display the command and crc and nothing else')
    args = parser.parse_args()

    # Turn on debug if needed
    if(args.debug):
        log.setLevel(logging.DEBUG)
        # ch.setLevel(logging.DEBUG)
    elif(args.info):
        log.setLevel(logging.INFO)
        # ch.setLevel(logging.INFO)

    log.info(f'mpp-solar version {__version__}')

    # process some arguments
    if args.tag:
        tag = args.tag
    else:
        tag = args.command
    if args.model == 'LV5048':
        log.info('Modle LV5048 specified, setting protocol to PI41')
        args.protocol = 'PI41'
    if args.model == 'PI18':
        log.info('Modle PI18 specified, setting protocol to PI48')
        args.protocol = 'PI18'
    if not args.showraw:
        args.showraw = False
    if not args.mqttbroker:
        args.mqttbroker = 'localhost'
    if args.listknown:
        log.error('listknown option is deprecated, please update your scripts')
        exit(1)
    if args.device:
        log.error('-d --device option is deprecated, please update your scripts to use -p instead')
        args.port = args.device
    if args.printcrc:
        log.info(f'Calculating CRC using protocol {args.protocol}')
        # TODO: calc CRC
        # _command = mp.getFullCommand(args.command)
        # if _command:
        #     print('{}'.format(_command.byte_command))
        # else:
        #     [crca, crcb] = mppcommand.crc(args.command)  # noqa: F821
        #     print("{0} {1:#x} {2:#x}".format(args.command, crca, crcb))
        exit(1)
    # create instance of device (supplying port + protocol types)
    log.info(f'Creating device "{args.name}" (type: "{args.type}") on port "{args.port}" using protocol "{args.protocol}" for command "{args.command}" (tag: {tag})')
    device_type = args.type.lower()
    try:
        device_module = importlib.import_module('mppsolar.devices.' + device_type, '.')
    except ModuleNotFoundError:
        # perhaps raise a mppsolar exception here??
        log.critical(f'No module found for device {device_type}')
        exit(1)
    device_class = getattr(device_module, device_type)
    log.debug(f'device_class {device_class}')
    # The device class __init__ will instantiate the port communications and protocol classes
    device = device_class(name=args.name, port=args.port, protocol=args.protocol)
    # run command or call helper function
    results = device.run_command(command=args.command, show_raw=args.showraw)

    #
    # mp = mppcommands.mppCommands(args.device, args.baud)
    #
    #
    # mp = mppUtils(args.device, args.baud, args.model)

    # elif(args.getStatus):
    #     fullStatus = mp.getFullStatus()
    #     print("================ Status ==================")
    #     print("{:<30}\t{:<15} {}".format('Parameter', 'Value', 'Unit'))
    #     for key in sorted(fullStatus):
    #         print("{:<30}\t{:<15} {}".format(key, fullStatus[key]['value'], fullStatus[key]['unit']))
    # elif(args.getSettings):
    #     settings = mp.getSettings()
    #     print("================ Settings ==================")
    #     print("{:<30}\t{:<10}\t{:<10} {}".format('Parameter', 'Default', 'Current', 'Unit'))
    #     for key in sorted(settings):
    #         print("{:<30}\t{:<10}\t{:<10} {}".format(key, settings[key]['default'],
    #                                                  settings[key]['value'],
    #                                                  settings[key]['unit']))
    # else:
    #     # TODO: check if command is valid
    #     # maybe check if query or setter and ...
    #     if(args.showraw):
    #         print(mp.getResponse(args.command))
    #     else:
    #         results = mp.getResponseDict(args.command)
    #         for key in sorted(results):
    #             print("{:<30}\t{:<15} {}".format(key, results[key][0], results[key][1]))

    # send to output processor(s)
    outputs = args.output.split(',')
    for output in outputs:
        log.info(f'attempting to create output processor: {output}')
        try:
            output_module = importlib.import_module('mppsolar.outputs.' + output, '.')
        except ModuleNotFoundError:
            # perhaps raise a Powermon exception here??
            log.critical(f'No module found for output processor {output}')
        output_class = getattr(output_module, output)

        # init function will do the processing
        output_class(results=results, tag=tag, mqtt_broker=args.mqttbroker)


def mpp_info_pub(*args, **kwargs):
    from argparse import ArgumentParser
    parser = ArgumentParser(description='MPP Solar Inverter Info Utility')
    parser.add_argument('-s', '--grabsettings', action='store_true', help='Also get the inverter settings')
    parser.add_argument('-t', '--getstatus', action='store_true', help='Use the getstatus "helper"')
    parser.add_argument('-c', '--command', type=str, help='Command to execute [comma separated]', default=None)
    parser.add_argument('-d', '--device', type=str, help='Serial device(s) to communicate with [comma separated]', default='/dev/ttyUSB0')
    parser.add_argument('-M', '--model', type=str, help='Specifies the inverter model to select commands for, defaults to "standard", currently supports LV5048', default='standard')
    parser.add_argument('-b', '--baud', type=int, help='Baud rate for serial communications', default=2400)
    parser.add_argument('-q', '--broker', type=str, help='MQTT Broker hostname', default='mqtt_broker')
    parser.add_argument('-i', '--influx', action='store_true', help='Use Influx Line Protocol for the messgae format')
    parser.add_argument('-I', '--influx2', action='store_true', help='Use Influx Line Protocol II for the messgae format')
    parser.add_argument('--tag', type=str, help='Influx tag to use for all commands in this execution', default=None)
    _args = parser.parse_args()
    print(_args)
    print(args)
    print(kwargs)
