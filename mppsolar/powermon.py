# !/usr/bin/python3
import logging
from argparse import ArgumentParser
from collections import deque
from datetime import date, timedelta  # noqa: F401
from time import sleep, time

import yaml

from mppsolar.libs.mqttbrokerc import MqttBroker
from mppsolar.libs.daemon import Daemon
from mppsolar.outputs import output_results
from mppsolar.ports import get_port
from mppsolar.protocols import get_protocol
from mppsolar.version import __version__  # noqa: F401

# from mppsolar.inout import get_port


# Set-up logger
log = logging.getLogger("")


class ConfigError(Exception):
    pass


sample_config = """
device:
  name: Test_Inverter
  id: 123456789
  port:
    path: /dev/ttyUSB0
    type: test
    baud: 2400
    protocol: PI30
  commands:
    - command: QPI
      outputs:
      - name: screen
  loop: once
"""

ADHOC_COMMANDS = deque([])
# SPLIT_TOKEN = ","


def mqtt_callback(client, userdata, msg):
    log.info(f"Received `{msg.payload}` on topic `{msg.topic}`")
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
    if args.once:
        _config["loop"] = "once"
    if args.info:
        _config["debuglevel"] = logging.INFO
    if args.debug:
        _config["debuglevel"] = logging.DEBUG
    return _config


def main():
    description = f"Power Device Monitoring Utility, version: {__version__}"
    parser = ArgumentParser(description=description)

    parser.add_argument(
        "-C",
        "--configFile",
        nargs="?",
        type=str,
        help="Full location of config file",
        const="./powermon.yaml",
        default=None,
    )
    parser.add_argument("-v", "--version", action="store_true", help="Display the version")
    parser.add_argument(
        "-d",
        "--dumpConfig",
        action="store_true",
        help="Print the config based on options supplied (including the defaults, config file and any overrides)",
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
    parser.add_argument("-I", "--info", action="store_true", help="Enable Info and above level messages")
    parser.add_argument(
        "--adhoc",
        type=str,
        default=None,
        help="Send adhoc command to mqtt adhoc command queue - needs config file specified and populated",
    )

    args = parser.parse_args()
    # prog_name = parser.prog

    # Temporarily set debug level based on command line options
    log.setLevel(logging.WARNING)
    if args.info:
        log.setLevel(logging.INFO)
    if args.debug:
        log.setLevel(logging.DEBUG)

    # Display version if asked
    log.info(description)
    if args.version:
        print(description)
        return None

    # Build configuration from defaults, config file and command line overrides
    log.info(f"Using config file: {args.configFile}")
    # build config - start with defaults
    config = yaml.safe_load(sample_config)
    # build config - update with details from config file
    config.update(readConfigFile(args.configFile))
    # build config - override with any command line arguments
    config.update(processCommandLineOverrides(args))

    # logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log.setLevel(config.get("debuglevel", logging.WARNING))

    # if generateConfigFile is true then print config out
    if args.dumpConfig:
        print("# yaml config for powermon")
        print("# default location ./powermon.yaml")
        print(yaml.dump(config))
        return

    # debug dump config
    log.info(f"config: {config}")

    # Build mqtt broker
    mqttconfig = config.get("mqttbroker", {})
    mqtt_broker = MqttBroker(config=mqttconfig)
    # is this just a call to send and adhoc command to the queue?
    if args.adhoc:
        print("ADHOC is todo")
        return
    # sub to command topic if defined
    mqtt_broker.setAdhocCommands(config=mqttconfig, callback=mqtt_callback)
    log.debug(mqtt_broker)

    device_config = config.get("device", None)
    if not device_config:
        log.error(f"No device definition in config. Check {args.configFile}?")
        exit(1)

    daemon = Daemon(config=config)
    log.debug(f"Got daemon config: {daemon}")

    # get port
    port_config = device_config["port"].copy()
    log.debug(f"portconfig: {port_config}")
    port = get_port(port_config)
    # port = get_port(porttype=porttype)
    if not port:
        log.error(f"No port for config '{port_config}' found")
        raise ConfigError(f"No port for config '{port_config}' found")

    # get protocol handler
    protocol = get_protocol(protocol=port_config["protocol"])

    # Get loop details
    loop = config.get("loop", "once")
    inDelay = False
    delayRemaining = loop
    doLoop = True

    # initialize daemon if needed
    daemon.initialize()

    # Catch keyboard interupt
    try:
        # connect to port
        port.connect()
        while doLoop:
            # Start timer
            start_time = time()
            daemon.notify("OK")
            # loop through command list
            for command in device_config["commands"]:
                # process any adhoc commands first
                while len(ADHOC_COMMANDS) > 0:
                    log.debug(f"adhoc command list: {ADHOC_COMMANDS}")
                    adhoc_command = ADHOC_COMMANDS.popleft().decode()  # FIXME: decode to str #
                    log.info(f"Processing command: {adhoc_command}")
                    results = port.process_command(command=adhoc_command, protocol=protocol)
                    log.debug(f"results {results}")
                    # send to output processor(s)
                    # TODO sort outputs
                    output_results(
                        results=results,
                        command=config["mqttbroker"]["adhoc_commands"],
                        mqtt_broker=mqtt_broker,
                        fullconfig=config,
                    )
                # process 'normal' commands
                if not inDelay:
                    log.info(f"Processing command: {command}")
                    if "f_command" in command:
                        _command = command["f_command"]
                        _command = eval(_command)
                    else:
                        _command = command["command"]
                    results = port.process_command(command=_command, protocol=protocol)
                    log.debug(f"results {results}")
                    # send to output processor(s)
                    output_results(
                        results=results,
                        command=command,
                        mqtt_broker=mqtt_broker,
                        fullconfig=config,
                    )
                    # pause
                    # pause_time = config["command_pause"]
                    # log.debug(f"Sleeping for {pause_time}secs")
            if loop == "once":
                doLoop = False
            else:
                # Small pause to ....
                sleep(0.1)
                end_time = time()
                delayRemaining = delayRemaining - (end_time - start_time)
                if delayRemaining > 0 and not inDelay:
                    log.debug(f"delaying for {loop}sec, delayRemaining: {delayRemaining}")
                    inDelay = True
                if delayRemaining < 0:
                    log.debug("setting inDelay to false")
                    inDelay = False
                    delayRemaining = loop
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        # Disconnect port
        port.disconnect()
        # Disconnect mqtt
        mqtt_broker.stop()
        # Notify the daemon
        daemon.stop()
