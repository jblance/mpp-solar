"""device.py"""
import logging


from powermon.commands.command import Command
from powermon.commands.result import Result
from powermon.dto.deviceDTO import DeviceDTO
from powermon.errors import CommandDefinitionMissing, ConfigError
from powermon.libs.mqttbroker import MqttBroker
from powermon.outputs.abstractoutput import AbstractOutput
from powermon.ports import from_config as port_from_config
from powermon.ports.abstractport import AbstractPort

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
        self.adhoc_commands: list = []

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
    def mqtt_broker(self, mqtt_broker):
        log.debug("Setting mqtt_broker to: %s", mqtt_broker)
        self._mqtt_broker = mqtt_broker
        # If we are setting an actual broker object also set callback for adhoc commands
        if isinstance(mqtt_broker, MqttBroker) and mqtt_broker.adhoc_topic is not None:
            log.info("Subscribing to adhoc_topic: %s", mqtt_broker.adhoc_topic)
            mqtt_broker.subscribe(topic=mqtt_broker.adhoc_topic, callback=self.adhoc_command_cb)

    def adhoc_command_cb(self, client, userdata, msg):
        """ callback for adhoc command messages """
        log.debug("received message on %s, with payload: %s", msg.topic, msg.payload)
        # build command object
        command_code = msg.payload.decode()
        adhoc_command = Command.from_code(command_code)
        adhoc_command.command_definition = self.port.protocol.get_command_definition(command_code)
        # add to adhoc queue
        self.adhoc_commands.append(adhoc_command)

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

    async def initialize(self):
        """Device initialization activities"""
        log.info("initializing device")

    async def finalize(self):
        """Device finalization activities"""
        log.info("finalizing device")
        # close connection on port
        await self.port.disconnect()

    async def run_adhoc_commands(self):
        """ check for any adhoc commands in the queue and run them """
        # check for any adhoc commands
        while len(self.adhoc_commands) > 0:
            # get the oldest adhoc command
            adhoc_command = self.adhoc_commands.pop(0)
            # run command
            log.info("Running adhoc command: %s", adhoc_command)
            try:
                # run command
                result: Result = await self.port.run_command(adhoc_command)
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
            # process result
            payload = str(result)  # FIXME: finish this
            # publish result
            print(payload)
            self.mqtt_broker.publish("powermon2/adhoc_commands_results", payload)  # FIXME: finish this

    async def run(self, force=False):
        """checks for commands to run and runs them"""
        # run any adhoc commands
        await self.run_adhoc_commands()

        # check for any commands in the queue
        if self.commands is None or len(self.commands) == 0:
            log.info("no commands in queue")
            return

        for command in self.commands:
            if force or command.is_due():
                log.info("Running command: %s", command)
                try:
                    # run command
                    result: Result = await self.port.run_command(command)
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
