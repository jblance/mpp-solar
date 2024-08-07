# !/usr/bin/python3
import logging
import time
from argparse import ArgumentParser
from platform import python_version

from mppsolar.version import __version__  # noqa: F401

from mppsolar.helpers import get_device_class
from mppsolar.daemon import get_daemon
from mppsolar.daemon import DaemonType
from mppsolar.libs.mqttbrokerc import MqttBroker
from mppsolar.outputs import get_outputs, list_outputs
from mppsolar.protocols import list_protocols

# Set-up logger
log = logging.getLogger("")
FORMAT = "%(asctime)-15s:%(levelname)s:%(module)s:%(funcName)s@%(lineno)d: %(message)s"
logging.basicConfig(format=FORMAT)


def main():
    description = f"Solar Device Command Utility, version: {__version__}, python version: {python_version()}"
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-n",
        "--name",
        help="Specifies the device name - used to differentiate different devices",
        default="unnamed",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Specifies the device communications port (/dev/ttyUSB0 [default], /dev/hidraw0, test, ...)",
        default="/dev/ttyUSB0",
    )
    parser.add_argument(
        "--porttype",
        help="overrides the device communications port type",
        default=None,
    )
    if parser.prog == "jkbms":
        parser.add_argument(
            "-P",
            "--protocol",
            nargs="?",
            const="help",
            help="Specifies the device command and response protocol, (default: JK04)",
            default="JK04",
        )
    else:
        parser.add_argument(
            "-P",
            "--protocol",
            nargs="?",
            const="help",
            help="Specifies the device command and response protocol, (default: PI30)",
            default="PI30",
        )
    parser.add_argument(
        "-T",
        "--tag",
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
        "-o",
        "--output",
        nargs="?",
        help="Specifies the output processor(s) to use [comma separated if multiple] (screen [default]) leave blank to give list",
        const="help",
        default="screen",
    )
    parser.add_argument(
        "--keepcase",
        action="store_true",
        help="Do not convert the field names to lowercase",
    )
    parser.add_argument(
        "--filter",
        help="Specifies the filter to reduce the output - only those fields that match will be output (uses re.search)",
        default=None,
    )
    parser.add_argument(
        "--exclfilter",
        help="Specifies the filter to reduce the output - any fields that match will be excluded from the output (uses re.search)",
        default=None,
    )
    parser.add_argument(
        "-q",
        "--mqttbroker",
        help="Specifies the mqtt broker to publish to if using a mqtt output (localhost [default], hostname, ip.add.re.ss ...)",
        default="localhost",
    )
    parser.add_argument(
        "--mqttport",
        type=int,
        help="Specifies the mqtt broker port if needed (default: 1883)",
        default=1883,
    )
    parser.add_argument(
        "--mqtttopic",
        help="provides an override topic (or prefix) for mqtt messages (default: None)",
        default=None,
    )
    parser.add_argument(
        "--mqttuser",
        help="Specifies the username to use for authenticated mqtt broker publishing",
        default=None,
    )
    parser.add_argument(
        "--mqttpass",
        help="Specifies the password to use for authenticated mqtt broker publishing",
        default=None,
    )
    parser.add_argument(
        "--udpport",
        type=int,
        help="Specifies the UDP port if needed (default: 5555)",
        default="5555",
    )
    parser.add_argument(
        "--postgres_url",
        help="PostgresSQL connection url, example postgresql://user:password@server:5432/postgres",
    )
    parser.add_argument(
        "--mongo_url",
        help="Mongo connection url, example mongodb://user:password@ip:port/admindb",
    )
    parser.add_argument(
        "--mongo_db",
        help="Mongo db name (default: mppsolar)",
        default="mppsolar",
    )
    parser.add_argument(
        "--pushurl",
        help=(
            "Any server used to send data to (PushGateway for Prometheus, for instance), "
            "(default: http://localhost:9091/metrics/job/pushgateway)"
        ),
        default="http://localhost:9091/metrics/job/pushgateway",
    )
    parser.add_argument(
        "--prom_output_dir",
        help=(
            "Output directory where Prometheus metrics are written as .prom files"
            "(default: /var/lib/node_exporter)"
        ),
        default="/var/lib/node_exporter",
    )
    parser.add_argument(
        "-c",
        "--command",
        nargs="?",
        const="help",
        help="Command to run; or list of hash separated commands to run",
    )
    if parser.prog == "jkbms":
        parser.add_argument(
            "-C",
            "--configfile",
            nargs="?",
            help="Full location of config file (default None, /etc/jkbms/jkbms.conf if -C supplied)",
            const="/etc/jkbms/jkbms.conf",
            default=None,
        )
    else:
        parser.add_argument(
            "-C",
            "--configfile",
            nargs="?",
            help="Full location of config file (default None, /etc/mpp-solar/mpp-solar.conf if -C supplied)",
            const="/etc/mpp-solar/mpp-solar.conf",
            default=None,
        )
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--getstatus", action="store_true", help="Get Inverter Status")
    parser.add_argument("--getsettings", action="store_true", help="Get Inverter Settings")
    parser.add_argument("--getDeviceId", action="store_true", help="Generate Device ID")

    parser.add_argument("-v", "--version", action="store_true", help="Display the version")
    parser.add_argument("--getVersion", action="store_true", help="Output the software version via the supplied output")
    parser.add_argument(
        "-D",
        "--debug",
        action="store_true",
        help="Enable Debug and above (i.e. all) messages",
    )
    parser.add_argument("-I", "--info", action="store_true", help="Enable Info and above level messages")

    args = parser.parse_args()
    prog_name = parser.prog
    if prog_name is None:
        prog_name = "mpp-solar"
    s_prog_name = prog_name.replace("-", "")
    # log_name = s_prog_name.upper()

    # logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    # Turn on debug if needed
    if args.debug:
        log.setLevel(logging.DEBUG)
    elif args.info:
        log.setLevel(logging.INFO)
    else:
        # set default log level
        log.setLevel(logging.WARNING)
    logging.basicConfig()

    # Display version if asked
    log.info(description)
    if args.version:
        print(description)
        return None

    # List available protocols if asked
    if args.protocol == "help":
        op = get_outputs("screen")[0]
        op.output(data=list_protocols())
        return None

    # List outputs if asked
    if args.output == "help":
        keep_case = True
        op = get_outputs("screen")[0]
        op.output(data=list_outputs())
        # print("Available output modules:")
        # for result in results:
        #    print(result)
        return None

    # mqttbroker:
    #     name: null
    #     port: 1883
    #     user: null
    #     pass: null
    mqtt_broker = MqttBroker(
        config={
            "name": args.mqttbroker,
            "port": args.mqttport,
            "user": args.mqttuser,
            "pass": args.mqttpass,
        }
    )
    mqtt_broker.set("results_topic", (args.mqtttopic if args.mqtttopic is not None else prog_name))
    log.debug(mqtt_broker)
    udp_port = args.udpport
    log.debug(f"udp port {udp_port}")
    postgres_url = args.postgres_url
    log.debug(f"Using Postgres {postgres_url}")
    mongo_url = args.mongo_url
    mongo_db = args.mongo_db
    log.debug(f"Using Mongo {mongo_url} with {mongo_db}")
    ##
    filter = args.filter
    excl_filter = args.exclfilter
    keep_case = args.keepcase
    mqtt_topic = args.mqtttopic
    push_url = args.pushurl
    prom_output_dir = args.prom_output_dir

    _commands = []

    # Initialize Daemon
    if not args.daemon:
        daemon = get_daemon(daemontype=DaemonType.DISABLED)
    else:
        daemon = get_daemon(daemontype=DaemonType.SYSTEMD)
        daemon.keepalive = 60
    log.info(daemon)


    # if args.daemon:
    #     try:
    #         import systemd.daemon
    #     except ImportError:
    #         print("You are missing dependencies in order to be able to use the --daemon flag.")
    #         print("To install them, use that command:")
    #         print("    python -m pip install 'mppsolar[systemd]'")
    #         exit(1)

    # Tell systemd that our service is ready
    daemon.initialize()
    daemon.notify("Service Initializing ...")
    # set some default-defaults
    pause = 60

    # If config file specified, process
    if args.configfile:
        import configparser

        log.debug(f"args.configfile is true: {args.configfile}")
        config = configparser.ConfigParser()
        try:
            config.read(args.configfile)
        except configparser.DuplicateSectionError as e:
            log.error(f"Config File '{args.configfile}' has duplicate sections")
            log.error(e)
            exit(1)
        sections = config.sections()
        # Check setup section exists
        if "SETUP" not in config:
            log.error(f"Config File '{args.configfile}'  is missing the required 'SETUP' section or does not exist")
            exit(1)
        # Process setup section
        pause = config["SETUP"].getint("pause", fallback=60)
        # Overide mqtt_broker settings
        mqtt_broker.update("name", config["SETUP"].get("mqtt_broker", fallback=None))
        mqtt_broker.update("port", config["SETUP"].getint("mqtt_port", fallback=None))
        mqtt_broker.update("username", config["SETUP"].get("mqtt_user", fallback=None))
        mqtt_broker.update("password", config["SETUP"].get("mqtt_pass", fallback=None))
        sections.remove("SETUP")

        # Process 'command' sections
        for section in sections:
            name = section
            protocol = config[section].get("protocol", fallback=None)
            _type = config[section].get("type", fallback="mppsolar")
            port = config[section].get("port", fallback="/dev/ttyUSB0")
            baud = config[section].get("baud", fallback=2400)
            _command = config[section].get("command")
            tag = config[section].get("tag")
            outputs = config[section].get("outputs", fallback="screen")
            porttype = config[section].get("porttype", fallback=None)
            filter = config[section].get("filter", fallback=None)
            excl_filter = config[section].get("exclfilter", fallback=None)
            udp_port = config[section].get("udpport", fallback=None)
            postgres_url = config[section].get("postgres_url", fallback=None)
            mongo_url = config[section].get("mongo_url", fallback=None)
            mongo_db = config[section].get("mongo_db", fallback=None)
            push_url = config[section].get("push_url", fallback=push_url)
            prom_output_dir = config[section].get("prom_output_dir", fallback=prom_output_dir)
            mqtt_topic = config[section].get("mqtt_topic", fallback=mqtt_topic)
            #
            device_class = get_device_class(_type)
            log.debug(f"device_class {device_class}")
            # The device class __init__ will instantiate the port communications and protocol classes
            device = device_class(
                name=name,
                port=port,
                protocol=protocol,
                outputs=outputs,
                baud=baud,
                porttype=porttype,
                mqtt_broker=mqtt_broker,
                udp_port=udp_port,
                postgres_url=postgres_url,
                mongo_url=mongo_url,
                mongo_db=mongo_db,
                push_url=push_url,
                prom_output_dir=prom_output_dir,
            )
            # build array of commands
            commands = _command.split("#")

            for command in commands:
                _commands.append((device, command, tag, outputs, filter, excl_filter))
            log.debug(f"Commands from config file {_commands}")

            if args.daemon:
                print(f"Config file: {args.configfile}")
                print(f"Config setting - pause: {pause}")
                # print(f"Config setting - mqtt_broker: {mqtt_broker}, port: {mqtt_port}")
                print(f"Config setting - command sections found: {len(sections)}")
            else:
                log.info(f"Config file: {args.configfile}")
                log.info(f"Config setting - pause: {pause}")
                # log.info(f"Config setting - mqtt_broker: {mqtt_broker}, port: {mqtt_port}")
                log.info(f"Config setting - command sections found: {len(sections)}")

    else:
        # No configfile specified
        # create instance of device (supplying port + protocol types)
        log.info(
            f'Creating device "{args.name}" (type: "{s_prog_name}") on port "{args.port} (porttype={args.porttype})" using protocol "{args.protocol}"'
        )
        device_class = get_device_class(s_prog_name)
        log.debug(f"device_class {device_class}")
        # The device class __init__ will instantiate the port communications and protocol classes
        device = device_class(
            name=args.name,
            port=args.port,
            protocol=args.protocol,
            baud=args.baud,
            porttype=args.porttype,
            mqtt_broker=mqtt_broker,
            udp_port=udp_port,
            mongo_url=mongo_url,
            mongo_db=mongo_db,
            push_url=push_url,
            prom_output_dir=prom_output_dir,
        )
        #

        # determine whether to run command or call helper function
        commands = []
        if args.command == "help":
            keep_case = True
            commands.append("list_commands")
        elif args.getstatus:
            # use get_status helper
            commands.append("get_status")
        elif args.getsettings:
            # use get_settings helper
            commands.append("get_settings")
        elif args.getDeviceId:
            # use get_settings helper
            commands.append("get_device_id")
        elif args.getVersion:
            # use get_version helper
            commands.append("get_version")
        elif args.command is None:
            # run the command
            commands.append("")
        else:
            commands = args.command.split("#")

        outputs = args.output
        for command in commands:
            if args.tag:
                tag = args.tag
            else:
                tag = command
            _commands.append((device, command, tag, outputs, filter, excl_filter))
        log.debug(f"Commands {_commands}")

    while True:
        # Loop through the configured commands
        if not args.daemon:
            log.info(f"Looping {len(_commands)} commands")
        for _device, _command, _tag, _outputs, filter, excl_filter in _commands:
            # for item in mppUtilArray:
            # Tell systemd watchdog we are still alive
            daemon.watchdog()
            daemon.notify(f"Getting results from device: {_device} for command: {_command}, tag: {_tag}, outputs: {_outputs}")
            log.info(f"Getting results from device: {_device} for command: {_command}, tag: {_tag}, outputs: {_outputs}")
            results = _device.run_command(command=_command)
            log.debug(f"results: {results}")
            # send to output processor(s)
            outputs = get_outputs(_outputs)
            for op in outputs:
                # maybe include the command and what the command is im the output
                # eg QDI run, Display Inverter Default Settings
                log.debug(f"Using output filter: {filter}")
                op.output(
                    data=results.copy(),
                    tag=_tag,
                    name=_device._name,
                    mqtt_broker=mqtt_broker,
                    udp_port=udp_port,
                    postgres_url=postgres_url,
                    mongo_url=mongo_url,
                    mongo_db=mongo_db,
                    push_url=push_url,
                    prom_output_dir=prom_output_dir,
                    # mqtt_port=mqtt_port,
                    # mqtt_user=mqtt_user,
                    # mqtt_pass=mqtt_pass,
                    mqtt_topic=mqtt_topic,
                    filter=filter,
                    excl_filter=excl_filter,
                    keep_case=keep_case,
                )
                # Tell systemd watchdog we are still alive
        if args.daemon:
            daemon.watchdog()
            print(f"Sleeping for {pause} sec")
            time.sleep(pause)
        else:
            # Dont loop unless running as daemon
            log.debug("Not daemon, so not looping")
            break


if __name__ == "__main__":
    main()
