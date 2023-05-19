"""device.py"""
import logging

from powermon.dto.deviceDTO import DeviceDTO
from powermon.libs.commandQueue import CommandQueue
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

    def __init__(self, config=None, commandConfig={}):
        if not config:
            log.warning("No device definition in config. Check configFile argument?")
            config = {"identifier": "unsupplied"}

        self.devicename = config.get("name", "unnamed_device")
        self.identifier = config.get("id")
        self.model = config.get("model")
        self.manufacturer = config.get("manufacturer")
        self.port = getPortFromConfig(config.get("port"))

        # build queue of commands
        if commandConfig is not None:
            self.commandQueue = CommandQueue(config=commandConfig)
        else:
            self.commandQueue = None

        # error out if unable to configure port
        if not self.port:
            log.error("Invalid port config '%s' found", config)
            raise ConfigError(f"Invalid port config '{config}' found")

        # Update commands with definition, now that we have a port / protocol
        for command in self.commandQueue.commands:
            command.command_defn = self.port.protocol.get_command_defn(command.name)

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
        if self.commandQueue.commands is None:
            log.info("no commands in queue")
            return False
        else:
            for command in self.commandQueue.commands:
                if command.dueToRun():
                    # update run times
                    command.touch()
                    # update full_command - expand any template / add crc etc
                    command.full_command = self.port.protocol.get_full_command(command.name)
                    # run command
                    result = self.port.run_command(command)
                    # decode result
                    result.decoded_response = self.port.protocol.decode(result.raw_response, command.name)
                    # loop each output and process result
                    for output in command.outputs:
                        log.debug(f"Using Output: {output}")
                        output.output(data=result.decoded_response)
                        # TODO: update outputer
                        # output.process(result=result)
            return True
