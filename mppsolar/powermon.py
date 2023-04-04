# !/usr/bin/python3
import logging
from argparse import ArgumentParser
from collections import deque
from datetime import date, timedelta  # noqa: F401
from time import sleep, time

import yaml

from mppsolar.libs.mqttbrokerc import MqttBroker
from mppsolar.libs.daemon import Daemon
from mppsolar.sender import output_results
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
    # is this just a call to send an adhoc command to the queue?
    if args.adhoc:
        print("ADHOC is todo")
        return
    # sub to the adhoc command topic ie listen for 'extra' commands
    mqtt_broker.setAdhocCommands(config=mqttconfig, callback=mqtt_callback)
    # debug dump mqttbroker details
    log.debug(f"mqtt_broker: {mqtt_broker}")

    # get the device config
    # this is required, and contains:
    #     device:
    #       name:
    #       id:
    #       model:
    #       manufacturer:
    #       port:
    #       commands:
    device_config = config.get("device", None)
    if not device_config:
        log.error(f"No device definition in config. Check {args.configFile}?")
        exit(1)

    

    # configure the daemon (optional)
    #     daemon:
    #       type: systemd  # noqa:
    #       keepalive: 10
    daemon = Daemon(config=config)
    log.debug(f"daemon: {daemon}")

    # config the port (required)
    # config depends on port type
    #   port:
    #     baud: 2400
    #     path: /dev/ttyUSB0
    #     type: serial  # noqa:
    #     protocol: PI30MAX
    port_config = device_config["port"].copy()
    log.debug(f"portconfig: {port_config}")
    portType = port_config["type"]
    portPath = port_config["path"]
    portBaud = port_config["baud"]
    port = get_port(portType, portPath, portBaud)
    log.debug(f"port: {port}")
    # error out if unable to configure port
    if not port:
        log.error(f"No port for config '{port_config}' found")
        raise ConfigError(f"No port for config '{port_config}' found")

    # get protocol handler
    protocol = get_protocol(protocol=port_config["protocol"])
    log.debug(f"protocol: {protocol}")

    # Get scheduled commands
    scheduling_config = config.get("scheduling", None)
    # Get loop timing details
    loop = scheduling_config["loop"]

    inDelay = False
    delayRemaining = loop
    doLoop = True

    # initialize daemon
    daemon.initialize()

    

    # Catch keyboard interupt
    try:
        # connect to port
        port.connect()
        while doLoop:
            # Start timer
            start_time = time()
            # tell the daemon we're still working
            daemon.watchdog()
            # loop through command list
            #log.debug(scheduling_config)
            for schedule in scheduling_config["schedules"]:
                if not inDelay and schedule["type"] == "loop":
                    for command in schedule["commands"]:
                    
                        log.info(f"Processing command: {command}")
                        if "f_command" in command:
                            _command = command["f_command"]
                            _command = eval(_command)
                        else:
                            _command = command["command"]
                        # TODO: allow protocol override
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
                elapsed_time = time() - start_time
                delayRemaining = delayRemaining - elapsed_time
                if delayRemaining > 0 and not inDelay:
                    log.debug(f"delaying for {loop}sec, delayRemaining: {delayRemaining}")
                    inDelay = True
                if delayRemaining < 0:
                    log.debug("setting inDelay to false")
                    inDelay = False
                    delayRemaining = loop
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print(e)
    finally:
        # Disconnect port
        port.disconnect()
        # Disconnect mqtt
        mqtt_broker.stop()
        # Notify the daemon
        daemon.stop()
