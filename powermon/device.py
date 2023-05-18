"""device.py"""
import logging

from powermon.dto.deviceDTO import DeviceDTO
from powermon.ports import getPortFromConfig
from powermon.ports.abstractport import AbstractPort

# Set-up logger
log = logging.getLogger("Device")


class ConfigError(Exception):
    """Exception for invaild configurations"""


class Device:
    """
    A device is a port with a protocol
    also contains the name, model and id of the device
    """

    def __str__(self):
        return f"Device: {self.devicename}, identifier: {self.identifier}, model: {self.model}, manufacturer: {self.manufacturer}, port: {self.port}, queue: {self.commandQueue}"

    def __init__(self, config):
        if not config:
            log.warning("No device definition in config. Check configFile argument?")
            config = {"identifier": "unsupplied"}

        self.devicename = config.get("name", "unnamed_device")
        self.identifier = config.get("id")
        self.model = config.get("model")
        self.manufacturer = config.get("manufacturer")
        self.port = getPortFromConfig(config.get("port"))

        self.commandQueue = None

        # error out if unable to configure port
        if not self.port:
            log.error("Invalid port config '%s' found", config)
            raise ConfigError(f"Invalid port config '{config}' found")

    def get_port(self) -> AbstractPort:
        return self.port

    def toDTO(self) -> DeviceDTO:
        dto = DeviceDTO(
            identifier=self.identifier,
            model=self.model,
            manufacturer=self.manufacturer,
            port=self.port.toDTO(),
        )
        return dto

    def initialize(self):
        log.info("initializing device")
        return

    def finalize(self):
        log.info("finalizing device")
        return

    def runLoop(self):
        return self.commandQueue.run_loop(device=self)
