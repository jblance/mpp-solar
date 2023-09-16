"""device.py"""
import logging
import time

from powermon.dto.deviceDTO import DeviceDTO
from powermon.ports import getPortFromConfig
from powermon.ports.abstractport import AbstractPort
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.commands.command import Command
from powermon.commands.result import Result

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
        return f"Device: {self.name}, {self.device_id=}, {self.model=}, {self.manufacturer=}, port: {self.port}, commands:{self.commands}"

    @classmethod
    def fromConfig(cls, config=None):
        if not config:
            log.warning("No device definition in config. Check configFile argument?")
            return cls(name="unnamed")
        name = config.get("name", "unnamed_device")
        device_id = config.get("id", "1") # device_id needs to be unique if there are two devices
        model = config.get("model")
        manufacturer = config.get("manufacturer")

        port = getPortFromConfig(config.get("port"))
        # error out if unable to configure port
        if not port:
            log.error("Invalid port config '%s' found", config)
            raise ConfigError(f"Invalid port config '{config}' found")

        return cls(name=name, device_id=device_id, model=model, manufacturer=manufacturer, port=port)

    def __init__(self, name : str, device_id : str = "", model : str = "", manufacturer : str = "", port : AbstractPort = None):

        self.name = name
        self.device_id = device_id
        self.model = model
        self.manufacturer = manufacturer
        self.port : AbstractPort = port
        self.commands : list[Command] = []

    def add_command(self, command: Command) -> None:
        """ add a command to the devices' list of commands """
        if command is None:
            return
        # get command definition from protocol
        command.set_command_definition(self.port.protocol.get_command_definition(command.code))
        # set the device_id in the command
        command.set_device_id(self.device_id)
        # append to commands list
        self.commands.append(command)
        log.debug("added command (%s), command list length: %i", command, len(self.commands))

    def get_port(self) -> AbstractPort:
        return self.port

    def toDTO(self) -> DeviceDTO:
        commands = []
        command: Command
        for command in self.commands:
            commands.append(command.to_dto())
        dto = DeviceDTO(
            device_id=self.device_id,
            model=self.model,
            manufacturer=self.manufacturer,
            port=self.port.toDTO(),
            commands=commands
        )
        return dto

    def initialize(self):
        log.info("initializing device")
        return

    def finalize(self):
        log.info("finalizing device")
        return

    def runLoop(self, force=False) -> bool:
        """
        the loop that checks for commands to run,
        runs them
        """
        time.sleep(0.1)
        if self.commands is None:
            log.info("no commands in queue")
            return False
        else:
            # open connection on port
            self.port.connect

            for command in self.commands:
                if force or command.dueToRun():
                    log.debug(f"Running command: {command.code}")
                    # run command
                    result: Result = self.port.run_command(command)
                    # decode result
                    self.port.get_protocol().decode(result=result, command=command)
                    result.set_device_id(self.device_id)
                    # loop through each output and process result
                    output: AbstractOutput
                    for output in command.outputs:
                        log.debug(f"Using Output: {output}")
                        output.process(result=result)

            #close connection on port
            self.port.disconnect
            return True
