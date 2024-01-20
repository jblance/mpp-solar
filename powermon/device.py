"""device.py"""
import logging

from powermon.commands.command import Command
from powermon.commands.result import Result
from powermon.dto.deviceDTO import DeviceDTO
from powermon.errors import ConfigError, CommandDefinitionMissing
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.ports import from_config as port_from_config
from powermon.ports.abstractport import AbstractPort
from powermon.libs.mqttbroker import MqttBroker

# Set-up logger
log = logging.getLogger("Device")


class DeviceInfo:
    """ struct like class to contain info about the device """
    def __init__(self, name, device_id, model, manufacturer):
        self.name = name
        self.device_id = device_id
        self.model = model
        self.manufacturer = manufacturer


class Device:
    """
    A device is a port with a protocol
    also contains the name, model and id of the device
    """

    def __str__(self):
        return f"Device: {self.device_info.name}, {self.device_info.device_id=}, " + \
            f"{self.device_info.model=}, {self.device_info.manufacturer=}, " + \
            f"port: {self.port}, mqtt_broker: {self.mqtt_broker}, commands:{self.commands}"

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

        port = port_from_config(config.get("port"))

        # raise error if unable to configure port
        if not port:
            log.error("Invalid port config '%s' found", config)
            raise ConfigError(f"Invalid port config '{config}' found")

        return cls(name=name, device_id=device_id, model=model, manufacturer=manufacturer, port=port)

    def __init__(self, name: str, device_id: str = "", model: str = "", manufacturer: str = "", port: AbstractPort = None):
        self.device_info = DeviceInfo(name=name, device_id=device_id, model=model, manufacturer=manufacturer)
        self.port: AbstractPort = port
        self.commands: list[Command] = []
        self.mqtt_broker = None

    @property
    def port(self) -> AbstractPort:
        """ the port associated with this device """
        return self._port

    @port.setter
    def port(self, value):
        log.debug("Setting port to: %s", value)
        self._port = value

    @property
    def mqtt_broker(self) -> MqttBroker:
        """ the mqtt_broker object """
        return self._mqtt_broker

    @mqtt_broker.setter
    def mqtt_broker(self, value):
        log.debug("Setting mqtt_broker to: %s", value)
        self._mqtt_broker = value

    def add_command(self, command: Command) -> None:
        """add a command to the devices' list of commands"""
        if command is None:
            return
        # get command definition from protocol
        try:
            command.command_definition = self.port.protocol.get_command_definition(command.code)
        except CommandDefinitionMissing as ex:
            print(ex)
            return

        # set the device_id in the command
        # command.set_device_id(self.device_id)
        # append to commands list
        self.commands.append(command)
        log.debug("added command (%s), command list length: %i", command, len(self.commands))

    def to_dto(self) -> DeviceDTO:
        """convert the Device to a Data Transfer Object"""
        commands = []
        command: Command
        for command in self.commands:
            commands.append(command.to_dto())
        dto = DeviceDTO(device_id=self.device_info.device_id,
                        model=self.device_info.model,
                        manufacturer=self.device_info.manufacturer,
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
                log.info("Running command: %s", command)
                try:
                    # run command
                    result: Result = self.port.run_command(command)
                    log.info("Got result: %s", result)
                except Exception as exception:  # pylint: disable=W0718
                    # specific errors need to incorporated into Result as part of the processing
                    # so any exceptions at this stage will be truely unexpected
                    log.error("Error decoding result: %s", exception)
                    # result = Result(result_type=ResultType.ERROR, command_definition=None, \
                    #   raw_response=b"Error decoding result", trimmed_response=b"Error decoding result")
                    # result.error_messages.append(f"Error decoding result: {exception}")
                    # result.error_messages.append(f"Exception Type: {exception.__class__.__name__}")
                    # result.error_messages.append(f"Exception args: {exception.args}")
                    raise exception
                # result.device_id = self.device_id

                # loop through each output and process result
                output: AbstractOutput
                for output in command.outputs:
                    log.debug("Using Output: %s", output)
                    output.process(command=command, result=result, mqtt_broker=self.mqtt_broker, device_info=self.device_info)
