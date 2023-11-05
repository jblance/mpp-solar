"""device.py"""
import logging

from powermon.commands.command import Command
from powermon.commands.result import Result, ResultType
from powermon.dto.deviceDTO import DeviceDTO
from powermon.errors import ConfigError
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.ports import getPortFromConfig
from powermon.ports.abstractport import AbstractPort

# Set-up logger
log = logging.getLogger("Device")


class Device:
    """
    A device is a port with a protocol
    also contains the name, model and id of the device
    """

    def __str__(self):
        return f"Device: {self.name}, {self.device_id=}, {self.model=}, {self.manufacturer=}, port: {self.port}, commands:{self.commands}"

    @classmethod
    def from_config(cls, config=None):
        """build the object from a config dict"""
        if not config:
            log.warning("No device definition in config. Check configFile argument?")
            return cls(name="unnamed")
        name = config.get("name", "unnamed_device")
        device_id = config.get("id", "1")  # device_id needs to be unique if there are two devices
        model = config.get("model")
        manufacturer = config.get("manufacturer")

        port = getPortFromConfig(config.get("port"))

        # raise error if unable to configure port
        if not port:
            log.error("Invalid port config '%s' found", config)
            raise ConfigError(f"Invalid port config '{config}' found")

        return cls(name=name, device_id=device_id, model=model, manufacturer=manufacturer, port=port)

    def __init__(self, name: str, device_id: str = "", model: str = "", manufacturer: str = "", port: AbstractPort = None):
        self.name = name
        self.device_id = device_id
        self.model = model
        self.manufacturer = manufacturer
        self.port: AbstractPort = port
        self.commands: list[Command] = []

    def add_command(self, command: Command) -> None:
        """add a command to the devices' list of commands"""
        if command is None:
            return
        # get command definition from protocol
        command.set_command_definition(self.port.protocol.get_command_with_command_string(command.code))
        # set the device_id in the command
        command.set_device_id(self.device_id)
        # append to commands list
        self.commands.append(command)
        log.debug("added command (%s), command list length: %i", command, len(self.commands))

    def get_port(self) -> AbstractPort:
        """return the port associated with this device"""
        return self.port

    def to_dto(self) -> DeviceDTO:
        """convert the Device to a Data Transfer Object"""
        commands = []
        command: Command
        for command in self.commands:
            commands.append(command.to_dto())
        dto = DeviceDTO(device_id=self.device_id,
                        model=self.model,
                        manufacturer=self.manufacturer,
                        port=self.port.to_dto(),
                        commands=commands)
        return dto

    def initialize(self):
        """Device initialization activities"""
        log.info("initializing device")

    def finalize(self):
        """Device finalization activities"""
        log.info("finalizing device")
        # close connection on port
        self.port.disconnect()

    def run(self, force=False):
        """checks for commands to run and runs them"""
        if self.commands is None or len(self.commands) == 0:
            log.info("no commands in queue")
            return

        for command in self.commands:
            if force or command.is_due():
                log.debug("Running command: %s", command.code)
                try:
                    # run command
                    result: Result = self.port.run_command(command)
                except Exception as exception:  # pylint: disable=W0718
                    log.error("Error decoding result: %s", exception)
                    result = Result(command_code=command.code, result_type=ResultType.ERROR)
                    result.error = True
                    result.error_messages.append(f"Error decoding result: {exception}")
                    result.error_messages.append(f"Exception Type: {exception.__class__.__name__}")
                    result.error_messages.append(f"Exception args: {exception.args}")
                result.set_device_id(self.device_id)  # FIXME: think this is limiting, should pass device and mqtt_broker to output

                # loop through each output and process result
                output: AbstractOutput
                for output in command.outputs:
                    log.debug("Using Output: %s", output)
                    output.process(result=result)  # FIXME: should also have device, mqtt_broker
