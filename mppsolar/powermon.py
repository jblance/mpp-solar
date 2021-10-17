# !/usr/bin/python3
import configparser
import logging
import io
from argparse import ArgumentParser

from .libs.mqttbroker import MqttBroker

# from .helpers import get_device_class, get_outputs
from .version import __version__  # noqa: F401

# Set-up logger
log = logging.getLogger("")
FORMAT = "%(asctime)-15s:%(levelname)s:%(module)s:%(funcName)s@%(lineno)d: %(message)s"
logging.basicConfig(format=FORMAT)

sample_config = """
    [CONFIG]
    port = /dev/ttyUSB0
    porttype = serial
    protocol = PI30
    mqttbroker_name = localhost
    mqttbroker_port = 1883
    mqttbroker_user =
    mqttbroker_pass =
    commands = QPIGS,QPIRI
    command_topic = test/topic
    """


def mqtt_callback(client, userdata, msg):
    print(f"Received `{msg}` from `{client}` topic")


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
    parser.add_argument(
        "-v", "--version", action="store_true", help="Display the version"
    )
    parser.add_argument(
        "--generateConfigFile",
        action="store_true",
        help="Print a new config file based on options supplied (including the existing config file)",
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
        # must be a better way
        with io.StringIO() as ss:
            config.write(ss)
            ss.seek(0)  # rewind
            print(ss.read())
        return

    # Build mqtt broker
    mqtt_client = MqttBroker(
        name=config.get("CONFIG", "mqttbroker_name"),
        port=config.getint("CONFIG", "mqttbroker_port"),
        username=config.get("CONFIG", "mqttbroker_user"),
        password=config.get("CONFIG", "mqttbroker_pass"),
    )
    print(mqtt_client)
    # sub to command topic
    mqtt_client.subscribe("topic", mqtt_callback)
    # connect to port

    # loop
    #   loop commands
    #     loop any adhoc commands
    #     send command
    #     get result
    #     post result
    #     pause

    # print for debug
    for section in config.sections():
        for key in config[section]:
            print(key, config[section][key])
