# !/usr/bin/python3
"""main powermon code"""

import json
import logging
from argparse import ArgumentParser
from datetime import date, timedelta  # noqa: F401

import yaml

from mppsolar.version import __version__  # noqa: F401
from powermon.device import Device
from powermon.libs.apicoordinator import ApiCoordinator
from powermon.libs.commandQueue import CommandQueue
from powermon.libs.configurationManager import ConfigurationManager
from powermon.libs.daemon import Daemon
from powermon.libs.mqttbroker import MqttBroker

# from time import sleep, time
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
    if args.config:
        _config = json.loads(args.config)
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
        "--config",
        type=str,
        default=None,
        help="""Supply config items on the commandline in json format, eg '{"device": {"port":{"type":"test"}}, "commands": [{"command":"QPI"}]}'""",
    )
    parser.add_argument("-v", "--version", action="store_true", help="Display the version")
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

    # Build configuration from config file and command line overrides
    log.info("Using config file: %s", args.configFile)
    # build config with details from config file
    config = read_yaml_file(args.configFile)

    # build config - override with any command line arguments
    config.update(process_command_line_overrides(args))

    # logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log.setLevel(config.get("debuglevel", logging.WARNING))

    # debug config
    log.info("config: %s" % config)

    # build device object (required)
    device = Device(config=config.get("device"))
    log.info(device)

    # build mqtt broker object (optional)
    mqtt_broker = MqttBroker(config=config.get("mqttbroker"))
    log.info(mqtt_broker)

    # build the daemon object (optional)
    daemon = Daemon(config=config.get("daemon"))
    log.info(daemon)

    # build queue of commands
    # QUESTION: should mqtt_broker and controller/command queue be part of device...
    device.commandQueue = CommandQueue(config=config.get("commands"))
    log.info(device.commandQueue)

    # build controller
    # TODO: follow same pattern as others, eg
    # scheduleController = ScheduleController(config=config.get("schedules"), device=, mqtt_broker=)
    controller = ConfigurationManager.parseControllerConfig(config, device, mqtt_broker)
    log.info(controller)

    # build api coordinator
    api_coordinator = ApiCoordinator(config=config.get("api"), device=device, mqtt_broker=mqtt_broker, schedule=controller)
    log.info(api_coordinator)

    # initialize daemon
    daemon.initialize()

    # initialize device
    device.initialize()
    controller.beforeLoop()

    # Main working loop
    keep_looping = True
    controller_looping = True
    device_looping = True
    try:
        while keep_looping:
            # tell the daemon we're still working
            daemon.watchdog()

            # run schedule loop
            if controller_looping:
                controller_looping = controller.runLoop()
            if device_looping:
                device_looping = device.runLoop()
            # stop looping if neither controller or device runLoops return True
            if not controller_looping and not device_looping:
                keep_looping = False

            # run api coordinator ...
            api_coordinator.run()

            # only run loop once if required
            if args.once:
                keep_looping = False

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as general_exception:
        print(general_exception)
    finally:
        # disconnect device
        device.finalize()

        # disconnect mqtt
        mqtt_broker.stop()

        # stop the daemon
        daemon.stop()
