# !/usr/bin/python3
"""main powermon code"""

import logging
from argparse import ArgumentParser

# from collections import deque
from datetime import date, timedelta  # noqa: F401

# from time import sleep, time

import yaml


from mppsolar.version import __version__  # noqa: F401
from powermon.libs.daemon import Daemon
from powermon.libs.mqttbroker import MqttBroker

from powermon.libs.schedule import Schedule
from powermon.libs.device import Device
from powermon.libs.apicoordinator import ApiCoordinator

# from powermon.ports import getPortFromConfig


# Set-up logger
log = logging.getLogger("")


def read_yaml_file(yaml_file=None):
    """function to read a yaml file and return dict"""
    _yaml = {}
    if yaml_file is not None:
        try:
            with open(yaml_file, "r", encoding="utf-8") as stream:
                _yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            log.error("Error processing yaml file: %s", exc)
        except FileNotFoundError as exc:
            log.error("Error opening yaml file: %s", exc)
    return _yaml


def process_command_line_overrides(args):
    """override config with command line options"""
    _config = {}
    if args.once:
        _config["loop"] = "once"
    if args.info:
        _config["debuglevel"] = logging.INFO
    if args.debug:
        _config["debuglevel"] = logging.DEBUG
    return _config


def main():
    """main entry point for powermon command"""
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
    parser.add_argument(
        "-v", "--version", action="store_true", help="Display the version"
    )
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
    parser.add_argument(
        "-I", "--info", action="store_true", help="Enable Info and above level messages"
    )
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

    # Build configuration from config file and command line overrides
    log.info("Using config file: %s", args.configFile)
    # build config with details from config file
    config = read_yaml_file(args.configFile)

    # build config - override with any command line arguments
    config.update(process_command_line_overrides(args))

    # logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log.setLevel(config.get("debuglevel", logging.WARNING))

    # if generateConfigFile is true then print config out
    if args.dumpConfig:
        print("# yaml config for powermon")
        print("# default location ./powermon.yaml")
        print(yaml.dump(config))
        return
    # debug config
    log.info("config: %s", config)

    # build mqtt broker object (optional)
    mqtt_broker = MqttBroker(config=config.get("mqttbroker", {}))
    log.debug("mqtt_broker: %s", mqtt_broker)

    # build device object (required)
    device = Device(config=config.get("device", None))
    log.debug("device: %s", device)

    # build the daemon object (optional)
    daemon = Daemon(config=config)
    log.debug("daemon: %s", daemon)

    # Get scheduled commands
    scheduling_config = config.get("scheduling", None)
    log.debug("scheduling_config: %s", scheduling_config)
    schedule = Schedule.parseScheduleConfig(scheduling_config, device, mqtt_broker)

    log.debug(schedule)

    # setup api coordinator
    api_coordinator = ApiCoordinator(
        config=config.get("api", None),
        device=device,
        mqtt_broker=mqtt_broker,
        schedule=schedule,
    )
    # TODO: run in the schedule loop

    # initialize daemon
    daemon.initialize()

    # Main working loop
    keep_looping = True
    try:
        schedule.beforeLoop()
        while keep_looping:
            # tell the daemon we're still working
            daemon.watchdog()
            keep_looping = schedule.runLoop()
            api_coordinator.run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as general_exception:
        print(general_exception)
    finally:
        # Disconnect port
        # port.disconnect()
        # Disconnect mqtt
        mqtt_broker.stop()
        # Notify the daemon
        daemon.stop()
