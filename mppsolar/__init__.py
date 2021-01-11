# !/usr/bin/python3
from argparse import ArgumentParser
import importlib
import logging
from sys import exit

from .version import __version__, __version_comment__  # noqa: F401

log = logging.getLogger("MPP-Solar")
# logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# set default log level
log.setLevel(logging.WARNING)
logging.basicConfig()

# Ongoing effort to map model "numbers" to the correct protocol
MODEL_PROTOCOL_MAP = {
    "standard": "PI30",
    "4048MS": "PI30",
    "LV5048": "PI41",
    "PI18": "PI18",
}


def get_outputs(output_list):
    """
    Take a comma separated list of output names
    attempt to find and instantiate the corresponding module
    return array of modules
    """
    ops = []
    outputs = output_list.split(",")
    for output in outputs:
        log.info(f"attempting to create output processor: {output}")
        try:
            output_module = importlib.import_module("mppsolar.outputs." + output, ".")
        except ModuleNotFoundError:
            # perhaps raise a Powermon exception here??
            # maybe warn and keep going, only error if no outputs found?
            log.critical(f"No module found for output processor {output}")
        output_class = getattr(output_module, output)
        ops.append(output_class())
    return ops


def get_device_class(device_type=None):
    """
    Take a device type string
    attempt to find and instantiate the corresponding module
    return class if found, otherwise return None
    """
    if device_type is None:
        return None
    device_type = device_type.lower()
    try:
        device_module = importlib.import_module("mppsolar.devices." + device_type, ".")
    except ModuleNotFoundError:
        # perhaps raise a mppsolar exception here??
        log.critical(f"No module found for device {device_type}")
        return None
    device_class = getattr(device_module, device_type)
    return device_class


def get_protocol_for_model(model=None):
    """
    Try to find the correct protocol for a given model of inverter
    """
    if model is None:
        return None
    if model in MODEL_PROTOCOL_MAP:
        protocol = MODEL_PROTOCOL_MAP[model]
        log.info(f"Model {model} specified, setting protocol to {protocol}")
        return protocol
    log.info(f"Cannot find protocol for model {model}")
    return None


