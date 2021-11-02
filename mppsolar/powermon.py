# !/usr/bin/python3
import configparser
import io
import logging
from argparse import ArgumentParser
from collections import deque
from time import sleep

from mppsolar.io import get_port
from mppsolar.libs.mqttbroker import MqttBroker
from mppsolar.outputs import output_results
from mppsolar.protocols import get_protocol
from mppsolar.version import __version__  # noqa: F401

# Set-up logger
log = logging.getLogger("")
FORMAT = "%(asctime)-15s:%(levelname)s:%(module)s:%(funcName)s@%(lineno)d: %(message)s"
logging.basicConfig(format=FORMAT)

sample_config = """
    [CONFIG]
    port = /dev/ttyUSB0
    porttype = test
    portbaud = 2400
    protocol = PI30
    mqttbroker_name = localhost
    mqttbroker_port = 1883
    mqttbroker_user =
    mqttbroker_pass =
    split_token = ,
    commands = QPIGS,QPIRI
    outputs = screen,mqtt
    tag = sample
    filter =
    command_topic = test/command_topic
    command_pause = 5
    """

ADHOC_COMMANDS = deque([])
SPLIT_TOKEN = ","


def mqtt_callback(client, userdata, msg):
    print(f"Received `{msg.payload}` on topic `{msg.topic}`")
    newCommand = msg.payload
    ADHOC_COMMANDS.append(newCommand)


def main():
    description = f"Power Device Monitoring Utility, version: {__version__}"
    parser = ArgumentParser(description=description)

    parser.add_argument(
        "-C",
        "--configFile",
        nargs="?",
        type=str,
        help="Full location of config file (default /etc/mpp-solar/powermon.conf)",
        const=None,
        default="/etc/mpp-solar/powermon.conf",
    )
    parser.add_argument("-v", "--version", action="store_true", help="Display the version")
    parser.add_argument(
        "--generateConfigFile",
        action="store_true",
        help="Print a new config file based on options supplied (including the existing config file)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Only loop through config once",
    )
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
    # prog_name = parser.prog

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

    # Build configuration from defaults, config file and command line overrides
    log.info(f"Using config file:{args.configFile}")
    # build config - start with defaults
    config = configparser.ConfigParser()
    config.read_string(sample_config)
    # build config - update with details from config file
    if args.configFile is not None:
        config.read(args.configFile)
    # build config - override with any command line arguments
    # TODO: command line overrides

    # if generateConfigFile is true then print config out
    if args.generateConfigFile:
        # FIXME must be a better way
        with io.StringIO() as ss:
            config.write(ss)
            ss.seek(0)  # rewind
            print(ss.read())
        return

    # debug dump config
    for section in config.sections():
        log.debug(f"config section [{section}]")
        for key in config[section]:
            print(f"{key} = {config[section][key]}")

    # split token
    SPLIT_TOKEN = config.get("CONFIG", "split_token")

    # Build mqtt broker
    mqtt_broker = MqttBroker(
        name=config.get("CONFIG", "mqttbroker_name"),
        port=config.getint("CONFIG", "mqttbroker_port"),
        username=config.get("CONFIG", "mqttbroker_user"),
        password=config.get("CONFIG", "mqttbroker_pass"),
    )
    log.debug(mqtt_broker)
    # sub to command topic
    mqtt_broker.connect()
    mqtt_broker.subscribe(config.get("CONFIG", "command_topic"), mqtt_callback)
    # connect to mqtt
    mqtt_broker.start()

    # get port
    port = get_port(
        port=config.get("CONFIG", "port"),
        porttype=config.get("CONFIG", "porttype"),
        baud=config.get("CONFIG", "portbaud"),
    )

    # get protocol handler
    protocol = get_protocol(protocol=config.get("CONFIG", "protocol"))

    loop = True

    try:
        # connect to port
        port.connect()
        while loop:
            # loop through command list
            for command in config.get("CONFIG", "commands").split(SPLIT_TOKEN):
                # process any adhoc commands first
                print(f"{ADHOC_COMMANDS}")
                while len(ADHOC_COMMANDS) > 0:
                    adhoc_command = ADHOC_COMMANDS.popleft().decode()  # FIXME: decode to str #
                    log.info(f"Processing command: {adhoc_command}")
                    results = port.process_command(command=adhoc_command, protocol=protocol)
                    log.debug(f"results {results}")
                    # send to output processor(s)
                    output_results(results=results, config=config, mqtt_broker=mqtt_broker)
                # process 'normal' commands
                log.info(f"Processing command: {command}")
                results = port.process_command(command=command, protocol=protocol)
                log.debug(f"results {results}")
                # send to output processor(s)
                output_results(results=results, config=config, mqtt_broker=mqtt_broker)
                # pause
                pause_time = config.getint("CONFIG", "command_pause")
                log.debug(f"Sleeping for {pause_time}secs")
            sleep(pause_time)
            if args.once:
                loop = False
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        # Disconnect port
        port.disconnect()
        # Disconnect mqtt
        mqtt_broker.stop()
