# !/usr/bin/python3
import logging
from argparse import ArgumentParser
from collections import deque
from time import sleep

import yaml

from mppsolar.libs.mqttbroker import MqttBrokerC as MqttBroker
from mppsolar.outputs import output_results
from mppsolar.ports import get_port
from mppsolar.protocols import get_protocol
from mppsolar.version import __version__  # noqa: F401

# from mppsolar.inout import get_port


# Set-up logger
log = logging.getLogger("")
FORMAT = "%(asctime)-15s:%(levelname)s:%(module)s:%(funcName)s@%(lineno)d: %(message)s"
logging.basicConfig(format=FORMAT)


class ConfigError(Exception):
    pass


sample_config = """
  port:
    path: /dev/ttyUSB0
    type: test
    baud: 2400
  protocol: PI30
  commands:
    - command: QPI
      outputs:
      - name: screen
"""

ADHOC_COMMANDS = deque([])
# SPLIT_TOKEN = ","


def mqtt_callback(client, userdata, msg):
    print(f"Received `{msg.payload}` on topic `{msg.topic}`")
    # TODO: define message format and extract command and config
    newCommand = msg.payload
    ADHOC_COMMANDS.append(newCommand)


def readConfigFile(configFile=None):
    _config = {}
    if configFile is not None:
        try:
            with open(configFile, "r") as stream:
                _config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            log.error(f"Error processing config file: {exc}")
        except FileNotFoundError as exc:
            log.error(f"Error opening config file: {exc}")
    return _config


def processCommandLineOverrides(args):
    _config = {}
    return _config


def buildMqttBroker(config):
    _mqttbroker = MqttBroker(config)
    if "mqttbroker" not in config:
        log.debug("No mqttbroker definition in config")
        return None
    if "name" not in config["mqttbroker"] or config["mqttbroker"]["name"] is None:
        log.debug("No mqttbroker name defined in config")
        return None
    _mqttbroker = MqttBroker(
        name=config["mqttbroker"]["name"],
        port=config["mqttbroker"]["port"],
        username=config["mqttbroker"]["user"],
        password=config["mqttbroker"]["pass"],
    )
    # sub to command topic if defined
    if "adhoc_commands" in config and "topic" in config["adhoc_commands"]:
        adhoc_commands_topic = config["adhoc_commands"]["topic"]
        if adhoc_commands_topic is not None:
            # TODO: move to mqttbroker -
            _mqttbroker.connect()
            _mqttbroker.subscribe(adhoc_commands_topic, mqtt_callback)
            # connect to mqtt
            # TODO: move to mqttbroker -
            _mqttbroker.start()
    return _mqttbroker


def main():
    description = f"Power Device Monitoring Utility, version: {__version__}"
    parser = ArgumentParser(description=description)

    parser.add_argument(
        "-C",
        "--configFile",
        nargs="?",
        type=str,
        help="Full location of config file",
        const="/etc/mpp-solar/powermon.yml",
        default=None,
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
        "-1",
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
    config = yaml.safe_load(sample_config)
    # build config - update with details from config file
    config.update(readConfigFile(args.configFile))
    # build config - override with any command line arguments
    config.update(processCommandLineOverrides(args))

    # if generateConfigFile is true then print config out
    if args.generateConfigFile:
        print("# yaml config for powermon")
        print("# default location /etc/mpp-solar/powermon.yml")
        print(yaml.dump(config))
        return

    # debug dump config
    log.debug(config)

    # Build mqtt broker
    mqttconfig = config.get("mqttbroker", {})
    mqtt_broker = MqttBroker(config=mqttconfig)
    # sub to command topic if defined
    mqtt_broker.setAdhocCommands(
        adhoc_commands=mqttconfig.get("adhoc_commands"), callback=mqtt_callback
    )
    log.debug(mqtt_broker)

    # get port
    portconfig = config["port"].copy()
    log.debug("portconfig", portconfig)
    port = get_port(portconfig)
    # port = get_port(porttype=porttype)
    if not port:
        log.error(f"No port for config '{portconfig}' found")
        raise ConfigError(f"No port for config '{portconfig}' found")

    # get protocol handler
    protocol = get_protocol(protocol=config["protocol"])

    loop = True
    try:
        # connect to port
        port.connect()
        while loop:
            # loop through command list
            for command in config["commands"]:
                # process any adhoc commands first
                log.debug(f"adhoc command list: {ADHOC_COMMANDS}")
                while len(ADHOC_COMMANDS) > 0:
                    adhoc_command = (
                        ADHOC_COMMANDS.popleft().decode()
                    )  # FIXME: decode to str #
                    log.info(f"Processing command: {adhoc_command}")
                    results = port.process_command(
                        command=adhoc_command, protocol=protocol
                    )
                    log.debug(f"results {results}")
                    # send to output processor(s)
                    # TODO sort outputs
                    output_results(
                        results=results,
                        outputs=config["adhoc_commands"],
                        mqtt_broker=mqtt_broker,
                    )
                # process 'normal' commands
                log.info(f"Processing command: {command}")
                results = port.process_command(
                    command=command["command"], protocol=protocol
                )
                log.debug(f"results {results}")
                # send to output processor(s)
                output_results(
                    results=results, outputs=command["outputs"], mqtt_broker=mqtt_broker
                )
                # pause
                # pause_time = config["command_pause"]
                # log.debug(f"Sleeping for {pause_time}secs")
            if args.once:
                loop = False
            else:
                # sleep(pause_time)
                sleep(5)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        # Disconnect port
        port.disconnect()
        # Disconnect mqtt
        mqtt_broker.stop()
