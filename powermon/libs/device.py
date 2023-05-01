"""device.py"""

import logging
import sys

# from mppsolar.protocols import get_protocol
from powermon.ports import getPortFromConfig
from powermon.libs.errors import ConfigError

# Set-up logger
log = logging.getLogger("Device")


class Device:
    """
    A device is a port with a protocol
    also contains the name, model and id of the device
    """

    def __init__(self, config=None):
        if not config:
            log.error("No device definition in config. Check configFile?")
            sys.exit(1)
        self.name = config.get("name", "mppsolar")
        self.identifier = config.get("identifier", "mppsolar")
        self.model = config.get("model", "mppsolar")
        self.manufacturer = config.get("manufacturer", "mppsolar")
        self.port = getPortFromConfig(config.get("port", None))
        # self.protocol = get_protocol(config.get("protocol", None))  # TODO: move to port

        # error out if unable to configure port
        if not self.port:
            log.error("Invalid port config '%s' found", config)
            raise ConfigError(f"Invalid port config '{config}' found")
