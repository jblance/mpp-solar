
from powermon.model.dto.commandDTO import CommandDTO
import logging
log = logging.getLogger("Command")

from powermon.outputs import getOutputFromConfig
from .device import Device
from powermon.libs.mqttbroker import MqttBroker

class Command:
    def __init__(self, command, commandType, outputs, port):
        self.command = command
        self.commandType = commandType
        self.outputs = outputs
        self.port = port

    def __str__(self):
        return f"Command: {self.command}, CommandType: {self.commandType}, Outputs: {self.outputs}"
    
    def toDTO(self):
        dto = CommandDTO(
            command=self.command,
            commandType=self.commandType,
        )
        return dto

    def run(self):
        log.debug(f"Running command: {self.command}")
        results = self.port.process_command(command=self.command)
        for output in self.outputs:
            log.debug(f"Output: {output}")
            output.output(data=results)

    @classmethod
    def parseCommandConfig(cls, command_config : dict, computed_topic : str, schedule_name: str, mqtt_broker : MqttBroker, device: Device):
        
        _command_query = command_config["command_query"]
        _commandType = command_config["type"]
        computed_topic = computed_topic + _command_query

        _outputs = []
        for outputConfig in command_config["outputs"]:
            _output = getOutputFromConfig(outputConfig, computed_topic, schedule_name, device, mqtt_broker)
            logging.debug(f"output: {_output}")
            _outputs.append(_output)

        return Command(_command_query, _commandType, _outputs, device.port)