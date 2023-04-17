# !/usr/bin/python3
import logging
from argparse import ArgumentParser
from collections import deque
from datetime import date, timedelta  # noqa: F401
from time import sleep, time

import yaml


from mppsolar.version import __version__  # noqa: F401
from powermon.libs.daemon import Daemon
from powermon.libs.mqttbroker import MqttBroker

from powermon.libs.schedule import Schedule
from powermon.libs.device import Device

from powermon.ports import getPortFromConfig


# Set-up logger
log = logging.getLogger()


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


def readYamlFile(yamlFile=None):
    _config = {}
    if yamlFile is not None:
        try:
            with open(yamlFile, "r") as stream:
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
    config.update(readYamlFile(args.configFile))
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
    log.debug(f"deviceconfig: {device_config}")

    
    device = Device.fromConfig(device_config)
    log.debug(f"device: {device}")
    # error out if unable to configure port
    if not device:
        log.error(f"No config '{device_config}' found")
        raise ConfigError(f"No port for config '{device_config}' found")

    

    # Get scheduled commands
    scheduling_config = config.get("scheduling", None)
    log.debug(f"scheduling_config: {scheduling_config}")
    schedule = Schedule.parseScheduleConfig(scheduling_config, device, mqtt_broker)

    log.debug(schedule)

    # initialize daemon
    daemon.initialize()
    
    # Main working loop
    doLoop = True
    try:
        schedule.beforeLoop()
        log.debug("Looping")
        while doLoop:
            # tell the daemon we're still working
            daemon.watchdog()
            schedule.runLoop()
   
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print(e)
    finally:
        # Disconnect port
        #port.disconnect()
        # Disconnect mqtt
        mqtt_broker.stop()
        # Notify the daemon
        daemon.stop()