def main():
    description = f"MPP Solar Command Utility, version: {__version__}, {__version_comment__}"
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Specifies the device name - used to differentiate different devices",
        default="unnamed",
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        help="Specifies the device type (default: mppsolar)",
        default="mppsolar",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=str,
        help="Specifies the device communications port (/dev/ttyUSB0 [default], /dev/hidraw0, test, ...)",
        default="/dev/ttyUSB0",
    )
    parser.add_argument(
        "-P",
        "--protocol",
        type=str,
        help="Specifies the device command and response protocol, (default: PI30)",
        default="PI30",
        choices=["PI00", "PI16", "PI18", "PI30", "PI41", "JK02", "JK04", "JK485"],
    )
    parser.add_argument(
        "-T",
        "--tag",
        type=str,
        help="Override the command name and use this instead (for mqtt and influx type output processors)",
    )
    parser.add_argument(
        "-b",
        "--baud",
        type=int,
        help="Baud rate for serial communications (default: 2400)",
        default=2400,
    )
    parser.add_argument(
        "-M",
        "--model",
        type=str,
        help='Specifies the inverter model to select commands for, defaults to "standard", currently supports LV5048',
        default="standard",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Specifies the output processor(s) to use [comma separated if multiple] (screen [default], influx_mqtt, influx2_mqtt, mqtt, hass_config, hass_mqtt)",
        default="screen",
    )
    parser.add_argument(
        "-q",
        "--mqttbroker",
        type=str,
        help="Specifies the mqtt broker to publish to if using a mqtt output (localhost [default], hostname, ip.add.re.ss ...)",
        default="localhost",
    )
    parser.add_argument(
        "--mqttuser",
        type=str,
        help="Specifies the username to use for authenticated mqtt broker publishing",
        default=None,
    )
    parser.add_argument(
        "--mqttpass",
        type=str,
        help="Specifies the password to use for authenticated mqtt broker publishing",
        default=None,
    )
    parser.add_argument("-c", "--command", help="Command to run")
    parser.add_argument(
        "-C",
        "--configfile",
        type=str,
        help="Full location of config file",
        default=None,
    )
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--listknown", action="store_true", help="List known commands")
    parser.add_argument("--getstatus", action="store_true", help="Get Inverter Status")
    parser.add_argument("--getsettings", action="store_true", help="Get Inverter Settings")
    parser.add_argument(
        "--printcrc",
        action="store_true",
        help="Display the command and crc and nothing else",
    )

    parser.add_argument("-R", "--showraw", action="store_true", help="Display the raw results")
    parser.add_argument("-v", "--version", action="store_true", help="Display the version")
    parser.add_argument(
        "-D",
        "--debug",
        action="store_true",
        help="Enable Debug and above (i.e. all) messages",
    )
    parser.add_argument(
        "-I", "--info", action="store_true", help="Enable Info and above level messages"
    )

    args = parser.parse_args()

    # Display verison if asked
    log.info(description)
    if args.version:
        print(description)
        exit(0)
    # Turn on debug if needed
    if args.debug:
        log.setLevel(logging.DEBUG)
        # ch.setLevel(logging.DEBUG)
    elif args.info:
        log.setLevel(logging.INFO)
        # ch.setLevel(logging.INFO)

    mqtt_broker = args.mqttbroker
    mqtt_user = args.mqttuser
    mqtt_pass = args.mqttpass

    # Initialize Daemon
    if args.daemon:
        import time
        import systemd.daemon

        # Tell systemd that our service is ready
        systemd.daemon.notify("READY=1")
        print("MPP-Solar-Service: Initializing ...")
        # set some default-defaults
        pause = 60

    # If config file specified, process
    if args.configfile:
        import configparser

        log.debug(f"args.configfile is true: {args.configfile}")
        config = configparser.ConfigParser()
        config.read(args.configfile)
        sections = config.sections()
        # Process setup section
        if "SETUP" in config:
            pause = config["SETUP"].getint("pause", fallback=60)
            mqtt_broker = config["SETUP"].get("mqtt_broker", fallback="localhost")
            mqtt_user = config["SETUP"].get("mqtt_user", fallback=None)
            mqtt_pass = config["SETUP"].get("mqtt_pass", fallback=None)
            sections.remove("SETUP")
        # Process 'command' sections
        _commands = []
        for section in sections:
            name = section
            protocol = config[section].get("protocol", fallback=None)
            model = config[section].get("model", fallback=None)
            if model is not None and protocol is None:
                protocol = get_protocol_for_model(model)
            type = config[section].get("type", fallback="mppsolar")
            port = config[section].get("port", fallback="/dev/ttyUSB0")
            baud = config[section].get("baud", fallback=2400)
            command = config[section].get("command")
            tag = config[section].get("tag")
            outputs = config[section].get("outputs", fallback="screen")
            # todo: build array of commands
            device_class = get_device_class(type)
            log.debug(f"device_class {device_class}")
            # The device class __init__ will instantiate the port communications and protocol classes
            device = device_class(
                name=name, port=port, protocol=protocol, outputs=outputs, baud=baud
            )
            _commands.append((device, command, tag, outputs))

        if args.daemon:
            print(f"MPP-Solar-Service: Config file: {args.configfile}")
            print(f"MPP-Solar-Service: Config setting - pause: {pause}")
            print(f"MPP-Solar-Service: Config setting - mqtt_broker: {mqtt_broker}")
            print(f"MPP-Solar-Service: Config setting - command sections found: {len(sections)}")

            while True:
                # Loop through the configured commands
                for _device, _command, _tag, _outputs in _commands:
                    ## for item in mppUtilArray:
                    # Tell systemd watchdog we are still alive
                    systemd.daemon.notify("WATCHDOG=1")
                    print(
                        f"MPP-Solar-Service: Getting results from device: {_device} for command: {_command}, tag: {_tag}, outputs: {_outputs}"
                    )
                    results = _device.run_command(command=_command, show_raw=False)
                    # send to output processor(s)
                    outputs = get_outputs(_outputs)
                    for op in outputs:
                        # maybe include the command and what the command is im the output
                        # eg QDI run, Display Inverter Default Settings
                        op.output(
                            data=results,
                            tag=_tag,
                            mqtt_broker=mqtt_broker,
                            mqtt_user=mqtt_user,
                            mqtt_pass=mqtt_pass,
                        )
                        # Tell systemd watchdog we are still alive
                        systemd.daemon.notify("WATCHDOG=1")

                print("MPP-Solar-Service: sleeping for {}sec".format(pause))
                time.sleep(pause)

        else:
            # supplied a configfile, but running on command line
            # this will run each section once
            log.info(f"Command line using config file: {args.configfile}")
            for _device, _command, _tag, _outputs in _commands:
                log.debug(
                    f"getting results from device: {_device} for command: {_command}, tag: {_tag}, outputs: {_outputs}"
                )
                results = _device.run_command(command=_command, show_raw=False)
                # send to output processor(s)
                log.debug(f"results: {results}")
                outputs = get_outputs(_outputs)
                for op in outputs:
                    # maybe include the command and what the command is im the output
                    # eg QDI run, Display Inverter Default Settings
                    op.output(
                        data=results,
                        tag=_tag,
                        mqtt_broker=mqtt_broker,
                        mqtt_user=mqtt_user,
                        mqtt_pass=mqtt_pass,
                    )
            exit(0)
    else:
        # No configfile specified
        # process some arguments
        if args.tag:
            tag = args.tag
        else:
            tag = args.command
        if args.model is not None and args.protocol is None:
            args.protocol = get_protocol_for_model(args.model)
        if not args.showraw:
            args.showraw = False
        if args.printcrc:
            log.info(f"Calculating CRC using protocol {args.protocol}")
            log.error("printcrc option is still todo")
            # TODO: calc CRC
            # _command = mp.getFullCommand(args.command)
            # if _command:
            #     print('{}'.format(_command.byte_command))
            # else:
            #     [crca, crcb] = mppcommand.crc(args.command)  # noqa: F821
            #     print("{0} {1:#x} {2:#x}".format(args.command, crca, crcb))
            exit(1)

        #
        # create instance of device (supplying port + protocol types)
        log.info(
            f'Creating device "{args.name}" (type: "{args.type}") on port "{args.port}" using protocol "{args.protocol}" for command "{args.command}" (tag: {tag})'
        )
        device_class = get_device_class(args.type)
        log.debug(f"device_class {device_class}")
        # The device class __init__ will instantiate the port communications and protocol classes
        device = device_class(name=args.name, port=args.port, protocol=args.protocol, baud=args.baud)

        # determine whether to run command or call helper function
        if args.listknown:
            results = device.list_commands()
        elif args.getstatus:
            # use get_status helper
            results = device.get_status(show_raw=args.showraw)
            # TODO: implement get_status
        elif args.getsettings:
            # use get_settings helper
            results = device.get_settings(show_raw=args.showraw)
            # TODO: implement get_settings
        elif args.command:
            # run the command
            results = device.run_command(command=args.command, show_raw=args.showraw)
        else:
            # run the default command
            results = device.run_default_command(show_raw=args.showraw)

        # send to output processor(s)
        log.debug(f"results: {results}")
        outputs = get_outputs(args.output)
        for op in outputs:
            # maybe include the command and what the command is im the output
            # eg QDI run, Display Inverter Default Settings
            op.output(
                data=results,
                tag=tag,
                mqtt_broker=mqtt_broker,
                mqtt_user=mqtt_user,
                mqtt_pass=mqtt_pass,
            )
