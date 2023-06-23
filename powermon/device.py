"""device.py"""
import logging

from powermon.dto.deviceDTO import DeviceDTO
from powermon.ports import getPortFromConfig
from powermon.ports.abstractport import AbstractPort
from powermon.commands.command import Command

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
        return f"Device: {self.name}, {self.identifier=}, {self.model=}, {self.manufacturer=}, port: {self.port}, commands:{self.commands}"

    @classmethod
    def fromConfig(cls, config=None):
        if not config:
            log.warning("No device definition in config. Check configFile argument?")
            return cls(name="unnamed")
        name = config.get("name", "unnamed_device")
        identifier = config.get("id")
        model = config.get("model")
        manufacturer = config.get("manufacturer")

        port = getPortFromConfig(config.get("port"))
        # error out if unable to configure port
        if not port:
            log.error("Invalid port config '%s' found", config)
            raise ConfigError(f"Invalid port config '{config}' found")

        return cls(name=name, identifier=identifier, model=model, manufacturer=manufacturer, port=port)

    def __init__(self, name : str, identifier : str = "", model : str = "", manufacturer : str = "", port : AbstractPort = None):

        self.name = name
        self.identifier = identifier
        self.model = model
        self.manufacturer = manufacturer
        self.port = port
        self.commands = []

    def add_command(self, command: Command = None) -> None:
        """ add a command to the device list of commands """
        if command is None:
            return
        # get command definition from protocol
        command.command_defn = self.port.protocol.get_command_defn(command.name)
        self.commands.append(command)

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

    def runLoop(self, force=False):
        """
        the loop that checks for commands to run,
        runs them
        """
        if self.commands is None:
            log.info("no commands in queue")
            return False
        else:
            for command in self.commands:
                if force or command.dueToRun():
                    # run command
                    result = self.port.run_command(command)
                    # decode result
                    self.port.protocol.decode(result)
                    # loop through each output and process result
                    for output in command.outputs:
                        log.debug(f"Using Output: {output}")
                        output.process(result=result)
            return True
